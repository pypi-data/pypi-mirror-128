import fire
from ironarms.utils import load_syms, list_tables

__all__ = ["syms"]


def tables(database_url=None, schema="public", verbose=False):
    """Prints tables, names, columns, and schemas.

    Usages::

        # only tables under schema public
        ironarms tables
        # tables under all schemas
        ironarms tables --schema=None

    """
    r = list_tables(database_url=database_url, schema=schema)

    if not verbose:
        for k, v in r.items():
            v["columns"] = [x["name"] for x in v["columns"]]
    for k, v in r.items():
        print(
            f"table={k!r} schema={v['schema']!r} shape=({v['rows']}, {v['cols']})\n"
            f"  cols={v['columns']}"
        )


def syms(sym_table=None, database_url=None):
    """Prints unique syms from pg table, line by line.

    Usages::

            ironarms syms
    """
    s = load_syms(sym_table=sym_table, database_url=database_url)
    for x in s:
        print(x)


def main():
    fire.Fire({"tables": tables, "syms": syms})
