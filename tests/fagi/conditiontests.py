import unittest

from gkgaas.fagi.condition import SimpleFAGIRuleConditionExpression, And, Or, Not, FAGIRuleCondition
from gkgaas.fagi.function import IsLiteralAbbreviation, IsSameCustomNormalize, IsSamePhoneNumberCustomNormalize, \
    IsPointGeometry, GeometriesCloserThan, IsDateKnownFormat


class FAGIRuleConditionTests(unittest.TestCase):
    def test_simple_fagi_rule_condition_expression(self):
        expr = SimpleFAGIRuleConditionExpression(
            IsLiteralAbbreviation('b1'))

        expected_expr_str = '<function>isLiteralAbbreviation(b1)</function>'

        self.assertEqual(expected_expr_str, str(expr))

    def test_conjunction_expression_01(self):
        expr = And(
            SimpleFAGIRuleConditionExpression(
                IsSamePhoneNumberCustomNormalize('a1', 'b1')),
            SimpleFAGIRuleConditionExpression(
                IsSameCustomNormalize('a', 'b', '0.6'))
        )

        expected_expr_str = """
                    <expression>
                        <and>
                            <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                            <function>isSameCustomNormalize(a,b,0.6)</function>
                        </and>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_conjunction_expression_02(self):
        expr = And(
            SimpleFAGIRuleConditionExpression(
                IsSamePhoneNumberCustomNormalize('a1', 'b1')),
            SimpleFAGIRuleConditionExpression(
                IsSameCustomNormalize('a', 'b', '0.6')),
            nesting_level=3
        )

        expected_expr_str = """
                                            <expression>
                                                <and>
                                                    <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                                                    <function>isSameCustomNormalize(a,b,0.6)</function>
                                                </and>
                                            </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_conjunction_expression_03(self):
        expr = And(
            And(
                SimpleFAGIRuleConditionExpression(
                    IsSamePhoneNumberCustomNormalize('a1', 'b1')),
                SimpleFAGIRuleConditionExpression(
                    IsSameCustomNormalize('a', 'b', '0.6')),
                nesting_level=1
            ),
            And(
                SimpleFAGIRuleConditionExpression(
                    IsLiteralAbbreviation('a2')),
                SimpleFAGIRuleConditionExpression(
                    IsPointGeometry('a3')),
                nesting_level=1
            )
        )

        expected_expr_str = """
                    <expression>
                        <and>
                            <expression>
                                <and>
                                    <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                                    <function>isSameCustomNormalize(a,b,0.6)</function>
                                </and>
                            </expression>
                            <expression>
                                <and>
                                    <function>isLiteralAbbreviation(a2)</function>
                                    <function>isPointGeometry(a3)</function>
                                </and>
                            </expression>
                        </and>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_conjunction_expression_04(self):
        expr = And(
            And(
                SimpleFAGIRuleConditionExpression(
                    IsSamePhoneNumberCustomNormalize('a1', 'b1')),
                SimpleFAGIRuleConditionExpression(
                    IsSameCustomNormalize('a', 'b', '0.6')),
                nesting_level=1
            ),
            And(
                And(
                    SimpleFAGIRuleConditionExpression(
                        IsLiteralAbbreviation('a2')),
                    SimpleFAGIRuleConditionExpression(
                        IsPointGeometry('a3')),
                    nesting_level=2
                ),
                SimpleFAGIRuleConditionExpression(GeometriesCloserThan('a3', 'b3', '23')),
                nesting_level=1
            )
        )

        expected_expr_str = """
                    <expression>
                        <and>
                            <expression>
                                <and>
                                    <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                                    <function>isSameCustomNormalize(a,b,0.6)</function>
                                </and>
                            </expression>
                            <expression>
                                <and>
                                    <expression>
                                        <and>
                                            <function>isLiteralAbbreviation(a2)</function>
                                            <function>isPointGeometry(a3)</function>
                                        </and>
                                    </expression>
                                    <function>geometriesCloserThan(a3,b3,23)</function>
                                </and>
                            </expression>
                        </and>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_disjunction_expression_01(self):
        expr = Or(
            SimpleFAGIRuleConditionExpression(
                IsSamePhoneNumberCustomNormalize('a1', 'b1')),
            SimpleFAGIRuleConditionExpression(
                IsSameCustomNormalize('a', 'b', '0.6'))
        )

        expected_expr_str = """
                    <expression>
                        <or>
                            <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                            <function>isSameCustomNormalize(a,b,0.6)</function>
                        </or>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_disjunction_expression_02(self):
        expr = Or(
            SimpleFAGIRuleConditionExpression(
                IsSamePhoneNumberCustomNormalize('a1', 'b1')),
            SimpleFAGIRuleConditionExpression(
                IsSameCustomNormalize('a', 'b', '0.6')),
            nesting_level=3
        )

        expected_expr_str = """
                                            <expression>
                                                <or>
                                                    <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                                                    <function>isSameCustomNormalize(a,b,0.6)</function>
                                                </or>
                                            </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_disjunction_expression_03(self):
        expr = Or(
            Or(
                SimpleFAGIRuleConditionExpression(
                    IsSamePhoneNumberCustomNormalize('a1', 'b1')),
                SimpleFAGIRuleConditionExpression(
                    IsSameCustomNormalize('a', 'b', '0.6')),
                nesting_level=1
            ),
            Or(
                SimpleFAGIRuleConditionExpression(
                    IsLiteralAbbreviation('a2')),
                SimpleFAGIRuleConditionExpression(
                    IsPointGeometry('a3')),
                nesting_level=1
            )
        )

        expected_expr_str = """
                    <expression>
                        <or>
                            <expression>
                                <or>
                                    <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                                    <function>isSameCustomNormalize(a,b,0.6)</function>
                                </or>
                            </expression>
                            <expression>
                                <or>
                                    <function>isLiteralAbbreviation(a2)</function>
                                    <function>isPointGeometry(a3)</function>
                                </or>
                            </expression>
                        </or>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_disjunction_expression_04(self):
        expr = Or(
            Or(
                SimpleFAGIRuleConditionExpression(
                    IsSamePhoneNumberCustomNormalize('a1', 'b1')),
                SimpleFAGIRuleConditionExpression(
                    IsSameCustomNormalize('a', 'b', '0.6')),
                nesting_level=1
            ),
            Or(
                Or(
                    SimpleFAGIRuleConditionExpression(
                        IsLiteralAbbreviation('a2')),
                    SimpleFAGIRuleConditionExpression(
                        IsPointGeometry('a3')),
                    nesting_level=2
                ),
                SimpleFAGIRuleConditionExpression(GeometriesCloserThan('a3', 'b3', '23')),
                nesting_level=1
            )
        )

        expected_expr_str = """
                    <expression>
                        <or>
                            <expression>
                                <or>
                                    <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                                    <function>isSameCustomNormalize(a,b,0.6)</function>
                                </or>
                            </expression>
                            <expression>
                                <or>
                                    <expression>
                                        <or>
                                            <function>isLiteralAbbreviation(a2)</function>
                                            <function>isPointGeometry(a3)</function>
                                        </or>
                                    </expression>
                                    <function>geometriesCloserThan(a3,b3,23)</function>
                                </or>
                            </expression>
                        </or>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_disjunction_expression_05(self):
        expr = Or(
            Or(
                SimpleFAGIRuleConditionExpression(
                    IsSamePhoneNumberCustomNormalize('a1', 'b1')),
                SimpleFAGIRuleConditionExpression(
                    IsSameCustomNormalize('a', 'b', '0.6')),
                nesting_level=1
            ),
            And(
                And(
                    SimpleFAGIRuleConditionExpression(
                        IsLiteralAbbreviation('a2')),
                    SimpleFAGIRuleConditionExpression(
                        IsPointGeometry('a3')),
                    nesting_level=2
                ),
                SimpleFAGIRuleConditionExpression(GeometriesCloserThan('a3', 'b3', '23')),
                nesting_level=1
            )
        )

        expected_expr_str = """
                    <expression>
                        <or>
                            <expression>
                                <or>
                                    <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                                    <function>isSameCustomNormalize(a,b,0.6)</function>
                                </or>
                            </expression>
                            <expression>
                                <and>
                                    <expression>
                                        <and>
                                            <function>isLiteralAbbreviation(a2)</function>
                                            <function>isPointGeometry(a3)</function>
                                        </and>
                                    </expression>
                                    <function>geometriesCloserThan(a3,b3,23)</function>
                                </and>
                            </expression>
                        </or>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_negation_expression_01(self):
        expr = Not(
            SimpleFAGIRuleConditionExpression(
                IsSamePhoneNumberCustomNormalize('a1', 'b1'))
        )

        expected_expr_str = """
                    <expression>
                        <not>
                            <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                        </not>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_negation_expression_02(self):
        expr = Not(
            SimpleFAGIRuleConditionExpression(
                IsSamePhoneNumberCustomNormalize('a1', 'b1')),
            nesting_level=3
        )

        expected_expr_str = """
                                            <expression>
                                                <not>
                                                    <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                                                </not>
                                            </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_negation_expression_03(self):
        expr = Not(
            Or(
                SimpleFAGIRuleConditionExpression(
                    IsSamePhoneNumberCustomNormalize('a1', 'b1')),
                SimpleFAGIRuleConditionExpression(
                    IsSameCustomNormalize('a', 'b', '0.6')),
                nesting_level=1
            )
        )

        expected_expr_str = """
                    <expression>
                        <not>
                            <expression>
                                <or>
                                    <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                                    <function>isSameCustomNormalize(a,b,0.6)</function>
                                </or>
                            </expression>
                        </not>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_negation_expression_04(self):
        expr = Not(
            Or(
                Or(
                    SimpleFAGIRuleConditionExpression(
                        IsLiteralAbbreviation('a2')),
                    SimpleFAGIRuleConditionExpression(
                        IsPointGeometry('a3')),
                    nesting_level=2
                ),
                SimpleFAGIRuleConditionExpression(GeometriesCloserThan('a3', 'b3', '23')),
                nesting_level=1
            )
        )

        expected_expr_str = """
                    <expression>
                        <not>
                            <expression>
                                <or>
                                    <expression>
                                        <or>
                                            <function>isLiteralAbbreviation(a2)</function>
                                            <function>isPointGeometry(a3)</function>
                                        </or>
                                    </expression>
                                    <function>geometriesCloserThan(a3,b3,23)</function>
                                </or>
                            </expression>
                        </not>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_negation_expression_05(self):
        expr = Not(
            And(
                Or(
                    SimpleFAGIRuleConditionExpression(
                        IsLiteralAbbreviation('a2')),
                    SimpleFAGIRuleConditionExpression(
                        IsPointGeometry('a3')),
                    nesting_level=2
                ),
                SimpleFAGIRuleConditionExpression(GeometriesCloserThan('a3', 'b3', '23')),
                nesting_level=1
            )
        )

        expected_expr_str = """
                    <expression>
                        <not>
                            <expression>
                                <and>
                                    <expression>
                                        <or>
                                            <function>isLiteralAbbreviation(a2)</function>
                                            <function>isPointGeometry(a3)</function>
                                        </or>
                                    </expression>
                                    <function>geometriesCloserThan(a3,b3,23)</function>
                                </and>
                            </expression>
                        </not>
                    </expression>"""

        self.assertEqual(expected_expr_str, str(expr))

    def test_rule_condition_01(self):
        condition = FAGIRuleCondition(
            Or(
                And(
                    SimpleFAGIRuleConditionExpression(
                        IsSamePhoneNumberCustomNormalize('a1', 'b1')),
                    SimpleFAGIRuleConditionExpression(
                        IsSameCustomNormalize('a', 'b', '0.6')),
                    nesting_level=1
                ),
                Not(
                    SimpleFAGIRuleConditionExpression(
                        IsSameCustomNormalize('a', 'b', '0.5')),
                    nesting_level=1
                )
            )
        )

        expected_condition_str = """
                <condition>
                    <expression>
                        <or>
                            <expression>
                                <and>
                                    <function>isSamePhoneNumberCustomNormalize(a1,b1)</function>
                                    <function>isSameCustomNormalize(a,b,0.6)</function>
                                </and>
                            </expression>
                            <expression>
                                <not>
                                    <function>isSameCustomNormalize(a,b,0.5)</function>
                                </not>
                            </expression>
                        </or>
                    </expression>
                </condition>"""

        self.assertEqual(expected_condition_str, str(condition))

    def test_rule_condition_02(self):
        condition = FAGIRuleCondition(
            SimpleFAGIRuleConditionExpression(IsLiteralAbbreviation('b1'))
        )

        expected_condition_str = """
                <condition>
                    <function>isLiteralAbbreviation(b1)</function>
                </condition>"""

        self.assertEqual(expected_condition_str, str(condition))

    def test_rule_condition_03(self):
        condition = FAGIRuleCondition(
            Not(SimpleFAGIRuleConditionExpression(IsDateKnownFormat('a')))
        )
        expected_condition_str = """
                <condition>
                    <expression>
                        <not>
                            <function>isDateKnownFormat(a)</function>
                        </not>
                    </expression>
                </condition>"""

        self.assertEqual(expected_condition_str, str(condition))

    def test_rule_condition_04(self):
        condition = FAGIRuleCondition(
            And(
                SimpleFAGIRuleConditionExpression(
                    IsSameCustomNormalize('a1', 'b1', '0.85')),
                SimpleFAGIRuleConditionExpression(
                    GeometriesCloserThan('a0', 'b0', '100')
                )
            )
        )
        expected_rule_condition_str = """
                <condition>
                    <expression>
                        <and>
                            <function>isSameCustomNormalize(a1,b1,0.85)</function>
                            <function>geometriesCloserThan(a0,b0,100)</function>
                        </and>
                    </expression>
                </condition>"""

        self.assertEqual(expected_rule_condition_str, str(condition))
