from internal.service import *
from internal.data import *


plant_attributes = Plant.plant_attributes

csv_attributes = [CsvAttribute('Palatable Human', plant_attributes[0]),
                  CsvAttribute('Height, Mature (feet)', plant_attributes[1], unit='feet'),
                  CsvAttribute('Flower Color', plant_attributes[2]),
                  CsvAttribute('Family', plant_attributes[3]),
                  CsvAttribute('Scientific Name', PlantAttribute('name', PlantAttributeType.CATEGORICAL))]

plants = parse('../data/PLANTS.txt', csv_attributes, 'Yes', 100)

users = [User(0, "Daniel", [1.0, 1.0, 1.0, 1.0], [UserPlant(plants[8], 10), UserPlant(plants[9], 10)])]

PlantRecommender.init_features(plants, plant_attributes)
UserService.init_user_attributes(users[0], plant_attributes)
recs = PlantRecommender.recommend_plant(plants, plant_attributes, users[0], False)

for user_plant in users[0].user_plants:
    print(user_plant.plant)
for rec in recs:
    print(rec)
