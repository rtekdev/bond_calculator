import ctypes

logic = ctypes.CDLL("./my_app.so")
logic.add.argtypes = (ctypes.c_int, ctypes.c_int)
logic.add.restype = ctypes.c_int

logic.getInflation.argtypes = (ctypes.c_char_p,)
logic.getInflation.restype = ctypes.c_double

# Compound Interest 
class CompoundReturn(ctypes.Structure):
    _fields_ = [
        ("total",          ctypes.c_double),
        ("profit",         ctypes.c_double),
        ("inflation_lost", ctypes.c_double),
    ]
logic.compound_interest.argtypes = (ctypes.c_float, ctypes.c_float, ctypes.c_int, ctypes.c_double)
logic.compound_interest.restype = CompoundReturn