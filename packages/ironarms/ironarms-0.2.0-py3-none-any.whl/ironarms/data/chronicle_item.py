# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime
import scrapy
import dateparser
from ironarms.utils import (
    path_from_dict,
    domain_from_url,
    safe_str,
    col_size_from_model,
)
from .chronicle_model import ChronicleModel

__all__ = ["ChronicleItem", "make_chronicle_item"]


MAX_SIZE = col_size_from_model(ChronicleModel)
"""Max size of some fields.  The same as defined in the :class:`ChronicleModel`."""


class ChronicleItem(scrapy.Item):
    """Item of a piece of chronicle information.

    Fields must be provided: ``["url", "title", "dt", "kind", "path"]``.

    It is recommended to use :func:`make_chronicle_item` to create
    :class:`ChronicleItem` object.

    A worker would fetch ``url``, save to ``path``, and update ``downloaded`` to
    ``True``.

    See Also
    --------

    make_chronicle_item
    """

    _model_cls = ChronicleModel

    # core information
    title = scrapy.Field()
    url = scrapy.Field()  # text, any length
    dt = scrapy.Field()  # when published
    sym = scrapy.Field()
    by = scrapy.Field()
    kind = scrapy.Field()
    # meta
    upd = scrapy.Field()  # when scraped
    path = scrapy.Field()  # from core information
    domain = scrapy.Field()  # from url
    status = scrapy.Field()  # cached, working, or null/None


def make_chronicle_item(**kwargs):
    """Returns an instance of :class:`ChronicleItem`.

    Keys ``["url", "title", "dt", "kind"]`` must be provided.

    The rest of keys would be computed automatically if not provided.

    If ``dt`` are strings, :func:`dateparser.parse` would be used to convert them to
    :class:`datetime.datetime`.

    ``path``, ``domain`` will be computed from other values, ``upd`` would be assigned
    current ``datetime.now()``, ``status`` would be assigned ``None``.

    Returns
    -------

    ChronicleItem

    Raises
    ------

    invalid input
    """
    must_have = ["url", "title", "dt", "kind"]
    d = kwargs.copy()
    missing = [x for x in must_have if x not in d]
    if len(missing) > 0:
        raise ValueError(f"missing keys: {missing}")

    for k in ["title", "kind"]:
        d[k] = safe_str(d[k])

    for k in MAX_SIZE:
        if k in d:
            d[k] = d[k][: MAX_SIZE[k]]

    if isinstance(d["dt"], str):
        v = dateparser.parse(d["dt"])
        if v is None:
            raise TypeError(f"invalid dt: {d['dt']}")
        d["dt"] = v

    d["path"] = path_from_dict(d, sym_sep="/")
    d["domain"] = domain_from_url(d["url"])
    d["status"] = None
    d["upd"] = datetime.now()
    for k in [x for x in MAX_SIZE if x in d]:
        n = MAX_SIZE[k]
        if k == "path" and len(d) > n:
            raise RuntimeError(
                f"implementation problem: path generated larger than {n}"
            )
        if d[k] is None:
            continue
        if k == "domain":
            d[k] = d[k][-n:]
        else:
            d[k] = d[k][:n]
    return ChronicleItem(**d)
