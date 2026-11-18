# Stochastic Calculus and Option Pricing - Fall 2026

Lecture slides, course notes, exercise sheets, synthesis notes, Python documentation and syllabi for the Fall 2026 course at NYU Tandon. PDF files and their LaTeX sources follow the same session structure as the instructor's course materials.

All materials in this repository can be viewed and downloaded without signing in to GitHub.

Updated November 18, 2026. All 14 slide decks are static handouts: questions,
answers and other slide content appear immediately, with no pauses or
progressive overlays. The LaTeX sources compile in this mode by default.

## Lectures

| Session | Slides | Course notes | Sources |
| --- | --- | --- | --- |
| 1 | [PDF](Seance%201/Slides/Slides_Lecture_1.pdf) | [PDF](Seance%201/Notes/Notes_Lecture_1.pdf) | [LaTeX](Seance%201/) |
| 2 | [PDF](Seance%202/Slides/Slides.pdf) | [PDF](Seance%202/Notes/Notes_Lecture_2.pdf) | [LaTeX](Seance%202/) |
| 3 | [PDF](Seance%203/Slides/Slides.pdf) | [PDF](Seance%203/Notes/Notes.pdf) | [LaTeX](Seance%203/) |
| 4 | [PDF](Seance%204/Slides/Slides.pdf) | [PDF](Seance%204/Notes/notes.pdf) | [LaTeX](Seance%204/) |
| 5 | [PDF](Seance%205/Slides/Slides.pdf) | [PDF](Seance%205/Notes/notes.pdf) | [LaTeX](Seance%205/) |
| 6 | [PDF](Seance%206/Slides/Slides.pdf) | [PDF](Seance%206/Notes/Notes.pdf) | [LaTeX](Seance%206/) |
| 7 | [PDF](Seance%207/Slides/Slides.pdf) | [PDF](Seance%207/Notes/Notes.pdf) | [LaTeX](Seance%207/) |
| 8 | [PDF](Seance%208/Slides/Slides.pdf) | [PDF](Seance%208/Notes/notes.pdf) | [LaTeX](Seance%208/) |
| 9 | [PDF](Seance%209/Slides/Slides.pdf) | [PDF](Seance%209/Notes/Notes.pdf) | [LaTeX](Seance%209/) |
| 10 | [PDF](Seance%2010/Slides/Slides.pdf) | [PDF](Seance%2010/Notes/Notes.pdf) | [LaTeX](Seance%2010/) |
| 11 | [PDF](Seance%2011/Slides/Slides.pdf) | [PDF](Seance%2011/Notes/Notes.pdf) | [LaTeX](Seance%2011/) |
| 12 | [PDF](Seance%2012/Slides/Slides.pdf) | — | [LaTeX](Seance%2012/) |
| 13 | [PDF](Seance%2013/Slides/Slides.pdf) | — | [LaTeX](Seance%2013/) |
| 14 | [PDF](Seance%2014/Slides/Slides.pdf) | — | [LaTeX](Seance%2014/) |

## End-of-semester plan

- Session 12: change of numeraire and fixed-income basics.
- Session 13: exotic option pricing, followed by correlation swaps and VIX futures.
- Session 14: review of Sessions 1–11 only; Sessions 12–13 are excluded.

See the [session plan and timings](PLAN_FIN_SEMESTRE.md) for details.
Sessions 12–14 use slides only; no separate course notes are provided.

## Exercises and reference material

- [Rapid fire — Lectures 1–11, 60 short questions (4 pages)](Exercises/03_Fire_Drill/Fire_Drill_Lectures_1_11.pdf)
- [Core exercise sheet — Lectures 1–11, 44 exercises](Exercises/01_Core/Exercises.pdf)
- [Optional further practice — Lectures 1–11, 36 problems](Exercises/02_Further_Practice/Further_Practice.pdf)
- [Exercise library and folder guide](Exercises/README.md)
- [Sources and worksheets by session](Exercises/04_By_Session/) · [In-class material](Exercises/05_In_Class/)
- [Essentials to master — Math and code, Lectures 1–11 (5 pages)](Synthesis/Essentials_Math_Code_1_11.pdf) and [LaTeX source](Synthesis/Essentials_Math_Code_1_11.tex)
- [Synthesis notes — Lectures 1–11](Synthesis/synthesis.pdf) and [LaTeX sources](Synthesis/)
- [Python documentation](Python/Python_doc.pdf) and [source](Python/Python_doc.tex)
- [Wednesday syllabus](Syllabus/Syllabus_6233_Wednesday.pdf)
- [Thursday syllabus](Syllabus/Syllabus_6233_Thursday.pdf)

Use the syllabus for your section for the course calendar and assessment arrangements.
The essentials sheet, rapid fire, synthesis and both exercise booklets cover Sessions 1–11 only. Material
introduced in Sessions 12–13 is excluded from this revision set.

## Scope

Homework, midterm and exam papers, grading records, resource archives, separate answer keys, instructor working documents and build files are excluded. Worked examples included in the lectures remain part of the course notes and slides.

## Building the LaTeX files

Use a TeX Live or MacTeX installation with `latexmk`. Compile from the directory containing the main `.tex` file so that relative figure and input paths resolve. For example:

```sh
cd "Seance 9/Slides"
latexmk -pdf -interaction=nonstopmode Slides.tex
```

The main exercise sheet is `Exercises/01_Core/Exercises.tex`; optional practice and the rapid fire have their own masters in `02_Further_Practice` and `03_Fire_Drill`. Shared weekly sources are in `Exercises/04_By_Session/`. The synthesis is `Synthesis/synthesis.tex`. Figures used in session 9 are included with their source attribution.

## Maintainer notes

- Keep the session folders aligned with the instructor's released course materials.
- Retain `handout` in every slide deck's `\documentclass` options and rebuild
  its PDF after changing the source. Preserve the student version of Lecture 4
  notes, which excludes the separate homework companion.
- Review new files before extending the explicit publication list in `.gitignore`.
- Commit reviewed updates and publish them with `git push`.
