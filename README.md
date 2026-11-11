# Cooling System Calculator

A tested Python library for engine cooling diagnosis and sizing. It covers coolant boiling point against radiator cap pressure, the coolant flow needed to carry engine heat, the temperature rise across the engine, and coolant expansion.

Built by an ASE-certified automotive technician to answer two common shop questions with physics: *"Is it actually boiling?"* and *"Why does it only overheat under load?"*

## The math

**1. Boiling point vs pressure.** The Antoine equation for water at absolute pressure (atmospheric + cap):

$$T_b = \frac{B}{A - \log_{10} P_{mmHg}} - C \qquad (A = 8.14019,\; B = 1810.94,\; C = 244.485)$$

A fixed boiling-point rise is then added for the glycol mix (about +7 °C for 50/50).

**2. Heat carried by coolant**

$$\dot{Q} = \dot{m}\, c_p\, \Delta T \quad\Rightarrow\quad \dot{V} = \frac{\dot{Q}}{\rho\, c_p\, \Delta T}$$

The 50/50 coolant properties are taken as c_p ≈ 3,500 J/kg·K and ρ ≈ 1,030 kg/m³.

**3. Thermal expansion**

$$\Delta V = V\, \beta\, \Delta T \qquad (\beta \approx 0.0006\ /K)$$

**4. Heat to coolant (rule of thumb):** roughly equal to crankshaft power for a gasoline engine. Use test data when you have it.

## Example

```bash
python examples/overheating_check.py
```

```
Boiling point, 50/50 mix:
   0 psi cap: 106.8 C
  13 psi cap: 125.9 C
  16 psi cap: 129.1 C
Reading 118 C vs 129 C with a good 16 psi cap: NOT boiling, margin 11 C
Same reading with a failed cap (0 psi): margin -11 C

Heat to coolant (estimate): 80 kW
Flow for a 8 C drop across the radiator: 166 L/min
If the pump only moves 60 L/min, the rise is 22.2 C
Expansion of 7.5 L from 20 to 105 C: 0.38 L
```

## Shop takeaways

- **The radiator cap is part of the cooling system.** With a good 16 psi cap, 118 °C is hot but not boiling. With a failed cap, the same engine boils over. Always pressure-test the cap.
- **Flow sets the temperature rise.** A worn water pump impeller or a collapsing hose cuts flow, so the engine runs much hotter than the radiator outlet under load, even when it idles fine.
- **Expansion explains the reservoir.** A normal system pushes several hundred mL into the overflow when hot. A level that keeps rising or bubbling points to combustion gas (head gasket), not normal expansion.

## Install and test

```bash
pip install pytest
pytest -q
```

## How this was built

1. **Started from overheating diagnoses** I do in the shop: cap failures, weak pumps, overflow complaints, and the "is it boiling?" question.
2. **Picked models that can be checked.** I used the Antoine equation for water's vapor pressure, with published constants, the basic heat balance (Q = ṁ c_p ΔT), and linear volumetric expansion.
3. **Checked against known values.** Water boils at about 100 °C at sea level and about 121 °C with a 15 psi cap. A 50/50 mix with a 16 psi cap falls in the expected 127 to 132 °C range. The flow and temperature-rise functions are checked against each other, and against a 60 kW hand calculation.
4. **Wrote 13 pytest tests,** including invalid inputs, and ran a worked example. The output above comes from actually running it.

**Limits:** coolant properties and the glycol boiling elevation are approximate, accurate to a few degrees. The heat estimate is a rule of thumb. Use this for diagnosis and learning, not for design sign-off.

## License

MIT
