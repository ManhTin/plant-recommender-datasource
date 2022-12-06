from internal.data import *

plant_attributes = Plant.plant_attributes
all_attributes = plant_attributes + Plant.other_attributes

csv_attributes = [CsvAttribute('Palatable Human', plant_attributes[0]),
                  CsvAttribute('Height, Mature (feet)', plant_attributes[1], unit='feet'),
                  CsvAttribute('Flower Color', plant_attributes[2]),
                  CsvAttribute('Family', plant_attributes[3]),
                  CsvAttribute('Scientific Name', all_attributes[4])]

plants = parse('../data/PLANTS.csv', csv_attributes, 'Yes')

export_plants('../export/plants.csv', plants, all_attributes)
