from internal.service import *
from internal.data import *
import json


def get_plant_by_name(plant_list, name):
    for plant in plant_list:
        if name == plant.scientific_name:
            return plant


plant_attributes = Plant.plant_attributes
all_attributes = plant_attributes + Plant.other_attributes

plants = parse_plants('../export/plants.csv', all_attributes)
PlantRecommender.init_features(plants, plant_attributes)

user = User(0, "Daniel", [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [])

# parse json
with open("example.json") as json_file:
    json_data = json.load(json_file)
    json_user = json_data['user']
    json_plants = json_user['plants']

    user_plants = []
    for plant_name in json_plants:
        user_plants.append(UserPlant(get_plant_by_name(plants, plant_name)))
    user.user_plants = user_plants

UserService.init_user_attributes(user, plant_attributes)
recs = PlantRecommender.recommend_plant(plants, plant_attributes, user, True)

for i in range(10):
    print(recs[i])
