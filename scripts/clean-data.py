from internal.data import *

plant_attributes = Plant.plant_attributes
other_attributes = Plant.other_attributes
all_attributes = plant_attributes + Plant.other_attributes

csv_attributes = [
    CsvAttribute('Active Growth Period', plant_attributes[0]),
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
    CsvAttribute('Growth Habit', plant_attributes[13]),
    CsvAttribute('Growth Rate', plant_attributes[14]),
    CsvAttribute('Height, Mature (feet)', plant_attributes[15], unit='feet'),
    CsvAttribute('Lifespan', plant_attributes[17]),
    CsvAttribute('pH (Minimum)', plant_attributes[20]),
    CsvAttribute('pH (Maximum)', plant_attributes[21]),
    CsvAttribute('Scientific Name', other_attributes[3]),
    CsvAttribute('Toxicity', plant_attributes[23]),
]

constant_attributes = [
    ConstantAttribute(plant_attributes[19], 'North America'),
    ConstantAttribute(plant_attributes[24], 'Outdoor Plant'),
]

plants = parse('../data/PLANTS.csv', csv_attributes, constant_attributes, 'Yes')

export_plants('../export/plants.csv', plants, all_attributes)
