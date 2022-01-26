import unittest

from gkgaas.fagi.function import IsDateKnownFormat, IsDatePrimaryFormat, \
    IsValidDate, DatesAreSame, IsGeometryMoreComplex, GeometriesCloserThan, \
    GeometriesHaveSameArea, IsSameCentroid, IsPointGeometry, \
    GeometriesIntersect, IsGeometryCoveredBy, IsLiteralAbbreviation, \
    IsSameNormalized, IsSameSimpleNormalize, IsSameCustomNormalize, \
    IsLiteralLonger, IsLiteralNumeric, IsNameValueOfficial, LiteralContains, \
    LiteralContainsTheOther, LiteralHasLanguageAnnotation, \
    LiteralsHaveSameLanguageAnnotation, IsPhoneNumberParsable, \
    IsSamePhoneNumber, IsSamePhoneNumberCustomNormalize, \
    IsSamePhoneNumberUsingExitCode, PhoneHasMoreDigits, Exists, NotExists


class TestFunctions(unittest.TestCase):
    def test_is_date_known_format(self):
        fn = IsDateKnownFormat('a')
        expected_fn_str = 'isDateKnownFormat(a)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_primary_format(self):
        fn = IsDatePrimaryFormat('a')
        expected_fn_str = 'isDatePrimaryFormat(a)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_valid_date(self):
        fn = IsValidDate('a', 'DD/MM/YYYY')
        expected_fn_str = 'isValidDate(a,DD/MM/YYYY)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_dates_are_same(self):
        fn = DatesAreSame(
            'a',
            'b',
            'yyyy/MM/dd',
            'yyyy-MM-dd',
            '10')
        expected_fn_str = 'datesAreSame(a,b,yyyy/MM/dd,yyyy-MM-dd,10)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_geometry_more_complex(self):
        fn = IsGeometryMoreComplex('a', 'b')
        expected_fn_str = 'isGeometryMoreComplex(a,b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_geometries_closer_than(self):
        fn = GeometriesCloserThan('a', 'b', '50')
        expected_fn_str = 'geometriesCloserThan(a,b,50)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_geometries_have_same_area(self):
        fn = GeometriesHaveSameArea('a', 'b', '100')
        expected_fn_str = 'geometriesHaveSameArea(a,b,100)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_same_centroid(self):
        fn = IsSameCentroid('a', 'b', '30')
        expected_fn_str = 'isSameCentroid(a,b,30)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_point_geometry(self):
        fn = IsPointGeometry('a')
        expected_fn_str = 'isPointGeometry(a)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_geometries_intersect(self):
        fn = GeometriesIntersect('a', 'b')
        expected_fn_str = 'geometriesIntersect(a,b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_geometry_covered_by(self):
        fn = IsGeometryCoveredBy('a', 'b')
        expected_fn_str = 'isGeometryCoveredBy(a,b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_literal_abbreviation(self):
        fn = IsLiteralAbbreviation('b')
        expected_fn_str = 'isLiteralAbbreviation(b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_same_normalized(self):
        fn = IsSameNormalized('a', 'b')
        expected_fn_str = 'isSameNormalized(a,b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_same_simple_normalize(self):
        fn = IsSameSimpleNormalize('a', 'b', '0.7')
        expected_fn_str = 'isSameSimpleNormalize(a,b,0.7)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_same_custom_normalize(self):
        fn = IsSameCustomNormalize('a', 'b', '0.6')
        expected_fn_str = 'isSameCustomNormalize(a,b,0.6)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_literal_longer(self):
        fn = IsLiteralLonger('a', 'b')
        expected_fn_str = 'isLiteralLonger(a,b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_literal_numeric(self):
        fn = IsLiteralNumeric('b')
        expected_fn_str = 'isLiteralNumeric(b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_name_value_offocial(self):
        fn = IsNameValueOfficial('a')
        expected_fn_str = 'isNameValueOfficial(a)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_literal_contains(self):
        fn = LiteralContains('a', 'bar')
        expected_fn_str = 'literalContains(a,bar)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_literal_contains_the_other(self):
        fn = LiteralContainsTheOther('b', 'a')
        expected_fn_str = 'literalContainsTheOther(b,a)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_literal_has_language_annotation(self):
        fn = LiteralHasLanguageAnnotation('a')
        expected_fn_str = 'literalHasLanguageAnnotation(a)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_literals_have_same_language_annotation(self):
        fn = LiteralsHaveSameLanguageAnnotation('a', 'b')
        expected_fn_str = 'literalsHaveSameLanguageAnnotation(a,b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_phone_number_parsable(self):
        fn = IsPhoneNumberParsable('a')
        expected_fn_str = 'isPhoneNumberParsable(a)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_same_phone_number(self):
        fn = IsSamePhoneNumber('a', 'b')
        expected_fn_str = 'isSamePhoneNumber(a,b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_same_phone_number_custom_normalize(self):
        fn = IsSamePhoneNumberCustomNormalize('a', 'b')
        expected_fn_str = 'isSamePhoneNumberCustomNormalize(a,b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_is_same_phone_number_using_exit_code(self):
        fn = IsSamePhoneNumberUsingExitCode('a', 'b', '0030')
        expected_fn_str = 'isSamePhoneNumberUsingExitCode(a,b,0030)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_phone_has_more_digits(self):
        fn = PhoneHasMoreDigits('a', 'b')
        expected_fn_str = 'phoneHasMoreDigits(a,b)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_exists(self):
        fn = Exists('a')
        expected_fn_str = 'exists(a)'

        self.assertEqual(expected_fn_str, str(fn))

    def test_not_exists(self):
        fn = NotExists('b')
        expected_fn_str = 'notExists(b)'

        self.assertEqual(expected_fn_str, str(fn))
