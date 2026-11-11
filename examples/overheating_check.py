"""Worked example: is a 2.5 L sedan at 118 C boiling, and what flow does it need?

Run from the repo root:  python examples/overheating_check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cooling import (boiling_point_c, coolant_flow_required,  # noqa: E402
                     coolant_temp_rise, expansion_volume, heat_to_coolant_estimate)

gauge_temp = 118          # C reading on the scan tool
q = heat_to_coolant_estimate(80_000)   # 80 kW at the crank, highway grade

print("Boiling point, 50/50 mix:")
for cap in (0, 13, 16):
    print(f"  {cap:2d} psi cap: {boiling_point_c(cap):5.1f} C")
bp = boiling_point_c(16)
print(f"Reading {gauge_temp} C vs {bp:.0f} C with a good 16 psi cap: "
      f"{'NOT boiling' if gauge_temp < bp else 'BOILING'}, margin {bp - gauge_temp:.0f} C")
print(f"Same reading with a failed cap (0 psi): margin {boiling_point_c(0) - gauge_temp:.0f} C")
print()
print(f"Heat to coolant (estimate): {q / 1000:.0f} kW")
print(f"Flow for a 8 C drop across the radiator: {coolant_flow_required(q, 8):.0f} L/min")
print(f"If the pump only moves 60 L/min, the rise is {coolant_temp_rise(q, 60):.1f} C")
print(f"Expansion of 7.5 L from 20 to 105 C: {expansion_volume(7.5, 20, 105):.2f} L")
