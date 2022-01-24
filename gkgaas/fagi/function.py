from abc import ABC, abstractmethod, abstractproperty


class FAGIEvaluationFunction(ABC):
    @abstractmethod
    def __str__(self):
        pass


class IsDateKnownFormat(FAGIEvaluationFunction):
    """
    Checks if a given string is written in a known format
    """
    function_name = 'isDateKnownFormat'

    def __init__(self, entity_variable: str):
        self.entity_variable = entity_variable

    def __str__(self):
        return f'{self.function_name}({self.entity_variable})'


class IsDatePrimaryFormat(FAGIEvaluationFunction):
    """
    Checks if the given date string is written in as a primary format.
    """
    function_name = 'isDatePrimaryFormat'

    def __init__(self, entity_variable: str):
        self.entity_variable = entity_variable

    def __str__(self):
        return f'{self.function_name}({self.entity_variable})'


class IsValidDate(FAGIEvaluationFunction):
    """
    Evaluates the given date against the target format.
    """
    function_name = 'isValidDate'

    def __init__(self, entity_variable: str, date_pattern: str):
        self.entity_variable = entity_variable
        self.date_pattern = date_pattern

    def __str__(self):
        return \
            f'{self.function_name}({self.entity_variable},{self.date_pattern})'


class DatesAreSame(FAGIEvaluationFunction):
    """
    Evaluates if the given dates are the same using a tolerance value in days.
    """
    function_name = 'datesAreSame'

    def __init__(
            self,
            first_entity_variable: str,
            second_entity_variable: str,
            first_entity_date_pattern: str,
            second_entity_date_pattern: str,
            tolerance: str):  # TODO: Check whether an int/float makes more sense here
        self.first_entity_variable = first_entity_variable
        self.first_entity_date_pattern = first_entity_date_pattern
        self.second_entity_variable = second_entity_variable
        self.second_entity_date_pattern = second_entity_date_pattern
        self.tolerance = tolerance

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_entity_variable},' \
            f'{self.second_entity_variable},' \
            f'{self.first_entity_date_pattern},' \
            f'{self.second_entity_date_pattern},' \
            f'{self.tolerance})'


class IsGeometryMoreComplex(FAGIEvaluationFunction):
    """
    Checks if the first geometry has more points than the second.
    """
    function_name = 'isGeometryMoreComplex'

    def __init__(
            self, first_geometry_variable: str, second_geometry_variable: str):

        self.first_geometry_variable = first_geometry_variable
        self.second_geometry_variable = second_geometry_variable

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_geometry_variable},{self.second_geometry_variable})'


class GeometriesCloserThan(FAGIEvaluationFunction):
    """
    Checks if the minimum distance (in meters) of the geometries are closer than
    the provided distance value. The method transforms the geometries to 3857
    CRS, computes the nearest points between them and then calculates the
    othodromic distance between the nearest points.
    """
    function_name = 'geometriesCloserThan'

    def __init__(
            self,
            first_geometry_variable: str,
            second_geometry_variable: str,
            distance: str):  # TODO: Check whether an int/float makes more sense here

        self.first_geometry_variable = first_geometry_variable
        self.second_geometry_variable = second_geometry_variable
        self.distance = distance

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_geometry_variable},' \
            f'{self.second_geometry_variable},' \
            f'{self.distance})'


class GeometriesHaveSameArea(FAGIEvaluationFunction):
    """
    Checks if the areas of the two geometries are the same given a tolerance
    value in square meters. The method transforms the geometries to 3857 CRS
    before calculating the areas.
    """
    function_name = 'geometriesHaveSameArea'

    def __init__(
            self,
            first_geometry_variable: str,
            second_geometry_variable: str,
            tolerance: str):  # TODO: Check whether an int/float makes more sense here

        self.first_geometry_variable = first_geometry_variable
        self.second_geometry_variable = second_geometry_variable
        self.tolerance = tolerance

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_geometry_variable},' \
            f'{self.second_geometry_variable},' \
            f'{self.tolerance})'


class IsSameCentroid(FAGIEvaluationFunction):
    """
    Checks if the geometries have the same centroid given a tolerance value in
    meters. The method transforms the geometries to 3857 CRS before calculating
    the orthodromic distance.
    """
    function_name = 'isSameCentroid'

    def __init__(
            self,
            first_geometry_variable: str,
            second_geometry_variable: str,
            tolerance: str):  # TODO: Check whether an int/float makes more sense here

        self.first_geometry_variable = first_geometry_variable
        self.second_geometry_variable = second_geometry_variable
        self.tolerance = tolerance

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_geometry_variable},' \
            f'{self.second_geometry_variable},' \
            f'{self.tolerance})'


class IsPointGeometry(FAGIEvaluationFunction):
    """
    Checks if the given geometry is a POINT geometry.
    """
    function_name = 'isPointGeometry'

    def __init__(self, geometry_variable: str):
        self.geometry_variable = geometry_variable

    def __str__(self):
        return f'{self.function_name}({self.geometry_variable})'


class GeometriesIntersect(FAGIEvaluationFunction):
    """
    Checks if the given geometries intersect.
    """
    function_name = 'geometriesIntersect'

    def __init__(
            self,
            first_geometry_variable: str,
            second_geometry_variable: str):

        self.first_geometry_variable = first_geometry_variable
        self.second_geometry_variable = second_geometry_variable

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_geometry_variable},' \
            f'{self.second_geometry_variable})'


class IsGeometryCoveredBy(FAGIEvaluationFunction):
    """
    Checks if the first geometry is covered by the second geometry. The
    definition of coveredBy can be found at
    https://en.wikipedia.org/wiki/DE-9IM .
    """
    function_name = 'isGeometryCoveredBy'

    def __init__(
            self,
            first_geometry_variable: str,
            second_geometry_variable: str):

        self.first_geometry_variable = first_geometry_variable
        self.second_geometry_variable = second_geometry_variable

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_geometry_variable},' \
            f'{self.second_geometry_variable})'


class IsLiteralAbbreviation(FAGIEvaluationFunction):
    """
    Checks if the given literal is or contains an abbreviation of some form.
    """
    function_name = 'isLiteralAbbreviation'

    def __init__(self, literal_variable: str):
        self.literal_variable = literal_variable

    def __str__(self):
        return f'{self.function_name}({self.literal_variable})'


class IsSameNormalized(FAGIEvaluationFunction):
    """
    Checks if the two given literals are the same. It normalizes the two
    literals with some basic steps and uses the provided similarity (default
    JaroWinkler). No threshold provided.
    """
    function_name = 'isSameNormalized'

    def __init__(
            self,
            first_literal_variable: str,
            second_literal_variable: str):

        self.first_literal_variable = first_literal_variable
        self.second_literal_variable = second_literal_variable

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_literal_variable},' \
            f'{self.second_literal_variable})'


class IsSameSimpleNormalize(FAGIEvaluationFunction):
    """
    This function is the same as IsSameNormalized but it uses a threshold as a
    tolerance value. Returns true if the result is above the provided threshold.
    The threshold must be between (0, 1) using a dot as decimal point
    """
    function_name = 'isSameSimpleNormalize'

    def __init__(
            self,
            first_literal_variable: str,
            second_literal_variable: str,
            threshold: str):  # TODO: Check whether a float makes more sense here

        self.first_literal_variable = first_literal_variable
        self.second_literal_variable = second_literal_variable
        self.threshold = threshold

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_literal_variable},' \
            f'{self.second_literal_variable},' \
            f'{self.threshold})'


class IsSameCustomNormalize(FAGIEvaluationFunction):
    """
    This function compares the two literals with the criteria same as
    IsSameSimpleNormalize and if the equality check fails the function
    normalizes further the two literals with some extra steps in addition to the
    simple normalization.
    """
    function_name = 'isSameCustomNormalize'

    def __init__(
            self,
            first_literal_variable: str,
            second_literal_variable: str,
            threshold: str):  # TODO: Check whether a float makes more sense here

        self.first_literal_variable = first_literal_variable
        self.second_literal_variable = second_literal_variable
        self.threshold = threshold

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_literal_variable},' \
            f'{self.second_literal_variable},' \
            f'{self.threshold})'


class IsLiteralLonger(FAGIEvaluationFunction):
    """
    Checks if the first literal is longer than the second. The method normalizes
    the two literals using the NFC normalization before comparing the lengths.
    """
    function_name = 'isLiteralLonger'

    def __init__(
            self,
            first_literal_variable: str,
            second_literal_variable: str):

        self.first_literal_variable = first_literal_variable
        self.second_literal_variable = second_literal_variable

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_literal_variable},' \
            f'{self.second_literal_variable})'


class IsLiteralNumeric(FAGIEvaluationFunction):
    """
    Checks if the given literal is numeric (at least one digit or more).
    """
    function_name = 'isLiteralNumeric'

    def __init__(self, literal_variable: str):
        self.literal_variable = literal_variable

    def __str__(self):
        return \
            f'{self.function_name}({self.literal_variable})'


class IsNameValueOfficial(FAGIEvaluationFunction):
    """
    Checks if the vlue of the name property is tagged as official.
    """
    function_name = 'isNameValueOfficial'

    def __init__(self, literal_variable: str):
        self.literal_variable = literal_variable

    def __str__(self):
        return \
            f'{self.function_name}({self.literal_variable})'


class LiteralContains(FAGIEvaluationFunction):
    """
    Checks if the literal contains the given value.
    """
    function_name = 'literalContains'

    def __init__(
            self,
            literal_variable: str,
            value: str):
        self.literal_variable = literal_variable
        self.value = value

    def __str__(self):
        return \
            f'{self.function_name}({self.literal_variable},{self.value})'


class LiteralContainsTheOther(FAGIEvaluationFunction):
    """
    Checks if the first literal contains the second.
    """
    function_name = 'literalContainsTheOther'

    def __init__(
            self, first_literal_variable: str, second_literal_variable: str):

        self.first_literal_variable = first_literal_variable
        self.second_literal_variable = second_literal_variable

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_literal_variable},' \
            f'{self.second_literal_variable})'


class LiteralHasLanguageAnnotation(FAGIEvaluationFunction):
    """
    Checks if the literal contains a language annotation tag.
    """
    function_name = 'literalHasLanguageAnnotation'

    def __init__(self, literal_variable: str):
        self.literal_variable = literal_variable

    def __str__(self):
        return \
            f'{self.function_name}({self.literal_variable})'


class LiteralsHaveSameLanguageAnnotation(FAGIEvaluationFunction):
    """
    Checks if the two literals have the same language annotation tag.
    """
    function_name = 'literalsHaveSameLanguageAnnotation'

    def __init__(
            self, first_literal_variable: str, second_literal_variable: str):

        self.first_literal_variable = first_literal_variable
        self.second_literal_variable = second_literal_variable

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_literal_variable},' \
            f'{self.second_literal_variable})'


class IsPhoneNumberParsable(FAGIEvaluationFunction):
    """
    Checks if a given phone number only consists of numbers or if it contains
    special character and/or exit code.
    """
    function_name = 'isPhoneNumberParsable'

    def __init__(self, literal_variable: str):
        self.literal_variable = literal_variable

    def __str__(self):
        return \
            f'{self.function_name}({self.literal_variable})'


class IsSamePhoneNumber(FAGIEvaluationFunction):
    """
    Checks if the given phone numbers are the same. Some phone normalization
    steps are executed if the first evaluation fails.
    """
    function_name = 'isSamePhoneNumber'

    def __init__(
            self, first_literal_variable: str, second_literal_variable: str):

        self.first_literal_variable = first_literal_variable
        self.second_literal_variable = second_literal_variable

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_literal_variable},' \
            f'{self.second_literal_variable})'


class IsSamePhoneNumberCustomNormalize(FAGIEvaluationFunction):
    """
    Checks if the given phone numbers are the same. If the equality check fails
    some custom steps for normalization are executed and the function rechecks
    for equality (e.g. two phone numbers are considered the same if one of them
    does not contain a country code but the line number is the same etc.)
    """
    function_name = 'isSamePhoneNumberCustomNormalize'

    def __init__(
            self, first_literal_variable: str, second_literal_variable: str):

        self.first_literal_variable = first_literal_variable
        self.second_literal_variable = second_literal_variable

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_literal_variable},' \
            f'{self.second_literal_variable})'


class IsSamePhoneNumberUsingExitCode(FAGIEvaluationFunction):
    """
    Same as IsSamePhoneNumberCustomNormalize, except the exit code, which is
    checked separately using the input value.
    """
    function_name = 'isSamePhoneNumberUsingExitCode'

    def __init__(
            self,
            first_literal_variable: str,
            second_literal_variable: str,
            digits: str):

        self.first_literal_variable = first_literal_variable
        self.second_literal_variable = second_literal_variable
        self.digits = digits

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_literal_variable},' \
            f'{self.second_literal_variable},' \
            f'{self.digits})'


class PhoneHasMoreDigits(FAGIEvaluationFunction):
    """
    Checks if the first phone number has more digits than the second.
    """
    function_name = 'phoneHasMoreDigits'

    def __init__(
            self, first_literal_variable: str, second_literal_variable: str):

        self.first_literal_variable = first_literal_variable
        self.second_literal_variable = second_literal_variable

    def __str__(self):
        return \
            f'{self.function_name}(' \
            f'{self.first_literal_variable},' \
            f'{self.second_literal_variable})'


class Exists(FAGIEvaluationFunction):
    """
    Checks if a given property exists in the model of the entity.
    """
    function_name = 'exists'

    def __init__(self, property_variable: str):
        self.property_variable = property_variable

    def __str__(self):
        return \
            f'{self.function_name}({self.property_variable})'


class NotExists(FAGIEvaluationFunction):
    """
    The reverse function of exists. Returns true if the selected property is not
    found in the model.
    """
    function_name = 'notExists'

    def __init__(self, property_variable: str):
        self.property_variable = property_variable

    def __str__(self):
        return \
            f'{self.function_name}({self.property_variable})'
