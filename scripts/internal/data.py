from .model import *
from collections.abc import Callable
import csv


def convert_unit(value: float, source_unit: str, target_unit: str):
    if source_unit == target_unit:
        return value
    if source_unit == 'feet':
        if target_unit == 'm':
            value *= 0.3048
    return value


def extract_keys(plants: list[Plant], plant_attributes: list[PlantAttribute]) -> set:
    keys = set()
    unique_plant_attribute = None
    for plant_attribute in plant_attributes:
        if plant_attribute.unique:
            unique_plant_attribute = plant_attribute
            break

    if unique_plant_attribute is not None:
        for plant in plants:
            keys.add(getattr(plant, unique_plant_attribute.attribute_name))

    return keys


class CsvAttribute:
    __slots__ = 'mapping_function', 'name', 'plant_attribute', 'unit'
    mapping_function: Optional[Callable[[str], str]]
    name: str
    plant_attribute: PlantAttribute
    unit: str

    def __init__(self, name, plant_attribute, unit='', mapping_function=None):
        self.mapping_function = mapping_function
        self.name = name
        self.plant_attribute = plant_attribute
        self.unit = unit


class ConstantAttribute:
    __slots__ = 'plant_attribute', 'value'
    plant_attribute: PlantAttribute
    value: str

    def __init__(self, plant_attribute, value):
        self.plant_attribute = plant_attribute
        self.value = value


class DerivedAttribute:
    __slots__ = 'plant_attribute', 'name', 'mapping'
    plant_attribute: PlantAttribute
    name: str
    mapping: Callable[[str], any]

    def __init__(self, name, plant_attribute, mapping):
        self.name = name
        self.plant_attribute = plant_attribute
        self.mapping = mapping


def parse(file: str, csv_attributes: list[CsvAttribute], constant_attributes: list[ConstantAttribute],
          derived_attributes: list[DerivedAttribute], true_name='True', max_count=-1, unique_keys: set = None,
          delimiter=',', quote_char='"') -> list[Plant]:
    if unique_keys is None:
        unique_keys = set()
    result = []

    with open(file, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter, quotechar=quote_char)
        current_count = 0
        for row in csv_reader:
            if current_count == max_count:
                break

            plant = Plant()
            valid = True
            for csv_attribute in csv_attributes:
                plant_attribute = csv_attribute.plant_attribute
                column_name = csv_attribute.name
                string_value = row[column_name]

                if not string_value and not plant_attribute.optional:
                    valid = False
                    continue

                if csv_attribute.mapping_function is not None:
                    string_value = csv_attribute.mapping_function(string_value)

                match plant_attribute.attribute_type:
                    case PlantAttributeType.NUMERIC:
                        if not string_value:
                            value = 0
                        else:
                            value = convert_unit(float(string_value), csv_attribute.unit, plant_attribute.unit)
                    case PlantAttributeType.BOOL:
                        value = string_value == true_name
                    case PlantAttributeType.COLOR:
                        value = string_value
                    case PlantAttributeType.CATEGORICAL:
                        value = string_value

                if valid and plant_attribute.unique:
                    if value in unique_keys:
                        valid = False
                        continue
                    else:
                        unique_keys.add(value)

                setattr(plant, plant_attribute.attribute_name, value)

            for derived_attribute in derived_attributes:
                string_value = row[derived_attribute.name]
                setattr(plant, derived_attribute.plant_attribute.attribute_name,
                        derived_attribute.mapping(string_value))

            if valid:
                for constant_attribute in constant_attributes:
                    setattr(plant, constant_attribute.plant_attribute.attribute_name, constant_attribute.value)

                result.append(plant)
                current_count += 1
    return result


def parse_and_merge(file: str, csv_attributes: list[CsvAttribute], plant_list: list[Plant], true_name='True',
                    delimiter=',', quote_char='"') -> list[Plant]:
    with open(file, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter, quotechar=quote_char)
        for row in csv_reader:
            scientific_name = row['scientific_name']
            plant = None
            for p in plant_list:
                if p.scientific_name == scientific_name:
                    plant = p
                    break

            if plant is None:
                print(f'No matching plant found for {scientific_name}')
                continue

            for csv_attribute in csv_attributes:
                plant_attribute = csv_attribute.plant_attribute
                column_name = csv_attribute.name
                string_value = row[column_name]

                if csv_attribute.mapping_function is not None:
                    string_value = csv_attribute.mapping_function(string_value)

                match plant_attribute.attribute_type:
                    case PlantAttributeType.NUMERIC:
                        if not string_value:
                            value = 0
                        else:
                            value = convert_unit(float(string_value), csv_attribute.unit, plant_attribute.unit)
                    case PlantAttributeType.BOOL:
                        value = string_value == true_name
                    case PlantAttributeType.COLOR:
                        value = string_value
                    case PlantAttributeType.CATEGORICAL:
                        value = string_value

                setattr(plant, plant_attribute.attribute_name, value)
    return plant_list


def parse_plants(file: str, plant_attributes: list[PlantAttribute], max_count=-1) -> list[Plant]:
    result = []
    with open(file, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        current_count = 0
        for row in csv_reader:
            if current_count == max_count:
                break

            plant = Plant()

            for plant_attribute in plant_attributes:
                column_name = plant_attribute.attribute_name
                string_value = row[column_name]

                match plant_attribute.attribute_type:
                    case PlantAttributeType.NUMERIC:
                        if not string_value:
                            value = 0
                        else:
                            value = float(string_value)
                    case PlantAttributeType.BOOL:
                        value = string_value == 'True'
                    case PlantAttributeType.COLOR:
                        value = string_value
                    case PlantAttributeType.CATEGORICAL:
                        value = string_value

                setattr(plant, plant_attribute.attribute_name, value)

            result.append(plant)
            current_count += 1
    return result


def get_common_terms(plants: list[Plant], plant_attribute: PlantAttribute, word_count: int = 1) -> dict[str, int]:
    common_terms = {}
    if word_count < 1:
        for plant in plants:
            value = getattr(plant, plant_attribute.attribute_name)
            if value not in common_terms:
                common_terms[value] = 1
            else:
                common_terms[value] += 1
    else:
        filter_list = ['a', 'an', 'and', 'in', 'with']
        for plant in plants:
            value = getattr(plant, plant_attribute.attribute_name)
            word_list_filtered = []
            for word in value.split(' '):
                word_formatted = word.lower().replace(',', '').replace('.', '')
                if word_formatted not in filter_list:
                    word_list_filtered.append(word_formatted)
            if len(word_list_filtered) >= word_count:
                for index in range(0, len(word_list_filtered) - word_count + 1):
                    current_term = ' '.join(word_list_filtered[index:index + word_count])
                    if current_term not in common_terms:
                        common_terms[current_term] = 1
                    else:
                        common_terms[current_term] += 1
    return common_terms


def colors():
    color_list = []

    with open('PLANTS.csv', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            color = row['Fruit Color']
            if color and color not in color_list:
                color_list.append(color)

    print(color_list)


def export_plants(file: str, plants: list[Plant], plant_attributes: list[PlantAttribute], append=False):
    mode = 'a' if append else 'w'
    with open(file, mode, newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"')

        if not append:
            header = []
            for plant_attribute in plant_attributes:
                header.append(plant_attribute.attribute_name)
            csv_writer.writerow(header)

        for plant in plants:
            row = []
            for plant_attribute in plant_attributes:
                if hasattr(plant, plant_attribute.attribute_name):
                    row.append(getattr(plant, plant_attribute.attribute_name))
                else:
                    row.append('')
            csv_writer.writerow(row)
