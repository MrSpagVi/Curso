# E2E Test Infra: Curso Politica Dashboard

## Test Philosophy
- **Opaque-box, requirement-driven**: Tests interact with `dashboard.html` as an end-user would (clicking buttons, selecting options, filling inputs, and checking DOM output).
- **Zero-dependency, local execution**: Leverages Python standard libraries (`unittest`, `http.server`) and native Web APIs (iframe-based test runner inside `runner.html`) to bypass network constraints.
- **Headless Browser Execution**: Uses native Edge (`msedge.exe`) or Firefox (`firefox.exe`) in headless mode to run tests automatically via CLI.

## Test Architecture
1. `tests/runner.html`: Runs in the browser. It embeds `dashboard.html` inside an `<iframe>` under the same HTTP origin, allowing full scripting access to the dashboard DOM. It runs 74 E2E test cases, renders visual results, and sends a JSON report back via a POST request to `/api/results`.
2. `tests/test_server.py`: A local HTTP server that serves files from the project root and handles POST requests at `/api/results` to write results into `tests/results.json`.
3. `tests/run_e2e.py`: A Python script that orchestrates the execution:
   - Finds a free port.
   - Spawns the local test server in a background process.
   - Detects Microsoft Edge or Firefox on Windows.
   - Launches the browser in headless mode pointing to the runner page.
   - Polls for `tests/results.json` with a timeout.
   - Cleans up browser and server processes.
   - Prints results and exits with code `0` (all pass) or `1` (any fail).

## Test Case Inventory

### Tier 1: Feature Coverage (30 Tests)
#### Feature 1: Dynamic Multi-Path Study Engine
1. **F1-T1: Selector UI Visibility**: Verify track selector element `#track-selector` or `.track-selector-group` is visible.
2. **F1-T2: Simple Track Sidebar Filter**: Verify selecting "Simple Track" filters the sidebar list to 25 stages.
3. **F1-T3: Simple Track Stage Indices**: Verify the 25 visible sidebar stages match the exact indices: `1, 2, 3, 5, 7, 8, 9, 11, 13, 15, 17, 23, 26, 30, 32, 34, 35, 41, 45, 48, 49, 53, 59, 66, 69`.
4. **F1-T4: Intermediate Track Sidebar Filter**: Verify selecting "Intermediate Track" filters the sidebar list to 60 stages.
5. **F1-T5: Intermediate Track Stage Indices**: Verify the 60 visible sidebar stages match the exact Intermediate Track indices defined in `PROJECT.md`.
6. **F1-T6: Advanced Track Sidebar Filter**: Verify selecting "Advanced Track" displays all 103 stages.
7. **F1-T7: Global Progress Updates**: Verify total task count denominator adjusts dynamically when switching tracks.
8. **F1-T8: Zero Emoji Audit**: Verify the UI headers, buttons, and track selector options contain zero emojis.
9. **F1-T9: High Legibility Dark Mode Contrast**: Verify that in dark mode, stage links do not use low-contrast blue text.

#### Feature 2: Personal Development & Critical Application Layer
10. **F2-T10: Growth Section Presence**: Verify the "Crecimiento y Aplicación Práctica" section is appended to the workspace detail.
11. **F2-T11: Machiavelli Concept Linking**: Verify Machiavelli's stage connects *virtù* to practical growth.
12. **F2-T12: Hobbes Concept Linking**: Verify Hobbes's stage connects the sovereign to actionable growth.
13. **F2-T13: Rawls Concept Linking**: Verify Rawls's stage connects the veil of ignorance to decision-making under uncertainty.

#### Feature 3: Interactive Mindmap Path Overlay
14. **F3-T14: Mindmap Rendering on Landing**: Verify SVG mindmap is correctly rendered on the landing page.
15. **F3-T15: Simple Track Node Highlighting**: Verify SVG mindmap highlights nodes in the Simple track and de-emphasizes others.
16. **F3-T16: SVG Edge Highlighting**: Verify connection lines are highlighted when part of the active track.
17. **F3-T17: Inactive Node Greying Out**: Verify nodes not in the active track are visually greyed out/attenuated.
18. **F3-T18: Zoom Into Phase Wave Sequence**: Verify clicking a Phase node zooms in and displays detailed stage nodes without overlaps.
19. **F3-T19: Stage Connection Halo Protection**: Verify connection lines have a clean background halo to prevent overlaps with labels.

#### Feature 4: Socratic Self-Assessment Engine
20. **F4-T20: Socratic Widget Appended**: Verify the Socratic quiz widget is present for each of the 9 phases.
21. **F4-T21: Socratic Card Flip**: Verify clicking a Socratic recall card flips it (adds `.flipped` class).
22. **F4-T22: Block Phase Completion**: Verify phase completion is disabled before passing the quiz.
23. **F4-T23: Enable Phase Completion**: Verify passing the quiz enables the phase completion checkbox.

#### Feature 5: Local Storage Track Persistence
24. **F5-T24: Segmented localStorage Key Check**: Verify checking a task writes to track-segmented localStorage keys.
25. **F5-T25: Non-Conflict of Track Progress**: Verify progress in Simple track does not modify Advanced track progress.

#### New Requirements (Syllabus, Debates, IA Assistant)
26. **REQ1-T26: Expanded Syllabus Audit**: Verify the total stages in Advanced Track exceed 103 (indicating syllabus expansion) and track selector options exist.
27. **REQ2-T27: Debates Section Presence**: Verify the "Debates, Críticas y Contrastes" section is appended to the workspace detail for the loaded stage.
28. **REQ3-T28: Socratic IA Widget Presence**: Verify the `.socratic-ai-widget` or similar chat interface is visible in the reading panel.
29. **REQ3-T29: Socratic IA Chat Input**: Verify the chat interface has a text input and a submit button.
30. **REQ3-T30: Socratic IA Shortcuts**: Verify shortcut buttons (e.g., 'Explicar de forma simple', 'Buscar contradicciones lógicas', 'Comparar con otros autores') are present.

---

### Tier 2: Boundary & Corner Cases (28 Tests)
31. **BC-F1-1: Null Active Track Fallback**: Verify clear localStorage defaults to 'Advanced' track and 103+ stages.
32. **BC-F1-2: Rapid Track Toggle Stability**: Verify rapidly toggling tracks 5 times in 200ms throws zero errors.
33. **BC-F1-3: Sidebar Scroll Position Retention**: Verify scroll position remains bounded and stable after switching tracks.
34. **BC-F1-4: Phase Empty State**: Verify that phases with no stages in a track (e.g., Phase 8 in Simple Track) are hidden or show empty state.
35. **BC-F1-5: Extreme Width Layout**: Verify track selector header behaves normally at 320px screen width.
36. **BC-F2-6: Missing Growth Content Fallback**: Verify stages without custom growth content show default fallback text.
37. **BC-F2-7: Concept Link Navigation**: Verify clicking growth section links changes hash without full page reload.
38. **BC-F2-8: XSS Prevention**: Verify HTML tags inside growth content are escaped and do not execute scripts.
39. **BC-F3-9: SVG Bounding Box Scale**: Verify mindmap SVG does not clip or overflow at high resolutions (1920x1080).
40. **BC-F3-10: Locked Phase Node Zoom**: Verify clicking a greyed-out phase node in Simple Track does not trigger zoom.
41. **BC-F3-11: Halo Color Adaptation**: Verify background halos adapt when switching light/dark themes.
42. **BC-F3-12: High Node Count Wave Layout**: Verify zoomed phases with large node counts (e.g. Phase 3) space nodes >= 30px apart.
43. **BC-F4-13: Part-Completed Phase Saving**: Verify checking tasks works even if the Socratic quiz is not yet completed.
44. **BC-F4-14: Quiz Session Recovery**: Verify Socratic quiz state (partially answered questions) survives page reload.
45. **BC-F4-15: Quiz Fail State Actions**: Verify failing a quiz shows review hints and keeps completion disabled.
46. **BC-F4-16: Empty Quiz Phase Unlock**: Verify a phase without quiz questions is instantly unlockable.
47. **BC-F4-17: Rapid Card Flipping**: Verify rapid clicking of cards doesn't corrupt card layout.
48. **BC-F5-18: Corrupt Backup JSON Import**: Verify importing malformed JSON displays an error and does not touch localStorage.
49. **BC-F5-19: Empty LocalStorage Export**: Verify exporting with no progress returns `{}`.
50. **BC-F5-20: Missing Track Data Preservation**: Verify importing a backup with only Simple track data preserves Advanced track progress.
51. **BC-F5-21: Large Storage Size Processing**: Verify backup utility handles 500+ task keys.
52. **BC-F5-22: Modal Close via Escape Key**: Verify pressing Escape closes the Backup modal.
53. **BC-F5-23: Scoped LocalStorage Keys**: Verify all progress keys start with track prefixes.
54. **BC-F5-24: Reset Progress Cancellation**: Verify canceling reset progress prompt preserves localStorage.
55. **BC-F5-25: Track State Preservation on Theme Toggle**: Verify theme toggle does not reset selected track or stage view.
56. **BC-REQ1-1: Expanded Syllabus Filter Toggle**: Verify that track filters correctly exclude/include the new audited stages on toggling.
57. **BC-REQ2-2: Debates Empty Fallback**: Verify that special stages (e.g. tutorials, setup stages) display a clean fallback for debates.
58. **BC-REQ3-3: Socratic IA Character Limit**: Verify that sending an empty message or extremely long text (>1000 chars) is handled gracefully by the widget.

---

### Tier 3: Cross-Feature Combinations (8 Tests)
59. **CF-1: Track Filter ↔ Mindmap Highlight Sync**: Changing track selector updates mindmap highlights instantly.
60. **CF-2: Segmented Progress ↔ Global Progress Scale**: Checking tasks in Simple track updates progress bar scale relative to Simple total, not Advanced total.
61. **CF-3: Socratic Widget ↔ Track Active Stage Checker**: Phase quiz only requires completion of stages present in the active track.
62. **CF-4: Backup Import ↔ Active UI Sync**: Restoring backup immediately updates checks, progress rings, and mindmap.
63. **CF-5: Socratic Quiz Status ↔ Segmented Backup**: Quiz pass state is exported in backup JSON and restored correctly.
64. **CF-6: Theme Toggle ↔ SVG Path Overlay**: SVG path highlights are preserved after theme toggle.
65. **CF-7: Socratic IA Context ↔ Track Switch**: Verify Socratic IA Widget updates its suggestions/shortcuts context when track is toggled.
66. **CF-8: Debates Section ↔ Zettelkasten Integration**: Verify debates section references click-to-open Zettelkasten concept notes.

---

### Tier 4: Real-World Application Scenarios (8 Tests)
67. **RW-1: E2E Course Progress (Simple Track)**: Switch to Simple track, check all tasks, pass quizzes, mark all complete. Verify global progress reaches 100%.
68. **RW-2: Track Upgrade (Simple → Intermediate)**: Complete Simple track, upgrade to Intermediate. Verify progress drops to 42%, list expands, and new stages show "Not Started".
69. **RW-3: Study Session Recovery**: Start phase quiz, fill question 1, reload page. Verify input is preserved.
70. **RW-4: Local Workspace Backup Porting**: Generate backup on desktop viewport, clear localStorage, resize to mobile viewport, paste and restore. Verify state matches.
71. **RW-5: Multi-Track Alternate Progress Work**: Work on Simple and Advanced tracks in parallel. Verify progress is isolated yet preserved on toggling.
72. **RW-6: Socratic Failure, Review, and Re-attempt**: Fail quiz, click review links, re-attempt, pass quiz. Verify transition states.
73. **RW-7: Full Study Session with IA Q&A and Debates**: Select stage, click debate concept, open Socratic IA, click shortcut "Buscar contradicciones", submit follow-up message. Verify message logs.
74. **RW-8: Offline Chat History Persistence**: Verify Socratic IA chat history for each stage is persisted in localStorage and restored across reloads.
