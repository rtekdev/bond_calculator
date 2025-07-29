import math 

def floor_to(x: float, places: int):
    f = 10 ** places
    return math.floor(x * f) / f