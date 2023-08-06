"""
meta.py
this script is responsible for introducing meta values.
"""
from enum import Enum


"""
constants
"""
PI = 3.141592653589793
E = 2.718281828459045


class Meta(Enum):
    """
    define some common terms in math.
    """
    ERROR = "error"
    INFINITY = "infinity"
    INFINITESIMAL = "infinitesimal"
    Q = "all real numbers"
    Z = "all integers"
    N = "all natural numbers"
    N_positive = "all positive natural numbers"
