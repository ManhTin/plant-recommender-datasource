import numpy as np
from enum import Enum
from typing import Optional


class Plant:
    __slots__ = "plant_id", "name", "blooms", "color", "color_name", "family", "height", "features"
    plant_id: int
    name: str

    blooms: bool
    color: np.array
    color_name: str
    family: str
    height: float

    features: np.array

    def __init__(self, plant_id: int, name: str = '', blooms: bool = False, color: np.array = None, family: str = '',
                 height: float = 0.0):
        if color is None:
            color = np.array([0.0, 0.0, 0.0])
        self.plant_id = plant_id
        self.name = name
        self.blooms = blooms
        self.color = color
        self.color_name = ''
        self.family = family
        self.height = height
        self.features = np.array([])

    def __str__(self):
        return f"[{self.plant_id}. {self.name}, ({self.family}), blooms: {self.blooms}, height: {self.height:2.2f} m, color: {self.color_name}]"


class PlantAttributeType(Enum):
    NUMERIC = 0
    BOOL = 1
    COLOR = 2
    CATEGORICAL = 3


class PlantAttribute:
    __slots__ = "feature_index", "attribute_name", "attribute_type", "max_value", "min_value", "unit", "categories"
    feature_index: int
    attribute_name: str
    attribute_type: PlantAttributeType
    max_value: float
    min_value: float
    unit: str
    categories: list[str]

    def __init__(self, attribute_name: str, attribute_type: PlantAttributeType, unit: str = ''):
        self.feature_index = -1
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type
        self.max_value = 0
        self.min_value = 0
        self.unit = unit
        self.categories = []


class UserPlant:
    __slots__ = "plant", "rating"
    plant: Plant
    rating: float

    def __init__(self, plant: Plant, rating: float = 5.0):
        self.plant = plant
        self.rating = rating


class UserAttributeData:
    __slots__ = "priority", "num_true", "true_ratio", "category_distribution"
    priority: float
    num_true: float
    true_ratio: float
    category_distribution: np.array

    def __init__(self, priority: float):
        self.priority = priority
        self.num_true = 0.0
        self.true_ratio = 0.0
        self.category_distribution = np.array([])


class User:
    __slots__ = "user_id", "name", "user_plants", "attribute_data"
    user_id: int
    name: str
    user_plants: list[UserPlant]
    attribute_data: list[UserAttributeData]

    def __init__(self,
                 user_id: int,
                 name: str,
                 attribute_priority: list[float],
                 user_plants: Optional[list[UserPlant]] = None):
        if user_plants is None:
            user_plants = []
        self.user_id = user_id
        self.name = name
        self.user_plants = user_plants

        self.attribute_data = []
        for attribute_index in range(0, len(attribute_priority)):
            data = UserAttributeData(attribute_priority[attribute_index])
            self.attribute_data.append(data)
