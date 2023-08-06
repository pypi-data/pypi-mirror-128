from datetime import datetime
from .url import ext_from_url
from .helper import safe_str, md5

__all__ = ["path_from_dict"]


def path_from_dict(
    d,
    sym_sep="/",
    max_kind_size=20,
    max_dt_size=20,
    max_title_size=100,
    url_hash_size=8,
    default_suffix=".html",
):
    """Makes a path string from a dictionary ``d``.

    Optional keys: ``["sym", "sym_sep"]``.

    Must have keys: ``["kind", "dt", "title", "url"]``.


    """
    if not isinstance(d, dict):
        raise TypeError(f"not a dict: {type(d)}")
    lst = []
    if not isinstance(d, dict):
        raise TypeError(f"should be str or dict: {type(d)}")
    keys = [x for x in ["kind", "dt", "title"] if x in d]
    for k in keys:
        v = d[k]
        if k == "kind":
            v = safe_str(v)[:max_kind_size]
        elif k == "dt":
            if isinstance(v, datetime):
                v = v.strftime("%Y%m%d_%H%M%S")
            v = v.replace("-", "").replace(":", "")
            v = safe_str(v)[:max_dt_size]
        elif k == "title":
            v = safe_str(v)[:max_title_size]
        lst.append(v)
    if "url" in d and d["url"] is not None and len(d["url"]) > 5:
        lst.append(safe_str(md5(d["url"]))[:url_hash_size])
    lst = [x for x in lst if x is not None and isinstance(x, str) and len(x) > 1]
    if len(lst) == 0:
        raise ValueError(f"invalid input: {d}")
    p = "_".join(lst)
    # sym
    if "sym" in d and d["sym"] is not None:
        sym = safe_str(d["sym"])
        p = sym + sym_sep + p
    # suffix
    suffix = default_suffix
    if "url" in d and d["url"] is not None and len(d["url"]) > 5:
        v = ext_from_url(d["url"]).lower()
        if v in [".html", ".shtml", ".phtml", ".htm", ".pdf", ".csv", ".txt"]:
            suffix = v
    p = p + suffix
    return p
