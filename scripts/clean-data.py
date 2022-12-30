from internal.data import *

plant_attributes = Plant.plant_attributes
other_attributes = Plant.other_attributes
all_attributes = plant_attributes + Plant.other_attributes

# PLANTS.cvs


def and_to_comma(value: str) -> str:
    return value.replace(' and ', ',').replace(' & ', ',').replace(', ', ',')


def active_growth_period_mapping(agp: str) -> str:
    if agp == 'Year Round':
        return 'Spring,Summer,Fall,Winter'
    else:
        return and_to_comma(agp)


csv_attributes = [
    CsvAttribute('Active Growth Period', plant_attributes[0], mapping_function=active_growth_period_mapping),
    CsvAttribute('Bloom Period', plant_attributes[1]),
    CsvAttribute('Common Name', other_attributes[0]),
    CsvAttribute('Drought Tolerance', plant_attributes[4]),
    CsvAttribute('Duration', plant_attributes[5]),
    CsvAttribute('Family', plant_attributes[6]),
    CsvAttribute('Family Common Name', other_attributes[1]),
    CsvAttribute('Flower Color', plant_attributes[7]),
    CsvAttribute('Foliage Color', plant_attributes[8]),
    CsvAttribute('Foliage Porosity Summer', plant_attributes[9]),
    CsvAttribute('Foliage Porosity Winter', plant_attributes[10]),
    CsvAttribute('Frost Free Days, Minimum', plant_attributes[11]),
    CsvAttribute('Fruit Color', plant_attributes[12]),
    CsvAttribute('Growth Habit', plant_attributes[13], mapping_function=and_to_comma),
    CsvAttribute('Growth Rate', plant_attributes[14]),
    CsvAttribute('Height, Mature (feet)', plant_attributes[15], unit='feet'),
    CsvAttribute('Shape and Orientation', plant_attributes[17]),
    CsvAttribute('Lifespan', plant_attributes[18]),
    CsvAttribute('pH (Minimum)', plant_attributes[21]),
    CsvAttribute('pH (Maximum)', plant_attributes[22]),
    CsvAttribute('Scientific Name', other_attributes[3]),
    CsvAttribute('Toxicity', plant_attributes[24]),
]

constant_attributes = [
    ConstantAttribute(plant_attributes[20], 'North America'),
    ConstantAttribute(plant_attributes[25], 'Outdoor Plant'),
]

plants = parse('../data/PLANTS.csv', csv_attributes, constant_attributes, [], 'Yes')

export_plants('../export/plants.csv', plants, all_attributes)

# how_many_plants_data.cvs


def toxicity_mapping(toxicity):
    toxicity_dict = {
        'Non-toxic. Completely pet safe!': "None",
        'Highly toxic to humans and pets if ingested.': "Moderate",
        'Mildly toxic to humans and pets if ingested.': "Severe"
    }
    return toxicity_dict[toxicity]


def drought_tolerance_mapping(water):
    drought_tolerance_dict = {
        'Keep soil just moist, but not soggy.': "None",
        'Allow top inches of soil to dry between waterings.': "Low",
        'Allow half of soil to dry out before watering again.': "Medium"
    }
    return drought_tolerance_dict[water]


def climate_mapping(climate: str) -> str:
    return and_to_comma(climate).replace('aird', 'arid').replace(' region', '')


def humidity_mapping(humidity: str) -> str:
    return humidity.replace('Ã¢Â€Â”', '. ')


def foliage_color_mapping(leaf_shape: str) -> str:
    color_list = ['Bright Green', 'Deep Green', 'Two-toned Green', 'Vivid Green', 'Glossy emerald Green',
                  'Brilliant Green', 'Glossy dark Green', 'Vibrant Green', 'Gray-Green', 'Plump Green',
                  'Plump vibrant Green', 'Olive Green', 'Dark Green', 'Green']
    for color in color_list:
        if color.lower() in leaf_shape.lower().replace('grey', 'gray'):
            return color
    return ''


def origin_mapping(origin: str) -> str:
    values = origin.split(', ')
    for value in values:
        words = value.split(' ')
        if '&' in words:
            values.remove(value)
            if len(words) == 4:
                values.append(f'{words[0]} {words[3]}')
                values.append(f'{words[2]} {words[3]}')
            else:
                values.append(and_to_comma(value))
    for i in range(len(values)):
        values[i] = values[i].replace('ern ', ' ')
    return ','.join(values)


csv_attributes = [
    CsvAttribute('name', other_attributes[0]),
    CsvAttribute('official_name', other_attributes[3]),
    CsvAttribute('origins', plant_attributes[20], mapping_function=origin_mapping),
    CsvAttribute('climate', plant_attributes[2], mapping_function=climate_mapping),
    CsvAttribute('difficulty', plant_attributes[3]),
    CsvAttribute('water', plant_attributes[4], mapping_function=drought_tolerance_mapping),
    CsvAttribute('light', plant_attributes[19]),
    CsvAttribute('humidity', plant_attributes[16], mapping_function=humidity_mapping),
    CsvAttribute('temperature', plant_attributes[23]),
    CsvAttribute('toxicity', plant_attributes[24], mapping_function=toxicity_mapping),
    # TODO CsvAttribute('height', plant_attributes[15]),
    CsvAttribute('format', plant_attributes[13]),
    CsvAttribute('leaf_shape', plant_attributes[17]),
    CsvAttribute('image_url', other_attributes[2]),
]

constant_attributes = [
    ConstantAttribute(plant_attributes[25], 'Indoor Plant'),
]

derived_attributes = [
    DerivedAttribute('leaf_shape', plant_attributes[8], foliage_color_mapping)
]

plants = parse('../data/how_many_plants_data.csv', csv_attributes, constant_attributes, derived_attributes, 'Yes')

export_plants('../export/plants.csv', plants, all_attributes, append=True)
