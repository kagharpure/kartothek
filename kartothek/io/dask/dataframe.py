# -*- coding: utf-8 -*-


import dask
import dask.dataframe as dd
import numpy as np

from kartothek.core.common_metadata import empty_dataframe_from_schema
from kartothek.core.factory import _ensure_factory
from kartothek.core.naming import DEFAULT_METADATA_VERSION
from kartothek.io_components.docs import default_docs
from kartothek.io_components.metapartition import parse_input_to_metapartition
from kartothek.io_components.update import update_dataset_from_partitions
from kartothek.io_components.utils import (
    _ensure_compatible_indices,
    check_single_table_dataset,
    normalize_arg,
    validate_partition_keys,
)

from ._update import _update_dask_partitions_one_to_one, _update_dask_partitions_shuffle
from ._utils import _maybe_get_categoricals_from_index
from .delayed import read_table_as_delayed


@default_docs
def read_dataset_as_ddf(
    dataset_uuid=None,
    store=None,
    table=None,
    columns=None,
    concat_partitions_on_primary_index=False,
    predicate_pushdown_to_io=True,
    categoricals=None,
    label_filter=None,
    dates_as_object=False,
    predicates=None,
    factory=None,
):
    """
    Retrieve a single table from a dataset as partition-individual :class:`~dask.dataframe.DataFrame` instance.

    Please take care when using categoricals with Dask. For index columns, this function will construct dataset
    wide categoricals. For all other columns, Dask will determine the categories on a partition level and will
    need to merge them when shuffling data.
    """
    ds_factory = _ensure_factory(
        dataset_uuid=dataset_uuid,
        store=store,
        factory=factory,
        load_dataset_metadata=False,
    )
    if isinstance(columns, dict):
        columns = columns[table]
    meta = _get_dask_meta_for_dataset(
        ds_factory, table, columns, categoricals, dates_as_object
    )

    if columns is None:
        columns = list(meta.columns)

    # that we can use factories instead of dataset_uuids
    delayed_partitions = read_table_as_delayed(
        factory=ds_factory,
        table=table,
        columns=columns,
        concat_partitions_on_primary_index=concat_partitions_on_primary_index,
        predicate_pushdown_to_io=predicate_pushdown_to_io,
        categoricals={table: categoricals},
        label_filter=label_filter,
        dates_as_object=dates_as_object,
        predicates=predicates,
    )

    return dd.from_delayed(delayed_partitions, meta=meta)


def _get_dask_meta_for_dataset(
    ds_factory, table, columns, categoricals, dates_as_object
):
    """
    Calculate a schema suitable for the dask dataframe meta from the dataset.
    """
    table_schema = ds_factory.table_meta[table]
    meta = empty_dataframe_from_schema(
        table_schema, columns=columns, date_as_object=dates_as_object
    )

    if categoricals:
        meta = meta.astype({col: "category" for col in categoricals})
        meta = dd.utils.clear_known_categories(meta, categoricals)

    categoricals_from_index = _maybe_get_categoricals_from_index(
        ds_factory, {table: categoricals}
    )
    if categoricals_from_index:
        meta = meta.astype(categoricals_from_index[table])
    return meta


@default_docs
def update_dataset_from_ddf(
    ddf,
    store=None,
    dataset_uuid=None,
    table=None,
    secondary_indices=None,
    shuffle=False,
    repartition_ratio=None,
    num_buckets=1,
    sort_partitions_by=None,
    delete_scope=None,
    metadata=None,
    df_serializer=None,
    metadata_merger=None,
    default_metadata_version=DEFAULT_METADATA_VERSION,
    partition_on=None,
    factory=None,
):
    """
    Update a dataset from a dask.dataframe.


    .. admonition:: Behavior without ``shuffle==False``

        In the case without ``partition_on`` every dask partition is mapped to a single kartothek partition

        In the case with ``partition_on`` every dask partition is mapped to N kartothek partitions, where N
        depends on the content of the respective partition, such that every resulting kartothek partition has
        only a single value in the respective ``partition_on`` columns.

    .. admonition:: Behavior with ``shuffle==True``

        ``partition_on`` is mandatory

        Perform a data shuffle to ensure that every primary key will have at most ``num_bucket``.

        .. note::
            The number of allowed buckets will have an impact on the required resources and runtime.
            Using a larger number of allowed buckets will usually reduce resource consumption and in some
            cases also improves runtime performance.

        :Example:

            >>> partition_on="primary_key"
            >>> num_buckets=2  # doctest: +SKIP
            primary_key=1/bucket1.parquet
            primary_key=1/bucket2.parquet

    .. note:: This can only be used for datasets with a single table!

    Parameters
    ----------
    ddf: Union[dask.dataframe.DataFrame, None]
        The dask.Dataframe to be used to calculate the new partitions from. If this parameter is `None`, the update pipeline
        will only delete partitions without creating new ones.
    shuffle: bool
        If True and partition_on is requested, shuffle the data to reduce number of output partitions
    repartition_ratio: Optional[Union[int, float]]
        If provided, repartition the dataframe before calculation starts to ``ceil(ddf.npartitions / repartition_ratio)``
    num_buckets: int
        If provided, the output partitioning will have ``num_buckets`` files per primary key partitioning.
        This effectively splits up the execution ``num_buckets`` times. Setting this parameter may be helpful when
        scaling.
        This only has an effect if ``shuffle==True``
    """
    partition_on = normalize_arg("partition_on", partition_on)
    secondary_indices = normalize_arg("secondary_indices", secondary_indices)
    delete_scope = dask.delayed(normalize_arg)("delete_scope", delete_scope)

    if table is None:
        raise TypeError("The parameter `table` is not optional.")
    ds_factory, metadata_version, partition_on = validate_partition_keys(
        dataset_uuid=dataset_uuid,
        store=store,
        default_metadata_version=default_metadata_version,
        partition_on=partition_on,
        ds_factory=factory,
    )

    if shuffle and not partition_on:
        raise ValueError(
            "If ``shuffle`` is requested, at least one ``partition_on`` column needs to be provided."
        )
    if ds_factory is not None:
        check_single_table_dataset(ds_factory, table)

    if repartition_ratio and ddf is not None:
        ddf = ddf.repartition(
            npartitions=int(np.ceil(ddf.npartitions / repartition_ratio))
        )

    if ddf is None:
        mps = [
            parse_input_to_metapartition(
                None, metadata_version=default_metadata_version
            )
        ]
    else:
        secondary_indices = _ensure_compatible_indices(ds_factory, secondary_indices)

        if shuffle and partition_on:
            mps = _update_dask_partitions_shuffle(
                ddf=ddf,
                table=table,
                secondary_indices=secondary_indices,
                metadata_version=metadata_version,
                partition_on=partition_on,
                store_factory=store,
                df_serializer=df_serializer,
                dataset_uuid=dataset_uuid,
                num_buckets=num_buckets,
                sort_partitions_by=sort_partitions_by,
            )
        else:
            delayed_tasks = ddf.to_delayed()
            delayed_tasks = [{"data": {table: task}} for task in delayed_tasks]
            mps = _update_dask_partitions_one_to_one(
                delayed_tasks=delayed_tasks,
                secondary_indices=secondary_indices,
                metadata_version=metadata_version,
                partition_on=partition_on,
                store_factory=store,
                df_serializer=df_serializer,
                dataset_uuid=dataset_uuid,
                sort_partitions_by=sort_partitions_by,
            )
    return dask.delayed(update_dataset_from_partitions)(
        mps,
        store_factory=store,
        dataset_uuid=dataset_uuid,
        ds_factory=ds_factory,
        delete_scope=delete_scope,
        metadata=metadata,
        metadata_merger=metadata_merger,
    )
