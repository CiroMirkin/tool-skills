# Complete Circuit Examples

Real-world circuit examples with full code.

## Example 1: 555 Timer LED Blinker

Classic astable multivibrator using 555 timer IC.

```python
import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing(file='555_blinker.svg') as d:
    d.config(fontsize=12)

    # 555 Timer IC
    T = elm.Ic555().label('555')

    # Ground connection
    BOT = elm.Ground().at(T.GND)
    elm.Dot()

    # Timing resistors (Ra and Rb)
    elm.Resistor().endpoints(T.DIS, T.THR).label('Rb\n10kΩ').idot()
    elm.Resistor().up().at(T.DIS).label('Ra\n10kΩ')
    elm.Vdd().label('+5V')

    # Timing capacitor
    elm.Line().endpoints(T.THR, T.TRG)
    elm.Capacitor().at(T.TRG).toy(BOT.start).label('C\n10µF')
    elm.Line().tox(BOT.start)

    # Control voltage bypass capacitor
    elm.Capacitor().at(T.CTL).toy(BOT.start).label('0.01µF', 'bottom').dot()

    # Junction dots
    elm.Dot().at(T.DIS)
    elm.Dot().at(T.THR)
    elm.Dot().at(T.TRG)

    # Reset and Vcc tied to power
    elm.Line().endpoints(T.RST, T.Vcc).dot()
    elm.Line().up(d.unit/4)
    elm.Vdd().label('+5V')

    # Output: LED with current limiting resistor
    elm.Resistor().right().at(T.OUT).label('330Ω')
    elm.LED().flip().toy(BOT.start)
    elm.Line().tox(BOT.start)
```

**Frequency**: f ≈ 1.44 / ((Ra + 2Rb) × C) ≈ 4.8 Hz (blinks ~2.4 times/second)

**Use cases**: LED flasher, pulse generator, timing circuits

## Example 2: Inverting Opamp with Detailed Power

Inverting amplifier with explicit power supply connections.

```python
import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing(file='inverting_amp_power.svg') as d:
    d.config(fontsize=12)

    # Main opamp (part name inside the body, clear of the power rails)
    op = elm.Opamp(leads=True).label('TL081', loc='center', ofst=(0.05, 0), fontsize=10)

    # Power supplies: short leads keep the rails inside the feedback loop
    elm.Line().up(d.unit/4).at(op.vd)
    elm.Vdd().label('+15V')

    elm.Line().down(d.unit/4).at(op.vs)
    elm.Vss().label('−15V')

    # Input resistor
    elm.Resistor().at(op.in1).left().label('$R_{in}$\n10kΩ', loc='bot')
    elm.Dot(open=True).label('$v_{in}$', 'left')

    # Feedback resistor, routed high enough to pass above the +15V label
    elm.Dot().at(op.in1)
    elm.Line().up(d.unit*0.9).at(op.in1)
    elm.Resistor().tox(op.out).label('$R_f$\n100kΩ')
    elm.Line().toy(op.out).dot()

    # Non-inverting input to ground
    elm.Line().down(d.unit/4).at(op.in2)
    elm.Ground(lead=False)

    # Output
    elm.Line().right(d.unit/4).at(op.out).dot(open=True).label('$v_{out}$', 'right')
```

**Specifications**:
- Gain: Av = -Rf/Rin = -10 (20 dB)
- Input impedance: ~10kΩ
- Bandwidth: Limited by opamp (TL081: ~3 MHz GBW)

## Example 3: Differential Amplifier

Subtracts two input signals.

```python
import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing(file='diff_amp.svg') as d:
    d.config(fontsize=12)

    op = elm.Opamp(leads=True)

    # Non-inverting input network (R1 label below so it clears R3)
    elm.Dot().at(op.in2)
    elm.Resistor().at(op.in2).left().label('$R_1$\n10kΩ', loc='bot').dot(open=True).label('$V_1$', 'left')
    elm.Resistor().at(op.in2).down().label('$R_2$\n10kΩ', loc='bot', ofst=0.5)
    elm.Ground()

    # Inverting input network
    elm.Dot().at(op.in1)
    elm.Resistor().at(op.in1).left().label('$R_3$\n10kΩ').dot(open=True).label('$V_2$', 'left')

    # Feedback
    elm.Line().up(d.unit/2).at(op.in1)
    elm.Resistor().tox(op.out).label('$R_4$\n10kΩ')
    elm.Line().toy(op.out).dot()

    # Output
    elm.Line().right(d.unit/4).at(op.out).dot(open=True).label('$V_{out} = V_1 - V_2$', 'right')
```

**Output**: Vout = (R4/R3) × (V1 - V2) when R1=R2 and R3=R4

**Use cases**: Sensor signal conditioning, noise rejection, instrumentation amplifier front-end

## Example 4: Common Emitter Amplifier

Single-stage BJT amplifier with biasing network.

```python
import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing(file='ce_amplifier.svg') as d:
    d.config(fontsize=11)

    Q1 = elm.BjtNpn(circle=True).label('Q1\n2N3904')

    # Base node moved left so R1/R2 don't overlap the transistor body
    elm.Line().at(Q1.base).left(d.unit / 2)
    B = elm.Dot()

    # Voltage divider for base bias
    R1 = elm.Resistor().at(B.center).up().label('$R_1$\n47kΩ')
    elm.Resistor().at(B.center).down().label('$R_2$\n10kΩ')
    elm.Ground()

    # Collector: RC up to the same height as R1, joined by the +12V rail
    RC = elm.Resistor().at(Q1.collector).up().toy(R1.end).label('$R_C$\n2.2kΩ', loc='bot')
    elm.Line().at(R1.end).to(RC.end)
    elm.Dot().at(R1.end)
    elm.Vdd().at(RC.end).label('+12V')

    # Emitter: RE to ground with bypass CE in parallel
    elm.Line().at(Q1.emitter).down(d.unit / 4)
    E = elm.Dot()
    elm.Resistor().at(E.center).down().label('$R_E$\n1kΩ', loc='bot')
    elm.Ground()
    elm.Line().at(E.center).right(d.unit * 0.75)
    elm.Capacitor().down().label('$C_E$\n47µF', loc='bot')
    elm.Ground()

    # Coupling capacitors
    elm.Capacitor().at(B.center).left().label('$C_{in}$\n10µF')
    elm.Dot(open=True).label('$v_{in}$', 'left')
    elm.Line().at(Q1.collector).right(d.unit * 0.75)
    elm.Capacitor().right().label('$C_{out}$\n10µF')
    elm.Dot(open=True).label('$v_{out}$', 'right')
```

**Characteristics**:
- Voltage gain: Av ≈ -RC/RE ≈ -2.2 (bypassed)
- Input impedance: ~R1||R2||βRE ≈ 6kΩ
- Phase shift: 180° (inverting)

## Example 5: H-Bridge Motor Driver

Bidirectional DC motor control with 4 MOSFETs.

```python
import schemdraw
from schemdraw import elements as elm

W = 6  # distance between the two legs

with schemdraw.Drawing(file='h_bridge.svg') as d:
    d.config(unit=2.5, fontsize=11)

    # +12V rail
    elm.Line().at((0, 2)).right(W)
    elm.Vdd().at((W/2, 2)).label('+12V')
    elm.Dot().at((W/2, 2))

    # Left leg: Q1 (high side) over Q3 (low side), gates on the outside.
    # .right() before .anchor() keeps drain on top and source below.
    elm.Line().at((0, 2)).down(1)
    Q1 = elm.NFet().right().reverse().anchor('drain').at((0, 1)).label('Q1', loc='right')
    elm.Line().at(Q1.source).down(1)
    elm.Dot().label('A', loc='left')
    A = d.here
    elm.Line().down(1)
    Q3 = elm.NFet().right().reverse().anchor('drain').label('Q3', loc='right')
    elm.Line().at(Q3.source).down(1)

    # Right leg: Q2 over Q4, mirrored
    elm.Line().at((W, 2)).down(1)
    Q2 = elm.NFet().right().anchor('drain').at((W, 1)).label('Q2', loc='left')
    elm.Line().at(Q2.source).down(1)
    elm.Dot().label('B', loc='right')
    B = d.here
    elm.Line().down(1)
    Q4 = elm.NFet().right().anchor('drain').label('Q4', loc='left')
    elm.Line().at(Q4.source).down(1)

    # Ground rail
    y_gnd = Q3.source[1] - 1
    elm.Line().at((0, y_gnd)).to((W, y_gnd))
    elm.Dot().at((W/2, y_gnd))
    elm.Ground().at((W/2, y_gnd))

    # Motor between the two mid-points
    elm.Line().at(A).right(1.5)
    elm.Motor().right(W - 3).label('M', loc='top')
    elm.Line().tox(B)

    # Gate inputs
    elm.Line().at(Q1.gate).left(0.75).dot(open=True).label('IN1', 'left')
    elm.Line().at(Q3.gate).left(0.75).dot(open=True).label('IN3', 'left')
    elm.Line().at(Q2.gate).right(0.75).dot(open=True).label('IN2', 'right')
    elm.Line().at(Q4.gate).right(0.75).dot(open=True).label('IN4', 'right')
```

**Control logic**:
- Forward: Q1 + Q4 ON, Q2 + Q3 OFF
- Reverse: Q2 + Q3 ON, Q1 + Q4 OFF
- Brake: Q3 + Q4 ON (or Q1 + Q2 ON)
- Coast: All OFF

## Example 6: RC Phase Shift Oscillator

Generates sine wave using opamp and RC network.

```python
import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing(file='rc_oscillator.svg') as d:
    d.config(fontsize=11)

    # Opamp as inverting amplifier
    op = elm.Opamp(leads=True)
    elm.Line().at(op.in2).down(0.75)
    elm.Ground(lead=False)

    # CR network, built leftward from the inverting input.
    # R_in is the third R: its far end sits at virtual ground.
    elm.Dot().at(op.in1)
    elm.Resistor().at(op.in1).left().label('$R_{in}$\n10kΩ')
    elm.Capacitor().left().label('$C_3$\n10nF')
    elm.Dot()
    d.push()
    elm.Resistor().down().label('$R_2$\n10kΩ', loc='bot', ofst=0.5)
    elm.Ground()
    d.pop()
    elm.Capacitor().left().label('$C_2$\n10nF')
    elm.Dot()
    d.push()
    elm.Resistor().down().label('$R_1$\n10kΩ', loc='bot', ofst=0.5)
    elm.Ground()
    d.pop()
    elm.Capacitor().left().label('$C_1$\n10nF')
    start = d.here

    # Gain-setting feedback: Rf/Rin = 33 (≥ 29)
    elm.Line().at(op.in1).up(1.5)
    elm.Resistor().tox(op.out).label('$R_f$\n330kΩ')
    elm.Line().toy(op.out)

    # Output feeds the network back from the top
    elm.Dot().at(op.out)
    elm.Line().at(op.out).right(1)
    elm.Dot()
    out = d.here
    elm.Line().right(0.75).dot(open=True).label('Out', 'right')
    elm.Line().at(out).up(3.25)
    elm.Line().tox(start)
    elm.Line().toy(start)
```

**Oscillation frequency**: f = 1/(2πRC√6) ≈ 650 Hz

**Condition**: Rf/Rin ≥ 29 for sustained oscillation (here 330kΩ / 10kΩ = 33). R_in is the network's third R: the inverting input is a virtual ground, so it works as the last shunt resistor.

## Tips for Natural Language Processing

When user describes a circuit in natural language, parse it systematically:

### 1. Identify Components

- "resistor" → `elm.Resistor()`
- "10k resistor" → `elm.Resistor().label('10kΩ')`
- "100 microfarad capacitor" → `elm.Capacitor().label('100µF')`
- "NPN transistor" → `elm.BjtNpn()`
- "opamp" or "operational amplifier" → `elm.Opamp()`

### 2. Parse Connections

- "in series with" → place elements sequentially
- "in parallel with" → use `d.push()`/`d.pop()` branching
- "connected to ground" → element `.down()` then `elm.Ground()`
- "between X and Y" → use `.at()` and `.to()` methods

### 3. Interpret Topology

Common circuit keywords:
- "voltage divider" → two resistors with tap point (see patterns.md)
- "RC filter" → resistor and capacitor to ground
- "inverting amplifier" → opamp with feedback (see patterns.md)
- "LED driver" → transistor switch pattern (see patterns.md)
- "H-bridge" → 4 transistors in bridge configuration

### 4. Extract Values

Handle various formats:
- "10 kiloohms" → "10kΩ"
- "100uF" → "100µF"
- "0.1 microfarads" → "0.1µF"
- "1 millihenry" → "1mH"
- Scientific notation: "1e-6F" → "1µF"

### 5. Determine Layout

Default strategies:
- Left-to-right signal flow
- Power on top, ground on bottom
- ICs in center, passives around them
- Group related components together

### Example Parsing

**User**: "Draw an inverting amplifier with 10k input resistor and 100k feedback resistor"

**Parse**:
1. Identify: opamp, two resistors
2. Topology: inverting amplifier (pattern #3)
3. Values: Rin=10kΩ, Rf=100kΩ
4. Generate code using inverting amp pattern from patterns.md

**User**: "Show me an LED connected to 5V through a 330 ohm resistor"

**Parse**:
1. Identify: LED, resistor, power supply
2. Connection: series (power → resistor → LED → ground)
3. Values: 5V, 330Ω
4. Generate simple series circuit

## Using Context7 for More Examples

For circuits not shown here:

```
mcp__context7__get-library-docs(
  context7CompatibleLibraryID: "/cdelker/schemdraw",
  mode: "code",
  topic: "specific circuit type + example"
)
```

Examples:
- `topic: "741 opamp example circuit"`
- `topic: "rectifier circuit full wave"`
- `topic: "LC tank oscillator"`
- `topic: "Wheatstone bridge example"`
