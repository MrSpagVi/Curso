# Project: Curso Politica Dashboard Enhancements

## Architecture
- `dashboard.html`: The main single-page application that holds the JSON dataset `COURSE_DATA` and performs rendering, navigation, and progress tracking.
- `docs/`: Holds the markdown syllabus stages.
- `scratch/build_dashboard.py`: Script that parses stages, aligns syllabus metadata, generates JSON datasets, and builds the finalized `dashboard.html`.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: E2E Testing Infrastructure Verification | Run initial E2E test suite and verify test execution | none | DONE |
| 2 | M2: Curriculum Expansion, Stage Title Alignment & Legacy Cleanup | Fix title alignments (stages 18, 19, 40, 68, 69, 72, 73), update stage 33 citations, clean legacy "87" references, expand post-reading guides for Gramsci, Althusser, Agamben, Butler, Fanon, Mbembe. | M1 | IN_PROGRESS |
| 3 | M3: UI Track Selector, Path-Specific Welcome Dashboards & Segmented Local Storage | Add track selector dropdown, welcome pages per path (with statistics, objectives, tips), segmented localStorage, backup/restore. | M2 | PLANNED |
| 4 | M4: Interactive SVG Mindmap Path Overlay | Highlight active path nodes/lines in SVG mindmap, grey out inactive nodes, halo background protection. | M2 | PLANNED |
| 5 | M5: Socratic Phase Review Quizzes & Gemini API Integration | Socratic quizzes blocking phase completion, client-side Gemini API with localStorage key, offline fallback, emoji filter. | M2 | PLANNED |
| 6 | M6: Verification, Forensic Audit & Challenger Hardening | Run E2E test suite, run Forensic Auditor, and run Challenger stress tests. | M3, M4, M5 | PLANNED |

## Interface Contracts
### Track Selector ↔ Course Data
- Selector component sets active track in localStorage (`active-track`) and updates the state.
- Dynamic filtering checks if stage belongs to the active track.
- Simple Track (25 stages): 1, 2, 3, 5, 7, 8, 9, 11, 13, 15, 17, 23, 26, 30, 32, 34, 35, 41, 45, 48, 49, 53, 59, 66, 69
- Intermediate Track (60 stages): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 39, 40, 41, 43, 44, 45, 46, 48, 49, 51, 52, 53, 54, 56, 57, 58, 59, 60, 66, 67, 68, 69, 70, 71, 73, 78
- Advanced Track: All 103 stages.

### Socratic IA Assistant ↔ Active Stage
- Interactive Q&A chat widget reading the active stage's metadata (author, work, core concepts) and post-reading debates.
- Shortcut presets to trigger Socratic prompts.
- Offline static fallback matching active stage when API key is missing.
- Emoji-free output filter cleans all client-facing text.

### Debates, Críticas y Contrastes
- Structured academic sections appended to each stage's reading workspace.
- Contains: Debates & Discussion, Criticisms (opposing schools), Support & Rationale (logic of core arguments), and Socratic chat trigger.

## Code Layout
- `dashboard.html` - Single Page Application containing all UI, JSON database, and style sheets.
- `scratch/build_dashboard.py` - Script that parses stage files and generates `dashboard.html`.
- `tests/` - Folder containing the test runner and E2E tests.
