import filecmp
import os
import shutil
import tempfile
import unittest

from rdflib import URIRef

from gkgaas.fagi.action import FusionAction, ValidationAction, DatasetAction
from gkgaas.fagi.condition import FAGIRuleCondition, \
    SimpleFAGIRuleConditionExpression, Not, Or, And
from gkgaas.fagi.function import IsSamePhoneNumber, IsLiteralAbbreviation, \
    IsDateKnownFormat, Exists, IsSameCustomNormalize, \
    IsSamePhoneNumberCustomNormalize, IsPhoneNumberParsable, \
    GeometriesCloserThan
from gkgaas.fagi.rule import FAGIRule, ActionRule, ExternalProperty, \
    FAGIRulesSpec, FAGIValidationRule, ValidationActionRule, Ensembles


class TestRule(unittest.TestCase):
    def test_to_str_01(self):
        expected_rule_str = """    <rule>
        <propertyA>http://www.opengis.net/ont/geosparql#hasGeometry http://www.opengis.net/ont/geosparql#asWKT</propertyA>
        <propertyB>http://www.opengis.net/ont/geosparql#hasGeometry http://www.opengis.net/ont/geosparql#asWKT</propertyB>
        <actionRuleSet/>
        <defaultAction>keep-more-points</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://www.opengis.net/ont/geosparql#hasGeometry'),
                URIRef('http://www.opengis.net/ont/geosparql#asWKT')
            ],
            property_b=[
                URIRef('http://www.opengis.net/ont/geosparql#hasGeometry'),
                URIRef('http://www.opengis.net/ont/geosparql#asWKT')
            ],
            action_rule_set=[],
            default_action=FusionAction.KEEP_MORE_POINTS
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_02(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#source http://slipo.eu/def#sourceRef</propertyA>
        <propertyB>http://slipo.eu/def#source http://slipo.eu/def#sourceRef</propertyB>
        <actionRuleSet/>
        <defaultAction>keep-left</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#source'),
                URIRef('http://slipo.eu/def#sourceRef')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#source'),
                URIRef('http://slipo.eu/def#sourceRef')
            ],
            action_rule_set=[],
            default_action=FusionAction.KEEP_LEFT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_03(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#source http://slipo.eu/def#poiRef</propertyA>
        <propertyB>http://slipo.eu/def#source http://slipo.eu/def#poiRef</propertyB>
        <actionRuleSet/>
        <defaultAction>keep-left</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#source'),
                URIRef('http://slipo.eu/def#poiRef')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#source'),
                URIRef('http://slipo.eu/def#poiRef')
            ],
            action_rule_set=[],
            default_action=FusionAction.KEEP_LEFT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_04(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#address http://slipo.eu/def#street</propertyA>
        <propertyB>http://slipo.eu/def#address http://slipo.eu/def#street</propertyB>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>exists(a)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-right</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#address'),
                URIRef('http://slipo.eu/def#street')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#address'),
                URIRef('http://slipo.eu/def#street')
            ],
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(Exists('a'))),
                    action=FusionAction.KEEP_LEFT
                )
            ],
            default_action=FusionAction.KEEP_RIGHT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_05(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#address http://slipo.eu/def#number</propertyA>
        <propertyB>http://slipo.eu/def#address http://slipo.eu/def#number</propertyB>
        <externalProperty id="a1">http://slipo.eu/def#address http://slipo.eu/def#street</externalProperty>
        <externalProperty id="b1">http://slipo.eu/def#address http://slipo.eu/def#street</externalProperty>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>exists(a1)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
            <actionRule>
                <condition>
                    <function>exists(a)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-right</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#address'),
                URIRef('http://slipo.eu/def#number')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#address'),
                URIRef('http://slipo.eu/def#number')
            ],
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(Exists('a1'))),
                    action=FusionAction.KEEP_LEFT
                ),
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(Exists('a'))),
                    action=FusionAction.KEEP_LEFT
                )
            ],
            external_property=[
                ExternalProperty(
                    id='a1',
                    uri=[
                        URIRef('http://slipo.eu/def#address'),
                        URIRef('http://slipo.eu/def#street')
                    ]
                ),
                ExternalProperty(
                    id='b1',
                    uri=[
                        URIRef('http://slipo.eu/def#address'),
                        URIRef('http://slipo.eu/def#street')
                    ]
                )
            ],
            default_action=FusionAction.KEEP_RIGHT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_06(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#address http://slipo.eu/def#postcode</propertyA>
        <propertyB>http://slipo.eu/def#address http://slipo.eu/def#postcode</propertyB>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>exists(a)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-right</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#address'),
                URIRef('http://slipo.eu/def#postcode')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#address'),
                URIRef('http://slipo.eu/def#postcode')
            ],
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(Exists('a'))),
                    action=FusionAction.KEEP_LEFT
                )
            ],
            default_action=FusionAction.KEEP_RIGHT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_07(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#address http://slipo.eu/def#locality</propertyA>
        <propertyB>http://slipo.eu/def#address http://slipo.eu/def#locality</propertyB>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>exists(a)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-right</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#address'),
                URIRef('http://slipo.eu/def#locality')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#address'),
                URIRef('http://slipo.eu/def#locality')
            ],
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(Exists('a'))),
                    action=FusionAction.KEEP_LEFT
                )
            ],
            default_action=FusionAction.KEEP_RIGHT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_08(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#address http://slipo.eu/def#country</propertyA>
        <propertyB>http://slipo.eu/def#address http://slipo.eu/def#country</propertyB>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>exists(a)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-right</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#address'),
                URIRef('http://slipo.eu/def#country')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#address'),
                URIRef('http://slipo.eu/def#country')
            ],
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(Exists('a'))),
                    action=FusionAction.KEEP_LEFT
                )
            ],
            default_action=FusionAction.KEEP_RIGHT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_09(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#phone http://slipo.eu/def#contactValue</propertyA>
        <propertyB>http://slipo.eu/def#phone http://slipo.eu/def#contactValue</propertyB>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>exists(a)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-right</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#phone'),
                URIRef('http://slipo.eu/def#contactValue')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#phone'),
                URIRef('http://slipo.eu/def#contactValue')
            ],
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(Exists('a'))),
                    action=FusionAction.KEEP_LEFT
                )
            ],
            default_action=FusionAction.KEEP_RIGHT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_10(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#phone http://slipo.eu/def#contactType</propertyA>
        <propertyB>http://slipo.eu/def#phone http://slipo.eu/def#contactType</propertyB>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>exists(a)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-right</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#phone'),
                URIRef('http://slipo.eu/def#contactType')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#phone'),
                URIRef('http://slipo.eu/def#contactType')
            ],
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(Exists('a'))),
                    action=FusionAction.KEEP_LEFT
                )
            ],
            default_action=FusionAction.KEEP_RIGHT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_11(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#fax http://slipo.eu/def#contactValue</propertyA>
        <propertyB>http://slipo.eu/def#fax http://slipo.eu/def#contactValue</propertyB>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>exists(a)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-right</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#fax'),
                URIRef('http://slipo.eu/def#contactValue')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#fax'),
                URIRef('http://slipo.eu/def#contactValue')
            ],
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(Exists('a'))
                    ),
                    action=FusionAction.KEEP_LEFT
                )
            ],
            default_action=FusionAction.KEEP_RIGHT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_12(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#homepage</propertyA>
        <propertyB>http://slipo.eu/def#homepage</propertyB>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>exists(a)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-right</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=URIRef('http://slipo.eu/def#homepage'),
            property_b=URIRef('http://slipo.eu/def#homepage'),
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(Exists('a'))
                    ),
                    action=FusionAction.KEEP_LEFT
                )
            ],
            default_action=FusionAction.KEEP_RIGHT
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_13(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#email http://slipo.eu/def#contactValue</propertyA>
        <propertyB>http://slipo.eu/def#email http://slipo.eu/def#contactValue</propertyB>
        <actionRuleSet/>
        <defaultAction>keep-longest</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#email'),
                URIRef('http://slipo.eu/def#contactValue')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#email'),
                URIRef('http://slipo.eu/def#contactValue')
            ],
            default_action=FusionAction.KEEP_LONGEST,
            action_rule_set=[]
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_14(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#dateA http://slipo.eu/def#lastModifiedA</propertyA>
        <propertyB>http://slipo.eu/def#dateB http://slipo.eu/def#lastModifiedB</propertyB>
        <externalProperty id="a1">http://www.w3.org/2000/01/rdf-schema#label</externalProperty>
        <externalProperty id="b1">http://www.w3.org/2000/01/rdf-schema#label</externalProperty>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>isLiteralAbbreviation(b1)</function>
                </condition>
                <action>keep-right</action>
            </actionRule>
            <actionRule>
                <condition>
                    <expression>
                        <not>
                            <function>isDateKnownFormat(a)</function>
                        </not>
                    </expression>
                </condition>
                <action>keep-both</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-left</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#dateA'),
                URIRef('http://slipo.eu/def#lastModifiedA')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#dateB'),
                URIRef('http://slipo.eu/def#lastModifiedB')
            ],
            default_action=FusionAction.KEEP_LEFT,
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(
                            IsLiteralAbbreviation('b1'))),
                    action=FusionAction.KEEP_RIGHT
                ),
                ActionRule(
                    condition=FAGIRuleCondition(
                        Not(SimpleFAGIRuleConditionExpression(
                            IsDateKnownFormat('a')))),
                    action=FusionAction.KEEP_BOTH
                )
            ],
            external_property=[
                ExternalProperty(
                    'a1', URIRef('http://www.w3.org/2000/01/rdf-schema#label')),
                ExternalProperty(
                    'b1', URIRef('http://www.w3.org/2000/01/rdf-schema#label'))
            ]
        )

        self.assertEqual(expected_rule_str, str(rule))

    def test_to_str_15(self):
        expected_rule_str = """    <rule>
        <propertyA>http://slipo.eu/def#phoneA http://slipo.eu/def#contactValueA</propertyA>
        <propertyB>http://slipo.eu/def#phoneB http://slipo.eu/def#contactValueB</propertyB>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>isSamePhoneNumber(a,b)</function>
                </condition>
                <action>keep-left</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>keep-left</defaultAction>
    </rule>"""

        rule = FAGIRule(
            property_a=[
                URIRef('http://slipo.eu/def#phoneA'),
                URIRef('http://slipo.eu/def#contactValueA')
            ],
            property_b=[
                URIRef('http://slipo.eu/def#phoneB'),
                URIRef('http://slipo.eu/def#contactValueB')
            ],
            default_action=FusionAction.KEEP_LEFT,
            action_rule_set=[
                ActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(
                            IsSamePhoneNumber('a', 'b'))),
                    action=FusionAction.KEEP_LEFT
                )
            ]
        )
        self.assertEqual(expected_rule_str, str(rule))


class TestValidationRule(unittest.TestCase):
    def test_to_str_01(self):
        expected_rule_str = """    <validationRule>
        <externalProperty id="a1">http://slipo.eu/def#phoneA http://slipo.eu/def#contactValueA</externalProperty>
        <externalProperty id="b1">http://slipo.eu/def#phoneB http://slipo.eu/def#contactValueB</externalProperty>
        <actionRuleSet>
            <actionRule>
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
                </condition>
                <action>reject-mark-ambiguous</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>accept</defaultAction>
    </validationRule>"""

        validation_rule = FAGIValidationRule(
            action_rule_set=[
                ValidationActionRule(
                    condition=FAGIRuleCondition(
                        Or(
                            And(
                                SimpleFAGIRuleConditionExpression(
                                    IsSamePhoneNumberCustomNormalize('a1', 'b1')
                                ),
                                SimpleFAGIRuleConditionExpression(
                                    IsSameCustomNormalize('a', 'b', '0.6')
                                ),
                                nesting_level=1
                            ),
                            Not(
                                SimpleFAGIRuleConditionExpression(
                                    IsSameCustomNormalize('a', 'b', '0.5')),
                                nesting_level=1
                            )
                        )
                    ),
                    action=ValidationAction.REJECT_MARK_AMBIGUOUS
                )
            ],
            default_action=ValidationAction.ACCEPT,
            external_property=[
                ExternalProperty(
                    id='a1',
                    uri=[
                        URIRef('http://slipo.eu/def#phoneA'),
                        URIRef('http://slipo.eu/def#contactValueA')
                    ]
                ),
                ExternalProperty(
                    id='b1',
                    uri=[
                        URIRef('http://slipo.eu/def#phoneB'),
                        URIRef('http://slipo.eu/def#contactValueB')
                    ]
                )
            ]
        )
        self.assertEqual(expected_rule_str, str(validation_rule))

    def test_to_str_02(self):
        expected_rule_str = """    <validationRule>
        <externalProperty id="a0">http://slipo.eu/def#phone http://slipo.eu/def#contactValue</externalProperty>
        <externalProperty id="b0">http://slipo.eu/def#name http://slipo.eu/def#nameValue</externalProperty>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <function>isPhoneNumberParsable(a0)</function>
                </condition>
                <action>accept</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>accept</defaultAction>
    </validationRule>"""

        validation_rule = FAGIValidationRule(
            action_rule_set=[
                ValidationActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(
                            IsPhoneNumberParsable('a0'))),
                    action=ValidationAction.ACCEPT
                )
            ],
            default_action=ValidationAction.ACCEPT,
            external_property=[
                ExternalProperty(
                    id='a0',
                    uri=[
                        URIRef('http://slipo.eu/def#phone'),
                        URIRef('http://slipo.eu/def#contactValue')
                    ]
                ),
                ExternalProperty(
                    id='b0',
                    uri=[
                        URIRef('http://slipo.eu/def#name'),
                        URIRef('http://slipo.eu/def#nameValue')
                    ]
                )
            ]
        )

        self.assertEqual(expected_rule_str, str(validation_rule))

    def test_to_str_03(self):
        expected_rule_str = """    <validationRule>
        <actionRuleSet/>
        <defaultAction>accept</defaultAction>
    </validationRule>"""

        validation_rule = FAGIValidationRule(
            action_rule_set=[],
            default_action=ValidationAction.ACCEPT
        )

        self.assertEqual(expected_rule_str, str(validation_rule))

    def test_to_str_04(self):
        expected_rule_str = """    <validationRule>
        <externalProperty id="a0">http://www.opengis.net/ont/geosparql#hasGeometry http://www.opengis.net/ont/geosparql#asWKT</externalProperty>
        <externalProperty id="b0">http://www.opengis.net/ont/geosparql#hasGeometry http://www.opengis.net/ont/geosparql#asWKT</externalProperty>
        <externalProperty id="a1">http://slipo.eu/def#address http://slipo.eu/def#street</externalProperty>
        <externalProperty id="b1">http://slipo.eu/def#address http://slipo.eu/def#street</externalProperty>
        <externalProperty id="a2">http://slipo.eu/def#name http://slipo.eu/def#nameValue</externalProperty>
        <externalProperty id="b2">http://slipo.eu/def#name http://slipo.eu/def#nameValue</externalProperty>
        <externalProperty id="a3">http://slipo.eu/def#phone http://slipo.eu/def#contactValue</externalProperty>
        <externalProperty id="b3">http://slipo.eu/def#phone http://slipo.eu/def#contactValue</externalProperty>
        <actionRuleSet>
            <actionRule>
                <condition>
                    <expression>
                        <and>
                            <function>geometriesCloserThan(a0,b0,150)</function>
                            <function>isSameCustomNormalize(a2,b2,0.8)</function>
                        </and>
                    </expression>
                </condition>
                <action>accept</action>
            </actionRule>
            <actionRule>
                <condition>
                    <expression>
                        <and>
                            <function>isSamePhoneNumberCustomNormalize(a3,b3)</function>
                            <function>geometriesCloserThan(a0,b0,150)</function>
                        </and>
                    </expression>
                </condition>
                <action>accept</action>
            </actionRule>
            <actionRule>
                <condition>
                    <expression>
                        <and>
                            <function>isSameCustomNormalize(a1,b1,0.85)</function>
                            <function>geometriesCloserThan(a0,b0,100)</function>
                        </and>
                    </expression>
                </condition>
                <action>accept</action>
            </actionRule>
            <actionRule>
                <condition>
                    <function>isSameCustomNormalize(a2,b2,0.9)</function>
                </condition>
                <action>accept</action>
            </actionRule>
        </actionRuleSet>
        <defaultAction>reject</defaultAction>
    </validationRule>"""

        validation_rule = FAGIValidationRule(
            action_rule_set=[
                ValidationActionRule(
                    condition=FAGIRuleCondition(
                        And(
                            SimpleFAGIRuleConditionExpression(
                                GeometriesCloserThan('a0', 'b0', '150')),
                            SimpleFAGIRuleConditionExpression(
                                IsSameCustomNormalize('a2', 'b2', '0.8'))
                        )
                    ),
                    action=ValidationAction.ACCEPT
                ),
                ValidationActionRule(
                    condition=FAGIRuleCondition(
                        And(
                            SimpleFAGIRuleConditionExpression(
                                IsSamePhoneNumberCustomNormalize('a3', 'b3')
                            ),
                            SimpleFAGIRuleConditionExpression(
                                GeometriesCloserThan('a0', 'b0', '150')
                            )
                        )
                    ),
                    action=ValidationAction.ACCEPT
                ),
                ValidationActionRule(
                    condition=FAGIRuleCondition(
                        And(
                            SimpleFAGIRuleConditionExpression(
                                IsSameCustomNormalize('a1', 'b1', '0.85')
                            ),
                            SimpleFAGIRuleConditionExpression(
                                GeometriesCloserThan('a0', 'b0', '100')
                            )
                        )
                    ),
                    action=ValidationAction.ACCEPT
                ),
                ValidationActionRule(
                    condition=FAGIRuleCondition(
                        SimpleFAGIRuleConditionExpression(
                            IsSameCustomNormalize('a2', 'b2', '0.9'))
                    ),
                    action=ValidationAction.ACCEPT
                )
            ],
            default_action=ValidationAction.REJECT,
            external_property=[
                ExternalProperty(
                    id='a0',
                    uri=[
                        URIRef(
                            'http://www.opengis.net/ont/geosparql#hasGeometry'),
                        URIRef('http://www.opengis.net/ont/geosparql#asWKT')
                    ]
                ),
                ExternalProperty(
                    id='b0',
                    uri=[
                        URIRef(
                            'http://www.opengis.net/ont/geosparql#hasGeometry'),
                        URIRef('http://www.opengis.net/ont/geosparql#asWKT')
                    ]
                ),
                ExternalProperty(
                    id='a1',
                    uri=[
                        URIRef('http://slipo.eu/def#address'),
                        URIRef('http://slipo.eu/def#street')
                    ]
                ),
                ExternalProperty(
                    id='b1',
                    uri=[
                        URIRef('http://slipo.eu/def#address'),
                        URIRef('http://slipo.eu/def#street')
                    ]
                ),
                ExternalProperty(
                    id='a2',
                    uri=[
                        URIRef('http://slipo.eu/def#name'),
                        URIRef('http://slipo.eu/def#nameValue')
                    ]
                ),
                ExternalProperty(
                    id='b2',
                    uri=[
                        URIRef('http://slipo.eu/def#name'),
                        URIRef('http://slipo.eu/def#nameValue')
                    ]
                ),
                ExternalProperty(
                    id='a3',
                    uri=[
                        URIRef('http://slipo.eu/def#phone'),
                        URIRef('http://slipo.eu/def#contactValue')
                    ]
                ),
                ExternalProperty(
                    id='b3',
                    uri=[
                        URIRef('http://slipo.eu/def#phone'),
                        URIRef('http://slipo.eu/def#contactValue')
                    ]
                )
            ]
        )
        self.assertEqual(expected_rule_str, str(validation_rule))


class TestEnsembles(unittest.TestCase):
    def test_to_str_01(self):
        expected_ensembles_str = """    <ensembles>
        <functionalProperties/>
        <nonFunctionalProperties/>
    </ensembles>"""

        ensembles = Ensembles(
            functional_properties=[],
            non_functional_properties=[]
        )

        self.assertEqual(expected_ensembles_str, str(ensembles))

    def test_to_str_02(self):
        expected_ensembles_str = """    <ensembles>
        <functionalProperties>http://slipo.eu/def#fax</functionalProperties>
        <nonFunctionalProperties>http://slipo.eu/def#name</nonFunctionalProperties>
    </ensembles>"""

        ensembles = Ensembles(
            functional_properties=[URIRef('http://slipo.eu/def#fax')],
            non_functional_properties=[URIRef('http://slipo.eu/def#name')]
        )

        self.assertEqual(expected_ensembles_str, str(ensembles))

    def test_to_str_03(self):
        expected_ensembles_str = """    <ensembles>
        <functionalProperties>http://slipo.eu/def#fax;http://slipo.eu/def#personalInfo http://slipo.eu/def#email</functionalProperties>
        <nonFunctionalProperties>http://slipo.eu/def#name;http://slipo.eu/def#personalInfo http://slipo.eu/def#sex</nonFunctionalProperties>
    </ensembles>"""

        ensembles = Ensembles(
            functional_properties=[
                URIRef('http://slipo.eu/def#fax'),
                [
                    URIRef('http://slipo.eu/def#personalInfo'),
                    URIRef('http://slipo.eu/def#email')
                ]
            ],
            non_functional_properties=[
                URIRef('http://slipo.eu/def#name'),
                [
                    URIRef('http://slipo.eu/def#personalInfo'),
                    URIRef('http://slipo.eu/def#sex')
                ]
            ]
        )

        self.assertEqual(expected_ensembles_str, str(ensembles))


class TestRulesSpec(unittest.TestCase):
    def test_to_file_01(self):
        import tests.fagi
        project_dir = os.path.dirname(tests.fagi.__file__)
        expected_file_path = os.path. join(project_dir, 'rules.xml')

        rule_spec = FAGIRulesSpec(
            rules=[
                FAGIValidationRule(
                    action_rule_set=[],
                    default_action=ValidationAction.ACCEPT
                ),
                FAGIRule(
                    property_a=[
                        URIRef(
                            'http://www.opengis.net/ont/geosparql#hasGeometry'),
                        URIRef('http://www.opengis.net/ont/geosparql#asWKT')
                    ],
                    property_b=[
                        URIRef(
                            'http://www.opengis.net/ont/geosparql#hasGeometry'),
                        URIRef('http://www.opengis.net/ont/geosparql#asWKT')
                    ],
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_MORE_POINTS
                ),
                FAGIRule(
                    property_a=[
                        URIRef('http://slipo.eu/def#email'),
                        URIRef('http://slipo.eu/def#contactValue')
                    ],
                    property_b=[
                        URIRef('http://slipo.eu/def#email'),
                        URIRef('http://slipo.eu/def#contactValue')
                    ],
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_LONGEST
                ),
                FAGIRule(
                    property_a=[
                        URIRef('http://slipo.eu/def#name'),
                        URIRef('http://slipo.eu/def#nameValue')
                    ],
                    property_b=[
                        URIRef('http://slipo.eu/def#name'),
                        URIRef('http://slipo.eu/def#nameValue')
                    ],
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_LONGEST
                ),
                FAGIRule(
                    property_a=[
                        URIRef('http://slipo.eu/def#address'),
                        URIRef('http://slipo.eu/def#street')
                    ],
                    property_b=[
                        URIRef('http://slipo.eu/def#address'),
                        URIRef('http://slipo.eu/def#street')
                    ],
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_LONGEST
                ),
                FAGIRule(
                    property_a=[
                        URIRef('http://slipo.eu/def#address'),
                        URIRef('http://slipo.eu/def#number')
                    ],
                    property_b=[
                        URIRef('http://slipo.eu/def#address'),
                        URIRef('http://slipo.eu/def#number')
                    ],
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_LONGEST
                ),
                FAGIRule(
                    property_a=[
                        URIRef('http://slipo.eu/def#address'),
                        URIRef('http://slipo.eu/def#postcode')
                    ],
                    property_b=[
                        URIRef('http://slipo.eu/def#address'),
                        URIRef('http://slipo.eu/def#postcode')
                    ],
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_LONGEST
                ),
                FAGIRule(
                    property_a=URIRef('http://slipo.eu/def#locality'),
                    property_b=URIRef('http://slipo.eu/def#locality'),
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_LONGEST
                ),
                FAGIRule(
                    property_a=URIRef('http://slipo.eu/def#country'),
                    property_b=URIRef('http://slipo.eu/def#country'),
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_LONGEST
                ),
                FAGIRule(
                    property_a=URIRef('http://slipo.eu/def#homepage'),
                    property_b=URIRef('http://slipo.eu/def#homepage'),
                    action_rule_set=[
                        ActionRule(
                            condition=FAGIRuleCondition(
                                SimpleFAGIRuleConditionExpression(
                                    Exists('a'))),
                            action=FusionAction.KEEP_LEFT
                        )
                    ],
                    default_action=FusionAction.KEEP_RIGHT
                ),
                FAGIRule(
                    property_a=[
                        URIRef('http://slipo.eu/def#phone'),
                        URIRef('http://slipo.eu/def#contactValue')
                    ],
                    property_b=[
                        URIRef('http://slipo.eu/def#phone'),
                        URIRef('http://slipo.eu/def#contactValue')
                    ],
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_LONGEST
                ),
                FAGIRule(
                    property_a=[
                        URIRef('http://slipo.eu/def#fax'),
                        URIRef('http://slipo.eu/def#contactValue')
                    ],
                    property_b=[
                        URIRef('http://slipo.eu/def#fax'),
                        URIRef('http://slipo.eu/def#contactValue')
                    ],
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_LONGEST
                ),
                FAGIRule(
                    property_a=[
                        URIRef('http://slipo.eu/def#openingHours'),
                        URIRef('http://slipo.eu/def#concat')
                    ],
                    property_b=[
                        URIRef('http://slipo.eu/def#openingHours'),
                        URIRef('http://slipo.eu/def#concat')
                    ],
                    action_rule_set=[],
                    default_action=FusionAction.KEEP_LONGEST
                )
            ],
            default_dataset_action=DatasetAction.KEEP_LEFT,
            ensembles=Ensembles(
                functional_properties=[],
                non_functional_properties=[]
            )
        )
        tmp_dir = tempfile.mkdtemp()
        result_file_path = os.path.join(tmp_dir, 'rules.xml')
        rule_spec.to_file(result_file_path)

        self.assertTrue(
            filecmp.cmp(expected_file_path, result_file_path),
            'Generated rules file content does not match the expected content')

        shutil.rmtree(tmp_dir)

    def test_to_file_02(self):
        import tests.fagi
        project_dir = os.path.dirname(tests.fagi.__file__)
        expected_file_path = os.path. join(project_dir, 'rules2.xml')

        rule_spec = FAGIRulesSpec(
            rules=[
                FAGIValidationRule(
                    action_rule_set=[],
                    default_action=ValidationAction.ACCEPT
                ),
                FAGIRule(
                    property_a=URIRef('http://slipo.eu/def#homepage'),
                    property_b=URIRef('http://slipo.eu/def#homepage'),
                    action_rule_set=[
                        ActionRule(
                            condition=FAGIRuleCondition(
                                SimpleFAGIRuleConditionExpression(Exists('a'))
                            ),
                            action=FusionAction.KEEP_LEFT
                        )
                    ],
                    default_action=FusionAction.KEEP_RIGHT
                ),
            ],
            default_dataset_action=DatasetAction.KEEP_BOTH,
            ensembles=Ensembles(
                functional_properties=[
                    URIRef('http://slipo.eu/def#fax'),
                    [
                        URIRef('http://slipo.eu/def#personalInfo'),
                        URIRef('http://slipo.eu/def#email')
                    ]
                ],
                non_functional_properties=[
                    URIRef('http://slipo.eu/def#name'),
                    [
                        URIRef('http://slipo.eu/def#personalInfo'),
                        URIRef('http://slipo.eu/def#sex')
                    ]
                ]
            )
        )
        tmp_dir = tempfile.mkdtemp()
        result_file_path = os.path.join(tmp_dir, 'rules.xml')
        rule_spec.to_file(result_file_path)

        self.assertTrue(
            filecmp.cmp(expected_file_path, result_file_path),
            'Generated rules file content does not match the expected content')

        shutil.rmtree(tmp_dir)
