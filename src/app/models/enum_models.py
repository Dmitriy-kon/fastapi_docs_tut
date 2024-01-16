from dataclasses import dataclass
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Models:
    def __init__(self, power: str, electricity: str, price: int):
        self.power: str | None = power
        self.electricity: str = electricity
        self.price: int | None = price
