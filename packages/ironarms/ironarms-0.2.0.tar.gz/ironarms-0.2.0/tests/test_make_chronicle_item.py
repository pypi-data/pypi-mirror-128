from ironarms.data import make_chronicle_item, ChronicleItem, ChronicleModel
from ironarms.data.chronicle_item import MAX_SIZE
import pytest


def test_max_size():
    assert isinstance(MAX_SIZE, dict)
    assert MAX_SIZE == {
        "title": 200,
        "sym": 20,
        "by": 100,
        "kind": 20,
        "path": 300,
        "domain": 20,
        "status": 20,
    }


def test_make_chronicle_item():
    with pytest.raises(
        ValueError, match=r"missing keys: \['url', 'title', 'dt', 'kind'\]"
    ):
        make_chronicle_item()
    d = dict(url="http://url", title="it's a title", dt="nonsense", kind="test")
    with pytest.raises(TypeError, match="invalid dt: nonsense"):
        make_chronicle_item(**d)
    d["dt"] = "2011-01-01"
    item = make_chronicle_item(**d)
    assert isinstance(item, ChronicleItem)
    assert set(item.keys()) == {
        "path",
        "upd",
        "status",
        "url",
        "dt",
        "kind",
        "title",
        "domain",
    }
    assert item._model_cls is ChronicleModel
    assert item["path"] == "test_20110101_000000_it_s_a_title_312c7f70.html"
