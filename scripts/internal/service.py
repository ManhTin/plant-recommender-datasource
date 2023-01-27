import math

from .model import *


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
                num_categories = len(attribute_list[attribute_index].categories)
                data.category_distribution = np.zeros(num_categories + 1)
                for user_plant in user.user_plants:
                    for category_index in range(num_categories):
                        is_in_category = user_plant.plant.features[feature_index + category_index]
                        data.category_distribution[category_index] += is_in_category
                        data.category_distribution[-1] += is_in_category


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
    def to_color(color_name):
        if color_name not in COLOR_DICT:
            result = COLOR_DICT['Black']
        else:
            rgb = COLOR_DICT[color_name]
            result = np.zeros(3)
            for i in range(3):
                result[i] = rgb[i] / 255.0
        return result

    @staticmethod
    def update_features(new_plants: list[Plant], current_plants: list[Plant], plant_attributes: list[PlantAttribute]):
        number_features = 0
        for plant_attribute in plant_attributes:
            plant_attribute.feature_index = number_features
            match plant_attribute.attribute_type:
                case PlantAttributeType.NUMERIC:
                    number_features += 1
                case PlantAttributeType.BOOL:
                    number_features += 1
                case PlantAttributeType.COLOR:
                    number_features += 3
                case PlantAttributeType.CATEGORICAL:
                    for plant in new_plants:
                        current_value = getattr(plant, plant_attribute.attribute_name)
                        current_value = current_value.split(',')
                        for val in current_value:
                            if val not in plant_attribute.categories:
                                plant_attribute.categories.append(val)
                    number_features += len(plant_attribute.categories)

        # init feature array
        for plant in new_plants:
            plant.features = np.zeros(number_features)

        for plant_attribute in plant_attributes:
            feature_index = plant_attribute.feature_index

            match plant_attribute.attribute_type:
                case PlantAttributeType.NUMERIC:
                    if current_plants:
                        max_value = plant_attribute.max_value
                        min_value = plant_attribute.min_value
                    else:
                        max_value = getattr(new_plants[0], plant_attribute.attribute_name)
                        min_value = getattr(new_plants[0], plant_attribute.attribute_name)

                    old_max_value = max_value
                    old_min_value = min_value

                    for plant in new_plants:
                        current_value = getattr(plant, plant_attribute.attribute_name)
                        if current_value > max_value:
                            max_value = current_value
                        if current_value < min_value:
                            min_value = current_value

                    plant_attribute.max_value = max_value
                    plant_attribute.min_value = min_value

                    if current_plants and (old_max_value != max_value or old_min_value != min_value):
                        for plant in current_plants:
                            current_value = getattr(plant, plant_attribute.attribute_name)
                            plant.features[feature_index] = (current_value - min_value) / (max_value - min_value)

                    for plant in new_plants:
                        current_value = getattr(plant, plant_attribute.attribute_name)
                        plant.features[feature_index] = (current_value - min_value) / (max_value - min_value)
                case PlantAttributeType.BOOL:
                    for plant in new_plants:
                        current_value = getattr(plant, plant_attribute.attribute_name)
                        plant.features[feature_index] = 1 if current_value else 0
                case PlantAttributeType.COLOR:
                    for plant in new_plants:
                        color_string = getattr(plant, plant_attribute.attribute_name)
                        current_value = PlantRecommender.to_color(color_string)
                        for i in range(0, 3):
                            plant.features[feature_index + i] = current_value[i]
                case PlantAttributeType.CATEGORICAL:
                    for plant in new_plants:
                        current_value = getattr(plant, plant_attribute.attribute_name)
                        current_value = current_value.split(',')
                        for val in current_value:
                            index = plant_attribute.categories.index(val)
                            plant.features[feature_index + index] = 1

    @staticmethod
    def init_features(plant_list: list[Plant], plant_attributes: list[PlantAttribute]):
        PlantRecommender.update_features(plant_list, [], plant_attributes)

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
                        num_categories = len(plant_attribute.categories)
                        attribute_data = user.attribute_data[attribute_index]
                        for category_index in range(num_categories):
                            is_in_category = plant.features[feature_index + category_index]
                            attribute_score += is_in_category * attribute_data.category_distribution[category_index]
                            attribute_score /= attribute_data.category_distribution[-1]

                score += user.attribute_data[attribute_index].priority * attribute_score

            prio = 0.0
            for attribute_index in range(0, len(plant_attributes)):
                prio += user.attribute_data[attribute_index].priority
            score /= prio
            result.append(PlantRecommendation(plant, score))

        result.sort(key=lambda x: x.score, reverse=True)
        return result
