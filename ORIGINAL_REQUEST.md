# Original User Request

## Initial Request — 2026-06-04T21:26:03Z

An advanced multi-path academic and personal development course system designed to explore political theory and literature at three levels of depth (Simple, Intermediate, and Advanced) with personalized learning paths, active reading tracking, and integrations.

Working directory: c:\Users\vicen\Documents\Libros Politica - Copy
Integrity mode: development

## Requirements

### R1. Dynamic Multi-Path Study Engine
Implement a client-side track selector (Simple, Intermediate, and Advanced) in `dashboard.html`. 
- **Simple Track**: Filters the syllabus to only 25 core stages focusing on foundational texts and introductory concepts.
- **Intermediate Track**: Filters the syllabus to 60 stages focusing on the standard canon.
- **Advanced Track**: Includes the complete set of 103 stages.
When a track is active, the sidebar list, global progress tracker, and phase completions must dynamically adjust to only show and count the stages in the selected track.

### R2. Personal Development & Critical Application Layer
For every stage, enhance the rendered workspace content to append a "Crecimiento y Aplicación Práctica" section. This section must link the theoretical concepts (e.g., Machiavelli's *virtù*, Hobbes's sovereign, Rawls's veil of ignorance) to actionable personal growth habits, cognitive tools, active recall, or mental models (e.g., identifying logical fallacies, Zettelkasten note links, decision-making under uncertainty).

### R3. Interactive Mindmap Path Overlay
Update the interactive SVG mindmap to support visual path overlays. Toggling between tracks must highlight the active path's nodes and connection lines using distinct colored overlays, while greying out or hiding stages that are not part of the active track.

### R4. Socratic Self-Assessment Engine
Design and embed a client-side interactive widget (e.g., active recall cards, socratic review prompts, or quizzes) for each of the 9 phases. The widget tests the user's conceptual comprehension of the phase's readings before they can mark the phase as completed.

### R5. Local Storage Track Persistence
Maintain progress tracking in `localStorage` segmented by track, ensuring that progress inside the Simple track is saved correctly and doesn't conflict with progress in the Advanced track. The Backup & Restore utility must support exporting/importing all tracks.

## Acceptance Criteria

### Interface & Navigation
- [ ] A track selector dropdown or button group is visible in the top header.
- [ ] Selecting a track filters the sidebar stages instantly without page reload.
- [ ] All lists and links are styled with high legibility (no low-contrast dark blue links in dark mode).
- [ ] The dashboard has zero emojis in any buttons, headers, or widgets.

### Mindmap & Connections
- [ ] The SVG mindmap highlights nodes belonging to the selected track and greys out inactive nodes.
- [ ] Zooming into a phase shows the WAVE sequence of stage nodes with no overlaps.
- [ ] Conceptual connection lines have a clean background halo and do not overlap text labels.

### Interactive Widgets
- [ ] The Socratic review cards are interactive (e.g. click to flip, self-grade, or input answers).
- [ ] The Zettelkasten Sandbox and Luhmann cabinets operate correctly without visual bugs.

### Robustness & Performance
- [ ] There are zero runtime JavaScript errors in the browser console.
- [ ] Switching themes (dark/light) preserves the selected track and active page view.

## Follow-up — 2026-06-04T21:32:39Z

Hola. El usuario ha solicitado ampliar los requisitos del proyecto curso_multiruta de forma inmediata. Debemos incorporar las siguientes especificaciones al plan de desarrollo:

1. **Syllabus Expandido e Investigación**: Realizar una auditoría del syllabus para expandir la lista de autores y obras.
2. **Debates y Contrastes**: Para cada una de las etapas, incorporar una sección específica titulada 'Debates, Críticas y Contrastes' que exponga los contraargumentos históricos y las posturas de escuelas de pensamiento opuestas.
3. **Asistente de IA Socrático**: Diseñar e integrar un widget interactivo de Asistente de IA socrático en el panel de lectura. El widget debe simular o permitir preguntas y respuestas (Q&A) de forma inteligente en base a la etapa activa, con accesos directos (ej: 'Explicar de forma simple', 'Buscar contradicciones lógicas', 'Comparar con otros autores') y soporte para búsquedas.

Por favor, actualiza tu plan en `PROJECT.md`, incorpora estas especificaciones en tus tareas de desarrollo activo y pruebas de integración, y adáptalas en tus milestones.


## Follow-up — 2026-06-05T10:30:01Z

An advanced multi-path academic and personal development course system designed to explore political theory and literature at three levels of depth (Simple, Intermediate, and Advanced) with personalized learning paths, active reading tracking, welcome landing pages, deep post-reading guides, and integrations.

Working directory: c:\Users\vicen\Documents\Libros Politica - Copy
Integrity mode: development

## Requirements

### R1. Dynamic Multi-Path Study Engine & Welcome Dashboards
- Implement a client-side track selector (Simple, Intermediate, and Advanced) in `dashboard.html`.
- When a track is active, the sidebar list, global progress tracker, and phase completions must dynamically adjust to only show and count the stages in the selected track.
- **Path-Specific Welcome Pages**: When no stage is selected, render a welcome dashboard tailored to the active path. It must explain the pedagogical rationale for that path, how it differs from the others, learning objectives, and tips for study.

### R2. Deep Academic Post-Reading Study Guides (Every Stage)
- Replace any generic placeholder text at the end of each stage's reading content with a structured academic post-reading card.
- For every stage, provide a detailed breakdown covering:
  - **Debates & Discussion Topics**: The most discussed issues and conflicts surrounding the text.
  - **Criticisms**: Major counter-arguments from other schools of thought.
  - **Support & Rationale**: The key supporting arguments and how the author logically arrived at those conclusions.
  - **Custom Socratic AI Prompt Button**: A recommended prompt for the user, with a clickable button that automatically sets the chatbot's system context and starts a conversation where the AI guides the user via questioning.

### R3. International Master's Curriculum Expansion
- Research and expand the advanced syllabus to include a broader, richer range of authors and works (such as Gramsci, Althusser, Agamben, Butler, Fanon, Mbembe, etc.), elevating the Advanced path to the standard of an international political philosophy master's program.
- Fully populate stage details, including concepts, tasks, deep post-reading study guides, and Socratic chatbot configs.

### R4. Interactive Mindmap Path Overlay
- Update the interactive SVG mindmap to support visual path overlays. Toggling between tracks must highlight the active path's nodes and connection lines using distinct colored overlays, while greying out or hiding stages that are not part of the active track.

### R5. Socratic Self-Assessment Engine
- Quizzes/assessments for each of the 9 phases. Conceptual comprehension must be tested before marking a phase as completed.

### R6. Local Storage Track Persistence & Chat Duality
- Segmented localStorage progress tracking by track.
- Client-side Google Gemini API integration with local storage key and offline fallback, emoji-free output filter.

## Acceptance Criteria

### Interface & Navigation
- [ ] A track selector dropdown or button group is visible in the top header.
- [ ] Each track has its own welcome/landing dashboard that renders in the central panel when no stage is selected, describing its objectives and differences.
- [ ] Selecting a track filters the sidebar stages instantly.
- [ ] All lists, links, and text labels are styled with high legibility (no low-contrast colors).
- [ ] The dashboard has zero emojis in any buttons, headers, or widgets.

### Syllabus & Post-Reading Contents
- [ ] The syllabus is expanded with new key authors and works to match a master's level political philosophy curriculum.
- [ ] Every stage contains a detailed, structured academic post-reading section (Debates, Criticisms, Support/Rationale, and Custom Socratic Prompt).

### Mindmap & Connections
- [ ] The SVG mindmap highlights nodes belonging to the selected track and greys out inactive nodes.
- [ ] Zooming into a phase shows the WAVE sequence of stage nodes with no overlaps.
- [ ] Conceptual connection lines have a clean background halo and do not overlap text labels.

### Interactive Widgets & AI
- [ ] The Socratic review cards are interactive (e.g., click to flip, self-grade, or input answers) and block phase completion until passed.
- [ ] The Zettelkasten Sandbox operates correctly.
- [ ] The AI chatbot widget integrates with the Gemini API using a locally-stored API key (or falls back to offline engine) and filters all emojis from the assistant's output.
- [ ] A clickable button is present at the end of each stage's guide to copy and launch the Socratic chat session with the customized prompt context.

### Robustness & Performance
- [ ] All E2E tests pass successfully.

## Follow-up — 2026-06-05T15:38:49Z

An advanced multi-path academic and personal development course system designed to explore political theory and literature at three levels of depth (Simple, Intermediate, and Advanced) with personalized learning paths, active reading tracking, welcome landing pages, deep post-reading guides, and integrations.

Working directory: c:\Users\vicen\Documents\Libros Politica - Copy
Integrity mode: development

## Requirements

### R1. Dynamic Multi-Path Study Engine & Welcome Dashboards
- Implement a client-side track selector (Simple, Intermediate, and Advanced) in `dashboard.html`.
- When a track is active, the sidebar list, global progress tracker, and phase completions must dynamically adjust to only show and count the stages in the selected track.
- **Path-Specific Welcome Pages**: When no stage is selected, render a welcome dashboard tailored to the active path. It must explain the pedagogical rationale for that path, how it differs from the others, learning objectives, and tips for study.

### R2. Deep Academic Post-Reading Study Guides (Every Stage)
- Replace any generic placeholder text at the end of each stage's reading content with a structured academic post-reading card.
- For every stage, provide a detailed breakdown covering:
  - **Debates & Discussion Topics**: The most discussed issues and conflicts surrounding the text.
  - **Criticisms**: Major counter-arguments from other schools of thought.
  - **Support & Rationale**: The key supporting arguments and how the author logically arrived at those conclusions.
  - **Custom Socratic AI Prompt Button**: A recommended prompt for the user, with a clickable button that automatically sets the chatbot's system context and starts a conversation where the AI guides the user via questioning.

### R3. International Master's Curriculum Expansion
- Research and expand the advanced syllabus to include a broader, richer range of authors and works (such as Gramsci, Althusser, Agamben, Butler, Fanon, Mbembe, etc.), elevating the Advanced path to the standard of an international political philosophy master's program.
- Fully populate stage details, including concepts, tasks, deep post-reading study guides, and Socratic chatbot configs.

### R4. Interactive Mindmap Path Overlay
- Update the interactive SVG mindmap to support visual path overlays. Toggling between tracks must highlight the active path's nodes and connection lines using distinct colored overlays, while greying out or hiding stages that are not part of the active track.

### R5. Socratic Self-Assessment Engine
- Quizzes/assessments for each of the 9 phases. Conceptual comprehension must be tested before marking a phase as completed.

### R6. Local Storage Track Persistence & Chat Duality
- Segmented localStorage progress tracking by track.
- Client-side Google Gemini API integration with local storage key and offline fallback, emoji-free output filter.

## Acceptance Criteria

### Interface & Navigation
- [ ] A track selector dropdown or button group is visible in the top header.
- [ ] Each track has its own welcome/landing dashboard that renders in the central panel when no stage is selected, describing its objectives and differences.
- [ ] Selecting a track filters the sidebar stages instantly.
- [ ] All lists, links, and text labels are styled with high legibility (no low-contrast colors).
- [ ] The dashboard has zero emojis in any buttons, headers, or widgets.

### Syllabus & Post-Reading Contents
- [ ] The syllabus is expanded with new key authors and works to match a master's level political philosophy curriculum.
- [ ] Every stage contains a detailed, structured academic post-reading section (Debates, Criticisms, Support/Rationale, and Custom Socratic Prompt).

### Mindmap & Connections
- [ ] The SVG mindmap highlights nodes belonging to the selected track and greys out inactive nodes.
- [ ] Zooming into a phase shows the WAVE sequence of stage nodes with no overlaps.
- [ ] Conceptual connection lines have a clean background halo and do not overlap text labels.

### Interactive Widgets & AI
- [ ] The Socratic review cards are interactive (e.g., click to flip, self-grade, or input answers) and block phase completion until passed.
- [ ] The Zettelkasten Sandbox operates correctly.
- [ ] The AI chatbot widget integrates with the Gemini API using a locally-stored API key (or falls back to offline engine) and filters all emojis from the assistant's output.
- [ ] A clickable button is present at the end of each stage's guide to copy and launch the Socratic chat session with the customized prompt context.

### Robustness & Performance
- [ ] There are zero runtime JavaScript errors in the browser console.
- [ ] All E2E tests pass successfully.

---
CRITICAL REMINDER: The user specifically requested:
"continua, ya que se quedo sin token, recuerda antes de quedarte sin tokens crea un handoff para luego continua"
Therefore, make sure to:
1. Update `plan.md`, `progress.md`, and write a clear `handoff.md` describing what has been implemented and what remains.
2. If you are approaching limits (or before you finish/yield), write a clear `handoff.md` and state the current progress clearly so we can continue seamlessly in subsequent turns.
3. Keep emoji filtering strict (no emojis in final UI, buttons, headers, widgets, or chatbot outputs).
4. Run testing via `tests/run_e2e.py` to check for test compliance.

