import os

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Category(object):
    name: str
    category_id: str
    sub_classes: List[Tuple[str, str]]

    def __str__(self):
        nl = os.linesep
        res = f'{self.name} #{self.category_id}{nl}  '

        res += f'{nl}  '.join(
            map(lambda c: f'{c[0]} #{c[1]}', self.sub_classes))

        return res

    def _csv_str__(self):
        nl = os.linesep
        return nl.join(
            map(
                lambda c:
                f'"{self.category_id}","{self.name}","{c[1]}","{c[0]}"',
                self.sub_classes))


@dataclass
class ClassificationSpecification(object):
    file_name: str
    categories: List[Category]

    def to_csv_file(self, target_dir_path):
        file_path = os.path.join(target_dir_path, self.file_name)
        nl = os.linesep

        with open(file_path, 'w') as out_file:
            out_file.write(
                '"type","maincategory_en","combotype","subcategory_en"' + nl)

            out_file.writelines(
                [f'{c._csv_str__()}{nl}' for c in self.categories])

    def to_yml_file(self, target_dir_path):
        file_path = os.path.join(target_dir_path, self.file_name)
        nl = os.linesep

        with open(file_path, 'w') as out_file:
            out_file.writelines([f'{str(c)}{nl}' for c in self.categories])
