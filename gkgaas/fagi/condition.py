from abc import ABC, abstractmethod
from dataclasses import dataclass

from gkgaas.fagi.function import FAGIEvaluationFunction


class FAGIRuleConditionExpression(ABC):
    @abstractmethod
    def __str__(self):
        pass


class SimpleFAGIRuleConditionExpression(FAGIRuleConditionExpression):
    """
    A simple FAGI rule condition expression refers to just one evaluation
    function and is rendered as in the following example:

    <function>isLiteralAbbreviation(b1)</function>

    A simple FAGI rule condition expression can appear directly inside a rule
    condition, or inside any logical connective.
    """

    def __init__(self, evaluation_function: FAGIEvaluationFunction):
        self.evaluation_function = evaluation_function

    def __str__(self):
        return \
            f'<function>{str(self.evaluation_function)}</function>'


class And(FAGIRuleConditionExpression):
    """
    A conjunction of FAGI rule condition expressions. A conjunction is rendered
    as follows:

    <expression>
        <and>
            <function>geometriesCloserThan(a0, b0, 150)</function>
            <function>isSameCustomNormalize(a2, b2, 0.8)</function>
        </and>
    </expression>

    (Example taken from https://github.com/SLIPO-EU/workbench/blob/master/common/vendor/fagi/config/profiles/SLIPO_GET_OSM_aaMode/rules.xml)

    However, conjunctions can contain any kind of FAGI rule condition
    expression, possibly also nested conjunctions, e.g.

    <expression>
        <and>
            <function>geometriesCloserThan(a0, b0, 150)</function>
            <expression>
                <and>
                    <function>geometriesCloserThan(a1, b1, 250)</function>
                    <function>isSameCustomNormalize(a2, b2, 0.8)</function>
                </and>
            </expression>
        </and>
    </expression>

    To ensure that the expression string is rendered with the correct
    indentation level we allow providing a nesting level parameter
    """

    def __init__(
            self,
            first_expression: FAGIRuleConditionExpression,
            second_expression: FAGIRuleConditionExpression,
            nesting_level: int = 0):

        self.first_expression = first_expression
        self.second_expression = second_expression
        self.nesting_level = nesting_level

    def __str__(self):
        return \
            f"""
                    {self.nesting_level * 8 * ' '}<expression>
                    {self.nesting_level * 8 * ' '}    <and>
                    {self.nesting_level * 8 * ' '}        {str(self.first_expression).strip()}
                    {self.nesting_level * 8 * ' '}        {str(self.second_expression).strip()}
                    {self.nesting_level * 8 * ' '}    </and>
                    {self.nesting_level * 8 * ' '}</expression>"""


class Or(FAGIRuleConditionExpression):
    """
    A disjunction of FAGI rule condition expressions. A disjunction is rendered
    as follows:

    <expression>
        <or>
            <function>geometriesCloserThan(a0, b0, 150)</function>
            <function>isSameCustomNormalize(a2, b2, 0.8)</function>
        </or>
    </expression>

    (Example adapted from https://github.com/SLIPO-EU/workbench/blob/master/common/vendor/fagi/config/profiles/SLIPO_GET_OSM_aaMode/rules.xml)

    However, disjunctions can contain any kind of FAGI rule condition
    expression, possibly also nested disjunctions, e.g.

    <expression>
        <or>
            <function>geometriesCloserThan(a0, b0, 150)</function>
            <expression>
                <or>
                    <function>geometriesCloserThan(a1, b1, 250)</function>
                    <function>isSameCustomNormalize(a2, b2, 0.8)</function>
                </or>
            </expression>
        </or>
    </expression>

    To ensure that the expression string is rendered with the correct
    indentation level we allow providing a nesting level parameter
    """

    def __init__(
            self,
            first_expression: FAGIRuleConditionExpression,
            second_expression: FAGIRuleConditionExpression,
            nesting_level: int = 0):

        self.first_expression = first_expression
        self.second_expression = second_expression
        self.nesting_level = nesting_level

    def __str__(self):
        return \
            f"""
                    {self.nesting_level * 8 * ' '}<expression>
                    {self.nesting_level * 8 * ' '}    <or>
                    {self.nesting_level * 8 * ' '}        {str(self.first_expression).strip()}
                    {self.nesting_level * 8 * ' '}        {str(self.second_expression).strip()}
                    {self.nesting_level * 8 * ' '}    </or>
                    {self.nesting_level * 8 * ' '}</expression>"""


class Not(FAGIRuleConditionExpression):
    """
    Negation of a FAGI rule condition expression. A negation is rendered as
    follows:

    <expression>
        <not>
            <function>isSameCustomNormalize(a,b,0.5)</function>
        </not>
    </expression>

    (Example taken from https://github.com/SLIPO-EU/FAGI .)
    """

    def __init__(
            self,
            expression: FAGIRuleConditionExpression,
            nesting_level: int = 0):

        self.expression = expression
        self.nesting_level = nesting_level

    def __str__(self):
        return \
            f"""
                    {self.nesting_level * 8 * ' '}<expression>
                    {self.nesting_level * 8 * ' '}    <not>
                    {self.nesting_level * 8 * ' '}        {str(self.expression).strip()}
                    {self.nesting_level * 8 * ' '}    </not>
                    {self.nesting_level * 8 * ' '}</expression>"""


@dataclass
class FAGIRuleCondition:
    expression: FAGIRuleConditionExpression

    def __str__(self):
        return \
            f"""
                <condition>
                    {str(self.expression).strip()}
                </condition>"""
