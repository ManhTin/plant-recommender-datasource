import math

from model import *


class PlantAttributeService:
    @staticmethod
    def get_number_of_feature_slots(attribute_type: PlantAttributeType):
        match attribute_type:
            case PlantAttributeType.NUMERIC:
                return 1
            case PlantAttributeType.BOOL:
                return 1
            case PlantAttributeType.COLOR:
                return 3
            case PlantAttributeType.CATEGORICAL:
                return 1


class UserService:
    @staticmethod
    def init_user_attributes(user: User, plant_attributes: list[PlantAttribute]):
        attribute_list = plant_attributes
        for attribute_index in range(0, len(attribute_list)):
            feature_index = attribute_list[attribute_index].feature_index
            data = user.attribute_data[attribute_index]
            if attribute_list[attribute_index].attribute_type == PlantAttributeType.BOOL:
                for user_plant in user.user_plants:
                    data.num_true += user_plant.plant.features[feature_index]
                data.true_ratio = (data.num_true / len(user.user_plants)) - 0.5
            elif attribute_list[attribute_index].attribute_type == PlantAttributeType.CATEGORICAL:
                data.category_distribution = np.zeros(len(attribute_list[attribute_index].categories))
                for user_plant in user.user_plants:
                    cat_index = user_plant.plant.features[feature_index]
                    data.category_distribution[int(cat_index)] += 1


class PlantRecommendation:
    __slots__ = "plant", "score"
    plant: Plant
    score: float

    def __init__(self, plant: Plant, score: float):
        self.plant = plant
        self.score = score

    def __str__(self):
        return str(self.plant) + ": " + str(self.score)


class PlantRecommender:
    @staticmethod
    def init_features(plant_list: list[Plant], plant_attributes: list[PlantAttribute]):
        # find number of features
        number_features = 0
        for plant_attribute in plant_attributes:
            plant_attribute.feature_index = number_features
            number_features += PlantAttributeService.get_number_of_feature_slots(plant_attribute.attribute_type)

        # init feature array
        for plant in plant_list:
            plant.features = np.zeros(number_features)

        # iterate over all features
        for plant_attribute in plant_attributes:
            feature_index = plant_attribute.feature_index

            match plant_attribute.attribute_type:
                case PlantAttributeType.NUMERIC:
                    max_value = getattr(plant_list[0], plant_attribute.attribute_name)
                    min_value = getattr(plant_list[0], plant_attribute.attribute_name)
                    for plant in plant_list:
                        current_value = getattr(plant, plant_attribute.attribute_name)
                        if current_value > max_value:
                            max_value = current_value
                        if current_value < min_value:
                            min_value = current_value

                    plant_attribute.max_value = max_value
                    plant_attribute.min_value = min_value

                    for plant in plant_list:
                        current_value = getattr(plant, plant_attribute.attribute_name)
                        plant.features[feature_index] = (current_value - min_value) / (max_value - min_value)
                case PlantAttributeType.BOOL:
                    for plant in plant_list:
                        current_value = getattr(plant, plant_attribute.attribute_name)
                        plant.features[feature_index] = 1 if current_value else 0
                case PlantAttributeType.COLOR:
                    for plant in plant_list:
                        current_value = getattr(plant, plant_attribute.attribute_name)
                        for i in range(0, 3):
                            plant.features[feature_index + i] = current_value[i]
                case PlantAttributeType.CATEGORICAL:
                    for plant in plant_list:
                        current_value = getattr(plant, plant_attribute.attribute_name)
                        index = None
                        if current_value in plant_attribute.categories:
                            index = plant_attribute.categories.index(current_value)
                        else:
                            index = len(plant_attribute.categories)
                            plant_attribute.categories.append(current_value)
                        plant.features[feature_index] = index

    @staticmethod
    def recommend_plant(plants: list[Plant], plant_attributes: list[PlantAttribute], user: User,
                        filter_user_plants: bool = False) -> list[PlantRecommendation]:
        result: list[PlantRecommendation] = []

        for plant in plants:
            if filter_user_plants and any(user_plant.plant == plant for user_plant in user.user_plants):
                continue

            score: float = 0.0

            for attribute_index in range(0, len(plant_attributes)):
                plant_attribute = plant_attributes[attribute_index]
                feature_index = plant_attribute.feature_index
                attribute_score = 0.0

                match plant_attribute.attribute_type:
                    case PlantAttributeType.NUMERIC:
                        for user_plant in user.user_plants:
                            attribute_score += (plant.features[feature_index]
                                                - user_plant.plant.features[feature_index]) ** 2
                        attribute_score = 1 - math.sqrt(attribute_score)
                    case PlantAttributeType.BOOL:
                        a = user.attribute_data[attribute_index].true_ratio
                        v = plant.features[feature_index]
                        attribute_score = 0.5 + v * a - (1 - v) * a
                    case PlantAttributeType.COLOR:
                        for user_plant in user.user_plants:
                            color_score = 0.0
                            for i in range(feature_index, feature_index + 3):
                                color_score += abs(plant.features[i] - user_plant.plant.features[i])
                            attribute_score += 1 - (color_score / 3)
                        attribute_score /= len(user.user_plants)
                    case PlantAttributeType.CATEGORICAL:
                        attribute_score = user.attribute_data[attribute_index].category_distribution[
                                              int(plant.features[feature_index])] / len(plant_attribute.categories)

                score += user.attribute_data[attribute_index].priority * attribute_score

            prio = 0.0
            for attribute_index in range(0, len(plant_attributes)):
                prio += user.attribute_data[attribute_index].priority
            score /= prio
            result.append(PlantRecommendation(plant, score))

        result.sort(key=lambda x: x.score, reverse=True)
        return result
