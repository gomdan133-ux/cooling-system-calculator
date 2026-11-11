"""Heat the coolant has to carry, and the flow needed to carry it."""

# 50/50 ethylene glycol / water, around 90 C (approximate)
CP_5050 = 3500.0      # J/(kg*K)
RHO_5050 = 1030.0     # kg/m^3


def heat_to_coolant_estimate(brake_power_w: float, ratio: float = 1.0) -> float:
    """Rough heat into the coolant (W).

    Rule of thumb: a gasoline engine sends roughly as much energy to the
    coolant as it makes at the crank (ratio about 0.8 to 1.2). Use real
    test data when you have it.
    """
    if brake_power_w < 0 or ratio <= 0:
        raise ValueError("invalid input")
    return brake_power_w * ratio


def coolant_flow_required(heat_w: float, delta_t_k: float,
                          cp: float = CP_5050, rho: float = RHO_5050) -> float:
    """Coolant flow (L/min) to carry heat_w with a given inlet-outlet temperature drop.

    Q = m_dot * cp * dT  ->  m_dot = Q / (cp * dT)
    """
    if heat_w < 0 or delta_t_k <= 0 or cp <= 0 or rho <= 0:
        raise ValueError("invalid input")
    m_dot = heat_w / (cp * delta_t_k)          # kg/s
    return m_dot / rho * 1000 * 60             # L/min


def coolant_temp_rise(heat_w: float, flow_l_min: float,
                      cp: float = CP_5050, rho: float = RHO_5050) -> float:
    """Temperature rise (K) across the engine for a given flow."""
    if heat_w < 0 or flow_l_min <= 0:
        raise ValueError("invalid input")
    m_dot = flow_l_min / 1000 / 60 * rho
    return heat_w / (m_dot * cp)
