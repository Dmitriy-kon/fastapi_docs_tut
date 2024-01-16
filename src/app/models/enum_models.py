from dataclasses import dataclass
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Models:
    def __init__(self, power: str, electricity: str, price: int = None):
        self.power = power
        self.electricity = electricity
        self.price = price
