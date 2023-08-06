from sqlalchemy import inspect

__all__ = ["cols_from_model", "col_size_from_model"]


def cols_from_model(model_cls):
    """Returns column from a sqlalchemy model class.

    To get the string names::

        [x.name for x in cols_from_model(model_cls)]

    ref: https://stackoverflow.com/a/33219353

    Returns
    ---------
    list
    """
    return [col for col in inspect(model_cls).c]


def col_size_from_model(model_cls):
    """Returns column size from a sqlalchemy model class.

    Returns
    ---------
    dict
    """
    cols = cols_from_model(model_cls)
    r = {}
    for c in cols:
        try:
            r[c.name] = c.type.length
        except AttributeError:
            pass
    r = {k: v for k, v in r.items() if v is not None}
    return r
