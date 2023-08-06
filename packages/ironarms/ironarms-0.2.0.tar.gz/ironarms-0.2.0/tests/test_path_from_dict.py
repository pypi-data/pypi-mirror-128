from datetime import datetime
from ironarms.utils import path_from_dict
import pytest


def test_path_from_dict_1():
    d = dict(
        url="http://finance.yahoo/some_url.htm", dt="2010-01-01", title="some title"
    )
    assert path_from_dict(d) == "20100101_some_title_208616d9.htm"
    d["dt"] = datetime(2010, 1, 1)
    assert path_from_dict(d) == "20100101_000000_some_title_208616d9.htm"


def test_path_from_dict_2():
    with pytest.raises(ValueError, match="invalid input:"):
        path_from_dict(dict())
    assert (
        path_from_dict(
            dict(
                url="http://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/search/rptid/690536337059/index.phtml"
            )
        )
        == "9acd0d62.phtml"
    )
    assert (
        path_from_dict(
            dict(
                url="http://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/search/rptid/690536337059/index.phtml",
                title="万科A(000002)：万物云战略路径清晰",
            )
        )
        == "万科A_000002_万物云战略路径清晰_9acd0d62.phtml"
    )
    assert (
        path_from_dict(
            dict(
                url="http://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/search/rptid/690536337059/index.phtml",
                title="万科A(000002)：万物云战略路径清晰",
                sym="000002.SZ",
            )
        )
        == "000002_SZ/万科A_000002_万物云战略路径清晰_9acd0d62.phtml"
    )
    assert (
        path_from_dict(
            dict(
                url="http://stock.finan/rptid/690536337059/index.phtml",
                title="万科A(000002)：万物云战略路径清晰",
                sym="000002.SZ",
            ),
            sym_sep="_",
        )
        == "000002_SZ_万科A_000002_万物云战略路径清晰_55e4489f.phtml"
    )
    assert (
        path_from_dict(
            dict(
                url="http://stock.finan/rptid/690536337059/index.phtml",
                title="万科A(000002)：万物云战略路径清晰",
                sym="000002.SZ",
            ),
            sym_sep="_",
            max_title_size=10,
        )
        == "000002_SZ_万科A_000002_55e4489f.phtml"
    )
