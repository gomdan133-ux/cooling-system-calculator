"""Boiling point vs radiator cap pressure."""
import math

ATM_PSI = 14.696
PSI_TO_MMHG = 51.715

# Antoine constants for water, about 99 to 374 C, pressure in mmHg
_A, _B, _C = 8.14019, 1810.94, 244.485

# Approximate boiling point rise over pure water at the same pressure
GLYCOL_ELEVATION_C = {0: 0.0, 30: 3.0, 50: 7.0, 60: 9.0}


def water_boiling_point_c(abs_pressure_psi: float) -> float:
    """Boiling point of pure water (C) at an absolute pressure (psia), Antoine equation."""
    if abs_pressure_psi <= 0:
        raise ValueError("pressure must be > 0")
    p_mmhg = abs_pressure_psi * PSI_TO_MMHG
    return _B / (_A - math.log10(p_mmhg)) - _C


def boiling_point_c(cap_psi: float, glycol_pct: int = 50) -> float:
    """Approximate coolant boiling point (C) with a working cap of cap_psi (gauge).

    Water boiling point at (atmospheric + cap) pressure, plus a fixed
    elevation for the glycol mix. Accuracy is a few degrees; good for
    diagnosis, not for design sign-off.
    """
    if cap_psi < 0:
        raise ValueError("cap pressure must be >= 0")
    if glycol_pct not in GLYCOL_ELEVATION_C:
        raise ValueError(f"glycol_pct must be one of {sorted(GLYCOL_ELEVATION_C)}")
    return water_boiling_point_c(ATM_PSI + cap_psi) + GLYCOL_ELEVATION_C[glycol_pct]
