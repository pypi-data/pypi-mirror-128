from datetime import datetime
from ironarms.utils import safe_str


def test_safe_str_1():
    assert safe_str("abcd_xy-12") == "abcd_xy_12"
    assert safe_str("ab测试cd_xy-12") == "ab测试cd_xy_12"
    assert safe_str("abcd  _xy-12") == "abcd_xy_12"
    assert safe_str("abcd\n_xy-12") == "abcd_xy_12"
    assert safe_str("abcd_\nxy\t-12") == "abcd_xy_12"
    assert safe_str("abcd  _\nxy \t - 12") == "abcd_xy_12"
    assert safe_str("abcd  _\nxy \t - 12") == "abcd_xy_12"
    assert safe_str("abcd “ 测试\n ”. _\nxy 。，\t - 12") == "abcd_测试_xy_12"
    assert (
        safe_str("国海证券：首予春秋航空(601021.SH)“增持”评级 需求红利促成长 规模持续高增")
        == "国海证券_首予春秋航空_601021_SH_增持_评级_需求红利促成长_规模持续高增"
    )
    assert safe_str("【自复制mRNA】 智源信使 （ Reliome） ") == "自复制mRNA_智源信使_Reliome"


def test_safe_str_2():
    assert safe_str(datetime(2001, 1, 2)) == "20010102_000000"
    assert safe_str(datetime(2001, 1, 2, 3, 4, 5)) == "20010102_030405"
    safe_str("finance.yahoo.com")


def test_safe_str_3():
    assert safe_str(dict(x=1, y=2.718, z="test", a="测试")) == "x_1_y_2_718_z_test_a_测试"
