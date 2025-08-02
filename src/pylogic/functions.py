from ctypes import *

logic = CDLL("./my_app.so")

logic.getInflation.argtypes = (c_char_p,)
logic.getInflation.restype = c_double

# Compound Interest 
class CompoundReturn(Structure):
    _fields_ = [
        ("total",          c_double),
        ("profit",         c_double),
        ("inflation_lost", c_double),
    ]
logic.compound_interest.argtypes = [
    POINTER(CompoundReturn),  # <-- result-out pointer
    c_float,                  # initial_amount
    c_double,                 # interest_rate
    c_int,                    # years
    c_double,                 # next_rate
    c_double,                 # inflation
    c_char_p,                 # type string
    c_int,                    # total years
    c_float,                  # regular amount
    c_char_p                  # regular type
]
logic.compound_interest.restype = None

class BondReturn(Structure):
    _fields_ = [
        ("name",                c_char_p),
        ("years",               c_int),
        ("interest_rate",       c_double),
        ("next_rate",           c_double),
        ("type",                c_char_p),
    ]

logic.getBonds.argtypes = (POINTER(c_int),)
logic.getBonds.restype = POINTER(BondReturn)

logic.freeBonds.argtypes = (POINTER(BondReturn), c_int)
logic.freeBonds.restype  = None