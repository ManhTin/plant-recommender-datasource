from model import *
import csv


class Test:
    name: str
    color: str
    height: str


COLOR_DICT = {
    'Black': [0.0, 0.0, 0.0],
    'Blue': [0.0, 0.0, 255.0],
    'Brown': [150.0, 75.0, 0.0],
    'Dark Green': [0.0, 100.0, 0.0],
    'Gray-Green': [94.0, 113.0, 106.0],
    'Green': [0.0, 255.0, 0.0],
    'Orange': [255.0, 165.0, 0.0],
    'Purple': [128.0, 0.0, 128.0],
    'Red': [255.0, 0.0, 0.0],
    'White': [255.0, 255.0, 255.0],
    'White-Gray': [235.0, 236.0, 240.0],
    'Yellow': [255.0, 255.0, 0.0],
    'Yellow-Green': [154.0, 205.0, 50.0],
}


def to_color(color_name):
    if color_name not in COLOR_DICT:
        result = COLOR_DICT['Black']
    else:
        rgb = COLOR_DICT[color_name]
        result = np.zeros(3)
        for i in range(3):
            result[i] = rgb[i] / 255.0
    return result


def convert_unit(value: float, source_unit: str, target_unit: str):
    if source_unit == target_unit:
        return value
    if source_unit == 'feet':
        if target_unit == 'm':
            value *= 0.3048
    return value


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


def parse(file: str, csv_attributes: list[CsvAttribute], true_name='True', max_count=-1, delimiter=',',
          quote_char='"') -> list[Plant]:
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
                        value = to_color(string_value)
                        setattr(plant, plant_attribute.attribute_name + '_name', string_value)
                    case PlantAttributeType.CATEGORICAL:
                        value = string_value

                setattr(plant, plant_attribute.attribute_name, value)

            if valid:
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
