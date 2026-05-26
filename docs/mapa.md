---
title: Mapa del corpus
---

# Mapa del corpus

> Las 7 ramas + bases comunes + temas-bisagra que cruzan disciplinas. Clic en cualquier nodo para entrar.

```mermaid
flowchart TB
    BASES(["BASES COMUNES<br/>lógica · falacias · cómo leer<br/>notas Zettelkasten · oratoria"]):::base

    BASES --> FIL["📚 Filosofía"]
    BASES --> CP["🏛 Ciencias Políticas"]
    BASES --> ECO["💰 Economía Política"]
    BASES --> PS["🤝 Política Social"]
    BASES --> SC["🎭 Estudios Culturales"]
    BASES --> SOC["👥 Sociología"]
    BASES --> RI["🌐 Relaciones Internacionales"]

    FIL --> FIL_A["Platón · Kant · Hegel<br/>Nietzsche · Wittgenstein · Foucault"]
    CP --> CP_A["Maquiavelo · Hobbes · Locke<br/>Weber · Arendt · Dahl · Levitsky"]
    ECO --> ECO_A["Smith · Marx · Keynes · Hayek<br/>Polanyi · Mazzucato · Prebisch · Diamand"]
    PS --> PS_A["Marshall · Titmuss · Polanyi · Sen<br/>Esping-Andersen · Filgueira · Fraser"]
    SC --> SC_A["Williams · Adorno · Benjamin · Hall<br/>Bourdieu · García Canclini · Fisher · Zuboff"]
    SOC --> SOC_A["Marx · Weber · Durkheim · Simmel<br/>Bourdieu · Goffman · Wacquant · Illouz"]
    RI --> RI_A["Tucídides · Hobbes · Kant · Carr<br/>Morgenthau · Waltz · Mearsheimer · Wallerstein"]

    B1(["⚙️ Temas-bisagra<br/>Ciudadanía · Trabajo · Estado<br/>Neoliberalismo · Desigualdad · Crisis<br/>+ Tecnología y democracia<br/>+ Ecología política"]):::bisagra

    B1 -.-> FIL
    B1 -.-> CP
    B1 -.-> ECO
    B1 -.-> PS
    B1 -.-> SC
    B1 -.-> SOC
    B1 -.-> RI

    click BASES "../empieza-aqui/" "Empezar acá — setup notas + Día 1"
    click FIL "../ramas/filosofia/" "Rama Filosofía"
    click CP "../ramas/ciencias-politicas/" "Rama Ciencias Políticas"
    click ECO "../ramas/economia/" "Rama Economía Política"
    click PS "../ramas/politica-social/" "Rama Política Social"
    click SC "../ramas/estudios-culturales/" "Rama Estudios Culturales y Comunicación"
    click SOC "../ramas/sociologia/" "Rama Sociología"
    click RI "../ramas/relaciones-internacionales/" "Rama Relaciones Internacionales"
    click B1 "../plan/temas-bisagra/" "Temas-bisagra"

    classDef base fill:#e8f4fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    classDef bisagra fill:#fff3cd,stroke:#856404,stroke-dasharray:5 5,color:#5d4037
```

---

## Cómo leer este mapa

- **Centro:** las **bases comunes** que toda rama necesita — lógica, cómo leer, falacias, sistema de notas, oratoria. Esto NO es opcional para ninguna ruta.
- **Ramas (7):** las disciplinas mayores. Cada una es una "puerta" al mismo corpus, con énfasis distinto. Compartimentos en la apariencia, pero los autores y debates se cruzan adentro.
- **Temas-bisagra (línea punteada):** problemas que cruzan **todas** las ramas. "Desigualdad" es a la vez dato económico, problema político, naturalización cultural. Por eso aparecen como nodo aparte conectado con todas las ramas.

---

## Otras vistas del corpus

- **[Ruta esencial — 12 libros, 6 meses](ruta-esencial.md)** — la versión mínima.
- **[Plan integrado completo](plan/maestro.md)** — 27-36 meses, todo el corpus cruzado deliberadamente.
- **[Las 7 ramas](ramas/index.md)** — overview con criterio para elegir.
- **[Canon ampliado](plan/canon-ampliado.md)** — 45 autores extra investigados en universidades top (Harvard, Oxford, LSE, UBA, UNAM, etc.).

[:material-arrow-left: Volver al inicio](index.md){ .md-button }
