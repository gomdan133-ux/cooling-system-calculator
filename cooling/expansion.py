"""Coolant thermal expansion, for reservoir sizing and overflow complaints."""

BETA_5050 = 0.0006  # 1/K, approximate volumetric expansion of 50/50 coolant


def expansion_volume(system_volume_l: float, t_cold_c: float, t_hot_c: float,
                     beta_per_k: float = BETA_5050) -> float:
    """Extra coolant volume (L) when the system warms up: dV = V * beta * dT."""
    if system_volume_l <= 0 or beta_per_k <= 0 or t_hot_c < t_cold_c:
        raise ValueError("invalid input")
    return system_volume_l * beta_per_k * (t_hot_c - t_cold_c)
