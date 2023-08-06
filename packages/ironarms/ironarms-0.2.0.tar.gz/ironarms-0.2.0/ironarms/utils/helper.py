import os
import re
from datetime import datetime
import hashlib
from scrapy.utils.project import get_project_settings

__all__ = ["safe_str", "md5", "now", "get_value"]


def get_value(key, settings=None):
    """Gets a value by key, first from environment, if failed, settings.

    If ``settings`` is ``None``, trying to get the project settings.
    """
    v = os.environ.get(key)
    if v is not None:
        return v
    if settings is None:
        settings = get_project_settings()
    if settings is None:
        return None
    return settings.get(key)


def now():
    """Returns current timestamp in datetime."""
    return datetime.now()


def md5(x):
    return hashlib.md5(x.encode()).hexdigest()


def safe_str(x):
    """Returns a string safe for file name.

    The returned string would only contains alphanumeric, e.g. ``[a-zA-Z0-9_]``, and
    Unicode word characters.

    Returns
    --------
    str, or None
    """
    if x is None:
        return
    if isinstance(x, datetime):
        x = x.strftime("%Y%m%d_%H%M%S")
    if not isinstance(x, str):
        x = str(x)
    x = re.sub(r"\s+|\W+", "_", x.strip())
    x = re.sub(r"[_]+", "_", x.strip())
    x = x.strip("_")
    if len(x) == 0:
        return None
    return x
