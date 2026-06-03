import os
import re
import json
import html

etapas_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"
files = [f for f in os.listdir(etapas_dir) if f.endswith(".md")]
files.sort()

def get_phase_info(stage_num):
    if 1 <= stage_num <= 6:
        return 0, "Fase 0 — Métodos"
    elif 7 <= stage_num <= 21:
        return 1, "Fase 1 — Filosofía clásica"
    elif 22 <= stage_num <= 29:
        return 2, "Fase 2 — Economía política"
    elif 30 <= stage_num <= 47:
        return 3, "Fase 3 — Sociopolítica s.XX"
    elif 48 <= stage_num <= 65:
        return 4, "Fase 4 — Iberoamericana"
    elif 66 <= stage_num <= 84:
        return 5, "Fase 5 — Síntesis global"
    elif 85 <= stage_num <= 89:
        return 6, "Fase 6 — Política social"
    elif 90 <= stage_num <= 97:
        return 7, "Fase 7 — Cultura"
    elif 98 <= stage_num <= 103:
        return 8, "Fase 8 — Cierre"
    return -1, "Unknown"

def md_to_html(text):
    if not text:
        return ""
    # Escape HTML
    text = html.escape(text)
    # Restore basic formatting
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank" class="dashboard-link">\1</a>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    
    # Process lists
    lines = text.split("\n")
    html_lines = []
    in_list = False
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue
        
        # Check if list item
        if line_strip.startswith("- ") or line_strip.startswith("* "):
            if not in_list:
                html_lines.append('<ul class="details-list">')
                in_list = True
            html_lines.append(f"<li>{line_strip[2:]}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<p>{line_strip}</p>")
            
    if in_list:
        html_lines.append("</ul>")
        
    return "\n".join(html_lines)

course_data = []

for file in files:
    path = os.path.join(etapas_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    num_match = re.search(r'etapa-(\d+)-', file)
    if not num_match:
        continue
    stage_num = int(num_match.group(1))
    phase_idx, phase_name = get_phase_info(stage_num)
    
    # Parse Title
    title_match = re.search(r'^#\s*(.*?)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file
    title = re.sub(r'^Etapa\s+\d+\s*[-—]\s*', '', title).strip()
    
    # Parse Quote
    quote_match = re.search(r'^>\s*(.*?)$', content, re.MULTILINE)
    quote = quote_match.group(1).strip() if quote_match else ""
    
    # Parse metadata
    hours = "N/A"
    reading_type = "Ensayo"
    meta_block_match = re.search(r'<div class="etapa-meta">(.*?)</div>', content, re.DOTALL)
    if meta_block_match:
        meta_content = meta_block_match.group(1)
        hours_match = re.search(r'clock-outline:\s*(.*?)\s*</span>|clock-outline:\s*(.*?)\s*</span>', meta_content)
        if hours_match:
            hours = next(x for x in hours_match.groups() if x is not None).strip()
        
        type_match = re.search(r'open-outline:\s*(.*?)\s*</span>|bookmark:\s*(.*?)\s*</span>', meta_content)
        if type_match:
            reading_type = next(x for x in type_match.groups() if x is not None).strip()
            
    # Parse Book Details Box
    english_title = ""
    recommended_edition = ""
    first_published = ""
    details_box_match = re.search(r'<div class="book-details-box">(.*?)</div>', content, re.DOTALL)
    if details_box_match:
        details_content = details_box_match.group(1)
        eng_match = re.search(r'Título en inglés:.*?class="book-detail-val"\s*>\s*(.*?)\s*</span>', details_content, re.DOTALL)
        if eng_match:
            english_title = eng_match.group(1).replace("<em>", "").replace("</em>", "").strip()
            
        pub_match = re.search(r'Primera publicación:.*?class="book-detail-val"\s*>\s*(.*?)\s*</span>', details_content, re.DOTALL)
        if pub_match:
            first_published = pub_match.group(1).strip()
            
        ed_match = re.search(r'Edición recomendada:.*?class="book-detail-val"\s*>\s*(.*?)\s*</span>', details_content, re.DOTALL)
        if ed_match:
            recommended_edition = ed_match.group(1).strip()
            
    # Parse Sections
    def get_section(section_name, text):
        pattern = re.compile(rf'##\s*{section_name}.*?\n(.*?)(##|$)', re.DOTALL | re.IGNORECASE)
        m = pattern.search(text)
        if m:
            return m.group(1).strip()
        return ""
        
    context = get_section("Contexto histórico y teórico", content)
    ideas = get_section("Las ideas clave.*", content)
    justification = get_section("Justificación de la.*", content)
    how_to_study = get_section("Cómo se estudia.*", content)
    resources = get_section("Recursos", content)
    
    # Parse Tasks
    tasks = []
    tasks_section = get_section("Tareas", content)
    if tasks_section:
        task_lines = re.findall(r'-\s+\[\s*([ xX]?)\s*\]\s*(.*)', tasks_section)
        for completed, label in task_lines:
            # Clean md links and bold in task labels if needed, done in js render
            tasks.append({
                "completed": completed.lower() == 'x',
                "label": label.strip()
            })
            
    course_data.append({
        "stage": stage_num,
        "title": title,
        "quote": quote,
        "hours": hours,
        "reading_type": reading_type,
        "phase_index": phase_idx,
        "phase_name": phase_name,
        "english_title": english_title,
        "first_published": first_published,
        "recommended_edition": recommended_edition,
        "context_html": md_to_html(context),
        "ideas_html": md_to_html(ideas),
        "justification_html": md_to_html(justification),
        "how_to_study_html": md_to_html(how_to_study),
        "resources_html": md_to_html(resources),
        "tasks": tasks
    })

print(f"Parsed {len(course_data)} stages successfully.")

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Itinerarios — Workspace Interactivo del Curso</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&family=Crimson+Pro:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: hsl(222, 47%, 7%);
            --bg-sidebar: hsl(222, 47%, 9%);
            --bg-workspace: hsl(222, 47%, 5%);
            --bg-card: hsl(222, 47%, 10%);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-main: hsl(210, 40%, 96%);
            --text-muted: hsl(215, 20%, 65%);
            --primary: hsl(243, 75%, 65%);
            --primary-glow: rgba(99, 102, 241, 0.15);
            --accent: hsl(150, 84%, 40%);
            --accent-glow: rgba(16, 185, 129, 0.15);
            --phase-header: hsl(222, 47%, 12%);
            --shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.5);
            --font-editorial: 'Crimson Pro', serif;
        }

        [data-theme="light"] {
            --bg-base: hsl(210, 40%, 98%);
            --bg-sidebar: hsl(210, 40%, 94%);
            --bg-workspace: hsl(0, 0%, 100%);
            --bg-card: hsl(210, 40%, 96%);
            --border-color: rgba(0, 0, 0, 0.08);
            --text-main: hsl(222, 47%, 12%);
            --text-muted: hsl(215, 16%, 45%);
            --primary: hsl(243, 75%, 55%);
            --primary-glow: rgba(79, 70, 229, 0.08);
            --accent: hsl(150, 84%, 32%);
            --accent-glow: rgba(5, 150, 105, 0.08);
            --phase-header: hsl(210, 40%, 90%);
            --shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.05);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: background-color 0.3s, color 0.3s;
        }

        /* Top Nav */
        header {
            height: 60px;
            background-color: var(--bg-sidebar);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 1.5rem;
            flex-shrink: 0;
            z-index: 10;
        }

        .header-title-area {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .header-title-area h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header-title-area span {
            color: var(--text-muted);
            font-size: 0.85rem;
            font-weight: 500;
            background: var(--bg-card);
            padding: 0.15rem 0.6rem;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .global-progress-box {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .global-progress-bar-container {
            width: 140px;
            height: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 999px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }

        .global-progress-bar {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 999px;
            transition: width 0.4s ease;
        }

        .theme-toggle-btn {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 0.4rem 0.8rem;
            border-radius: 9999px;
            color: var(--text-main);
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        .theme-toggle-btn:hover {
            background: var(--border-color);
        }

        /* Layout Grid */
        .workspace-grid {
            display: grid;
            grid-template-columns: 320px 1fr 340px;
            height: calc(100vh - 60px);
            width: 100%;
            overflow: hidden;
            flex-grow: 1;
        }

        @media (max-width: 1024px) {
            .workspace-grid {
                grid-template-columns: 280px 1fr;
            }
            .sidebar-right {
                display: none;
            }
        }

        @media (max-width: 768px) {
            .workspace-grid {
                grid-template-columns: 1fr;
            }
            .sidebar-left {
                display: none;
            }
        }

        /* Sidebar Left (Navigation) */
        .sidebar-left {
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .search-container {
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
        }

        .search-box {
            width: 100%;
            background: var(--bg-workspace);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-size: 0.85rem;
            color: var(--text-main);
            outline: none;
        }

        .search-box:focus {
            border-color: var(--primary);
        }

        .navigation-scroller {
            flex-grow: 1;
            overflow-y: auto;
            padding-bottom: 2rem;
        }

        .phase-group {
            border-bottom: 1px solid var(--border-color);
        }

        .phase-header-btn {
            width: 100%;
            background: var(--phase-header);
            border: none;
            padding: 0.8rem 1rem;
            text-align: left;
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-main);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .phase-header-btn:hover {
            background: var(--border-color);
        }

        .phase-stages-list {
            display: flex;
            flex-direction: column;
        }

        .stage-nav-item {
            width: 100%;
            background: transparent;
            border: none;
            padding: 0.6rem 1rem 0.6rem 1.5rem;
            text-align: left;
            font-size: 0.85rem;
            color: var(--text-muted);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            border-left: 2px solid transparent;
        }

        .stage-nav-item:hover {
            background: rgba(255, 255, 255, 0.02);
            color: var(--text-main);
        }

        .stage-nav-item.active {
            background: var(--primary-glow);
            color: var(--primary);
            font-weight: 600;
            border-left-color: var(--primary);
        }

        .stage-nav-item .progress-ring-mini {
            width: 16px;
            height: 16px;
            flex-shrink: 0;
        }

        /* Central Workspace */
        .workspace-panel {
            background-color: var(--bg-workspace);
            overflow-y: auto;
            padding: 2.5rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .workspace-welcome {
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            gap: 1rem;
            color: var(--text-muted);
        }

        .workspace-welcome h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            color: var(--text-main);
        }

        .stage-hero {
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .stage-hero-meta {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .hero-num-badge {
            background: var(--primary-glow);
            color: var(--primary);
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 0.75rem;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }

        .hero-phase-badge {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }

        .hero-time-badge, .hero-type-badge {
            color: var(--text-muted);
            font-size: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.2rem;
        }

        .stage-hero h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.25;
            color: var(--text-main);
        }

        .workspace-quote {
            font-family: var(--font-editorial);
            font-size: 1.25rem;
            font-style: italic;
            color: var(--text-muted);
            border-left: 3px solid var(--primary);
            padding-left: 1.5rem;
            margin: 1.5rem 0;
            line-height: 1.5;
        }

        .workspace-section {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .workspace-section h3 {
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--primary);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.3rem;
        }

        .workspace-section p {
            font-family: var(--font-editorial);
            font-size: 1.15rem;
            line-height: 1.6;
            margin-bottom: 0.8rem;
            color: var(--text-main);
        }

        .workspace-section a {
            color: var(--primary);
            text-decoration: none;
            border-bottom: 1px dashed var(--primary);
        }

        .workspace-section a:hover {
            color: var(--accent);
            border-color: var(--accent);
        }

        .details-list {
            padding-left: 1.5rem;
            margin-bottom: 1rem;
        }

        .details-list li {
            font-family: var(--font-editorial);
            font-size: 1.15rem;
            margin-bottom: 0.5rem;
            color: var(--text-main);
        }

        /* Sidebar Right (Checks & Metadata) */
        .sidebar-right {
            background-color: var(--bg-sidebar);
            border-left: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            padding: 1.5rem;
            gap: 1.5rem;
        }

        .right-section {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .right-section h3 {
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.25rem;
        }

        .book-details-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem;
            font-size: 0.85rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
            box-shadow: var(--shadow);
        }

        .book-detail-row {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .book-detail-row strong {
            color: var(--text-muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }

        .book-detail-row span {
            color: var(--text-main);
            font-weight: 500;
        }

        .checklist-wrapper {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .task-card {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 0.75rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            user-select: none;
            box-shadow: var(--shadow);
        }

        .task-card:hover {
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.03);
        }

        .task-card input[type="checkbox"] {
            margin-top: 0.2rem;
            width: 16px;
            height: 16px;
            accent-color: var(--accent);
            cursor: pointer;
        }

        .task-card.completed {
            border-color: rgba(16, 185, 129, 0.2);
            background: rgba(16, 185, 129, 0.02);
        }

        .task-card.completed .task-label {
            text-decoration: line-through;
            color: var(--text-muted);
        }

        .task-label {
            font-size: 0.85rem;
            color: var(--text-main);
            line-height: 1.4;
            flex-grow: 1;
        }

        /* SVG Rings on sidebar */
        .ring-svg {
            transform: rotate(-90deg);
        }

        .ring-bg {
            fill: none;
            stroke: var(--border-color);
            stroke-width: 3;
        }

        .ring-fill {
            fill: none;
            stroke: var(--accent);
            stroke-width: 3;
            stroke-dasharray: 44; /* 2 * PI * r (r=7) */
            stroke-dashoffset: 44;
            transition: stroke-dashoffset 0.3s ease;
        }
    </style>
</head>
<body data-theme="dark">

    <header>
        <div class="header-title-area">
            <h1>Itinerarios Académicos</h1>
            <span>Workspace</span>
        </div>
        <div class="header-right">
            <div class="global-progress-box">
                Progreso Global: <span id="global-pct-text">0%</span>
                <div class="global-progress-bar-container">
                    <div class="global-progress-bar" id="global-progress-bar"></div>
                </div>
            </div>
            <button class="theme-toggle-btn" onclick="toggleTheme()">
                <span id="theme-btn-icon">☀️</span> Modo Claro
            </button>
        </div>
    </header>

    <div class="workspace-grid">
        <!-- Sidebar Left -->
        <div class="sidebar-left">
            <div class="search-container">
                <input type="text" class="search-box" id="search-box" placeholder="Buscar etapa, autor o concepto..." oninput="handleSearch()">
            </div>
            <div class="navigation-scroller" id="nav-scroller">
                <!-- Navigation phases injected by JS -->
            </div>
        </div>

        <!-- Central Content Workspace -->
        <div class="workspace-panel" id="workspace-panel">
            <div class="workspace-welcome">
                <h2>Bienvenido al Workspace del Curso</h2>
                <p>Selecciona una etapa de la barra lateral izquierda para comenzar a estudiar.</p>
                <p style="font-size:0.85rem;">Tu progreso se guarda automáticamente en este navegador.</p>
            </div>
        </div>

        <!-- Sidebar Right -->
        <div class="sidebar-right" id="sidebar-right">
            <div class="workspace-welcome" style="text-align:center; height:auto;">
                <p>Información complementaria y checklists disponibles al seleccionar una etapa.</p>
            </div>
        </div>
    </div>

    <script>
        const COURSE_DATA = %COURSE_DATA_JSON%;
        
        let selectedStageNum = null;
        let searchQuery = "";
        let openPhases = [true, false, false, false, false, false, false, false, false]; // Phase 0 open by default
        
        function init() {
            loadCheckboxStates();
            renderNavigation();
            updateGlobalProgress();
            
            // Auto-select stage 1 if available
            selectStage(1);
        }
        
        function toggleTheme() {
            const body = document.body;
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            body.setAttribute('data-theme', newTheme);
            
            const btnIcon = document.getElementById('theme-btn-icon');
            btnIcon.textContent = newTheme === 'dark' ? '☀️' : '🌙';
            
            const btnText = document.querySelector('.theme-toggle-btn');
            btnText.innerHTML = newTheme === 'dark' ? '<span id="theme-btn-icon">☀️</span> Modo Claro' : '<span id="theme-btn-icon">🌙</span> Modo Oscuro';
        }
        
        function loadCheckboxStates() {
            COURSE_DATA.forEach(stage => {
                stage.tasks.forEach((task, tIdx) => {
                    const key = `stage-${stage.stage}-task-${tIdx}`;
                    const saved = localStorage.getItem(key);
                    if (saved !== null) {
                        task.completed = saved === 'true';
                    }
                });
            });
        }
        
        function toggleTask(stageNum, taskIdx, checkbox) {
            const stage = COURSE_DATA.find(d => d.stage === stageNum);
            const task = stage.tasks[taskIdx];
            task.completed = checkbox.checked;
            
            const key = `stage-${stageNum}-task-${taskIdx}`;
            localStorage.setItem(key, checkbox.checked);
            
            // Update UI elements
            const cardEl = document.getElementById(`task-card-${stageNum}-${taskIdx}`);
            if (checkbox.checked) {
                cardEl.classList.add('completed');
            } else {
                cardEl.classList.remove('completed');
            }
            
            updateGlobalProgress();
            updateStageProgressRing(stageNum);
        }
        
        function getStageStats(stage) {
            const total = stage.tasks.length;
            const completed = stage.tasks.filter(t => t.completed).length;
            const pct = total > 0 ? (completed / total) : 0;
            return { total, completed, pct };
        }
        
        function updateStageProgressRing(stageNum) {
            const stage = COURSE_DATA.find(d => d.stage === stageNum);
            const { pct } = getStageStats(stage);
            
            // Update sidebar ring
            const ringEl = document.getElementById(`ring-fill-${stageNum}`);
            if (ringEl) {
                const r = 7;
                const circ = 2 * Math.PI * r; // ~44
                const offset = circ - (pct * circ);
                ringEl.style.strokeDashoffset = offset;
            }
        }
        
        function updateGlobalProgress() {
            let total = 0;
            let completed = 0;
            
            COURSE_DATA.forEach(stage => {
                stage.tasks.forEach(t => {
                    total++;
                    if (t.completed) completed++;
                });
            });
            
            const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
            document.getElementById('global-pct-text').textContent = `${pct}%`;
            document.getElementById('global-progress-bar').style.width = `${pct}%`;
        }
        
        function togglePhaseCollapse(pIdx) {
            openPhases[pIdx] = !openPhases[pIdx];
            renderNavigation();
        }
        
        function handleSearch() {
            searchQuery = document.getElementById('search-box').value.toLowerCase().trim();
            renderNavigation();
        }
        
        function renderNavigation() {
            const scroller = document.getElementById('nav-scroller');
            
            // Organize stages by phase
            const phases = [];
            for (let i = 0; i < 9; i++) {
                phases.push({
                    index: i,
                    name: "",
                    stages: []
                });
            }
            
            COURSE_DATA.forEach(stage => {
                phases[stage.phase_index].stages.push(stage);
                if (!phases[stage.phase_index].name) {
                    phases[stage.phase_index].name = stage.phase_name;
                }
            });
            
            let html = '';
            
            phases.forEach(phase => {
                // Filter stages if search query is active
                let filteredStages = phase.stages;
                if (searchQuery !== "") {
                    filteredStages = phase.stages.filter(s => {
                        const searchStr = `${s.stage} ${s.title} ${s.reading_type} ${s.english_title}`.toLowerCase();
                        return searchStr.includes(searchQuery);
                    });
                }
                
                // If search query is active and phase has no matches, don't render phase
                if (searchQuery !== "" && filteredStages.length === 0) {
                    return;
                }
                
                // If search is active, keep phase open automatically
                const isOpen = searchQuery !== "" ? true : openPhases[phase.index];
                const caret = isOpen ? "▼" : "▶";
                
                html += `
                    <div class="phase-group">
                        <button class="phase-header-btn" onclick="togglePhaseCollapse(${phase.index})">
                            <span>${phase.name}</span>
                            <span style="font-size:0.7rem; color:var(--text-muted);">${caret}</span>
                        </button>
                        <div class="phase-stages-list" style="display: ${isOpen ? 'flex' : 'none'};">
                            ${filteredStages.map(s => {
                                const activeClass = s.stage === selectedStageNum ? 'active' : '';
                                const { pct } = getStageStats(s);
                                const circ = 2 * Math.PI * 7;
                                const offset = circ - (pct * circ);
                                
                                return `
                                    <button class="stage-nav-item ${activeClass}" onclick="selectStage(${s.stage})">
                                        <svg class="progress-ring-mini" viewBox="0 0 16 16">
                                            <circle class="ring-bg" cx="8" cy="8" r="7" />
                                            <circle class="ring-fill" id="ring-fill-${s.stage}" cx="8" cy="8" r="7" style="stroke-dashoffset: ${offset};" />
                                        </svg>
                                        <span style="flex-grow:1;">${s.stage}. ${s.title}</span>
                                    </button>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            });
            
            scroller.innerHTML = html;
        }
        
        function selectStage(stageNum) {
            selectedStageNum = stageNum;
            
            // Mark active item in sidebar
            const items = document.querySelectorAll('.stage-nav-item');
            items.forEach(it => it.classList.remove('active'));
            
            renderNavigation();
            
            const stage = COURSE_DATA.find(d => d.stage === stageNum);
            
            // Render central panel
            const panel = document.getElementById('workspace-panel');
            
            let quoteHtml = stage.quote ? `<div class="workspace-quote">"${stage.quote}"</div>` : '';
            
            panel.innerHTML = `
                <div class="stage-hero">
                    <div class="stage-hero-meta">
                        <span class="hero-num-badge">Etapa ${stage.stage}</span>
                        <span class="hero-phase-badge">${stage.phase_name}</span>
                        <span class="hero-time-badge">⏱️ ${stage.hours}</span>
                        <span class="hero-type-badge">📖 ${stage.reading_type}</span>
                    </div>
                    <h2>${stage.title}</h2>
                </div>
                
                ${quoteHtml}
                
                ${stage.context_html ? `
                    <div class="workspace-section">
                        <h3>Contexto Histórico y Teórico</h3>
                        ${stage.context_html}
                    </div>
                ` : ''}
                
                ${stage.ideas_html ? `
                    <div class="workspace-section">
                        <h3>Ideas Clave</h3>
                        ${stage.ideas_html}
                    </div>
                ` : ''}
                
                ${stage.justification_html ? `
                    <div class="workspace-section">
                        <h3>Justificación del Diseño</h3>
                        ${stage.justification_html}
                    </div>
                ` : ''}
            `;
            
            // Render right panel (meta & checks)
            const right = document.getElementById('sidebar-right');
            
            let specsHtml = '';
            const hasSpecs = stage.english_title || stage.recommended_edition || stage.first_published;
            if (hasSpecs) {
                specsHtml = `
                    <div class="right-section">
                        <h3>Metadatos del Libro</h3>
                        <div class="book-details-card">
                            ${stage.english_title ? `<div class="book-detail-row"><strong>Título en inglés</strong><span>${stage.english_title}</span></div>` : ''}
                            ${stage.first_published ? `<div class="book-detail-row"><strong>Primera publicación</strong><span>${stage.first_published}</span></div>` : ''}
                            ${stage.recommended_edition ? `<div class="book-detail-row"><strong>Edición recomendada</strong><span>${stage.recommended_edition}</span></div>` : ''}
                        </div>
                    </div>
                `;
            }
            
            let checklistHtml = '';
            if (stage.tasks.length > 0) {
                checklistHtml = `
                    <div class="right-section">
                        <h3>Checklist de Tareas</h3>
                        <div class="checklist-wrapper">
                            ${stage.tasks.map((task, tIdx) => {
                                const completedClass = task.completed ? 'completed' : '';
                                const checked = task.completed ? 'checked' : '';
                                return `
                                    <div class="task-card ${completedClass}" id="task-card-${stage.stage}-${tIdx}" onclick="document.getElementById('check-${stage.stage}-${tIdx}').click();">
                                        <input type="checkbox" id="check-${stage.stage}-${tIdx}" ${checked} onchange="toggleTask(${stage.stage}, ${tIdx}, this); event.stopPropagation();">
                                        <span class="task-label">${task.label}</span>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            }
            
            right.innerHTML = `
                ${specsHtml}
                ${checklistHtml}
                
                ${stage.how_to_study_html ? `
                    <div class="right-section">
                        <h3>Guía de Estudio</h3>
                        <div style="font-size:0.85rem; color:var(--text-main);">${stage.how_to_study_html}</div>
                    </div>
                ` : ''}
                
                ${stage.resources_html ? `
                    <div class="right-section">
                        <h3>Recursos y Enlaces</h3>
                        <div style="font-size:0.85rem; color:var(--text-main);">${stage.resources_html}</div>
                    </div>
                ` : ''}
            `;
            
            // Auto scroll panel top
            panel.scrollTop = 0;
            right.scrollTop = 0;
        }
        
        window.onload = init;
    </script>
</body>
</html>
"""

# Embed JSON data
html_template = html_template.replace("%COURSE_DATA_JSON%", json.dumps(course_data, ensure_ascii=False, indent=4))

# Write final file in workspace root
dashboard_path = r"c:\Users\vicen\Documents\Libros Politica - Copy\dashboard.html"
with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print("Obsidian/Notion dual-pane interactive dashboard.html compiled successfully in workspace root!")
