import numpy as np
from enum import Enum
from typing import Optional


COLOR_DICT = {
    'Black': [0.0, 0.0, 0.0],
    'Blue': [0.0, 0.0, 255.0],
    'Brown': [150.0, 75.0, 0.0],
    'Dark Green': [0.0, 100.0, 0.0],
    'Gray-Green': [94.0, 113.0, 106.0],
    'Green': [0.0, 255.0, 0.0],
    'Orange': [255.0, 165.0, 0.0],
    'Purple': [128.0, 0.0, 128.0],
    'Red': [255.0, 0.0, 0.0],
    'White': [255.0, 255.0, 255.0],
    'White-Gray': [235.0, 236.0, 240.0],
    'Yellow': [255.0, 255.0, 0.0],
    'Yellow-Green': [154.0, 205.0, 50.0],
}


class PlantAttributeType(Enum):
    NUMERIC = 0
    BOOL = 1
    COLOR = 2
    CATEGORICAL = 3


class PlantAttribute:
    __slots__ = "feature_index", "attribute_name", "attribute_type", "unique", "max_value", "min_value", "unit", "categories"
    feature_index: int
    attribute_name: str
    attribute_type: PlantAttributeType
    max_value: float
    min_value: float
    unique: bool
    unit: str
    categories: list[str]

    def __init__(self, attribute_name: str, attribute_type: PlantAttributeType, unit: str = '', unique: bool = False):
        self.feature_index = -1
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type
        self.max_value = 0
        self.min_value = 0
        self.unique = unique
        self.unit = unit
        self.categories = []


class Plant:
    __slots__ = "name", "palatable", "color", "family", "height", "features"
    name: str

    palatable: bool
    color: str
    family: str
    height: float

    features: np.array

    plant_attributes: list[PlantAttribute] = [PlantAttribute("palatable", PlantAttributeType.BOOL),
                                              PlantAttribute("height", PlantAttributeType.NUMERIC, 'm'),
                                              PlantAttribute("color", PlantAttributeType.COLOR),
                                              PlantAttribute("family", PlantAttributeType.CATEGORICAL)]
    other_attributes: list[PlantAttribute] = [PlantAttribute("name", PlantAttributeType.CATEGORICAL, unique=True)]

    def __init__(self, name: str = '', palatable: bool = False, color: str = '', family: str = '',
                 height: float = 0.0):
        self.name = name
        self.palatable = palatable
        self.color = color
        self.family = family
        self.height = height
        self.features = np.array([])

    def __str__(self):
        return f"[{self.name}, ({self.family}), palatable: {self.palatable}, height: {self.height:2.2f} m, color: {self.color}]"


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
