from pathlib import Path
import re

__all__ = ["save"]


def save(x, path, fix_encoding=True):
    """Saves content of x to path.

    The parent directory of ``path`` would be created if not already.

    Parameters
    ----------
    x: str
    path: str, or Path
    fix_encoding: bool, default True
        If True, replace ``charset`` inside ``x`` from ``gb2312`` to ``utf-8``.

    """
    if fix_encoding:
        x = re.sub("charset=gb2312", "charset=utf-8", x)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(x)
