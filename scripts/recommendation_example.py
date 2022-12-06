from internal.service import *
from internal.data import *


plant_attributes = Plant.plant_attributes
all_attributes = plant_attributes + Plant.other_attributes

plants = parse_plants('../export/plants.csv', all_attributes)

users = [User(0, "Daniel", [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
              [UserPlant(plants[8], 10), UserPlant(plants[9], 10)])]

PlantRecommender.init_features(plants, plant_attributes)
UserService.init_user_attributes(users[0], plant_attributes)
recs = PlantRecommender.recommend_plant(plants, plant_attributes, users[0], False)

for user_plant in users[0].user_plants:
    print(user_plant.plant)
for rec in recs:
    print(rec)
