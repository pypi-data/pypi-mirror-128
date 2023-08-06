import akrophonobolos as obol
from fractions import Fraction
import pytest


def test_ig_I_3_369_7():
    # 𐅊· τόκος τούτον ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ
    assert obol.loan_term("𐅊", "ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ") == 1397
    assert obol.interest("𐅊", 1397) == obol.Khremata("ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ")
    assert obol.principal("ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ", 1397) == obol.Khremata("𐅊")


@pytest.mark.xfail(reason="Different from restorated text")
def test_ig_I_3_369_7_8():
    # 𐅉[𐅉𐅈ΤΤΤ𐅆𐅅ΗΔΙΙΙ𐅁]· τόκος τούτον ΤΧ𐅅ΗΗΔ𐅃𐅂𐅂𐅂𐅂ΙΙ
    assert obol.principal("ΤΧ𐅅ΗΗΔ𐅃𐅂𐅂𐅂𐅂ΙΙ", 1349) == "𐅉𐅉𐅈ΤΤΤ𐅆𐅅ΗΔΙΙΙ𐅁"


def test_ig_I_3_369_12():
    # 𐅋· τόκος τούτον ΤΤΤ𐅆𐅅ΗΗΗΗΔΔΔΔ
    assert obol.loan_term("𐅋", "ΤΤΤ𐅆𐅅ΗΗΗΗΔΔΔΔ") == 1197
    assert obol.interest("𐅋", 1197) == obol.Khremata("ΤΤΤ𐅆𐅅ΗΗΗΗΔΔΔΔ")
    assert obol.principal("ΤΤΤ𐅆𐅅ΗΗΗΗΔΔΔΔ", 1197) == obol.Khremata("𐅋")


def test_id_I_3_369_88():
    # ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι, τόκος τούτο 𐅂ΙΙΙΙΙ𐅁
    assert obol.loan_term("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", "𐅂ΙΙΙΙΙ𐅁") == 17

    assert float(obol.loan_term("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", "𐅂ΙΙΙΙΙ𐅁",
                                roundoff=False)) == 16.82188307572285

    assert obol.interest("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", 17, roundup=False) == \
        11.621766666666666

    assert obol.principal("𐅂ΙΙΙΙΙ𐅁", 17, roundup=False) == 20294.11764705882


@pytest.mark.xfail(reason="Different rounding")
def test_id_I_3_369_88_rounded_interest():
    # 1d 5¾b vs. 1d 5½b
    assert obol.interest("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι", 17) == obol.Khremata("𐅂ΙΙΙΙΙ𐅁")


@pytest.mark.xfail(reason="Different rounding")
def test_id_I_3_369_88_rounded_principal():
    # 3382d 2¼b vs 3418d 1b
    assert obol.principal("𐅂ΙΙΙΙΙ𐅁", 17) == obol.Khremata("ΧΧΧΗΗΗΗΔ𐅃𐅂𐅂𐅂Ι")
