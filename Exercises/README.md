# Exercises — Lectures 1–11

| Collection | Use | PDF | LaTeX |
| --- | --- | --- | --- |
| `01_Core` | Weekly practice: 44 exercises, four per lecture | [Core exercises](01_Core/Exercises.pdf) | [Source](01_Core/Exercises.tex) |
| `02_Further_Practice` | Additional practice: 36 optional problems | [Further practice](02_Further_Practice/Further_Practice.pdf) | [Source](02_Further_Practice/Further_Practice.tex) |
| `03_Fire_Drill` | Quick self-check: 60 short questions in six sections | [Rapid fire](03_Fire_Drill/Fire_Drill_Lectures_1_11.pdf) | [Source](03_Fire_Drill/Fire_Drill_Lectures_1_11.tex) |

[04_By_Session](04_By_Session/) groups the weekly sources by lecture, along
with the standalone sheets already provided for Lectures 4–6 and 9–11.
[05_In_Class](05_In_Class/) contains the in-class material.

For a concise formula and code checklist, use the
[five-page essentials sheet](../Synthesis/Essentials_Math_Code_1_11.pdf).
The revision materials cover Lectures 1–11.

To build a collection, compile its master from its own directory:

```sh
cd 01_Core
latexmk -pdf -interaction=nonstopmode -halt-on-error Exercises.tex
```

The `Week_N_Exercises.tex` files in `04_By_Session` are shared fragments
used by the core and optional masters. Compile a master or an available
standalone `Week_N_Exercise_Sheet.tex`.
