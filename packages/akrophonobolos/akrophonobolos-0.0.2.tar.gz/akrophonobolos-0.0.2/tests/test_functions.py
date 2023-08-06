import akrophonobolos as obol
from fractions import Fraction


def test_version():
    assert obol.version() == "0.0.2"


def test_parse_amt():
    assert obol.parse_amount("1T") == 36_000
    assert obol.parse_amount("1t") == 36_000
    assert obol.parse_amount("813D") == 4_878
    assert obol.parse_amount("813d") == 4_878
    assert obol.parse_amount("1.5O") == 1.5
    assert obol.parse_amount("1.5o") == 1.5
    assert obol.parse_amount("1.5b") == 1.5
    assert obol.parse_amount("1t813d") == 40878
    assert obol.parse_amount("1t813d") == 40878
    assert obol.parse_amount("1T1.5O") == 36_001.5
    assert obol.parse_amount("813D1.5O") == 4_879.5

    assert obol.parse_amount("1T813D1½O") == 40879.5
    assert obol.parse_amount("1t 813d 1½b") == 40879.5
    assert obol.parse_amount("1T813D1½O") == 40879.5
    assert obol.parse_amount("1t 813d 1½b") == 40879.5
    assert obol.parse_amount("1t 813d 1¼b") == 40879.25
    assert obol.parse_amount("1t 813d ½b") == 40878.5


def test_parse_amt_obol_rounding():
    assert obol.parse_amount("1O") == 1
    assert obol.parse_amount("0.9O") == 0.9

    assert obol.parse_amount("0.8O") == 0.8
    assert obol.parse_amount("0.75O") == 0.75
    assert obol.parse_amount("0.7O") == 0.7

    assert obol.parse_amount("0.6O") == 0.6
    assert obol.parse_amount("0.5O") == 0.5
    assert obol.parse_amount("0.4O") == 0.4

    assert obol.parse_amount("0.3O") == 0.3
    assert obol.parse_amount("0.25O") == 0.25
    assert obol.parse_amount("0.1O") == 0.1
    assert obol.parse_amount("0.3O") == 0.3


def test_parse_greek_amt():
    assert obol.parse_greek_amount("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁") == 40_879.5
    assert obol.parse_greek_amount("ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ") == 83_820


def test_format_amount_abbreviation():
    assert obol.format_amount(36_007) == "1t 1d 1b"
    assert obol.format_amount(72_014) == "2t 2d 2b"
    assert obol.format_amount(72_002) == "2t 2b"
    assert obol.format_amount(72_014.5) == "2t 2d 2½b"
    assert obol.format_amount(72_013.25) == "2t 2d 1¼b"
    assert obol.format_amount(72_012.25) == "2t 2d ¼b"

    # Abbreviation is the default
    assert obol.format_amount(144_028, obol.Fmt.ABBR) == \
        obol.format_amount(144_028)


def test_format_amount_abbreviation_decimal():
    assert obol.format_amount(36_007, obol.Fmt.DECIMAL) == "1t 1d 1b"
    assert obol.format_amount(72_014, obol.Fmt.DECIMAL) == "2t 2d 2b"
    assert obol.format_amount(72_002, obol.Fmt.DECIMAL) == "2t 2b"
    assert obol.format_amount(72_014.5, obol.Fmt.DECIMAL) == "2t 2d 2.5b"
    assert obol.format_amount(72_013.25, obol.Fmt.DECIMAL) == "2t 2d 1.25b"
    assert obol.format_amount(72_012.25, obol.Fmt.DECIMAL) == "2t 2d 0.25b"
    assert obol.format_amount(72_012.125, obol.Fmt.DECIMAL) == "2t 2d 0.125b"
    assert obol.format_amount(72_012.0625, obol.Fmt.DECIMAL) == "2t 2d 0.0625b"


def test_format_greek():
    assert obol.format_amount(40_879.5, obol.Fmt.GREEK) == "Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁"
    assert obol.format_amount(83_820, obol.Fmt.GREEK) == "ΤΤΧ𐅅ΗΗΗΗ𐅄ΔΔ"


def test_format_amount_english():
    assert obol.format_amount(36_007, obol.Fmt.ENGLISH) == \
        "1 talent, 1 drachma, 1 obol"
    assert obol.format_amount(72_014, obol.Fmt.ENGLISH) == \
        "2 talents, 2 drachmas, 2 obols"
    assert obol.format_amount(72_002, obol.Fmt.ENGLISH) == \
        "2 talents, 2 obols"
    assert obol.format_amount(72_014.5, obol.Fmt.ENGLISH) == \
        "2 talents, 2 drachmas, 2½ obols"
    assert obol.format_amount(72_013.25, obol.Fmt.ENGLISH) == \
        "2 talents, 2 drachmas, 1¼ obols"
    assert obol.format_amount(72_012.25, obol.Fmt.ENGLISH) == \
        "2 talents, 2 drachmas, ¼ obol"

    # An eighth of an obol should round down to 0
    assert obol.format_amount(72_012.125, obol.Fmt.ENGLISH) == \
        "2 talents, 2 drachmas, 0 obol"


def test_format_amount_english_decimal():
    assert obol.format_amount(
        36_007, obol.Fmt.ENGLISH | obol.Fmt.DECIMAL) == \
        "1 talent, 1 drachma, 1 obol"
    assert obol.format_amount(
        72_014, obol.Fmt.ENGLISH | obol.Fmt.DECIMAL) == \
        "2 talents, 2 drachmas, 2 obols"
    assert obol.format_amount(
        72_002, obol.Fmt.ENGLISH | obol.Fmt.DECIMAL) == \
        "2 talents, 2 obols"
    assert obol.format_amount(
        72_014.5, obol.Fmt.ENGLISH | obol.Fmt.DECIMAL) == \
        "2 talents, 2 drachmas, 2.5 obols"
    assert obol.format_amount(
        72_013.25, obol.Fmt.ENGLISH | obol.Fmt.DECIMAL) == \
        "2 talents, 2 drachmas, 1.25 obols"
    assert obol.format_amount(
        72_012.25, obol.Fmt.ENGLISH | obol.Fmt.DECIMAL) == \
        "2 talents, 2 drachmas, 0.25 obol"


def test_valid_amount_str():
    assert obol.valid_amount_str("1T")
    assert not obol.valid_amount_str("1Z")
    assert obol.valid_amount_str("261T5600D")


def test_valid_greek_str():
    assert obol.valid_greek_amount("Τ𐅅ΗΗΗΔ𐅂𐅂𐅂Ι𐅁")
    assert not obol.valid_greek_amount("1Z")


def test_fractions():
    assert obol.format_amount(0.25) == "¼b"
    assert obol.format_amount(0.5) == "½b"
    assert obol.format_amount(0.75) == "¾b"


def test_interest_rate():
    # It should return a fraction
    assert isinstance(obol.interest_rate(), Fraction)

    # With defaults it should be 1/30000
    assert obol.interest_rate() == Fraction(1, 30_000)

    # It should accept instances of Khremata
    assert obol.interest_rate(obol.Khremata("2t")) == Fraction(1, 12_000)
    assert obol.interest_rate(r=obol.Khremata("1t")) == Fraction(1, 5)

    # It should accept strings
    assert obol.interest_rate("2t") == Fraction(1, 12_000)
    assert obol.interest_rate(r="1t") == Fraction(1, 5)

    # It should accept numbers
    assert obol.interest_rate(72_000) == Fraction(1, 12_000)
    assert obol.interest_rate(r=3_6000) == Fraction(1, 5)


def test_interest():
    # It should return an instance of Khremata
    assert isinstance(obol.interest("1t 1748d", 17), obol.Khremata)

    # It should accept an instance of Khremata
    assert obol.interest(obol.Khremata("5t"), 1) == 6
    assert obol.interest(obol.Khremata("1t 1748d"), 17) == 26.5

    # It should accept a string
    assert obol.interest("5t", 1) == 6
    assert obol.interest("1t 1748d", 17) == 26.5

    # It should accept a number
    assert obol.interest(180_000, 1) == 6
    assert obol.interest(46_488, 17) == 26.5

    # It should let you calculate exactly
    assert obol.interest(180_000, 1, roundup=False) == 6
    assert obol.interest(46_488, 17, roundup=False) == 26.343200000000003


def test_principal():
    # It should return an instance of Khremata
    assert isinstance(obol.principal("1d", 1), obol.Khremata)

    # It should accept an instance of Khremata
    assert obol.principal(obol.Khremata("1d"), 1) == 180_000

    # It should accept a string
    assert obol.principal("1d", 1) == 180_000

    # It should accept a number
    assert obol.principal(6, 1) == 180_000

    # It should let you calculate exactly
    assert obol.principal(6, 1, roundup=False) == 180_000
    assert obol.principal(26.5, 17, roundup=False) == 46764.70588235294


def test_loan_term():
    # It should return a float
    # assert isinstance(obol.loan_term("5t", "1d"), float)

    # It should accept instances of Khremata
    assert obol.loan_term(obol.Khremata("5t"), obol.Khremata("1d")) == 1

    # It should accept strings
    assert obol.loan_term("5t", "1d") == 1

    # It should accept numbers
    assert obol.loan_term(180_000, 6) == 1

    # It should accept a mix
    assert obol.loan_term(obol.Khremata("5t"), "1d") == 1
    assert obol.loan_term(obol.Khremata("5t"), 6) == 1
    assert obol.loan_term("5t", obol.Khremata("1d")) == 1
    assert obol.loan_term(180_000, obol.Khremata("1d")) == 1

    # It should let you calculate exactly
    assert obol.loan_term("5t", "1d", roundoff=False) == 1
    assert float(obol.loan_term("3419d", "1d 5.5b", roundoff=False)) == \
        16.817782977478796


def test_roundup_to_quarter():
    # Should round up to the quarter obol
    assert obol.roundup_to_quarter_obol(26.343200000000003) == 26.5
    assert obol.roundup_to_quarter_obol(26.1) == 26.25
    assert obol.roundup_to_quarter_obol(26) == 26

    # If given a Khremata, should return a Khremata
    assert isinstance(
        obol.roundup_to_quarter_obol(obol.Khremata(26.343200000000003)),
        obol.Khremata)

    # Otherwise should return a float
    assert isinstance(obol.roundup_to_quarter_obol(26.343200000000003),
                      float)
    assert isinstance(obol.roundup_to_quarter_obol(26),
                      float)
