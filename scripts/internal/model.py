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
    __slots__ = "feature_index", "attribute_name", "attribute_type", "unique", "max_value", "min_value", "optional", "unit", "categories", "default_priority"
    # general
    attribute_name: str
    attribute_type: PlantAttributeType

    # used for parsing
    optional: bool
    unique: bool
    unit: str

    # used for recommendations
    categories: list[str]
    default_priority: float
    feature_index: int
    max_value: float
    min_value: float

    def __init__(self, attribute_name: str, attribute_type: PlantAttributeType, default_priority: float = 1.0,
                 unit: str = '', unique: bool = False, optional: bool = False):
        self.feature_index = -1
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type
        self.max_value = 0
        self.min_value = 0
        self.optional = optional
        self.unique = unique
        self.unit = unit
        self.categories = []
        self.default_priority = default_priority


class Plant:
    common_name: str
    family_common_name: str
    scientific_name: str

    active_growth_period: str
    bloom_period: str
    drought_tolerance: str
    duration: str
    family: str
    flower_color: str
    foliage_color: str
    foliage_porosity_summer: str
    foliage_porosity_winter: str
    frost_free_days: float
    fruit_color: str
    growth_habit: str
    growth_rate: str
    height: float
    lifespan: str
    ph_minimum: float
    ph_maximum: float
    toxicity: str
    type: str

    features: np.array

    plant_attributes: list[PlantAttribute] = [
        PlantAttribute("active_growth_period", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("bloom_period", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("climate", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("difficulty", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("drought_tolerance", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("duration", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("family", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("flower_color", PlantAttributeType.COLOR, 0.5),
        PlantAttribute("foliage_color", PlantAttributeType.COLOR, 0.5),
        PlantAttribute("foliage_porosity_summer", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("foliage_porosity_winter", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("frost_free_days", PlantAttributeType.NUMERIC, 0.5),
        PlantAttribute("fruit_color", PlantAttributeType.COLOR, 0.5),
        PlantAttribute("growth_habit", PlantAttributeType.CATEGORICAL, 1.0),
        PlantAttribute("growth_rate", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("height", PlantAttributeType.NUMERIC, 1.0, unit='m', optional=True),
        PlantAttribute("humidity", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("leaf_shape", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("lifespan", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("light", PlantAttributeType.CATEGORICAL, 0.5),
        PlantAttribute("origin", PlantAttributeType.CATEGORICAL, 0.1),
        PlantAttribute("ph_minimum", PlantAttributeType.NUMERIC, 0.2),
        PlantAttribute("ph_maximum", PlantAttributeType.NUMERIC, 0.2),
        PlantAttribute("temperature", PlantAttributeType.CATEGORICAL, 0.3),
        PlantAttribute("toxicity", PlantAttributeType.CATEGORICAL, 0.4),
        PlantAttribute("type", PlantAttributeType.CATEGORICAL, 1.0),
        PlantAttribute("width", PlantAttributeType.NUMERIC, 1.0, unit='m', optional=True),
    ]

    other_attributes: list[PlantAttribute] = [
        PlantAttribute("common_name", PlantAttributeType.CATEGORICAL, optional=True),
        PlantAttribute("family_common_name", PlantAttributeType.CATEGORICAL, optional=True),
        PlantAttribute("image", PlantAttributeType.CATEGORICAL, optional=True),
        PlantAttribute("scientific_name", PlantAttributeType.CATEGORICAL, unique=True),
    ]

    def __str__(self):
        return f"[{self.scientific_name}]"


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
