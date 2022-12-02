import math
from data import *
from service import *

# TODO
# use CIE LAB color space to compare colors
# add support for multiple category values (maybe bit mask?)
# try out different comparisons for numeric values
# global plant id for parsing


def diversity(values: list[float]):
    total = 0
    for value in values:
        total += value
    p = []
    for value in values:
        p.append(value / total)
    div = 0
    for pi in p:
        div += pi * math.log2(pi)
    return -1 * div


if __name__ == '__main__':
    plants_test: list[Plant] = [Plant(0, "A", True, np.array([1.0, 0.0, 0.0]), "rose", 20.0),
                                Plant(1, "B", True, np.array([1.0, 0.0, 0.0]), "rose", 21.0),
                                Plant(2, "C", True, np.array([1.0, 0.0, 0.0]), "bamboo", 200.0),
                                Plant(3, "D", False, np.array([1.0, 0.0, 0.0]), "bamboo", 100.0)]

    plant_attributes: list[PlantAttribute] = [PlantAttribute("blooms", PlantAttributeType.BOOL),
                                              PlantAttribute("height", PlantAttributeType.NUMERIC, 'm'),
                                              PlantAttribute("color", PlantAttributeType.COLOR),
                                              PlantAttribute("family", PlantAttributeType.CATEGORICAL)]

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
    # colors()
    export_plants('../export/plants.csv', plants, plant_attributes)
