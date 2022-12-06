from internal.data import *

plant_attributes = Plant.plant_attributes
other_attributes = Plant.other_attributes
all_attributes = plant_attributes + Plant.other_attributes

csv_attributes = [
    CsvAttribute('Active Growth Period', plant_attributes[0]),
    CsvAttribute('Bloom Period', plant_attributes[1]),
    CsvAttribute('Common Name', other_attributes[0]),
    CsvAttribute('Drought Tolerance', plant_attributes[2]),
    CsvAttribute('Family', plant_attributes[3]),
    CsvAttribute('Family Common Name', other_attributes[1]),
    CsvAttribute('Flower Color', plant_attributes[4]),
    CsvAttribute('Foliage Color', plant_attributes[5]),
    CsvAttribute('Foliage Porosity Summer', plant_attributes[6]),
    CsvAttribute('Foliage Porosity Winter', plant_attributes[7]),
    CsvAttribute('Frost Free Days, Minimum', plant_attributes[8]),
    CsvAttribute('Fruit Color', plant_attributes[9]),
    CsvAttribute('Growth Habit', plant_attributes[10]),
    CsvAttribute('Growth Rate', plant_attributes[11]),
    CsvAttribute('Height, Mature (feet)', plant_attributes[12], unit='feet'),
    CsvAttribute('Lifespan', plant_attributes[13]),
    CsvAttribute('Palatable Human', plant_attributes[14]),
    CsvAttribute('pH (Minimum)', plant_attributes[15]),
    CsvAttribute('pH (Maximum)', plant_attributes[16]),
    CsvAttribute('Scientific Name', other_attributes[2]),
    CsvAttribute('Toxicity', plant_attributes[17]),
]

plants = parse('../data/PLANTS.csv', csv_attributes, 'Yes')

export_plants('../export/plants.csv', plants, all_attributes)
