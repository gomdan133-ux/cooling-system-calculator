import pytest

from cooling import (boiling_point_c, coolant_flow_required, coolant_temp_rise,
                     expansion_volume, heat_to_coolant_estimate, water_boiling_point_c)


def test_water_boils_near_100_at_sea_level():
    assert water_boiling_point_c(14.696) == pytest.approx(100.0, abs=0.3)


def test_water_15psi_cap_about_121():
    assert water_boiling_point_c(14.696 + 15) == pytest.approx(121.0, abs=1.0)


def test_5050_with_16psi_cap():
    bp = boiling_point_c(16, 50)
    assert 127 <= bp <= 132


def test_higher_cap_raises_boiling_point():
    assert boiling_point_c(18) > boiling_point_c(13) > boiling_point_c(0)


def test_flow_and_temp_rise_are_inverse():
    flow = coolant_flow_required(60_000, 8)
    assert coolant_temp_rise(60_000, flow) == pytest.approx(8)


def test_flow_known_value():
    # 60 kW, 8 K drop: m_dot = 60000/(3500*8) = 2.143 kg/s -> 124.8 L/min
    assert coolant_flow_required(60_000, 8) == pytest.approx(124.8, rel=1e-3)


def test_expansion():
    assert expansion_volume(10, 20, 95) == pytest.approx(0.45)


def test_heat_estimate():
    assert heat_to_coolant_estimate(100_000, 0.9) == pytest.approx(90_000)


@pytest.mark.parametrize("fn,args", [
    (water_boiling_point_c, (0,)),
    (boiling_point_c, (-1,)),
    (boiling_point_c, (15, 45)),
    (coolant_flow_required, (1000, 0)),
    (expansion_volume, (10, 90, 20)),
])
def test_invalid(fn, args):
    with pytest.raises(ValueError):
        fn(*args)
