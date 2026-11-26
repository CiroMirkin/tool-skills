# All-at-Once Build

The build path for circuits with fewer than 5 components when the user asked for the whole diagram in one go. It replaces Steps B–D of `SKILL.md`; Steps A, E and F stay the same.

1. **Generate complete code** - one schemdraw script implementing every connection from the Step A list.
2. **Execute** - run the script and save the SVG.
3. **Review** - render a screenshot and run the Visual Verification Checklist of `SKILL.md` against it. Write down every problem before touching the code, so the whole list gets fixed in one pass.
4. **Fix and re-render** - apply all fixes at once, take a fresh screenshot, and review again. Repeat until your checklist pass comes back clean.
5. **Show the user** - present the screenshot; the user's approval is the gate. Apply their changes and repeat from step 3.

Then continue with Step E (final verification) and Step F (deliver).
