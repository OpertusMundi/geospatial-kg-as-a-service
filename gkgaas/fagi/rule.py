import os
from dataclasses import dataclass
from typing import List, Union

from rdflib import URIRef

from gkgaas.fagi.action import FusionAction, ValidationAction, DatasetAction
from gkgaas.fagi.condition import FAGIRuleCondition


@dataclass
class ActionRule:
    condition: FAGIRuleCondition
    action: FusionAction

    def __str__(self):
        return \
            f"""            <actionRule>
                {str(self.condition).strip()}
                <action>{str(self.action)}</action>
            </actionRule>"""


@dataclass
class ValidationActionRule:
    condition: FAGIRuleCondition
    action: ValidationAction

    def __str__(self):
        return \
            f"""            <actionRule>
                {str(self.condition).strip()}
                <action>{str(self.action)}</action>
            </actionRule>"""


@dataclass
class ExternalProperty:
    id: str
    uri: Union[URIRef, List[URIRef]]

    def __str__(self):
        if isinstance(self.uri, URIRef):
            return \
                f'<externalProperty id="{self.id}">{str(self.uri)}' \
                f'</externalProperty>'
        else:
            uri_str = ' '.join(self.uri)
            return \
                f'<externalProperty id="{self.id}">{uri_str}' \
                f'</externalProperty>'


@dataclass
class FAGIRule:
    property_a: Union[URIRef, List[URIRef]]
    property_b: Union[URIRef, List[URIRef]]
    default_action: FusionAction
    action_rule_set: List[ActionRule]

    external_properties: List[ExternalProperty] = None

    def __mk_property_str(self, property_a_b: str) -> str:
        if property_a_b == 'a':
            prop_str = '<propertyA>'

            if isinstance(self.property_a, URIRef):
                prop_str += str(self.property_a)
            else:
                prop_str += ' '.join(self.property_a)

            prop_str += '</propertyA>'

        else:
            prop_str = '<propertyB>'

            if isinstance(self.property_b, URIRef):
                prop_str += str(self.property_b)
            else:
                prop_str += ' '.join(self.property_b)

            prop_str += '</propertyB>'

        return prop_str

    def __mk_action_ruleset(self) -> str:
        if len(self.action_rule_set) == 0:
            return '<actionRuleSet/>'

        ruleset_str = '        <actionRuleSet>\n'

        for action_rule in self.action_rule_set:
            ruleset_str += f'{str(action_rule)}\n'

        ruleset_str += '        </actionRuleSet>'

        return ruleset_str

    def __str__(self):
        rule_str = f"""    <rule>
        {self.__mk_property_str('a')}
        {self.__mk_property_str('b')}
"""

        if self.external_properties:
            for ext_prop in self.external_properties:
                rule_str += f'        {str(ext_prop)}\n'

        rule_str += f"""        {self.__mk_action_ruleset().strip()}
        <defaultAction>{str(self.default_action)}</defaultAction>
    </rule>"""

        return rule_str


@dataclass
class FAGIValidationRule:
    default_action: ValidationAction
    action_rule_set: List[ValidationActionRule]

    external_properties: List[ExternalProperty] = None

    def __mk_action_ruleset(self) -> str:
        if len(self.action_rule_set) == 0:
            return '<actionRuleSet/>'

        ruleset_str = '        <actionRuleSet>\n'

        for action_rule in self.action_rule_set:
            ruleset_str += f'{str(action_rule)}\n'

        ruleset_str += '        </actionRuleSet>'

        return ruleset_str

    def __str__(self):
        rule_str = f"""    <validationRule>
"""

        if self.external_properties:
            for ext_prop in self.external_properties:
                rule_str += f'        {str(ext_prop)}\n'

        rule_str += f"""        {self.__mk_action_ruleset().strip()}
        <defaultAction>{str(self.default_action)}</defaultAction>
    </validationRule>"""

        return rule_str


@dataclass
class Ensembles:
    functional_properties: List[Union[List[URIRef], URIRef]]
    non_functional_properties: List[Union[List[URIRef], URIRef]]

    def __mk_functional_properties_str(self):
        if len(self.functional_properties) == 0:
            return '<functionalProperties/>'

        func_prop_str = '<functionalProperties>'

        for func_prop in self.functional_properties:
            if isinstance(func_prop, URIRef):
                func_prop_str += f'{str(func_prop)};'
            else:  # List of URIRef's
                func_prop_str += f'{" ".join(func_prop)};'

        return func_prop_str[:-1] + '</functionalProperties>'

    def __mk_non_functional_properties_str(self):
        if len(self.non_functional_properties) == 0:
            return '<nonFunctionalProperties/>'

        non_func_prop_str = '<nonFunctionalProperties>'

        for non_func_prop in self.non_functional_properties:
            if isinstance(non_func_prop, URIRef):
                non_func_prop_str += f'{str(non_func_prop)};'
            else:  # List of URIRef's
                non_func_prop_str += f'{" ".join(non_func_prop)};'

        return non_func_prop_str[:-1] + '</nonFunctionalProperties>'

    def __str__(self):
        return \
            f"""    <ensembles>
        {self.__mk_functional_properties_str()}
        {self.__mk_non_functional_properties_str()}
    </ensembles>"""


@dataclass
class FAGIRulesSpec:
    rules: List[Union[FAGIRule, FAGIValidationRule]]
    default_dataset_action: DatasetAction
    ensembles: Ensembles

    def to_file(self, file_path: str):
        with open(file_path, 'w') as out_file:
            out_file.write('<?xml version="1.0" encoding="UTF-8"?>' + os.linesep)
            out_file.write('<rules>' + os.linesep)

            for rule in self.rules:
                out_file.write(str(rule) + os.linesep)

            out_file.write(
                f'    <defaultDatasetAction>{str(self.default_dataset_action)}'
                f'</defaultDatasetAction>' + os.linesep)
            out_file.write(str(self.ensembles) + os.linesep)

            out_file.write('</rules>' + os.linesep)
