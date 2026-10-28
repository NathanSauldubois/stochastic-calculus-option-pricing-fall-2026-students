# Stochastic Calculus and Option Pricing - Fall 2026

Lecture slides, course notes, exercise sheets, synthesis notes, Python documentation and syllabi for the Fall 2026 course at NYU Tandon. PDF files and their LaTeX sources follow the same session structure as the instructor's course materials.

All materials in this repository can be viewed and downloaded without signing in to GitHub.

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
| 12 | [PDF](Seance%2012/Slides/Slides.pdf) | [PDF](Seance%2012/Notes/Notes.pdf) | [LaTeX](Seance%2012/) |
| 13 | [PDF](Seance%2013/Slides/Slides.pdf) | [PDF](Seance%2013/Notes/Notes.pdf) | [LaTeX](Seance%2013/) |
| 14 | [PDF](Seance%2014/Slides/Slides.pdf) | [PDF](Seance%2014/Notes/Notes.pdf) | [LaTeX](Seance%2014/) |

## Exercises and reference material

- [Complete exercise sheet](Exercises/Exercise%20Sheet/Exercises.pdf)
- [Exercise sources and session worksheets](Exercises/)
- [Synthesis notes](Synthesis/synthesis.pdf) and [LaTeX sources](Synthesis/)
- [Python documentation](Python/Python_doc.pdf) and [source](Python/Python_doc.tex)
- [Wednesday syllabus](Syllabus/Syllabus_6233_Wednesday.pdf)
- [Thursday syllabus](Syllabus/Syllabus_6233_Thursday.pdf)

Use the syllabus for your section for the course calendar and assessment arrangements.

## Scope

Homework, midterm and exam papers, grading records, resource archives, separate answer keys, instructor working documents and build files are excluded. Worked examples included in the lectures remain part of the course notes and slides.

## Building the LaTeX files

Use a TeX Live or MacTeX installation with `latexmk`. Compile from the directory containing the main `.tex` file so that relative figure and input paths resolve. For example:

```sh
cd "Seance 9/Slides"
latexmk -pdf -interaction=nonstopmode Slides.tex
```

The main exercise sheet is `Exercises/Exercise Sheet/Exercises.tex`; the synthesis is `Synthesis/synthesis.tex`. Figures used in session 9 are included with their source attribution.

## Maintainer notes

- Keep the session folders aligned with the instructor's released course materials.
- Review new files before extending the explicit publication list in `.gitignore`.
- Commit reviewed updates and publish them with `git push`.
