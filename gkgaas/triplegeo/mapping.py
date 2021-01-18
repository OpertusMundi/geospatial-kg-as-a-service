import os
from dataclasses import dataclass
from functools import reduce
from typing import List


@dataclass
class MapProperties(object):
    name: str
    entity_type: str = None
    predicate: str = None
    resource_type: str = None
    language: str = None
    instance: str = None
    part: str = None
    generator_function: str = None
    function_arguments: List[str] = None
    # TODO: Maybe find better type
    datatype: str = None  # originally org.apache.jena.datatype.RDFDatatype

    nl: str = os.linesep

    def to_yml_str(self):
        result = f'{self.name}:{self.nl}'

        if self.part is not None:
            result += f'  partOf: {self.part}{self.nl}'
        if self.instance is not None:
            result += f'  instanceOf: {self.instance}{self.nl}'
        if self.entity_type is not None:
            result += f'  entity: {self.entity_type}{self.nl}'
        if self.predicate is not None:
            result += f'  predicate: {self.predicate}{self.nl}'
        if self.resource_type is not None:
            result += f'  type: {self.resource_type}{self.nl}'
        if self.datatype is not None:
            result += f'  datatype: {self.datatype}{self.nl}'
        if self.language is not None:
            result += f'  language: {self.language}{self.nl}'
        if self.generator_function is not None:
            fn = self.generator_function[:]
            if self.function_arguments:
                fn += \
                    '(' + \
                    reduce(lambda l, r: f'{l},{r}', self.function_arguments) + \
                    ')'

            result += f'  generateWith: {fn}{self.nl}'

        return result


@dataclass
class MappingSpecification(object):
    map_properties_list: List[MapProperties]
    file_name: str

    def to_yml_dir(self, dir_path: str):
        file_path = dir_path + os.sep + self.file_name

        with open(file_path, 'w') as file_out:
            for map_properties in self.map_properties_list:
                file_out.writelines(map_properties.to_yml_str())
