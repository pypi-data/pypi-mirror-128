import pandas
from pandas import DataFrame, Series
from pandas.core.groupby import GroupBy
from pandas.io import sql
import psycopg2
from lariat.patch.statsd_config import DEFAULT_STATSD_CLIENT as STATSD_CLIENT
from lariat.patch.util import try_make_json

_read_parquet = pandas.read_parquet
_to_parquet = DataFrame.to_parquet
_merge = pandas.merge
_groupby = DataFrame.groupby
_df_apply = DataFrame.apply

_groupby_apply = GroupBy.apply
_series_apply = Series.apply

pandas_string = "pandas."

def _compute_axes(self):
    axes = self.index._format_data()
    if axes is not None:
        try:
            axes = eval(axes.rstrip(", "))
        except:
            axes = None

    return axes


def _patched_create_engine(url, **kwargs):
    engine = _create_engine(url, **kwargs)
    listen(engine, "before_cursor_execute", _before_cursor_execute)
    return engine


def _compute_columns(self):
    if hasattr(self, "columns"):
        return self.columns
    else:
        return None


def _compute_data_transform_pre(self):
    axes = _compute_axes(self)
    columns = _compute_columns(self)

    meta = {"pre": {"size": self.index.size, "axes": axes, "shape": self.index.shape}}
    if columns is not None:
        meta["pre"]["columns"] = str(columns)

    pre = str(self)
    return {"meta": meta, "pre": pre}


def _compute_data_transform_post(self, data_transform):
    axes = _compute_axes(self)
    columns = _compute_columns(self)

    data_transform["meta"]["post"] = {
        "size": self.index.size,
        "axes": axes,
        "shape": self.index.shape,
    }

    if columns is not None:
        data_transform["meta"]["post"]["columns"] = str(columns)

    data_transform["post"] = str(self)
    return data_transform


def read_parquet_patched(*args, **kwargs):
    """
    New read_parquet function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}read_parquet"):
        return _read_parquet(*args, **kwargs)


def to_parquet_patched(*args, **kwargs):
    """
    New to_parquet function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}to_parquet"):
        return _to_parquet(*args, **kwargs)


def merge_patched(*args, **kwargs):
    """
    New merge function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}merge"):
        return _merge(*args, **kwargs)


def dataframe_groupby_patched(*args, **kwargs):
    """
    New DataFrame.groupby function
    """
    with STATSD_CLIENT.timer(f"{pandas_string}df_groupby"):
        return _groupby(*args, **kwargs)


def dataframe_apply_patched(*args, **kwargs):
    """
    New DataFrame.apply function
    """
    meta = {}
    meta_hooks = ()

    if len(args) > 0:
        self = args[0]
        meta["data_transform"] = _compute_data_transform_pre(self)

        if hasattr(self, "index"):
            meta["index"] = str(self.index)

        if hasattr(args[0], "columns"):
            meta["columns"] = str(self.columns)

        meta_hooks = (lambda dt: _compute_data_transform_post(self, dt),)

    with STATSD_CLIENT.timer(
        f"{pandas_string}df_apply", meta=meta, meta_hooks=meta_hooks
    ):
        return _df_apply(*args, **kwargs)


def series_apply_patched(*args, **kwargs):
    """
    New Series.apply function
    """
    meta = {}
    meta_hooks = ()

    if len(args) > 0:
        self = args[0]

        meta["data_transform"] = _compute_data_transform_pre(self)

        if hasattr(self, "index"):
            meta["index"] = str(self.index)

        if hasattr(self, "columns"):
            meta["columns"] = str(self.columns)

        if hasattr(self, "name"):
            meta["name"] = str(self.name)

        meta_hooks = (lambda dt: _compute_data_transform_post(self, dt),)

    with STATSD_CLIENT.timer(
        f"{pandas_string}series_apply", meta=meta, meta_hooks=meta_hooks
    ):
        return _series_apply(*args, **kwargs)


def groupby_apply_patched(*args, **kwargs):
    """
    New GroupBy.apply function
    """
    with STATSD_CLIENT.timer(
        f"{pandas_string}groupby_apply",
        meta={
            #'args': str(args),
            #'kwargs': str(kwargs),
        },
    ):
        return _groupby_apply(*args, **kwargs)


class PatchedSQLiteDatabase(sql.SQLiteDatabase):
    def read_query(self, *args, **kwargs):
        if args:
            statement = args[0]
            parameters = []
            full_statement = []

            for elem in statement._wrapped:
                if isinstance(elem, psycopg2.sql.SQL):
                    full_statement.append(elem.string)
                elif isinstance(elem, psycopg2.sql.Literal):
                    parameters.append(elem.wrapped)
        if full_statement:
            full_statement = ''.join(full_statement)

        result = super().read_query(*args, **kwargs)

        STATSD_CLIENT.event(
            STATSD_CLIENT.context.trace_id,
            "pandas.io.sql.read_query",
            meta={
                "statement": full_statement,
                "parameters": parameters,
                "result": try_make_json(result),
            }
        )
        return result


class PatchedSQLDatabase(sql.SQLDatabase):
    def execute(self, *args, **kwargs):
        result = super().execute(*args, **kwargs)
        return result


def patch():
    # pandas.read_parquet = read_parquet_patched
    # DataFrame.to_parquet = to_parquet_patched
    # pandas.merge = merge_patched
    # DataFrame.groupby = dataframe_groupby_patched
    # DataFrame.apply = dataframe_apply_patched
    # Series.apply = series_apply_patched
    # GroupBy.apply = groupby_apply_patched
    sql.SQLDatabase = PatchedSQLDatabase
    sql.SQLiteDatabase = PatchedSQLiteDatabase
