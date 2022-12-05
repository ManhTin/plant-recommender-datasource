from .model import *
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
    __slots__ = 'name', 'plant_attribute', 'optional', 'unit'
    name: str
    plant_attribute: PlantAttribute
    optional: bool
    unit: str

    def __init__(self, name, plant_attribute, optional=False, unit=''):
        self.name = name
        self.plant_attribute = plant_attribute
        self.optional = optional
        self.unit = unit


def parse(file: str, csv_attributes: list[CsvAttribute], true_name='True', max_count=-1, unique_keys: set = None,
          delimiter=',', quote_char='"') -> list[Plant]:
    if unique_keys is None:
        unique_keys = set()
    result = []

    with open(file, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter, quotechar=quote_char)
        next_id = 0
        for row in csv_reader:
            if next_id == max_count:
                break

            plant = Plant(next_id)

            valid = True
            for csv_attribute in csv_attributes:
                plant_attribute = csv_attribute.plant_attribute
                column_name = csv_attribute.name
                string_value = row[column_name]

                if not string_value and not csv_attribute.optional:
                    valid = False
                    continue

                value = None
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

                if plant_attribute.unique and value in unique_keys:
                    valid = False
                    continue
                else:
                    unique_keys.add(value)

                setattr(plant, plant_attribute.attribute_name, value)

            if valid:
                result.append(plant)
                next_id += 1
    return result


def parse_plants(file: str, plant_attributes: list[PlantAttribute], max_count=-1) -> list[Plant]:
    result = []
    with open(file, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        next_id = 0
        for row in csv_reader:
            if next_id == max_count:
                break

            plant = Plant(next_id)

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
                        value = bool(string_value)
                    case PlantAttributeType.COLOR:
                        value = string_value
                    case PlantAttributeType.CATEGORICAL:
                        value = string_value

                setattr(plant, plant_attribute.attribute_name, value)

            result.append(plant)
            next_id += 1
    return result


def colors():
    color_list = []

    with open('PLANTS.txt', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            color = row['Fruit Color']
            if color and color not in color_list:
                color_list.append(color)

    print(color_list)


def export_plants(file: str, plants: list[Plant], plant_attributes: list[PlantAttribute]):
    with open(file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"')

        header = []
        for plant_attribute in plant_attributes:
            header.append(plant_attribute.attribute_name)
        csv_writer.writerow(header)

        for plant in plants:
            row = []
            for plant_attribute in plant_attributes:
                row.append(getattr(plant, plant_attribute.attribute_name))
            csv_writer.writerow(row)
