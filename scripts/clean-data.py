from internal.data import *

plant_attributes = Plant.plant_attributes
all_attributes = plant_attributes + Plant.other_attributes

csv_attributes = [CsvAttribute('Palatable Human', plant_attributes[0]),
                  CsvAttribute('Height, Mature (feet)', plant_attributes[1], unit='feet'),
                  CsvAttribute('Flower Color', plant_attributes[2]),
                  CsvAttribute('Family', plant_attributes[3]),
                  CsvAttribute('Scientific Name', PlantAttribute('name', PlantAttributeType.CATEGORICAL))]

plants = parse('../data/PLANTS.txt', csv_attributes, 'Yes', max_count=10)
keys = extract_keys(plants, all_attributes)
plants = parse('../data/PLANTS.txt', csv_attributes, 'Yes', max_count=12, unique_keys=keys)

export_plants('../export/plants.csv', plants, all_attributes)
