---
name: tool:diagrama-hardware
description: "Generate professional circuit diagrams using schemdraw Python library. Creates vector graphics (SVG/PDF/PNG) from natural language descriptions. Components: resistors, capacitors, inductors, diodes, transistors, opamps, ICs, logic gates, etc. Use when: (1) User requests circuit diagrams or schematics, (2) User wants publication-quality output, (3) User needs SVG/PDF for documentation, (4) Complex circuits with ICs/opamps/digital logic, (5) User mentions schemdraw or wants alternative to ASCII circuits."
---

# Schemdraw Circuit Generator

Generate professional, publication-quality circuit diagrams using schemdraw Python library. Outputs to vector formats (SVG, PDF) or raster (PNG).

## Quick Start Workflow

Every diagram follows the same skeleton:

1. **Connection list** (Step A) - every connection written as a SPICE netlist (`circuito.cir`) with 1–3 expected value ranges, before any code. It is the spec.
2. **Build** - pick one path:
   - **Incremental** (default): add one component or connection per iteration, render, show the user, wait for approval, repeat. Steps B–D below.
   - **All at once**: only when the circuit has fewer than 5 components *and* the user asked for the whole diagram in one go. Follow [`references/all-at-once.md`](references/all-at-once.md) instead of Steps B–D.
3. **Final verification** (Step E) - two scripts first: the drawing matches the netlist, and the netlist simulates in range. Then the screenshot review; the user approves.
4. **Deliver** (Step F) - netlist, script results, SVG, Python code, screenshot.

**Never install anything without asking.** If `schemdraw`, `ngspice` or any other dependency is missing, tell the user what is missing and the command that would install it, and wait for their OK.

## Visual Verification Checklist (MANDATORY)

**Two reviewers, two roles.** You review each screenshot first against the checklist below and fix what you find. Then the user reviews it, and their approval is the gate. Your pass catches clear failures (a label on a symbol, a dangling line); the user catches the layout problems you tend to miss (cramped spacing, a connection that only looks ambiguous). Report what you checked and leave the "looks good" verdict to the user.

### The Verification Loop

1. **GENERATE SCREENSHOT**
2. **REVIEW IT** against the checklist below; fix what you find and re-render
3. **SHOW TO USER** and ask for feedback
4. **APPLY THE USER'S CHANGES**
5. **REPEAT** until the user approves

### Visual Verification Categories

#### 1. Connection Visibility Test

**"Technically connected" ≠ "Visually connected"**

For each connection in your connection list:

- ✅ Can you visually TRACE the line end-to-end?
- ✅ Are junction dots visible at split points?
- ❌ Are lines overlapping IC edges? (Human can't see the connection!)
- ❌ Are lines hidden behind component bodies?
- ❌ Are connection points ambiguous?

**Common failure**: a line that ends exactly on the IC box edge looks disconnected even though the code is correct.

**Fix**: Route with Manhattan segments so the last one reaches the pin across open space:

```python
elm.Line().at(junction).down(0.5)
elm.Line().left(SMALL_SPACING)  # Clear the IC edge
elm.Dot()
elm.Line().down(0.5)
elm.Dot()
elm.Line().right(SMALL_SPACING + 1.0)  # Visible approach to the pin
```

#### 2. Label Overlap Detection

**🚨 CRITICAL RULE: Labels must NEVER overlap component symbols**

**Common overlap zones:**

- **Labels on component symbols** - ❌ FORBIDDEN (e.g., "10kΩ" text on resistor zigzag)
- Adjacent components on same signal path (R1 ↔ R2)
- IC center label ↔ pin labels (IC name ↔ VOUT)
- Component labels ↔ value labels
- Labels ↔ junction dots or lines

**Visual test questions:**

- ❌ Is label text sitting ON TOP of component symbol? (resistor, capacitor, inductor)
- ❌ Are any characters touching between different labels?
- ❌ Is label text crowded or cramped?
- ✅ Can you clearly read each label independently?
- ✅ Can you see the complete component symbol without text obscuring it?

**Fix priority order:**

1. **First: Increase spacing** - Most effective, cleanest solution

   ```python
   HORIZONTAL_SPACING = 1.5  # Increase from 1.0
   VERTICAL_SPACING = 1.5    # Increase from 1.0
   SMALL_SPACING = 0.75      # Increase from 0.5
   ```

2. **Second: Adjust label position** - Change `loc` parameter

   ```python
   # R1/R2 overlap example:
   elm.Resistor().label('R1\n10kΩ', loc='top', ofst=0.2)  # Push up
   elm.Resistor().label('R2\n1kΩ', loc='left')  # Move to opposite side
   ```

3. **Third: Reduce font size** - Only if spacing isn't feasible

   ```python
   .label('U2\nLM2596S', fontsize=10)  # Reduce from 11
   ```

4. **Fourth: Add offset** - Fine-tune position

   ```python
   .label('IC', ofst=-0.3)  # Shift left by 0.3 units
   ```

#### 3. Line Overlap Detection

**🚨 CRITICAL RULE: Lines touching IC edges = Connection ambiguity**

**Problem areas:**

- **Lines touching/overlapping IC box edges** - ❌ FORBIDDEN ("Is this connected?" - impossible to tell!)
- Lines crossing component bodies
- Lines crossing other lines without junction
- Lines crossing ground symbols

**Fix rules:**

- Approach each IC pin with explicit segments: `.at(junction)` then a direction (`.right(1.0)`), ending on the pin lead
- Use Manhattan routing (horizontal → vertical → horizontal only)
- Add intermediate junction dots to clarify path
- Route around component bodies, not through them
- **Leave visible gap between IC edge and incoming lines**

**Example - IC connection with a visible gap:**

```python
elm.Line().at(junction).right(1.0)  # Stop before the IC edge
# IC connects from current position automatically
```

#### 4. Definition of "Complete"

A diagram is complete ONLY when:

- ✅ Code executes without errors
- ✅ SVG generates successfully
- ✅ `verificar_dibujo.py` passes: the drawing matches `circuito.cir`
- ✅ `simular.py` passes, or the user agreed to skip it (see Step E)
- ✅ **USER has visually reviewed screenshot and approved** (MOST IMPORTANT)
- ✅ **USER confirms all connections are traceable**
- ✅ **USER confirms no visual issues** (overlaps, spacing, clarity)
- ✅ Every item from connection list is verified in diagram

**🚨 CRITICAL: Never claim "complete" without explicit user approval of visual output!**

Your checklist pass comes first; the user's approval is what closes the diagram.

### Screenshot Generation for USER Review

**Purpose: Generate the screenshot you review first and then show the user.**

Use HTML wrapper + headless browser to create screenshots for user review. The `headless-browser` skill is an **external dependency** (installed from Takazudo/zudo-test-wisdom — not part of this repo). If it isn't installed, degrade gracefully with a warning instead of failing the whole workflow:

```bash
# Generate SVG first
python3 /tmp/circuit.py

# Create HTML wrapper
cat > /tmp/view_diagram.html << 'EOF'
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Check</title>
<style>
body{margin:20px;background:white;display:flex;justify-content:center;align-items:center;min-height:100vh;}
svg{border:2px solid #333;max-width:100%;max-height:90vh;}
</style>
</head><body>
[Paste SVG content here]
</body></html>
EOF

# Capture screenshot (headless-browser skill required; external: Takazudo/zudo-test-wisdom)
if [ -f "$HOME/.claude/skills/headless-browser/scripts/headless-check.js" ]; then
  node $HOME/.claude/skills/headless-browser/scripts/headless-check.js \
    --url file:///tmp/view_diagram.html \
    --screenshot viewport
else
  echo "headless-browser skill not installed (external: Takazudo/zudo-test-wisdom) — skipping screenshot check"
fi
```

When a screenshot was produced, review it against the Visual Verification Checklist, then show it to the user.

### Common IC Connection Patterns (Context7 Reference)

When working with ICs, query context7 for proper connection syntax:

```
topic: "IC integrated circuit pin connection"
topic: "wire routing shapes manhattan"
topic: "element positioning at anchor"
```

**Key IC patterns learned:**

- IC connects via **sequential flow** - current position flows to first left pin automatically
- Use `.at(ic.pinname)` to start FROM a specific pin
- Use `.at(junction)` BEFORE routing TO a pin to avoid edge overlap
- Pin names are anchors: `ic.VIN`, `ic.GND`, `ic.FB`, `ic.VOUT`

**Example of proper IC connection:**

```python
# Create junction BEFORE IC
elm.Dot()
pre_ic_junction = d.here

# IC connects automatically from current position (sequential flow)
ic = elm.Ic(pins=[...])

# Route from junction to IC pin explicitly
elm.Line().at(pre_ic_junction).down(1.0)
elm.Dot()
elm.Line().right(1.0)  # Now connects to IC.PIN visibly
```

## Using Context7 for Documentation

**CRITICAL**: Schemdraw has extensive features. When you need specific syntax, advanced features, or uncommon components, use context7:

```
mcp__context7__get-library-docs(
  context7CompatibleLibraryID: "/cdelker/schemdraw",
  mode: "code",
  topic: "your specific topic"
)
```

**When to use context7:**

- Uncommon components not in references/components.md
- Advanced features (custom elements, annotations, etc.)
- Specific IC pinout configurations
- Latest API changes or new features
- Troubleshooting unusual errors

**Examples:**

- `topic: "opamp operational amplifier circuits"`
- `topic: "transistor bjt npn pnp"`
- `topic: "wire routing shapes"`
- `topic: "seven segment display multiplexer"`

## Installation

Ask the user before installing anything.

```bash
pip install schemdraw          # drawing
sudo apt install ngspice       # simulation in Step E (scripts/simular.py)
```

**Dependencies**: numpy, pillow (for PNG export), matplotlib (optional backend)

## Core Concepts

### Drawing Context

All diagrams use context manager:

```python
import schemdraw
from schemdraw import elements as elm

with schemdraw.Drawing(file='output.svg') as d:
    elm.Resistor().label('1kΩ')
    elm.Capacitor().down().label('10µF')
```

### Element Chaining

Elements chain sequentially, each picking up where last ended:

```python
elm.Resistor().right().label('R1')  # Goes right
elm.Capacitor().down().label('C1')  # Goes down from R1's end
elm.Line().left()                    # Goes left from C1's end
```

### Directional Methods

- `.up()`, `.down()`, `.left()`, `.right()` - Cardinal directions
- `.theta(angle)` - Arbitrary angle in degrees
- Optional length: `.up(length=2)`

### Positioning

- `.at(position)` - Place at specific location or anchor
- `.to(position)` - Draw to endpoint
- `.toy(y)` / `.tox(x)` - Manhattan routing
- `.anchor(name)` - Set which part is positioned

### Anchors

Elements have named connection points:

- Two-terminal: `start`, `end`, `center`
- Transistors: `base`, `collector`, `emitter` (BJT) or `gate`, `drain`, `source` (FET)
- Opamps: `in1`, `in2`, `out`, `vd`, `vs`
- ICs: Custom pin names

### Labels

```python
elm.Resistor().label('R1')                   # Simple label
elm.Resistor().label('$R_1$')                # LaTeX math
elm.Resistor().label('1kΩ', loc='bottom')   # Position
elm.Capacitor().label(('−', '$V_o$', '+'))  # Multiple (polarity)
```

### Connections

- `elm.Dot()` - Junction (filled circle)
- `elm.Dot(open=True)` - Terminal (open circle)
- `elm.Line()` - Straight connection
- `elm.Wire('shape')` - Routed: `'-|'`, `'|-'`, `'N'`, `'Z'`

## Step-by-Step Workflow (Incremental Approach)

### Step A: Create Connection List

**CRITICAL**: Start with explicit connection list, not the diagram.

Write it as a SPICE netlist, `circuito.cir`, next to the circuit script. Use the same designators as the drawing labels (`R1`, `D1`…), name every node, and use `0` for ground. Show it to the user before drawing.

```spice
* LED con resistencia            <- line 1 is always the title, SPICE ignores it
V1 vcc 0 DC 5                    ; V: n+ n-
R1 vcc a 330                     ; R C L: two nodes, any order
D1 a 0 DLED                      ; D: anode cathode
.model DLED D(IS=1e-20 N=1.8 RS=5)
*? v(a) 1.8 2.2                  ; expected range: LED forward voltage
*? i(v1) -0.02 -0.005            ; LED current 5–20 mA (source current is negative)
.control
op
print v(a) i(v1)
.endc
.end
```

Rules:

- **Line types the checker reads:** `R C L` (C with `polar=True`: first node is +), `D` anode cathode, `V I` n+ n-, `Q` collector base emitter, `M J` drain gate source, and `*@ U1.PIN node` for ICs and opamps (`PIN` is the schemdraw anchor name: `VIN`, `in1`, `out`…).
- **Model-only lines** (`X E F G H B`, or any line containing `solo-sim`) are simulated but not looked for in the drawing. An opamp is drawn as `elm.Opamp` with `*@` lines, and simulated as `E1 out 0 inp inn 1e5 ; solo-sim`.
- **Expected ranges (`*?`)**: write 1–3 that prove the circuit does its job: LED current, divider output, amplifier gain, RC time constant (`meas tran t63 when v(out)=3.16 rise=1`). Each name must be printed by a `print` or `meas` in the `.control` block. Derive each range from the design intent, not from a first simulation run.
- **MOSFETs: add the body diode.** A generic `PMOS`/`NMOS` model has none, so a MOSFET with drain and source swapped still simulates fine. Add it as a model-only line: anode on the drain for a P-MOSFET (`DB1 drain source DBODY ; solo-sim`), anode on the source for an N-MOSFET (`DB1 source drain DBODY ; solo-sim`), with `.model DBODY D(IS=1e-12 N=1.2)`. Then a swapped MOSFET leaks through the diode and an "off" range catches it.
- **Parts without a SPICE model** (a microcontroller, a 555 without a vendor model): keep their pins as `*@` lines so the drawing is still checked, and tell the user the simulation can't cover that part.

This netlist is the specification. The drawing must match EVERY line.

### Step B: Incremental Build - Start with Foundation

**CRITICAL**: Build circuit incrementally, one component/connection at a time.

**Typical build order:**

1. Start with IC only (no connections)
2. Add power connections (VIN, ON pins to input rail)
3. Add ground connection
4. Add input decoupling capacitors
5. Add output stage (VOUT → switching node → L1 → output)
6. Add flyback diode and output capacitor
7. Add feedback network
8. Connect feedback to FB pin

**Example - First iteration (IC only):**

```python
import schemdraw
from schemdraw import elements as elm

# Black foreground with transparent background (default)
with schemdraw.Drawing(
    font='Arial',
    fontsize=11,
    color='black',
    transparent=True
) as d:
    d.config(unit=3)

    # Iteration 1: IC only
    ic = elm.Ic(
        pins=[
            elm.IcPin(name='GND', pin='3', side='left', slot='1/3'),
            elm.IcPin(name='ON', pin='5', side='left', slot='2/3'),
            elm.IcPin(name='VIN', pin='1', side='left', slot='3/3'),
            elm.IcPin(name='FB', pin='4', side='right', slot='1/2'),
            elm.IcPin(name='VOUT', pin='2', side='right', slot='2/2'),
        ],
        edgepadW=2.5,
        edgepadH=0.8,
        pinspacing=1.0,
        leadlen=1.0
    ).label('U2\nLM2596S', loc='center', fontsize=10)

    d.save('/tmp/buck_converter.svg')
```

### Step C: Execute and Verify

After EACH iteration:

1. **Run the script:**

   ```bash
   python3 /tmp/circuit_generator.py
   ```

2. **Generate screenshot** (requires the external `headless-browser` skill — Takazudo/zudo-test-wisdom; degrades with a warning if absent):

   ```bash
   cat > /tmp/view.html << 'EOF'
   <!DOCTYPE html>
   <html><head><meta charset="UTF-8"><title>Circuit Check</title>
   <style>
   body{margin:20px;background:white;display:flex;justify-content:center;align-items:center;min-height:100vh;}
   svg{border:2px solid #333;max-width:100%;max-height:90vh;}
   </style>
   </head><body>
   EOF
   cat /tmp/buck_converter.svg >> /tmp/view.html
   echo "</body></html>" >> /tmp/view.html
   if [ -f "$HOME/.claude/skills/headless-browser/scripts/headless-check.js" ]; then
     node $HOME/.claude/skills/headless-browser/scripts/headless-check.js \
       --url file:///tmp/view.html --screenshot viewport
   else
     echo "headless-browser skill not installed (external: Takazudo/zudo-test-wisdom) — skipping screenshot check"
   fi
   ```

3. **Show user the screenshot**

4. **Get user confirmation:** "Looks good, add next component"

5. **Update code for next iteration** (e.g., add GND connection)

6. **REPEAT** steps C1-C5 until circuit complete

### Step D: Conversational Build Loop

**User guides the process:**

- "Add GND connection next"
- "Connect the input rail"
- "Shorten that line by half"
- "Move the label to the right side"

**You respond with:**

- Code update for requested change
- Execute script
- Generate screenshot
- Show result
- Wait for next instruction

**Benefits:**

- User can correct spacing/positioning immediately
- Catches label overlaps before they compound
- Easy to adjust layout decisions in real-time
- No need to untangle complex multi-component issues

### Step E: Final Verification

Once all components added and user confirms diagram looks complete, run the two checks **before** the final screenshot. The scripts are in `scripts/` inside this skill's base directory.

1. **Drawing matches the netlist.** Keep each component in a variable and end the circuit script with:

   ```python
   import sys; sys.path.insert(0, '<skill base dir>/scripts')
   from verificar_dibujo import verificar
   verificar(d, {V1: 'V1', R1: 'R1', D1: 'D1', U1: 'U1', vdd: '=vcc'}, 'circuito.cir')
   ```

   The dict maps each drawn component to its netlist designator; supply symbols (`Vdd`, `Vss`) map to `'=node'`, grounds need no entry. Decorative elements (an antenna, a cable drawn as a picture) map to `None` and are left out of the check; a component missing from the dict is an error. Block diagrams with no SPICE parts are checked the same way, with only `*@` lines, and skip `simular.py`. It rebuilds the nets from the anchor positions (T-junctions on a long ground line included) and exits with code 1 on a pin in the wrong node, a pin cut off from its node, a diode or source drawn backwards (`.reverse()` included), a component missing on either side, or a wire end that touches nothing. Fix the drawing, not the netlist, unless the netlist is the one that's wrong.
2. **Netlist works electrically.** `python3 scripts/simular.py circuito.cir` runs `ngspice -b` and exits with code 1 if ngspice reports anything suspicious (singular matrix, floating node, failed convergence), if a `*?` value is missing, or if one is out of range. ngspice exits with 0 even for a floating node; the script catches what the exit code misses. If `ngspice` is not installed, ask the user before installing it; if they decline, say the circuit was only checked structurally.
3. **Visual check:** Generate final screenshot and review it with the Visual Verification Checklist. The scripts already proved the connections; the screenshot is for what only shows visually (labels, spacing, clarity).
4. **Component verification:** Check all values, labels, pin numbers against the netlist
5. **User approval:** Get final confirmation

What the checks don't cover: whatever has no `*?` range, parts without a model, power ratings, and whether the circuit is the right one for the job. Say so when it applies.

### Step F: Deliver

Provide to user:

1. **Netlist** (`circuito.cir`, from Step A)
2. **Check results** (output of both scripts, or which one was skipped and why)
3. **Final SVG diagram** (verified version)
4. **Python code** (for reproducibility)
5. **Screenshot** (for documentation)

## Common Patterns

See `references/patterns.md` for copy-paste patterns:

- Voltage divider
- RC filter (low-pass, high-pass)
- Inverting/non-inverting opamp
- Transistor switch
- LED driver
- Buck converter
- Comparator
- And more...

## Reference Documentation

### components.md

Complete component library reference with syntax for all elements:

- Passive: Resistors, capacitors, inductors
- Semiconductors: Diodes, transistors (BJT/FET)
- Sources: Voltage, current, AC, batteries
- ICs: Opamps, logic gates, specialized ICs
- Power/Ground: Various ground and supply symbols
- Connections: Dots, lines, wires

### patterns.md

Copy-paste code for common circuits:

- Simple circuits (voltage divider, RC filter, LED)
- Opamp configurations (inverting, non-inverting, buffer, comparator)
- Transistor circuits (switch, amplifier)
- Advanced circuits (H-bridge, oscillators)

### best-practices.md

Guidelines for professional diagrams:

- Layout strategies
- Labeling conventions
- Connection techniques
- Readability tips
- Code organization
- Common mistakes to avoid

### examples.md

Complete working examples:

- 555 timer LED blinker
- Inverting opamp with power
- Differential amplifier
- Common emitter amplifier
- H-bridge motor driver
- RC oscillator
- Natural language parsing tips

### troubleshooting.md

Solutions to common problems:

- Installation and import issues
- Layout and positioning problems
- Label issues (Unicode, LaTeX)
- Connection problems
- Orientation issues
- Output problems
- Advanced issues

## Best Practices (Learned from Real Usage)

### 1. Consistent Label Positioning for Vertical Components

**Problem:** Labels on vertical components (resistors, capacitors going up/down) need consistent positioning to avoid overlaps and maintain professional appearance.

**Solution:** Use `loc='bot', ofst=0.5` pattern for all vertical components:

```python
# For components going upward
elm.Capacitor().up(2.0).label('C3\n470µF\n25V', loc='bot', ofst=0.5)
elm.Ground().flip()  # Flipped ground at top

# For components going downward
elm.Resistor().down().label('R1\n10kΩ', loc='bot', ofst=0.5)
elm.Resistor().down().label('R2\n1kΩ', loc='bot', ofst=0.5)
elm.Ground()  # Normal ground at bottom
```

**Why this works:** `loc='bot'` anchors label at component's bottom reference point, `ofst=0.5` shifts it right, positioning label cleanly on the right side of the component body without overlapping the symbol or connection lines.

### 2. IC Edge Padding for Label Clearance

**Problem:** IC center label (e.g., "U2 LM2596S") overlaps with pin labels on the right side.

**Solution:** Use adequate `edgepadW` parameter instead of label offsets:

```python
ic = elm.Ic(
    pins=[...],
    edgepadW=2.5,  # Wider box prevents label overlap
    edgepadH=0.8,
    pinspacing=1.0,
    leadlen=1.0
).label('U2\nLM2596S', loc='center', fontsize=10)
```

**Why this works:** Widening the IC box is cleaner than using label offsets. Typical values: `edgepadW=2.5` for ICs with 5+ pins.

### 3. Precise Junction Positioning

**Problem:** Need junction at exact midpoint for symmetrical connections.

**Solution:** Calculate position mathematically:

```python
# For horizontal rail between two pins
junction_y = (ic.VIN[1] + ic.ON[1]) / 2

# Build entire rail at calculated height
elm.Dot(open=True).at((x_position, junction_y)).label('+15V', loc='left')
elm.Line().right(2.0)
elm.Dot()
# ... all elements at same Y coordinate
```

**Why this works:** Calculating exact coordinates ensures straight lines and symmetrical layout. No diagonal connections or misaligned junctions.

### 4. Proper Push/Pop Stack Management

**Problem:** Multiple branches require careful stack management to return to correct positions.

**Solution:** Track push/pop pairs systematically:

```python
elm.Dot()
junction1 = d.here
d.push()  # Save junction1

# Branch 1
elm.Line().right(1.0)
elm.Dot()
junction2 = d.here
d.push()  # Save junction2

# Branch 2
elm.Line().right(1.0)
elm.Dot(open=True)

# Return to junction2
d.pop()  # Now at junction2

# Continue from junction2
elm.Line().down(0.5)
elm.Resistor()...

# Return to junction1
d.pop()  # Now at junction1
```

**Rule:** Every `d.push()` must have a matching `d.pop()`. Stack structure: LIFO (Last In, First Out).

### 5. Ground Symbol Orientation

**Problem:** Ground symbols appear upside-down when components go upward.

**Solution:** Use `.flip()` for upward-facing components:

```python
# Component going UP - flip ground
elm.Capacitor().up(2.0)
elm.Ground().flip()  # Ground symbol at top, points down

# Component going DOWN - normal ground
elm.Resistor().down()
elm.Ground()  # Ground symbol at bottom, points down
```

**Rule:** Ground always "points down" toward earth. Flip when it's physically above the component.

### 6. User Correction Responsiveness

**Problem:** User says "NO!" or expresses frustration - you misunderstood the request.

**Solution:**

1. **STOP immediately** - Drop the current approach
2. **Re-read user's EXACT words** - What did they literally say?
3. **Use exact parameters specified** - "right side" means `loc='right'`
4. **Show result immediately** - Generate screenshot and let the user judge it
5. **Wait for confirmation** - Let user verify before proceeding


### 7. Spacing Adjustments

**Problem:** User requests specific spacing changes during build.

**Solution:** Be responsive to spacing requests:

```python
# User: "halve the line there"
elm.Line().right(1.0)  # Changed from 2.0

# User: "change distance 1 -> 0.5 for each line"
elm.Line().down(0.5)  # Changed from 1.0
elm.Resistor()...
elm.Line().down(0.5)  # All spacing changed consistently
```

**Why this matters:** Small spacing adjustments (0.5 vs 1.0) significantly impact readability and label overlap prevention.

## Quick Tips

1. **Black foreground with transparent background** - Always use `font='Arial', color='black', transparent=True` for web documentation
2. **Start simple** - Use patterns from `patterns.md` as starting point
3. **Query context7** - For components/features not in references
4. **Save references** - Assign elements to variables: `Q1 = elm.BjtNpn()`
5. **Use dots** - Always at T-junctions, open dots for terminals
6. **Check anchors** - Use correct anchor names for element type
7. **Manhattan routing** - Use `.toy()` and `.tox()` for clean lines
8. **Increase spacing** - `d.config(unit=3)` if too cramped
9. **SVG format** - Best for documentation (vector, scalable)
10. **Consistent labels** - Use `loc='bot', ofst=0.5` for vertical components
11. **Listen carefully** - When user corrects you, use their EXACT words

## Output Formats

```python
# SVG (recommended - vector, scalable)
with schemdraw.Drawing(
    file='circuit.svg',
    font='Arial',
    fontsize=11,
    color='black',
    transparent=True
) as d:
    d.config(unit=3)
    # ... components ...

# PNG (raster, for compatibility)
# Note: Generate SVG first, then save as PNG
d.save('circuit.png', dpi=300, transparent=True)

# PDF (for print)
with schemdraw.Drawing(
    file='circuit.pdf',
    font='Arial',
    fontsize=11,
    color='black',
    transparent=True
) as d:
    d.config(unit=3)
    # ... components ...
```

## Black Foreground with Transparent Background (Default)

**All diagrams should use black foreground with transparent background by default:**

```python
with schemdraw.Drawing(
    font='Arial',         # Sans-serif font
    fontsize=11,
    color='black',        # Black foreground
    transparent=True      # Transparent background
) as d:
    d.config(unit=3)
    # ... components ...
```

**Why transparent background with black foreground:**

- Allows HTML container background to show through (e.g., custom background colors)
- Black lines and text are visible on light container backgrounds
- Works seamlessly with web-based documentation (Docusaurus, etc.)
- Professional appearance with clean contrast
- Integrates with any light-themed documentation

**Solid background (if specifically requested):**

```python
# Dark theme with solid black background and white foreground
with schemdraw.Drawing(
    font='Arial',
    fontsize=11,
    color='white',
    bgcolor='black'
) as d:
    # ... components ...

# Light theme with solid white background and black foreground
with schemdraw.Drawing(
    font='Arial',
    fontsize=11,
    color='black',
    bgcolor='white'
) as d:
    # ... components ...
```

## Example: Simple Voltage Divider

```python
import schemdraw
from schemdraw import elements as elm

# Black foreground with transparent background (default)
with schemdraw.Drawing(
    file='voltage_divider.svg',
    font='Arial',
    fontsize=11,
    color='black',
    transparent=True
) as d:
    elm.SourceV().label('12V')
    elm.Line().right(d.unit/2)
    elm.Resistor().down().label('R1\n10kΩ')
    elm.Dot()
    d.push()
    elm.Line().right(d.unit/2).dot(open=True).label('Vout\n(6V)', 'right')
    d.pop()
    elm.Resistor().down().label('R2\n10kΩ')
    elm.Ground()
```

## When to Use This Skill

- User requests circuit diagrams or schematics
- Publication-quality output needed
- Vector graphics (SVG/PDF) for documentation
- Complex circuits with ICs, opamps, logic
- Alternative to ASCII art diagrams
- Technical papers or presentations

## When NOT to Use

- User specifically wants ASCII art (use ascii-circuit-diagram-creator instead)
- Quick sketches where quality doesn't matter
- No Python environment available
