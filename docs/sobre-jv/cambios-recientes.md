---
title: Cambios recientes
---

# Cambios recientes

> Bitácora honesta del proyecto. El sitio cambió mucho en pocos días. Acá registro qué pasó y por qué.

---

## 2026-05-26 — Rediseño UX-V4: tipo Coursera / MIT OCW

**Motivo:** después de 8+ iteraciones acumulé capas que generaban confusión real ("no encuentro cómo empezar"). 3 agentes investigaron modelos existentes (Auditor del sitio + MOOCs formales + Modelos no-MOOC), un Manager sintetizó propuesta híbrida (esqueleto TYCS + carne MIT OCW).

**Cambios:**

- Home reescrita: par de CTAs ("Empezar el plan" + "Solo mirar la biblioteca") + 3 perfiles de tiempo (5 min / 1 hora / lector experto).
- Nav reorganizado a 7 secciones top-level con vocabulario limpio: Inicio / Cómo usar / El plan / Método / Biblioteca / Mi panel / Plantillas.
- "Caminos" eliminado del top-level — las 7 ramas viven en Biblioteca bajo "Tu rama (elegida en Fase 4)".
- "Ciclo III" eliminado del top-level — vive dentro de "El plan".
- "Ruta esencial" deja de ser camino paralelo — vive dentro de "El plan" como "versión corta (12 libros)".
- Checkpoints (sem 4 + mes 4) movidos de "Empezar acá" a "El plan".
- "Referencia" renombrado a "Biblioteca".
- "Mi práctica" dividido en "Mi panel" + "Plantillas".
- Nueva sección **Sobre JV** (esta página + Quién soy + Por qué este sitio).
- División de `metodo.md` en sub-páginas (sigue siendo hub).
- Cajas "Cómo se estudia esta fase" embebidas al inicio de cada `fase-*.md`.

**Commits:** `c685b8f` (quick wins) + commit actual (medium + diferibles).

---

## 2026-05-25 — Tronco común + 2 hitos (sistema multi-agente)

Sistema multi-agente (UX-revisor + Investigador-estructura + Manager) propuso tronco común de 4 semanas con 2 checkpoints rituales (sem 4 + mes 4). Decisión: bifurcación de ruta se difiere al mes 4 para que el usuario elija con vocabulario formado.

Commit: `ab21bb5`.

---

## 2026-05-25 — Sección Falacias formativa

Bug pedagógico detectado: el sitio pedía "capturá una falacia desde el Día 1" sin enseñar qué eran las falacias. Diseñé sección formativa con entrada de 5 min + top-5 detallado + manual completo + práctica con auto-test de 10 casos.

Commits: `5355549` + `96f3774` + `ea271ce`.

---

## 2026-05-25 — Canon ampliado: investigación de 14 universidades top

3 agentes investigaron syllabi 2024-2026 de Harvard, Oxford, Sciences Po, Stanford, LSE, UBA, UTDT, UdeSA, UCA, FLACSO, PUC Chile, Uniandes, UNAM, Colmex. 10 autores Tier 1 críticos incorporados (O'Donnell, Germani, Botana, Halperin, Ferrer, González Casanova, Florestan Fernandes, Bolívar Echeverría, Kymlicka, James C. Scott). 35 Tier 2 catalogados.

Commit: `a77ab85`.

---

## 2026-05-25 — Rebrand a "Itinerarios" + 7 ramas + mapa visual

Sistema multi-agente (Ramas canónicas + Pedagogía moderna + Visualización). Sitio rebrandeado, mapa Mermaid en home, 7 ramas separadas (separé Política Social de Cultura, agregué Sociología y RR.II.), página "Cómo se aprende acá" con 5 prompts IA + regla anti-Dunning-Kruger.

Commit: `d7fc085`.

---

## 2026-05-25 — Portal de 4 cursos / itinerarios

4 agentes curadores diseñaron itinerarios sobre el corpus único (Filosofía / CC.PP. / Economía / Política Social y Cultura). Modelo B (itinerarios sobre corpus) elegido para no romper temas-bisagra.

Commit: `d0868fe`.

---

## 2026-05-25 — Lecturas complementarias

Mapeo de 14 libros descargados (Graeber, CLR James, Bevins, Rothstein, Evangelista, Merchant, etc.) a fases/temas-bisagra del plan.

Commit: `f4f71e8`.

---

## 2026-05-25 — Ciclo III (M5 política social + M6 cultura + temas-bisagra + tesina)

Plan extendido a 36 meses opcional. 5 agentes en paralelo (Auditor + 3 Curadores + Arquitecto). M5 política social, M6 desarrollo cultural, 6 temas-bisagra, tesina de 8-10k pal.

Commit: `3519ce7`.

---

## 2026-05-25 — Fixes Auditor

Corrección de inconsistencias del plan maestro: solapamiento de meses Fase 4/5, lecturas fantasma en Fase 3, sincronización con vocabulario actualizado.

Commit: `5208adc`.

---

[:material-arrow-left: Por qué este sitio](por-que-este-sitio.md){ .md-button }
[:material-github: Repo en GitHub](https://github.com/MrSpagVi/Libros-Politica){ .md-button target="_blank" }
