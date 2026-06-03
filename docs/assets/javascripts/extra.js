/* ============================================================
   Itinerarios — minimal interactive layer
   Pure vanilla JS, localStorage-backed
   - persistTaskLists: saves task checkboxes per page
   - setupCursoGlobalProgress: shows tronco-único progress (84 etapas)
   - migrateCursoTaskState: one-shot migration from old layouts
   ============================================================ */

(function () {
  'use strict';

  function loadJSON(key, fallback) {
    try {
      const v = localStorage.getItem(key);
      if (v == null) return fallback;
      return JSON.parse(v);
    } catch (e) {
      return fallback;
    }
  }

  function saveJSON(key, val) {
    try {
      localStorage.setItem(key, JSON.stringify(val));
    } catch (e) { /* quota exceeded — ignore */ }
  }

  function getPathPrefix() {
    if (location.pathname.startsWith('/Curso')) return '/Curso';
    if (location.pathname.startsWith('/Libros-Politica')) return '/Libros-Politica';
    return '';
  }

  // ---------- Task list persistence ----------

  function persistTaskLists() {
    const items = document.querySelectorAll('.md-typeset .task-list-item');
    if (items.length === 0) return;
    const pageKey = `lp.tasks.${location.pathname}`;
    const state = loadJSON(pageKey, {});
    items.forEach((li, idx) => {
      const cb = li.querySelector('input[type="checkbox"]');
      if (!cb) return;
      const key = `${idx}::${li.textContent.trim().slice(0, 80)}`;
      if (state[key]) cb.checked = true;
      cb.addEventListener('change', () => {
        const cur = loadJSON(pageKey, {});
        if (cb.checked) cur[key] = true;
        else delete cur[key];
        saveJSON(pageKey, cur);
      });
    });
  }

  // ---------- Tronco único — global progress (85 etapas) ----------
  // Totales curados (excluyen checkboxes de rúbrica). Regenerar con scripts/regen_etapas_js.py.
  const ETAPAS = [
    { slug: 'etapa-01-setup-sistema-de-notas', total: 6, title: 'Setup del sistema de notas', phase: 0 },
    { slug: 'etapa-02-tutorial-tomar-notas', total: 4, title: 'Tutorial — aprender a tomar notas (30 días)', phase: 0 },
    { slug: 'etapa-03-adler-como-leer-un-libro', total: 5, title: 'Adler — Cómo leer un libro', phase: 0 },
    { slug: 'etapa-04-schopenhauer-arte-tener-razon', total: 4, title: 'Schopenhauer — El arte de tener razón', phase: 0 },
    { slug: 'etapa-05-crashcourse-falacias', total: 4, title: 'CrashCourse Philosophy — falacias', phase: 0 },
    { slug: 'etapa-06-manual-falacias', total: 5, title: 'Manual de falacias — captura diaria 30 días', phase: 0 },
    { slug: 'etapa-07-platon-apologia', total: 4, title: 'Platón — Apología de Sócrates', phase: 1 },
    { slug: 'etapa-08-aristoteles-politica', total: 4, title: 'Aristóteles — Política (selección Libros I, III, VII)', phase: 1 },
    { slug: 'etapa-09-maquiavelo-principe', total: 5, title: 'Maquiavelo — El Príncipe', phase: 1 },
    { slug: 'etapa-10-yale-maquiavelo', total: 3, title: 'Yale PLSC 114 — Maquiavelo (Lec. 10-11)', phase: 1 },
    { slug: 'etapa-11-hobbes-leviatan', total: 5, title: 'Hobbes — Leviatán (selección caps. 13-21)', phase: 1 },
    { slug: 'etapa-12-yale-hobbes', total: 3, title: 'Yale PLSC 114 — Hobbes (Lec. 12-14)', phase: 1 },
    { slug: 'etapa-13-rousseau-contrato-social', total: 5, title: 'Rousseau — Contrato social (Libros I-IV)', phase: 1 },
    { slug: 'etapa-14-yale-rousseau', total: 3, title: 'Yale PLSC 114 — Rousseau (Lec. 18-20)', phase: 1 },
    { slug: 'etapa-15-mill-sobre-la-libertad', total: 5, title: 'Mill — Sobre la libertad', phase: 1 },
    { slug: 'etapa-16-sandel-justice', total: 3, title: 'Sandel — Justice (Episodios 1 y 5)', phase: 1 },
    { slug: 'etapa-17-locke-segundo-tratado', total: 5, title: 'Locke — Segundo tratado del gobierno civil (selección)', phase: 1 },
    { slug: 'etapa-18-tocqueville-democracia-en-america', total: 4, title: 'Tocqueville — La democracia en América (selección)', phase: 1 },
    { slug: 'etapa-19-pocock-momento-maquiavelico', total: 7, title: 'Pocock — El momento maquiavélico (selección)', phase: 1 },
    { slug: 'etapa-20-chang-economia-99', total: 4, title: 'Chang — Economía para el 99% (10 caps. seleccionados)', phase: 2 },
    { slug: 'etapa-21-smith-riqueza-naciones', total: 5, title: 'Smith — La riqueza de las naciones (Libros I y IV)', phase: 2 },
    { slug: 'etapa-22-hegel-fenomenologia', total: 4, title: 'Hegel — Fenomenología del Espíritu + Filosofía del derecho', phase: 2 },
    { slug: 'etapa-23-marx-capital', total: 4, title: 'Marx — El Capital Libro I (caps. 1, 4, 24)', phase: 2 },
    { slug: 'etapa-24-harvey-reading-marx', total: 4, title: 'Harvey — Reading Marx\'s Capital (13 clases video)', phase: 2 },
    { slug: 'etapa-25-mariategui-7-ensayos', total: 5, title: 'Mariátegui — 7 Ensayos de interpretación (II-III)', phase: 2 },
    { slug: 'etapa-26-weber-politica-vocacion', total: 4, title: 'Weber — La política como vocación', phase: 3 },
    { slug: 'etapa-27-foucault', total: 6, title: 'Foucault — Vigilar y castigar / Nacimiento de la biopolítica', phase: 3 },
    { slug: 'etapa-28-rawls-teoria-justicia', total: 5, title: 'Rawls — Teoría de la Justicia (caps. I y III)', phase: 3 },
    { slug: 'etapa-29-berlin-dos-conceptos', total: 4, title: 'Berlin — Dos conceptos de libertad', phase: 3 },
    { slug: 'etapa-30-habermas-esfera-publica', total: 6, title: 'Habermas — Esfera pública (selección)', phase: 3 },
    { slug: 'etapa-31-lenin-imperialismo', total: 4, title: 'Lenin — El imperialismo, fase superior del capitalismo', phase: 3 },
    { slug: 'etapa-32-gramsci-cuadernos', total: 5, title: 'Gramsci — Cuadernos desde la prisión (selección Hoare-Smith)', phase: 3 },
    { slug: 'etapa-33-hayek-camino-servidumbre', total: 6, title: 'Hayek — Camino de servidumbre (caps. 1, 3, 5-7)', phase: 3 },
    { slug: 'etapa-34-popper-sociedad-abierta', total: 5, title: 'Popper — La sociedad abierta y sus enemigos', phase: 3 },
    { slug: 'etapa-35-nozick-anarquia-estado-utopia', total: 4, title: 'Nozick — Anarquía, Estado y utopía (Partes I y III)', phase: 3 },
    { slug: 'etapa-36-bolivar-carta-jamaica', total: 6, title: 'Bolívar — Carta de Jamaica', phase: 4 },
    { slug: 'etapa-37-marti-nuestra-america', total: 6, title: 'Martí — Nuestra América', phase: 4 },
    { slug: 'etapa-38-rodo-ariel', total: 4, title: 'Rodó — Ariel', phase: 4 },
    { slug: 'etapa-39-vasconcelos-raza-cosmica', total: 5, title: 'Vasconcelos — La raza cósmica', phase: 4 },
    { slug: 'etapa-40-paz-laberinto-soledad', total: 4, title: 'Paz — El laberinto de la soledad', phase: 4 },
    { slug: 'etapa-41-galeano-venas-abiertas', total: 4, title: 'Galeano — Las venas abiertas de América Latina', phase: 4 },
    { slug: 'etapa-42-bueno-mito-izquierda', total: 5, title: 'Bueno — El mito de la izquierda (selección)', phase: 4 },
    { slug: 'etapa-43-echeverria-modernidad-blanquitud', total: 4, title: 'Bolívar Echeverría — Modernidad y blanquitud', phase: 4 },
    { slug: 'etapa-44-dussel-1492', total: 7, title: 'Dussel — 1492: el encubrimiento del Otro', phase: 4 },
    { slug: 'etapa-45-quijano-colonialidad', total: 3, title: 'Quijano — Colonialidad del poder', phase: 4 },
    { slug: 'etapa-46-cusicanqui-chixinakax', total: 5, title: 'Cusicanqui — Ch\'ixinakax utxiwa', phase: 4 },
    { slug: 'etapa-47-freire-pedagogia-oprimido', total: 5, title: 'Freire — Pedagogía del oprimido (caps. 1-2)', phase: 4 },
    { slug: 'etapa-48-gutierrez-teologia-liberacion', total: 4, title: 'Gutiérrez — Teología de la liberación (selección)', phase: 4 },
    { slug: 'etapa-49-gonzalez-feminismo-afrolatinoamericano', total: 4, title: 'Lélia González — Por un feminismo afrolatinoamericano', phase: 4 },
    { slug: 'etapa-50-lugones-heterosexualismo', total: 4, title: 'Lugones — Heterosexualismo y sistema de género colonial moderno', phase: 4 },
    { slug: 'etapa-51-gago-potencia-feminista', total: 4, title: 'Gago — La potencia feminista', phase: 4 },
    { slug: 'etapa-52-segato-guerra-mujeres', total: 6, title: 'Segato — La guerra contra las mujeres', phase: 4 },
    { slug: 'etapa-53-wallerstein-sistemas-mundo', total: 5, title: 'Wallerstein — Análisis de sistemas-mundo (selección)', phase: 5 },
    { slug: 'etapa-54-mearsheimer-great-power', total: 6, title: 'Mearsheimer — The Tragedy of Great Power Politics', phase: 5 },
    { slug: 'etapa-55-agamben', total: 4, title: 'Agamben — Homo Sacer / Estado de excepción', phase: 5 },
    { slug: 'etapa-56-fanon-condenados-tierra', total: 4, title: 'Frantz Fanon — Los condenados de la tierra', phase: 5 },
    { slug: 'etapa-57-said-orientalismo', total: 5, title: 'Edward Said — Orientalismo', phase: 5 },
    { slug: 'etapa-58-mbembe-necropolitica', total: 4, title: 'Mbembe — Necropolítica', phase: 5 },
    { slug: 'etapa-59-novela-politica', total: 4, title: 'Novela Política Latinoamericana — La Dictadura y el Poder', phase: 5 },
    { slug: 'etapa-60-relectura-activa', total: 3, title: 'Relectura activa de un libro de Fases 1-4 que te marcó', phase: 5 },
    { slug: 'etapa-61-gandhi-hind-swaraj', total: 4, title: 'Gandhi — Hind Swaraj', phase: 5 },
    { slug: 'etapa-62-confucio-analectas', total: 4, title: 'Confucio — Analectas (selección)', phase: 5 },
    { slug: 'etapa-63-sen-identidad-violencia', total: 4, title: 'Sen — Identidad y violencia', phase: 5 },
    { slug: 'etapa-64-hardt-negri-imperio', total: 5, title: 'Hardt and Negri — Imperio (caps. 1-4)', phase: 5 },
    { slug: 'etapa-65-wang-hui', total: 5, title: 'Wang Hui — El nuevo orden de China', phase: 5 },
    { slug: 'etapa-66-maruyama', total: 4, title: 'Maruyama — Pensamiento político de Japón moderno', phase: 5 },
    { slug: 'etapa-67-ambedkar-annihilation-caste', total: 4, title: 'Ambedkar — Annihilation of Caste', phase: 5 },
    { slug: 'etapa-68-ensayo-final', total: 5, title: 'Ensayo final integrador (1500-2000 palabras)', phase: 5 },
    { slug: 'etapa-69-grabacion-final', total: 4, title: 'Grabación oral final (10 minutos, sin notas)', phase: 5 },
    { slug: 'etapa-70-marshall-ciudadania', total: 5, title: 'Marshall — Ciudadanía y clase social', phase: 6 },
    { slug: 'etapa-71-polanyi-gran-transformacion', total: 6, title: 'Polanyi — La gran transformación (caps. 4, 6, 11-14)', phase: 6 },
    { slug: 'etapa-72-esping-andersen', total: 4, title: 'Esping-Andersen — Los tres mundos del Estado del bienestar', phase: 6 },
    { slug: 'etapa-73-filgueira-universalismo-basico', total: 4, title: 'Filgueira et al. — Universalismo básico en América Latina', phase: 6 },
    { slug: 'etapa-74-tesina-m5', total: 5, title: 'Tesina módulo M5: qué tipo de welfare es el argentino', phase: 6 },
    { slug: 'etapa-75-williams-marxismo-literatura', total: 4, title: 'Williams — Marxismo y literatura', phase: 7 },
    { slug: 'etapa-76-benjamin-obra-arte', total: 4, title: 'Benjamin — La obra de arte en la época de su reproductibilidad técnica', phase: 7 },
    { slug: 'etapa-77-bourdieu-distincion', total: 6, title: 'Bourdieu — La distinción (caps. 1 y 3)', phase: 7 },
    { slug: 'etapa-78-hall-encoding-decoding', total: 4, title: 'Hall — Encoding/Decoding', phase: 7 },
    { slug: 'etapa-79-garcia-canclini-culturas-hibridas', total: 4, title: 'García Canclini — Culturas híbridas (selección)', phase: 7 },
    { slug: 'etapa-80-martin-barbero', total: 4, title: 'Martín-Barbero — De los medios a las mediaciones (Parte III)', phase: 7 },
    { slug: 'etapa-81-zuboff-vigilancia', total: 6, title: 'Zuboff — La era del capitalismo de la vigilancia (selección)', phase: 7 },
    { slug: 'etapa-82-ensayo-neoliberalismo', total: 4, title: 'Ensayo tema-bisagra — Neoliberalismo', phase: 8 },
    { slug: 'etapa-83-ensayo-ciudadania', total: 4, title: 'Ensayo tema-bisagra — Ciudadanía', phase: 8 },
    { slug: 'etapa-84-ensayo-trabajo', total: 4, title: 'Ensayo tema-bisagra — Trabajo', phase: 8 },
    { slug: 'etapa-85-ensayo-estado', total: 4, title: 'Ensayo tema-bisagra — Estado', phase: 8 },
    { slug: 'etapa-86-ensayo-desigualdad', total: 4, title: 'Ensayo tema-bisagra — Desigualdad', phase: 8 },
    { slug: 'etapa-87-tesina-final', total: 6, title: 'Tesina final integrada (8-10k palabras, 1 tema-bisagra)', phase: 8 },
  ];

  function etapaPathCandidates(slug) {
    const p = getPathPrefix();
    const prefixes = ['', '/Libros-Politica', '/Curso'];
    if (p && !prefixes.includes(p)) prefixes.push(p);
    const paths = [];
    prefixes.forEach(pref => {
      paths.push(`${pref}/etapas/${slug}/`);
      paths.push(`${pref}/etapas/${slug}`);
    });
    return paths;
  }

  function countCompletedForEtapa(slug) {
    for (const path of etapaPathCandidates(slug)) {
      const state = loadJSON(`lp.tasks.${path}`, null);
      if (state && typeof state === 'object') {
        return Object.values(state).filter(Boolean).length;
      }
    }
    return 0;
  }

  function renderGlobalProgressInto(box) {
    if (!box) return;
    const elCompleted = box.querySelector('#curso-completed') || document.getElementById('curso-completed');
    const elTotal = box.querySelector('#curso-total') || document.getElementById('curso-total');
    const elPct = box.querySelector('#curso-pct') || document.getElementById('curso-pct');
    const elBar = box.querySelector('#curso-bar') || document.getElementById('curso-bar');
    const total = ETAPAS.reduce((s, e) => s + e.total, 0);
    const completed = ETAPAS.reduce((s, e) => s + Math.min(countCompletedForEtapa(e.slug), e.total), 0);
    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
    if (elCompleted) elCompleted.textContent = completed;
    if (elTotal) elTotal.textContent = total;
    if (elPct) elPct.textContent = pct + '%';
    if (elBar) elBar.style.width = pct + '%';
    box.style.display = '';
  }

  function setupCursoGlobalProgress() {
    const boxes = [
      document.getElementById('curso-progress'),
      document.getElementById('curso-progress-mini')
    ].filter(Boolean);
    if (boxes.length === 0) return;
    boxes.forEach(renderGlobalProgressInto);
    const items = document.querySelectorAll('.md-typeset .task-list-item input[type="checkbox"]');
    items.forEach(cb => cb.addEventListener('change', () => boxes.forEach(renderGlobalProgressInto)));
  }

  // ---------- Legacy migration (v1 → v2 84 etapas) ----------
  // The v1 layout used etapa-NN-<slug> with different slugs (e.g. etapa-01-setup-notas).
  // Map old slugs → new slugs so progress carries over.
  const V1_TO_V2 = {
    'etapa-01-setup-notas': 'etapa-01-setup-sistema-de-notas',
    'etapa-02-tutorial-notas': 'etapa-02-tutorial-tomar-notas',
    'etapa-04-dia-1-adler': 'etapa-03-adler-como-leer-un-libro',
    'etapa-05-adler-2-4': 'etapa-03-adler-como-leer-un-libro',
    'etapa-06-primera-ficha': 'etapa-03-adler-como-leer-un-libro',
    'etapa-07-primera-nota-permanente': 'etapa-03-adler-como-leer-un-libro',
    'etapa-08-schopenhauer': 'etapa-04-schopenhauer-arte-tener-razon',
    'etapa-03-falacias-familias': 'etapa-06-manual-falacias',
    'etapa-09-falacias-top-5': 'etapa-06-manual-falacias',
    'etapa-10-maquiavelo': 'etapa-09-maquiavelo-principe',
    'etapa-11-hobbes': 'etapa-11-hobbes-leviatan'
  };

  function migrateCursoTaskState() {
    const FLAG = 'lp.tasks.migrated.v2';
    if (localStorage.getItem(FLAG)) return;
    const prefix = getPathPrefix();
    Object.entries(V1_TO_V2).forEach(([oldSlug, newSlug]) => {
      const oldCandidates = [
        `lp.tasks.${prefix}/etapas/${oldSlug}/`,
        `lp.tasks.${prefix}/etapas/${oldSlug}`,
        `lp.tasks./etapas/${oldSlug}/`,
        `lp.tasks./etapas/${oldSlug}`
      ];
      let merged = false;
      for (const k of oldCandidates) {
        const raw = localStorage.getItem(k);
        if (!raw) continue;
        try {
          const old = JSON.parse(raw);
          if (old && typeof old === 'object' && Object.keys(old).length > 0) {
            const target = `lp.tasks.${prefix}/etapas/${newSlug}/`;
            const existing = loadJSON(target, {});
            saveJSON(target, Object.assign({}, existing, old));
            merged = true;
          }
        } catch (e) { /* ignore */ }
      }
      // We don't delete the old keys — kept as safety net.
      void merged;
    });
    localStorage.setItem(FLAG, '1');
  }

  // ---------- Migration v2 → v3 (insercion de Hegel en etapa 22) ----------
  // Al insertar Hegel como etapa 22, las etapas 22-84 pasaron a 23-85 (slug = num+1,
  // mismo sufijo). El slug viejo de cada etapa >=23 es (num-1) con identico sufijo.
  function migrateCursoTaskStateV3() {
    const FLAG = 'lp.tasks.migrated.v3';
    if (localStorage.getItem(FLAG)) return;
    const prefix = getPathPrefix();
    ETAPAS.forEach(e => {
      const m = e.slug.match(/^etapa-(\d+)-(.+)$/);
      if (!m) return;
      const num = parseInt(m[1], 10);
      if (num < 23) return; // 1-21 no se movieron; 22 es Hegel nuevo (sin datos previos)
      const oldSlug = `etapa-${String(num - 1).padStart(2, '0')}-${m[2]}`;
      const candidates = [
        `lp.tasks.${prefix}/etapas/${oldSlug}/`,
        `lp.tasks.${prefix}/etapas/${oldSlug}`,
        `lp.tasks./etapas/${oldSlug}/`,
        `lp.tasks./etapas/${oldSlug}`
      ];
      for (const k of candidates) {
        const raw = localStorage.getItem(k);
        if (!raw) continue;
        try {
          const old = JSON.parse(raw);
          if (old && typeof old === 'object' && Object.keys(old).length > 0) {
            const target = `lp.tasks.${prefix}/etapas/${e.slug}/`;
            const existing = loadJSON(target, {});
            saveJSON(target, Object.assign({}, existing, old));
          }
        } catch (err) { /* ignore */ }
      }
      // No borramos las claves viejas — red de seguridad.
    });
    localStorage.setItem(FLAG, '1');
  }

  // ---------- Migration v3 → v4 (insercion de Fanon y Said en etapas 56 y 57) ----------
  // Al insertar Fanon (56) y Said (57), las etapas 56-85 pasaron a 58-87 (slug = num+2,
  // mismo sufijo). El slug viejo de cada etapa >=58 es (num-2) con identico sufijo.
  function migrateCursoTaskStateV4() {
    const FLAG = 'lp.tasks.migrated.v4';
    if (localStorage.getItem(FLAG)) return;
    const prefix = getPathPrefix();
    ETAPAS.forEach(e => {
      const m = e.slug.match(/^etapa-(\d+)-(.+)$/);
      if (!m) return;
      const num = parseInt(m[1], 10);
      if (num < 58) return; // 1-55 no se movieron; 56 y 57 son nuevas (sin datos previos)
      const oldSlug = `etapa-${String(num - 2).padStart(2, '0')}-${m[2]}`;
      const candidates = [
        `lp.tasks.${prefix}/etapas/${oldSlug}/`,
        `lp.tasks.${prefix}/etapas/${oldSlug}`,
        `lp.tasks./etapas/${oldSlug}/`,
        `lp.tasks./etapas/${oldSlug}`
      ];
      for (const k of candidates) {
        const raw = localStorage.getItem(k);
        if (!raw) continue;
        try {
          const old = JSON.parse(raw);
          if (old && typeof old === 'object' && Object.keys(old).length > 0) {
            const target = `lp.tasks.${prefix}/etapas/${e.slug}/`;
            const existing = loadJSON(target, {});
            saveJSON(target, Object.assign({}, existing, old));
          }
        } catch (err) { /* ignore */ }
      }
    });
    localStorage.setItem(FLAG, '1');
  }

  // ---------- Coursera Dashboard & Accordion Timeline Rendering ----------

  function renderCourseHomepage() {
    const dashboardEl = document.getElementById('curso-dashboard');
    const timelineEl = document.getElementById('curso-syllabus-timeline');
    if (!dashboardEl && !timelineEl) return;

    // Calculate stats
    const totalTasks = ETAPAS.reduce((s, e) => s + e.total, 0);
    const completedTasks = ETAPAS.reduce((s, e) => s + Math.min(countCompletedForEtapa(e.slug), e.total), 0);
    const completedPct = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

    let completedEtapasCount = 0;
    let inProgressEtapasCount = 0;
    let notStartedEtapasCount = 0;
    let firstIncompleteEtapa = null;

    const stagesData = ETAPAS.map(e => {
      const done = Math.min(countCompletedForEtapa(e.slug), e.total);
      let state = 'not-started';
      if (done >= e.total && e.total > 0) {
        state = 'completed';
        completedEtapasCount++;
      } else if (done > 0) {
        state = 'in-progress';
        inProgressEtapasCount++;
        if (!firstIncompleteEtapa) firstIncompleteEtapa = e;
      } else {
        state = 'not-started';
        notStartedEtapasCount++;
        if (!firstIncompleteEtapa) firstIncompleteEtapa = e;
      }
      return { ...e, done, state };
    });

    if (!firstIncompleteEtapa && ETAPAS.length > 0) {
      firstIncompleteEtapa = ETAPAS[ETAPAS.length - 1]; // fallback to last stage if all done
    }

    const prefix = getPathPrefix();

    // 1. Render Dashboard
    if (dashboardEl) {
      const resumeUrl = firstIncompleteEtapa ? `${prefix}/etapas/${firstIncompleteEtapa.slug}/` : '#';
      const resumeText = firstIncompleteEtapa 
        ? `▶ Continuar — Etapa ${parseInt(firstIncompleteEtapa.slug.match(/\d+/)[0])}: ${firstIncompleteEtapa.title}`
        : '▶ Empezar curso';

      dashboardEl.innerHTML = `
        <div class="curso-dashboard-container">
          <div class="curso-dashboard-header">
            <div class="curso-dashboard-info">
              <h3 class="curso-dashboard-title">Panel de Aprendizaje</h3>
              <p class="curso-dashboard-desc">Seguí tu avance en la lectura del corpus. Tu progreso se guarda automáticamente en este navegador.</p>
              <div class="resume-btn-container">
                <a href="${resumeUrl}" class="g-btn g-btn-primary hero-cta-xl" style="width: 100%; text-align: center;">${resumeText}</a>
              </div>
            </div>
            
            <div class="curso-dashboard-stats-grid">
              <div class="curso-stat-card">
                <span class="curso-stat-number">${completedPct}%</span>
                <span class="curso-stat-label">Tareas completadas</span>
              </div>
              <div class="curso-stat-card">
                <span class="curso-stat-number">${completedEtapasCount} / ${ETAPAS.length}</span>
                <span class="curso-stat-label">Etapas completadas</span>
              </div>
              <div class="curso-stat-card">
                <span class="curso-stat-number">${inProgressEtapasCount}</span>
                <span class="curso-stat-label">Etapas en curso</span>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    // 2. Render Accordion Syllabus Timeline
    if (timelineEl) {
      const phaseNames = [
        "Fase 0 — Métodos y Herramientas",
        "Fase 1 — Filosofía Política Clásica",
        "Fase 2 — Economía Política",
        "Fase 3 — Sociología Política del Siglo XX",
        "Fase 4 — Pensamiento Iberoamericano y Decolonial",
        "Fase 5 — Síntesis Global y Geopolítica",
        "Ciclo III · M5 — Política Social",
        "Ciclo III · M6 — Estudios Culturales",
        "Cierre — Ensayos Bisagra y Tesina"
      ];

      const phases = [];
      for (let i = 0; i < phaseNames.length; i++) {
        phases.push({
          index: i,
          name: phaseNames[i],
          stages: stagesData.filter(s => s.phase === i)
        });
      }

      let html = '<div class="timeline-accordion-container">';
      let expandedFirstIncomplete = false;

      phases.forEach(p => {
        const totalStagesInPhase = p.stages.length;
        const completedStagesInPhase = p.stages.filter(s => s.state === 'completed').length;
        const inProgressStagesInPhase = p.stages.filter(s => s.state === 'in-progress').length;
        
        let phaseStateClass = '';
        let badgeText = '';
        if (completedStagesInPhase === totalStagesInPhase) {
          phaseStateClass = 'completed';
          badgeText = 'Completada';
        } else if (completedStagesInPhase > 0 || inProgressStagesInPhase > 0) {
          phaseStateClass = 'in-progress';
          badgeText = `${completedStagesInPhase}/${totalStagesInPhase} completadas`;
        } else {
          badgeText = 'Sin empezar';
        }

        const isFirstIncompletePhase = p.stages.some(s => s.state !== 'completed');
        const isInitiallyOpen = isFirstIncompletePhase && !expandedFirstIncomplete;
        if (isInitiallyOpen) {
          expandedFirstIncomplete = true;
        }

        html += `
          <div class="phase-accordion ${isInitiallyOpen ? 'open' : ''}">
            <div class="phase-accordion-header">
              <div class="phase-accordion-title-block">
                <span class="phase-accordion-num">Bloque ${p.index}</span>
                <h4 class="phase-accordion-name">${p.name}</h4>
              </div>
              <div class="phase-accordion-meta">
                <span class="phase-accordion-badge ${phaseStateClass}">${badgeText}</span>
                <span class="phase-accordion-chevron">
                  <svg viewBox="0 0 24 24"><path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"/></svg>
                </span>
              </div>
            </div>
            <div class="phase-accordion-body" style="${isInitiallyOpen ? 'max-height: 2000px;' : 'max-height: 0;'}">
              <ul class="stage-list">
        `;

        p.stages.forEach(s => {
          const num = parseInt(s.slug.match(/\d+/)[0]);
          let itemStateClass = s.state; // 'completed', 'in-progress', 'not-started'
          let progressIndicator = '';
          
          if (s.state === 'completed') {
            progressIndicator = `<span class="stage-progress-text">Completada (${s.total}/${s.total})</span><span class="stage-state-dot"></span>`;
          } else if (s.state === 'in-progress') {
            progressIndicator = `<span class="stage-progress-text">En curso (${s.done}/${s.total} tareas)</span><span class="stage-state-dot"></span>`;
          } else {
            progressIndicator = `<span class="stage-progress-text">Sin empezar (${s.total} tareas)</span><span class="stage-state-dot"></span>`;
          }

          html += `
            <li class="stage-item ${itemStateClass}">
              <a href="${prefix}/etapas/${s.slug}/" class="stage-link-block">
                <span class="stage-num-badge">${num}</span>
                <span class="stage-item-title">${s.title}</span>
              </a>
              <div class="stage-item-progress-info">
                ${progressIndicator}
              </div>
            </li>
          `;
        });

        html += `
              </ul>
            </div>
          </div>
        `;
      });
      html += '</div>';
      timelineEl.innerHTML = html;

      // Add event listeners to headers for accordion toggling
      const accordionHeaders = timelineEl.querySelectorAll('.phase-accordion-header');
      accordionHeaders.forEach(h => {
        h.addEventListener('click', () => {
          const acc = h.parentElement;
          const body = acc.querySelector('.phase-accordion-body');
          const isOpen = acc.classList.contains('open');
          
          if (isOpen) {
            body.style.maxHeight = '0px';
            acc.classList.remove('open');
          } else {
            acc.classList.add('open');
            body.style.maxHeight = body.scrollHeight + 100 + 'px';
            setTimeout(() => {
              if (acc.classList.contains('open')) {
                body.style.maxHeight = '2000px';
              }
            }, 300);
          }
        });
      });
    }
  }

  // ---------- Task list classification and decoration ----------

  function enrichTaskListsUI() {
    const items = document.querySelectorAll('.md-typeset .task-list-item');
    items.forEach(li => {
      const strong = li.querySelector('strong');
      if (!strong) return;
      const text = strong.textContent.trim().toLowerCase();
      
      let badgeInfo = null;
      if (text.includes('lectura completa')) {
        badgeInfo = { className: 'badge-reading-full', label: 'Lectura Completa' };
      } else if (text.includes('lectura selección') || text.includes('lectura de selección') || text.includes('lectura seleccion')) {
        badgeInfo = { className: 'badge-reading-select', label: 'Selección' };
      } else if (text.includes('ejercicio') || text.includes('tarea') || text.includes('examen') || text.includes('evaluación')) {
        badgeInfo = { className: 'badge-exercise', label: 'Ejercicio' };
      } else if (text.includes('redacción') || text.includes('redaccion') || text.includes('ensayo') || text.includes('tesina')) {
        badgeInfo = { className: 'badge-writing', label: 'Redacción' };
      } else if (text.includes('vídeo') || text.includes('video') || text.includes('conferencia') || text.includes('clase') || text.includes('documental')) {
        badgeInfo = { className: 'badge-video', label: 'Vídeo' };
      } else if (text.includes('ficha') || text.includes('zettelkasten')) {
        badgeInfo = { className: 'badge-zettel', label: 'Zettelkasten' };
      }
      
      if (badgeInfo && !li.querySelector('.task-badge')) {
        const badgeEl = document.createElement('span');
        badgeEl.className = `task-badge ${badgeInfo.className}`;
        badgeEl.textContent = badgeInfo.label;
        strong.parentNode.insertBefore(badgeEl, strong);
      }
    });
  }

  // ---------- Stage Metadata Emoji to Material Icons parser ----------

  function replaceIconsWithMaterial() {
    const metaBox = document.querySelector('.etapa-meta');
    if (!metaBox) return;
    
    let html = metaBox.innerHTML;
    const iconMappings = [
      { code: ':material-clock-outline:', icon: 'schedule' },
      { code: ':material-progress-check:', icon: 'assignment_turned_in' },
      { code: ':material-bookmark:', icon: 'bookmark' },
      { code: ':material-book-open-outline:', icon: 'menu_book' }
    ];
    
    iconMappings.forEach(m => {
      const escapedCode = m.code.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
      const regex = new RegExp(escapedCode, 'g');
      html = html.replace(regex, `<span class="material-icons-round">${m.icon}</span>`);
    });
    
    metaBox.innerHTML = html;
  }

  // ---------- Boot ----------

  function boot() {
    migrateCursoTaskState();
    migrateCursoTaskStateV3();
    migrateCursoTaskStateV4();
    persistTaskLists();
    setupCursoGlobalProgress();
    renderCourseHomepage();
    enrichTaskListsUI();
    replaceIconsWithMaterial();
  }

  if (typeof document$ !== 'undefined') {
    // eslint-disable-next-line no-undef
    document$.subscribe(() => boot());
  } else if (document.readyState !== 'loading') {
    boot();
  } else {
    document.addEventListener('DOMContentLoaded', boot);
  }
})();
