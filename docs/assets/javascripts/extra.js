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

  // ---------- Tronco único — global progress (84 etapas) ----------
  // Totals are hardcoded — if you edit checkbox counts in an etapa file, update here too.
  const ETAPAS = [
    { slug: 'etapa-01-setup-sistema-de-notas',                total: 6 },
    { slug: 'etapa-02-tutorial-tomar-notas',                  total: 4 },
    { slug: 'etapa-03-adler-como-leer-un-libro',              total: 5 },
    { slug: 'etapa-04-schopenhauer-arte-tener-razon',         total: 4 },
    { slug: 'etapa-05-crashcourse-falacias',                  total: 4 },
    { slug: 'etapa-06-manual-falacias',                       total: 5 },
    { slug: 'etapa-07-platon-apologia',                       total: 4 },
    { slug: 'etapa-08-aristoteles-politica',                  total: 4 },
    { slug: 'etapa-09-maquiavelo-principe',                   total: 5 },
    { slug: 'etapa-10-yale-maquiavelo',                       total: 3 },
    { slug: 'etapa-11-hobbes-leviatan',                       total: 5 },
    { slug: 'etapa-12-yale-hobbes',                           total: 3 },
    { slug: 'etapa-13-rousseau-contrato-social',              total: 5 },
    { slug: 'etapa-14-yale-rousseau',                         total: 3 },
    { slug: 'etapa-15-mill-sobre-la-libertad',                total: 5 },
    { slug: 'etapa-16-sandel-justice',                        total: 3 },
    { slug: 'etapa-17-locke-segundo-tratado',                 total: 5 },
    { slug: 'etapa-18-tocqueville-democracia-en-america',     total: 5 },
    { slug: 'etapa-19-pocock-momento-maquiavelico',           total: 5 },
    { slug: 'etapa-20-chang-economia-99',                     total: 4 },
    { slug: 'etapa-21-smith-riqueza-naciones',                total: 5 },
    { slug: 'etapa-22-marx-capital',                          total: 5 },
    { slug: 'etapa-23-harvey-reading-marx',                   total: 3 },
    { slug: 'etapa-24-mariategui-7-ensayos',                  total: 4 },
    { slug: 'etapa-25-weber-politica-vocacion',               total: 4 },
    { slug: 'etapa-26-foucault',                              total: 5 },
    { slug: 'etapa-27-rawls-teoria-justicia',                 total: 5 },
    { slug: 'etapa-28-berlin-dos-conceptos',                  total: 4 },
    { slug: 'etapa-29-habermas-esfera-publica',               total: 4 },
    { slug: 'etapa-30-lenin-imperialismo',                    total: 4 },
    { slug: 'etapa-31-gramsci-cuadernos',                     total: 5 },
    { slug: 'etapa-32-hayek-camino-servidumbre',              total: 4 },
    { slug: 'etapa-33-popper-sociedad-abierta',               total: 5 },
    { slug: 'etapa-34-nozick-anarquia-estado-utopia',         total: 4 },
    { slug: 'etapa-35-bolivar-carta-jamaica',                 total: 4 },
    { slug: 'etapa-36-marti-nuestra-america',                 total: 4 },
    { slug: 'etapa-37-rodo-ariel',                            total: 4 },
    { slug: 'etapa-38-vasconcelos-raza-cosmica',              total: 4 },
    { slug: 'etapa-39-paz-laberinto-soledad',                 total: 5 },
    { slug: 'etapa-40-galeano-venas-abiertas',                total: 5 },
    { slug: 'etapa-41-bueno-mito-izquierda',                  total: 5 },
    { slug: 'etapa-42-echeverria-modernidad-blanquitud',      total: 4 },
    { slug: 'etapa-43-dussel-1492',                           total: 5 },
    { slug: 'etapa-44-quijano-colonialidad',                  total: 3 },
    { slug: 'etapa-45-cusicanqui-chixinakax',                 total: 4 },
    { slug: 'etapa-46-freire-pedagogia-oprimido',             total: 5 },
    { slug: 'etapa-47-gutierrez-teologia-liberacion',         total: 4 },
    { slug: 'etapa-48-gonzalez-feminismo-afrolatinoamericano',total: 3 },
    { slug: 'etapa-49-lugones-heterosexualismo',              total: 3 },
    { slug: 'etapa-50-gago-potencia-feminista',               total: 4 },
    { slug: 'etapa-51-segato-guerra-mujeres',                 total: 4 },
    { slug: 'etapa-52-wallerstein-sistemas-mundo',            total: 4 },
    { slug: 'etapa-53-mearsheimer-great-power',               total: 5 },
    { slug: 'etapa-54-agamben',                               total: 4 },
    { slug: 'etapa-55-mbembe-necropolitica',                  total: 4 },
    { slug: 'etapa-56-novela-politica',                       total: 3 },
    { slug: 'etapa-57-relectura-activa',                      total: 3 },
    { slug: 'etapa-58-gandhi-hind-swaraj',                    total: 4 },
    { slug: 'etapa-59-confucio-analectas',                    total: 4 },
    { slug: 'etapa-60-sen-identidad-violencia',               total: 4 },
    { slug: 'etapa-61-hardt-negri-imperio',                   total: 5 },
    { slug: 'etapa-62-wang-hui',                              total: 4 },
    { slug: 'etapa-63-maruyama',                              total: 4 },
    { slug: 'etapa-64-ambedkar-annihilation-caste',           total: 4 },
    { slug: 'etapa-65-ensayo-final',                          total: 5 },
    { slug: 'etapa-66-grabacion-final',                       total: 4 },
    { slug: 'etapa-67-marshall-ciudadania',                   total: 4 },
    { slug: 'etapa-68-polanyi-gran-transformacion',           total: 5 },
    { slug: 'etapa-69-esping-andersen',                       total: 4 },
    { slug: 'etapa-70-filgueira-universalismo-basico',        total: 4 },
    { slug: 'etapa-71-tesina-m5',                             total: 5 },
    { slug: 'etapa-72-williams-marxismo-literatura',          total: 4 },
    { slug: 'etapa-73-benjamin-obra-arte',                    total: 4 },
    { slug: 'etapa-74-bourdieu-distincion',                   total: 5 },
    { slug: 'etapa-75-hall-encoding-decoding',                total: 3 },
    { slug: 'etapa-76-garcia-canclini-culturas-hibridas',     total: 4 },
    { slug: 'etapa-77-martin-barbero',                        total: 4 },
    { slug: 'etapa-78-zuboff-vigilancia',                     total: 5 },
    { slug: 'etapa-79-ensayo-neoliberalismo',                 total: 4 },
    { slug: 'etapa-80-ensayo-ciudadania',                     total: 4 },
    { slug: 'etapa-81-ensayo-trabajo',                        total: 4 },
    { slug: 'etapa-82-ensayo-estado',                         total: 4 },
    { slug: 'etapa-83-ensayo-desigualdad',                    total: 4 },
    { slug: 'etapa-84-tesina-final',                          total: 6 }
  ];

  function etapaPathCandidates(slug) {
    const prefixes = ['', '/Libros-Politica'];
    const paths = [];
    prefixes.forEach(p => {
      paths.push(`${p}/etapas/${slug}/`);
      paths.push(`${p}/etapas/${slug}`);
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
    const prefix = location.pathname.startsWith('/Libros-Politica') ? '/Libros-Politica' : '';
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

  // ---------- Boot ----------

  function boot() {
    migrateCursoTaskState();
    persistTaskLists();
    setupCursoGlobalProgress();
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
