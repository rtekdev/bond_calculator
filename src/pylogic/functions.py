import ctypes

logic = ctypes.CDLL("./my_app.so")

logic.getInflation.argtypes = (ctypes.c_char_p,)
logic.getInflation.restype = ctypes.c_double

# Compound Interest 
class CompoundReturn(ctypes.Structure):
    _fields_ = [
        ("total",          ctypes.c_double),
        ("profit",         ctypes.c_double),
        ("inflation_lost", ctypes.c_double),
    ]
logic.compound_interest.argtypes = (
    ctypes.c_float, ctypes.c_double, ctypes.c_int, ctypes.c_double, ctypes.c_double)
logic.compound_interest.restype = CompoundReturn

class BondReturn(ctypes.Structure):
    _fields_ = [
        ("name",                ctypes.c_char_p),
        ("years",               ctypes.c_int),
        ("interest_rate",       ctypes.c_double),
        ("next_rate",           ctypes.c_double),
        ("type",                ctypes.c_char_p),
    ]

logic.load_bond_types.argtypes = (ctypes.POINTER(ctypes.c_size_t),)
logic.load_bond_types.restype = ctypes.POINTER(BondReturn)

logic.free_bond_types.argtypes = (ctypes.POINTER(BondReturn), ctypes.c_size_t)
logic.free_bond_types.restype  = None