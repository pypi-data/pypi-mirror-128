from .strategies import (
    Simple_GA,
    Simple_ES,
    CMA_ES,
    Differential_ES,
    PSO_ES,
    Open_NES,
    PEPG_ES,
    PBT_ES,
    Persistent_ES,
    xNES,
)


Strategies = {
    "Simple_GA": Simple_GA,
    "Simple_ES": Simple_ES,
    "CMA_ES": CMA_ES,
    "Differential_ES": Differential_ES,
    "PSO_ES": PSO_ES,
    "Open_NES": Open_NES,
    "PEPG_ES": PEPG_ES,
    "PBT_ES": PBT_ES,
    "Persistent_ES": Persistent_ES,
    "xNES": xNES,
}

__all__ = [
    "Simple_GA",
    "Simple_ES",
    "CMA_ES",
    "Differential_ES",
    "PSO_ES",
    "Open_NES",
    "PEPG_ES",
    "PBT_ES",
    "Persistent_ES",
    "xNES",
    "Strategies",
]
