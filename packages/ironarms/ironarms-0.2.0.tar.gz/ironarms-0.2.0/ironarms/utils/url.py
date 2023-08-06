from os.path import splitext
from urllib.parse import urlparse

__all__ = ["ext_from_url", "domain_from_url"]


def ext_from_url(x):
    """Returns extension of a url string"""
    path = urlparse(x).path
    ext = splitext(path)[1]
    return ext


def domain_from_url(x):
    """Returns domain from url string."""
    d = urlparse(x).netloc
    lst = d.split(".")
    lst = [x for x in lst if x not in ["vip", "com", "edu", "cn"]]
    return ".".join(lst)
