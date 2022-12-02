from internal.data import *

plant_attributes = Plant.plant_attributes

csv_attributes = [CsvAttribute('Palatable Human', plant_attributes[0]),
                  CsvAttribute('Height, Mature (feet)', plant_attributes[1], unit='feet'),
                  CsvAttribute('Flower Color', plant_attributes[2]),
                  CsvAttribute('Family', plant_attributes[3]),
                  CsvAttribute('Scientific Name', PlantAttribute('name', PlantAttributeType.CATEGORICAL))]

plants = parse('../data/PLANTS.txt', csv_attributes, 'Yes', 100)

export_plants('../export/plants.csv', plants, plant_attributes)
