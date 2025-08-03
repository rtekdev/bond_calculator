import math 
from enum import Enum

def floor_to(x: float, places: int):
    f = 10 ** places
    return math.floor(x * f) / f

# Future
# class Settings(Enum):
#     # Default
#     AUTO = 0
#     MANUAL = 1