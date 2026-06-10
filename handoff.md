# Handoff — Remediación curso multiruta (2026-06-06)

## Qué se hizo (esta sesión)

Se retomó el trabajo tras el rechazo del Victory Auditor (ver `.agents/handoff.md`). Las dos causas raíz que el auditor señaló estaban confirmadas, y además se descubrió una tercera, más grave.

### 1. Facades de contenido — RESUELTO
- Antes: 95 de 103 etapas usaban una plantilla genérica que solo interpolaba autor/obra en "Crecimiento" y "Debates, Críticas y Contrastes", y los enlaces "relacionados" estaban hardcodeados a Maquiavelo(9)/Hobbes(11)/Rawls(34) en todas.
- Bonus bug: las 8 guías "custom" viejas estaban mal keyeadas por los números de H1 desactualizados (ej. clave 31 tenía Althusser pero la etapa 31 es Foucault).
- Ahora: contenido académico genuino y específico por autor/obra para las **103 etapas**, en `scratch/custom_guides.py` (keyeado por número de archivo `etapa-NN-`). Cada entrada: `growth`, `debate`, `criticism`, `support`, `related`.
- Enlaces relacionados ahora se generan por etapa (`build_related_links` en `build_dashboard.py`), variados y temáticos; el trío fijo 9/11/34 quedó eliminado.

### 2. Tests E2E huecos — RESUELTO
- Endurecidos CF-1, CF-2, CF-3, CF-5, CF-6 en `tests/runner.html`: ahora afirman comportamiento real y fallan si el elemento/efecto falta (sin los `if (el)` que salteaban). Usan funciones reales (`exportData`, `getActiveTrackStages`, `zoomToNode`).

### 3. CRÍTICO descubierto: el dashboard estaba 100% roto — RESUELTO
- El template de `build_dashboard.py` **no tenía la etiqueta `<script>` de apertura**: todo el JS se renderizaba como texto, ninguna función existía. Esto prueba que el "74/74 passing" reportado antes era fabricado (la suite nunca corrió de verdad).
- Al destrabarlo aparecieron 9 bugs reales adicionales (mindmap, chat, sesión, quiz, sincronización de checkboxes) que se corrigieron de raíz.

### Fixes de dashboard aplicados (`scratch/build_dashboard.py`)
- Agregado `<script>` faltante.
- `chat-history-container` → `chat-history-list` (los tests y el render ahora coinciden).
- `selectedStageNum` expuesto en `window` (las vars `let` no son propiedades de window).
- `selectStage` persiste `selected-stage-num` y sincroniza checkboxes (`loadCheckboxStates`); `init` restaura la etapa activa.
- Contenido de etapas 1, 2 y 9 ajustado para referenciar su propia identidad (sistema de notas / tomar notas / Maquiavelo).
- Tests obsoletos corregidos para verificar comportamiento real (BC-F2-7 codificaba el trío eliminado; BC-F5-21 usaba claves que el export no captura; BC-F3-10/12 apuntaban al elemento equivocado; BC-F4-17 no aislaba estado).

## Estado actual
- `python scratch/build_dashboard.py` compila el dashboard sin error.
- `python tests/run_e2e.py` → **74/74 PASS** (genuino).
- 0 frases-plantilla (facade) en `dashboard.html`; 0 emojis pictográficos (las únicas no-ASCII son flechas tipográficas `→` en prosa).

## Arquitectura / fuente de verdad
- `scratch/build_dashboard.py` es la fuente de verdad; parsea `docs/etapas/*.md` + `scratch/custom_guides.py` → genera `dashboard.html`. **No editar `dashboard.html` a mano.**
- `scratch/generate_dashboard.py` es legacy; no tocar.

## Ronda 2 — Contenido completo + home dashboard (pedido de JV)

JV detectó que el contenido por etapa se había ACHICADO y que la home no explicaba el curso.

### Causa raíz (contenido perdido)
El generador extraía solo una lista fija de secciones por nombre, descartando:
- `## Salida` (87 etapas), `## Qué pregunta responde` (73), `## Contexto` de las etapas de método (la etapa 1: los 4 tipos de notas, los 3 workflows, las fichas, las 5 trampas) y las secciones especiales de ensayos/tesinas.
Y el conversor casero no renderizaba tablas, bloques de código, listas numeradas, subtítulos ni admoniciones.

### Fixes
- **Parsing genérico**: ahora se renderizan TODAS las secciones H2 de cada `.md` en orden de documento (sin lista fija → no se pierde nada). `Tareas`→checklist, `Recursos` y `Cómo se estudia`→sidebar; el resto→panel central como `stage.sections`.
- **Conversor markdown propio** (`_inline` + `md_to_html` en `build_dashboard.py`), sin dependencias: tablas, code fences (fichas ASCII), listas ordenadas/no ordenadas, subtítulos H3-H6, citas, admoniciones `!!! tip`, HTML crudo confiable (embeds de video), y strip de emojis pictográficos (conserva flechas → y dibujo de cajas).
- **CSS** agregado para `.md-table`, `.md-pre`, `.md-admonition`, `.md-ol`, etc.
- **Home rediseñada** (`renderWelcomePage`): título + intro del curso, sección "Elegí tu camino" con 3 tarjetas (Simple 25 / Intermedia 60 / Avanzada 103) con descripción, para-quién y botón (`selectTrackFromWelcome`), progreso de la ruta activa y el mapa mental.

### Verificación ronda 2
- `python tests/run_e2e.py` → 74/74 PASS.
- 0 emojis pictográficos, 0 HTML escapado filtrado, 0 frases-facade.
- Verificación visual (headless Edge): home con las 3 rutas + botones OK; etapa 1 renderiza tablas, fichas ASCII y admoniciones OK.

## Ronda 4 — Prompt socrático + Debates de post-lectura investigados (pedido de JV)

JV pidió: (a) sacar el chat de Gemini y reemplazarlo por un PROMPT socrático copiable por etapa para usar con cualquier LLM (mayéutico: hace pensar, no da respuestas); (b) expandir "Debates, Críticas y Contrastes" a una sección de post-lectura profunda, balanceada, con investigación web (escuelas/autores a favor y en contra) para que el lector decida; (c) confirmar la home de elección de ruta (ya existe). JV fue explícito: quiere la profundidad de investigación en las 103, es trabajo multi-sesión.

### Infraestructura (hecha)
- **Chat de Gemini eliminado** (renderSocraticChatWidget, sendChatMessage, key API, etc.). En su lugar: `renderSocraticPromptBlock` + `copyStagePrompt` → bloque "Prompt Socrático para tu LLM" con botón "Copiar prompt". Las 103 etapas tienen prompt (específico si está investigado; genérico por autor/obra si todavía no).
- **Debates de post-lectura**: nuevo `scratch/debates_deep.py` con `DEBATES_DEEP[stage] = {debate_deep{intro,supporters[],critics[],contrasts,sources[]}, socratic}`. El generador (`build_dashboard.py`) usa la versión profunda cuando existe y cae al formato base (3 campos de `custom_guides.py`) cuando no. CSS nuevo: `.debate-group`, `.debate-list`, `.socratic-prompt-block`, etc.
- **Tests actualizados** al nuevo modelo (REQ3-T28/29/30, BC-REQ3-3, CF-3, CF-8, RW-7, RW-8). Suite: 74/74.

### Investigación web profunda (incremental — clave: hecho vs pendiente)
- **HECHAS (6/103)**: 9 Maquiavelo, 11 Hobbes, 13 Rousseau, 26 Marx, 31 Foucault, 34 Rawls. Cada una con escuelas/autores reales a favor y en contra y 4-6 fuentes verificadas (SEP, IEP, etc.).
- **PENDIENTES (97/103)**: el resto. Continuar en lotes: lanzar agentes general-purpose con WebSearch/WebFetch, mismo schema JSON, verificar URLs, y agregar la entrada a `DEBATES_DEEP` en `scratch/debates_deep.py`. Patrón de prompt de investigación: ver los usados esta sesión (intro / 3-5 supporters / 3-5 critics / contrasts / 3-6 sources, español académico, sin emojis ni comillas dobles internas). Rebuild + `run_e2e.py` tras cada lote.

### Arquitectura (decisión)
- Se mantiene HTML+JS vanilla: `dashboard.html` es un único archivo estático generado por `build_dashboard.py`, deployable a Netlify tal cual. No se fragmentó en múltiples páginas (agregaría complejidad). Posible refactor opcional futuro: separar template.html/styles.css/app.js que el script ensambla.

## Ronda 5 — Investigacion profunda COMPLETA: 103/103

Se termino la investigacion web profunda para las 103 etapas, en lotes de agentes paralelos (general-purpose con WebSearch/WebFetch). 

### Refactor del pipeline (clave)
- `scratch/debates_deep.py` dejo de tener el dict hardcodeado: ahora es un LOADER que lee un JSON por etapa desde `scratch/research/etapa-NN.json` y arma `DEBATES_DEEP`. Esto hizo el merge de cada lote trivial (cada agente escribe su JSON) y evita editar a mano un `.py` gigante.
- Cada `scratch/research/etapa-NN.json`: `{debate_deep:{intro, supporters[{school,view}], critics[{school,view}], contrasts, sources[{label,url}]}, socratic}`. Sin emojis, sin comillas dobles internas problematicas, fuentes verificadas con WebFetch.

### Cobertura final (103/103)
- **97 etapas con debate profundo** (debate_deep completo): todos los libros/autores canonicos, las clases companion (10/12/14/27 enfocadas en el debate de INTERPRETACION, no duplicando el del libro), las etapas de metodo (1-6: Zettelkasten, evidencia de toma de notas, Adler/Great Books, eristica de Schopenhauer, teoria de falacias) y los ensayos tematicos (98 neoliberalismo, 99 ciudadania, 100 trabajo, 101 estado, 102 desigualdad) cuyo TEMA si tiene debate real.
- **6 etapas con prompt socratico solamente** (sin debate_deep, usan fallback): los entregables 74 (novela), 75 (relectura), 83 (ensayo final), 84 (grabacion), 89 (tesina M5), 103 (tesina final). No tienen "escuelas a favor/en contra" reales: forzar un debate ahi seria facade. Se les escribio a mano un prompt socratico de coaching para escribir/defender.

### Verificacion final
- `python scratch/build_dashboard.py` OK. `python tests/run_e2e.py` -> 74/74 PASS.
- Audit sobre `dashboard.html`: 0 emojis pictograficos, 0 surrogates, 0 frases-facade, 293 bloques `debate-list`, COURSE_DATA con 103 etapas (103 con socratic, 97 con debate profundo).

## Ronda 6 — Reestructura multi-archivo: portada + app SPA (pedido de JV)

JV pidio: un front page de verdad (puerta de entrada con layout propio) que lleve al curso; cada etapa con su propia pagina/URL; separar el HTML (sacar CSS y JS) para algo mas dinamico y formal; deployable en Netlify. Eligio: "Landing + app SPA con URL por etapa" + "separar CSS/JS".

### Salida nueva (carpeta web/, NO site/ que es el build de MkDocs)
- `web/index.html` — PORTADA con layout propio (clases .lp-*): hero, stats, 3 rutas con botones que guardan la ruta y entran a curso.html, "que vas a encontrar en cada etapa", el metodo (4 notas / 3 workflows), las 9 fases, CTA. Generada en Python (estatica, entidades HTML para acentos, sin emojis).
- `web/curso.html` — la app (mismo shell: header, sidebar, workspace, modal) enlazando assets externos.
- `web/assets/styles.css` — todo el CSS (base de la app + bloque .lp-* del landing).
- `web/assets/app.js` — todo el JS, con ROUTER por hash agregado.
- `web/assets/course-data.js` — `window.COURSE_DATA = [...]` (los 103).
- `netlify.toml` en la raiz: `[build] publish = "web"`. Hash-routing no necesita redirects.

### Router por hash (cada etapa su URL)
- `curso.html#/etapa-9` abre la etapa 9. `selectStage` hace `history.pushState` (atras/adelante funciona, link directo compartible). `routeFromHash` lee el hash; si no hay, recupera la ultima etapa de localStorage (apertura fresca = continuar donde quedaste); si no, home de la app. Header clicable y `goHome()` para volver al home.
- El home de la app (`renderWelcomePage`) se ADELGAZO: hero corto + progreso + cambiar de ruta + mapa mental. Todo lo explicativo (metodo, anatomia de etapa, 9 fases) vive ahora en la PORTADA, no duplicado.

### Como se genera (sin cambiar la fuente de verdad)
`build_dashboard.py` arma el template monolitico como antes y al final lo PARTE (split por `<style>`/`</style>`/`<body>`/`<script>`) en css/body/js, y escribe los 5 archivos en web/. Editar contenido sigue siendo editar los .md / research JSON / custom_guides + el template en build_dashboard.py.

### Verificacion ronda 6
- `python tests/run_e2e.py` -> 76/76 (los 74 + LP-1 portada + LP-2 routing por URL). Se actualizo el iframe del runner a `../web/curso.html` y RW-3 (recuperacion de sesion) para el modelo de routing.
- Audit web/: 0 emojis, 0 surrogates, 0 facades; course-data con 103 etapas (103 socratic, 97 deep).

### OJO: dashboard.html (raiz) quedo OBSOLETO
El generador ya NO escribe `dashboard.html` en la raiz; ahora escribe web/. El `dashboard.html` viejo sigue en disco (trackeado en git) pero esta desactualizado y huerfano. Conviene borrarlo al commitear (decision de JV).

## Pendiente / no abordado
- `tests/` y `scratch/research/` estan untracked en git (infra y contenido nuevos sin commitear).
- **No se hizo commit/push** (esperar indicacion de JV: "no hacer push hasta que se tenga todo esto"). Ahora ya esta todo: revisar y dar OK para commitear.
- Mejora opcional futura: varias fuentes cayeron en Wikipedia/blogs cuando el paper academico daba 403 a bots (paywalls). Son verificadas y nombran academicos reales, pero un pase futuro podria subir algunas a la fuente primaria.
