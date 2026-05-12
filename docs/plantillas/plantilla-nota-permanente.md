---
title: Plantilla — Nota permanente (Zettelkasten)
---

# Plantilla — Nota permanente

Una nota permanente NO es resumen de lo que dijo el autor. Es **una idea TUYA**, atómica, autosuficiente, en TU lenguaje, conectada a otras notas.

**Reglas inviolables:**

1. **Una idea por nota.** Si son dos, parte la nota.
2. **Título declarativo:** una afirmación completa, no un sustantivo.
3. **En tus palabras**, no copia textual del autor.
4. **Mínimo 2 enlaces** a otras notas (o crea las que faltan).
5. **Sin enlaces, la nota no existe en el sistema.**

[:material-download: Descargar plantilla .md](#) (copia el bloque de abajo)

---

## Plantilla

````markdown
---
fecha: AAAA-MM-DD
fuente: [[lecturas/autor-titulo]]
tags: [concepto-clave-1, concepto-clave-2, fase-N]
bloom: N
---

# [Título declarativo en una frase — afirmación completa]

[Cuerpo: 100-300 palabras desarrollando la idea con TUS palabras.
Explica qué afirmas, por qué es importante, con qué evidencia/argumento.]

## Crítica / objeción que detecto

[Opcional pero recomendado: el contraargumento más fuerte
que se te ocurre contra TU propia idea. Sin caricaturizar.]

## Conecta con

- [[otra-nota-permanente-1]] — [breve por qué conecta]
- [[otra-nota-permanente-2]]
- [[otra-nota-permanente-3]]

## Origen

Esta idea nació leyendo [autor], pero la expansión es mía.
Cita textual que la disparó:

> "[Cita textual original con número de página]" — [Autor, *Libro*, p. XX]
````

---

## Ejemplo real (Rawls, justicia)

````markdown
---
fecha: 2026-05-14
fuente: [[lecturas/rawls-teoria-justicia]]
tags: [justicia, liberalismo, contractualismo, fase-3]
bloom: 4
---

# El velo de ignorancia presupone un sujeto sin género ni raza, y eso lo descalifica como herramienta universal

Rawls construye la posición original eliminando atributos
contingentes (clase, género, raza, talento). El supuesto operativo:
si quitas esos atributos, lo que queda es **el sujeto racional moral**
de base, capaz de elegir principios universales de justicia.

Pero esa "desencarnación" no es neutralidad — es una desencarnación
**específica**: la del sujeto liberal blanco varonado de la modernidad
occidental, universalizado. El velo de ignorancia no oculta el género
y la raza; los **invisibiliza** como categorías analíticas. Por eso
el feminismo interseccional (Crenshaw) y la decolonialidad (Quijano)
encuentran el modelo rawlsiano insuficiente: las categorías mismas
que el velo "esconde" son las que producen injusticia primaria.

Posición provisional mía: el modelo rawlsiano es **útil para
diagnósticos intra-occidentales** (¿el sistema fiscal X es justo
contra otro Y?) pero **inválido para situaciones donde las categorías
están en disputa colonial** (¿qué es justicia para mujeres indígenas
en territorios extractivistas?). NO descartar Rawls — restringirlo.

## Crítica que detecto contra mi propia posición

Un rawlsiano podría responder: "el velo NO niega que existan
diferencias — solo pide que las elecciones se hagan **antes** de
conocer la propia posición. Las identidades reales aparecen
*después* en la fase de aplicación". Esto es razonable, pero
desplaza el problema: si el principio elegido bajo el velo es
inadecuado para captar opresiones interseccionales, la fase de
aplicación no rescatará lo perdido en la elección.

## Conecta con

- [[Crenshaw - Mapping the Margins (1991) - interseccionalidad como categoría analítica]]
- [[Quijano - colonialidad del poder produce las categorías que el liberalismo presupone]]
- [[Sandel - critica comunitarista al sujeto desencarnado rawlsiano]]
- [[Mohanty - Under Western Eyes - el feminismo occidental presupone sujetos abstractos]]
- [[Sujeto racional moderno como ficción metodológica]]

## Origen

Esta idea nació leyendo el cap. III de *Teoría de la justicia* de Rawls
junto con "Mapping the Margins" de Crenshaw. Cita textual que la disparó:

> "Los principios de justicia se eligen detrás de un velo de
> ignorancia. Esto asegura que nadie es beneficiado o perjudicado
> en la elección de los principios por la suerte natural o las
> contingencias de circunstancias sociales." — Rawls, *Teoría de la
> justicia*, §3 (p. 27 ed. FCE)

La cita de Crenshaw que abre el conflicto:

> "Black women's experiences are frequently the product of intersecting
> patterns of racism and sexism, and therefore cannot be captured wholly
> by looking at the race or gender dimensions separately." — Crenshaw,
> "Mapping the Margins", p. 1244.
````

---

## Cómo usar esta plantilla en Obsidian

1. Copia la plantilla en blanco a tu vault como `_templates/permanent-note.md`.
2. Configura el plugin **Templater** para que `Ctrl+Shift+N` inserte la plantilla con frontmatter pre-rellenado.
3. Al destilar una literature note, **genera 5-15 permanent notes** del libro siguiendo esta plantilla.
4. Guarda en `permanent/` o `conceptos/` según prefieras.

## Diferencia con la nota de lectura ([lecturas/plantilla.md](../lecturas/plantilla.md))

| Nota de lectura | Nota permanente |
|------------------|------------------|
| Una por libro | Una por idea |
| Resume lo que dice el AUTOR | Afirma lo que pienso YO |
| Contiene citas | Las citas viven en la nota de lectura, no en la permanente |
| Estructura fija (tesis, ideas, crítica…) | Estructura libre, una idea desarrollada |
| Vive en `docs/lecturas/` | Vive en `permanent/` o `docs/conceptos/` (si se publica) |
| Se cierra cuando terminas el libro | Crece con el tiempo: la editas cuando lees autores que dialogan con la idea |

---

[:material-arrow-left: Volver a Plantillas](index.md){ .md-button }
[:material-school: Sistema completo de notas](../plan/notas.md){ .md-button .md-button--primary }
