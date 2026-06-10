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
    # Restore links
    text = re.sub(r'&lt;a href=&quot;(.*?)&quot; target=&quot;_blank&quot;&gt;(.*?)&lt;/a&gt;', r'<a href="\1" target="_blank">\2</a>', text)
    # Restore italics in book details
    text = re.sub(r'&lt;em&gt;(.*?)&lt;/em&gt;', r'<em>\1</em>', text)
    # Markdown links [text](url)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank" class="dashboard-link">\1</a>', text)
    # Bold **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Italics *text* or _text_
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    # Checklist item (needs separate treatment, but if left in text)
    text = re.sub(r'- \[ \]\s*(.*)', r'<li>\1</li>', text)
    # Unordered list item
    text = re.sub(r'^\s*-\s+(.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\*\s+(.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
    # Bullet points groupings
    # Convert consecutive <li> into <ul>
    # Paragraphs (split by double newline)
    paragraphs = text.split("\n\n")
    html_out = []
    in_list = False
    for p in paragraphs:
        p_strip = p.strip()
        if not p_strip:
            continue
        if p_strip.startswith("<li>") or "<li>" in p_strip:
            if not in_list:
                html_out.append("<ul>")
                in_list = True
            # if lines are not all <li>, wrap lines
            lines = p_strip.split("\n")
            for line in lines:
                line_s = line.strip()
                if line_s.startswith("<li>"):
                    html_out.append(line_s)
                elif line_s:
                    if line_s.startswith("<ul>") or line_s.endswith("</ul>"):
                        html_out.append(line_s)
                    else:
                        html_out.append(f"<li>{line_s}</li>")
        else:
            if in_list:
                html_out.append("</ul>")
                in_list = False
            # Clean up linebreaks in regular paragraphs
            p_clean = p_strip.replace("\n", "<br>")
            html_out.append(f"<p>{p_clean}</p>")
    if in_list:
        html_out.append("</ul>")
    
    return "\n".join(html_out)

course_data = []

for file in files:
    path = os.path.join(etapas_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Get stage number
    num_match = re.search(r'etapa-(\d+)-', file)
    if not num_match:
        continue
    stage_num = int(num_match.group(1))
    phase_idx, phase_name = get_phase_info(stage_num)
    
    # Parse Title
    title_match = re.search(r'^#\s*(.*?)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file
    # Remove "Etapa X —" from title if present
    title = re.sub(r'^Etapa\s+\d+\s*[-—]\s*', '', title).strip()
    
    # Parse Quote
    quote_match = re.search(r'^&gt;\s*(.*?)$', content, re.MULTILINE)
    if not quote_match:
        # try markdown blockquote
        quote_match = re.search(r'^>\s*(.*?)$', content, re.MULTILINE)
    quote = quote_match.group(1).strip() if quote_match else ""
    
    # Parse metadata (Hours & Type)
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
            
    # Parse Sections using regex
    def get_section(section_name, text):
        # find ## section_name
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
            tasks.append({
                "completed": completed.lower() == 'x',
                "label": label.strip()
            })
            
    # Convert sections to HTML
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

# Compute statistics
phase_counts = [0] * 9
for c in course_data:
    phase_counts[c["phase_index"]] += 1

# Generate the dashboard.html contents
html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Itinerarios — Dashboard Interactivo del Curso</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #0b0f19;
            --bg-card: rgba(17, 25, 40, 0.75);
            --bg-card-hover: rgba(23, 33, 53, 0.85);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.15);
            --accent: #10b981;
            --accent-glow: rgba(16, 185, 129, 0.15);
            --phase-badge: #4f46e5;
            --card-expanded-bg: #131b2e;
            --shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        [data-theme="light"] {
            --bg-base: #f8fafc;
            --bg-card: rgba(255, 255, 255, 0.8);
            --bg-card-hover: rgba(255, 255, 255, 0.95);
            --border-color: rgba(0, 0, 0, 0.06);
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #4f46e5;
            --primary-glow: rgba(79, 70, 229, 0.08);
            --accent: #059669;
            --accent-glow: rgba(5, 150, 105, 0.08);
            --phase-badge: #6366f1;
            --card-expanded-bg: #ffffff;
            --shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            transition: background-color 0.3s, border-color 0.3s, color 0.3s;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            padding: 2rem;
            min-height: 100vh;
            line-height: 1.6;
        }

        header {
            max-width: 1200px;
            margin: 0 auto 2rem auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .header-left h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }

        .header-left p {
            color: var(--text-muted);
            font-size: 1rem;
        }

        .theme-toggle-btn {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 0.6rem 1.2rem;
            border-radius: 9999px;
            color: var(--text-main);
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: var(--shadow);
        }

        .theme-toggle-btn:hover {
            background: var(--bg-card-hover);
        }

        /* Stats Grid */
        .stats-container {
            max-width: 1200px;
            margin: 0 auto 2rem auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
        }

        .stat-card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            position: relative;
            overflow: hidden;
        }

        .stat-card h3 {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
        }

        .stat-card .value {
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
        }

        .stat-card .progress-container {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 999px;
            margin-top: 0.5rem;
            overflow: hidden;
        }

        .stat-card .progress-bar {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 999px;
            transition: width 0.5s ease-out;
        }

        /* Chart card */
        .chart-card {
            grid-column: span 2;
            display: flex;
            flex-direction: column;
        }

        @media (max-width: 768px) {
            .chart-card {
                grid-column: span 1;
            }
        }

        .chart-svg {
            width: 100%;
            height: 120px;
            margin-top: auto;
        }

        /* Controls Section */
        .controls-container {
            max-width: 1200px;
            margin: 0 auto 2rem auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .search-bar-wrapper {
            position: relative;
            width: 100%;
        }

        .search-input {
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            font-size: 1rem;
            color: var(--text-main);
            box-shadow: var(--shadow);
            outline: none;
        }

        .search-input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }

        .filters-wrapper {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .filter-btn {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            color: var(--text-muted);
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
        }

        .filter-btn.active, .filter-btn:hover {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        /* Stages Grid */
        .stages-grid {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 1.5rem;
        }

        @media (max-width: 480px) {
            .stages-grid {
                grid-template-columns: 1fr;
            }
        }

        .stage-card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            box-shadow: var(--shadow);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .stage-card:hover {
            transform: translateY(-4px);
            background: var(--bg-card-hover);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
        }

        .stage-card-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            position: relative;
        }

        .stage-meta-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .stage-num-badge {
            background: var(--primary-glow);
            color: var(--primary);
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-size: 0.8rem;
        }

        .phase-badge {
            background: var(--phase-badge);
            color: white;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.6rem;
            border-radius: 9999px;
        }

        .stage-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1.3;
        }

        .stage-type-hours {
            display: flex;
            gap: 1rem;
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        .stage-type-hours span {
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        .quote-block {
            padding: 1rem 1.5rem;
            background: rgba(255, 255, 255, 0.02);
            font-style: italic;
            font-size: 0.9rem;
            color: var(--text-muted);
            border-left: 3px solid var(--primary);
            margin: 0.5rem 1.5rem;
            border-radius: 0 6px 6px 0;
        }

        /* Card Expansion Content */
        .stage-card-content {
            padding: 1.5rem;
            display: none;
            flex-direction: column;
            gap: 1.5rem;
            border-top: 1px solid var(--border-color);
            background: var(--card-expanded-bg);
            cursor: default;
        }

        .stage-card.expanded {
            grid-column: 1 / -1;
            cursor: default;
        }

        .stage-card.expanded:hover {
            transform: none;
        }

        .stage-card.expanded .stage-card-content {
            display: flex;
        }

        .details-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
        }

        @media (max-width: 768px) {
            .details-grid {
                grid-template-columns: 1fr;
            }
        }

        .details-left, .details-right {
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
        }

        .details-section h4 {
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--primary);
            margin-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.25rem;
        }

        .details-section p, .details-section li {
            font-size: 0.92rem;
            color: var(--text-main);
            margin-bottom: 0.5rem;
        }

        .details-section ul {
            padding-left: 1.2rem;
        }

        .book-specs-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            font-size: 0.85rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .book-spec-item strong {
            color: var(--text-muted);
        }

        /* Checkbox list styled beautifully */
        .tasks-list {
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
        }

        .task-item {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            padding: 0.8rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            user-select: none;
        }

        .task-item:hover {
            background: rgba(99, 102, 241, 0.05);
            border-color: var(--primary);
        }

        .task-item input[type="checkbox"] {
            margin-top: 0.2rem;
            width: 18px;
            height: 18px;
            accent-color: var(--accent);
            cursor: pointer;
        }

        .task-item.completed {
            border-color: rgba(16, 185, 129, 0.3);
            background: rgba(16, 185, 129, 0.03);
        }

        .task-item.completed .task-label {
            text-decoration: line-through;
            color: var(--text-muted);
        }

        .task-label {
            font-size: 0.9rem;
            color: var(--text-main);
            flex: 1;
        }

        .close-expanded-btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            align-self: flex-end;
            margin-top: 1rem;
        }

        .close-expanded-btn:hover {
            opacity: 0.9;
        }

        .dashboard-link {
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
            border-bottom: 1px dashed var(--primary);
        }

        .dashboard-link:hover {
            color: var(--accent);
            border-color: var(--accent);
        }
    </style>
</head>
<body data-theme="dark">

    <header>
        <div class="header-left">
            <h1>Itinerarios Académicos</h1>
            <p>Dashboard Interactivo del Curso de Autoestudio (103 Etapas)</p>
        </div>
        <button class="theme-toggle-btn" onclick="toggleTheme()">
            <span id="theme-btn-icon">☀️</span> Modo Claro
        </button>
    </header>

    <div class="stats-container">
        <div class="stat-card">
            <h3>Progreso de Tareas</h3>
            <div class="value" id="stats-progress-text">0 / 0</div>
            <div class="progress-container">
                <div class="progress-bar" id="stats-progress-bar"></div>
            </div>
        </div>
        <div class="stat-card">
            <h3>Etapas Totales</h3>
            <div class="value">103</div>
            <p style="color:var(--text-muted); font-size:0.9rem;">Ordenadas en 9 fases</p>
        </div>
        <div class="stat-card">
            <h3>Tiempo de Lectura</h3>
            <div class="value" id="stats-hours">~350 h</div>
            <p style="color:var(--text-muted); font-size:0.9rem;">Horas estimadas de estudio</p>
        </div>
        <div class="stat-card chart-card">
            <h3>Distribución por Fase</h3>
            <svg class="chart-svg" viewBox="0 0 450 100" id="phase-chart-svg"></svg>
        </div>
    </div>

    <div class="controls-container">
        <div class="search-bar-wrapper">
            <input type="text" class="search-input" id="search-box" placeholder="Buscar autor, libro, concepto o etapa..." oninput="handleFilterChange()">
        </div>
        <div class="filters-wrapper" id="filters-buttons">
            <button class="filter-btn active" onclick="setFilterPhase('all')">Todas</button>
            <button class="filter-btn" onclick="setFilterPhase(0)">M0</button>
            <button class="filter-btn" onclick="setFilterPhase(1)">M1</button>
            <button class="filter-btn" onclick="setFilterPhase(2)">M2</button>
            <button class="filter-btn" onclick="setFilterPhase(3)">M3</button>
            <button class="filter-btn" onclick="setFilterPhase(4)">M4</button>
            <button class="filter-btn" onclick="setFilterPhase(5)">M5</button>
            <button class="filter-btn" onclick="setFilterPhase(6)">M6</button>
            <button class="filter-btn" onclick="setFilterPhase(7)">M7</button>
            <button class="filter-btn" onclick="setFilterPhase(8)">Cierre</button>
        </div>
    </div>

    <div class="stages-grid" id="stages-wrapper"></div>

    <script>
        // Data injected dynamically by Python script
        const COURSE_DATA = %COURSE_DATA_JSON%;
        
        let activePhaseFilter = 'all';
        let activeSearchQuery = '';

        function init() {
            // Load checkbox states from localStorage
            loadCheckboxStates();
            // Draw chart
            drawChart();
            // Render stages
            renderStages();
            // Update stats
            updateStats();
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

        function drawChart() {
            const counts = [0, 0, 0, 0, 0, 0, 0, 0, 0];
            COURSE_DATA.forEach(d => {
                counts[d.phase_index]++;
            });
            const maxVal = Math.max(...counts);
            const svg = document.getElementById('phase-chart-svg');
            
            let svgHtml = '';
            const barWidth = 35;
            const barGap = 12;
            const startX = 20;
            const chartHeight = 80;
            
            counts.forEach((c, idx) => {
                const h = (c / maxVal) * chartHeight;
                const x = startX + idx * (barWidth + barGap);
                const y = chartHeight - h + 10;
                
                svgHtml += `
                    <rect x="${x}" y="${y}" width="${barWidth}" height="${h}" rx="4" fill="var(--primary)" opacity="0.6" />
                    <text x="${x + barWidth/2}" y="${y - 4}" text-anchor="middle" font-size="9" fill="var(--text-main)" font-weight="600">${c}</text>
                    <text x="${x + barWidth/2}" y="${chartHeight + 20}" text-anchor="middle" font-size="8" fill="var(--text-muted)">M${idx}</text>
                `;
            });
            svg.innerHTML = svgHtml;
        }

        function loadCheckboxStates() {
            COURSE_DATA.forEach((stage, sIdx) => {
                stage.tasks.forEach((task, tIdx) => {
                    const key = `advanced-stage-${stage.stage}-task-${tIdx}`;
                    const saved = localStorage.getItem(key);
                    task.completed = saved === 'true';
                });
            });
        }

        function toggleTask(stageNum, taskIdx, checkbox) {
            const stage = COURSE_DATA.find(d => d.stage === stageNum);
            const task = stage.tasks[taskIdx];
            task.completed = checkbox.checked;
            
            const key = `advanced-stage-${stageNum}-task-${taskIdx}`;
            localStorage.setItem(key, checkbox.checked);
            
            const taskElement = document.getElementById(`task-item-${stageNum}-${taskIdx}`);
            if (checkbox.checked) {
                taskElement.classList.add('completed');
            } else {
                taskElement.classList.remove('completed');
            }
            
            updateStats();
        }

        function updateStats() {
            let totalTasks = 0;
            let completedTasks = 0;
            
            COURSE_DATA.forEach(stage => {
                stage.tasks.forEach(task => {
                    totalTasks++;
                    if (task.completed) {
                        completedTasks++;
                    }
                });
            });
            
            const pct = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;
            document.getElementById('stats-progress-text').textContent = `${completedTasks} / ${totalTasks} (${pct}%)`;
            document.getElementById('stats-progress-bar').style.width = `${pct}%`;
        }

        function setFilterPhase(phase) {
            activePhaseFilter = phase;
            
            const buttons = document.querySelectorAll('#filters-buttons .filter-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            const activeIndex = phase === 'all' ? 0 : phase + 1;
            buttons[activeIndex].classList.add('active');
            
            renderStages();
        }

        function handleFilterChange() {
            activeSearchQuery = document.getElementById('search-box').value.toLowerCase().trim();
            renderStages();
        }

        function toggleCardExpand(card, event) {
            // If clicked on input, label or link, don't collapse/expand
            if (event.target.tagName === 'INPUT' || event.target.tagName === 'LABEL' || event.target.tagName === 'A' || event.target.classList.contains('dashboard-link') || event.target.closest('.tasks-list')) {
                return;
            }
            
            const wasExpanded = card.classList.contains('expanded');
            
            // Collapse all
            document.querySelectorAll('.stage-card').forEach(c => c.classList.remove('expanded'));
            
            if (!wasExpanded) {
                card.classList.add('expanded');
                // Scroll card into view
                setTimeout(() => {
                    card.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            }
        }

        function renderStages() {
            const wrapper = document.getElementById('stages-wrapper');
            let html = '';
            
            const filtered = COURSE_DATA.filter(d => {
                // Phase filter
                if (activePhaseFilter !== 'all' && d.phase_index !== activePhaseFilter) {
                    return false;
                }
                // Search query
                if (activeSearchQuery !== '') {
                    const searchStr = `${d.stage} ${d.title} ${d.phase_name} ${d.reading_type} ${d.quote} ${d.english_title} ${d.recommended_edition}`.toLowerCase();
                    return searchStr.includes(activeSearchQuery);
                }
                return true;
            });

            if (filtered.length === 0) {
                wrapper.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">No se encontraron etapas con los filtros actuales.</div>`;
                return;
            }
            
            filtered.forEach(d => {
                const hasBookDetails = d.english_title || d.recommended_edition || d.first_published;
                
                let specsHtml = '';
                if (hasBookDetails) {
                    specsHtml = `
                        <div class="book-specs-box">
                            ${d.english_title ? `<div class="book-spec-item"><strong>Título inglés:</strong> <em>${d.english_title}</em></div>` : ''}
                            ${d.first_published ? `<div class="book-spec-item"><strong>Publicado:</strong> ${d.first_published}</div>` : ''}
                            ${d.recommended_edition ? `<div class="book-spec-item"><strong>Edición recomendada:</strong> ${d.recommended_edition}</div>` : ''}
                        </div>
                    `;
                }
                
                let tasksHtml = '';
                if (d.tasks.length > 0) {
                    tasksHtml = `
                        <div class="details-section">
                            <h4>Tareas a Realizar</h4>
                            <div class="tasks-list">
                                ${d.tasks.map((task, tIdx) => {
                                    const completedClass = task.completed ? 'completed' : '';
                                    const checked = task.completed ? 'checked' : '';
                                    return `
                                        <div class="task-item ${completedClass}" id="task-item-${d.stage}-${tIdx}" onclick="document.getElementById('check-${d.stage}-${tIdx}').click();">
                                            <input type="checkbox" id="check-${d.stage}-${tIdx}" ${checked} onchange="toggleTask(${d.stage}, ${tIdx}, this); event.stopPropagation();">
                                            <span class="task-label">${task.label}</span>
                                        </div>
                                    `;
                                }).join('')}
                            </div>
                        </div>
                    `;
                }

                html += `
                    <div class="stage-card" id="stage-card-${d.stage}" onclick="toggleCardExpand(this, event)">
                        <div class="stage-card-header">
                            <div class="stage-meta-row">
                                <span class="stage-num-badge">Etapa ${d.stage}</span>
                                <span class="phase-badge">${d.phase_name.split(' — ')[1] || d.phase_name}</span>
                            </div>
                            <h2 class="stage-title">${d.title}</h2>
                            <div class="stage-type-hours">
                                <span>⏱️ ${d.hours}</span>
                                <span>📖 ${d.reading_type}</span>
                            </div>
                        </div>
                        
                        ${d.quote ? `<div class="quote-block">"${d.quote}"</div>` : ''}
                        
                        <div class="stage-card-content">
                            <div class="details-grid">
                                <div class="details-left">
                                    ${d.context_html ? `<div class="details-section"><h4>Contexto Histórico y Teórico</h4>${d.context_html}</div>` : ''}
                                    ${d.ideas_html ? `<div class="details-section"><h4>Ideas Clave</h4>${d.ideas_html}</div>` : ''}
                                    ${d.justification_html ? `<div class="details-section"><h4>Justificación del Diseño</h4>${d.justification_html}</div>` : ''}
                                </div>
                                <div class="details-right">
                                    ${specsHtml}
                                    ${tasksHtml}
                                    ${d.how_to_study_html ? `<div class="details-section"><h4>Guía de Estudio</h4>${d.how_to_study_html}</div>` : ''}
                                    ${d.resources_html ? `<div class="details-section"><h4>Recursos de Soporte</h4>${d.resources_html}</div>` : ''}
                                </div>
                            </div>
                            <button class="close-expanded-btn" onclick="document.getElementById('stage-card-${d.stage}').classList.remove('expanded'); event.stopPropagation();">
                                Cerrar Etapa
                            </button>
                        </div>
                    </div>
                `;
            });
            
            wrapper.innerHTML = html;
        }

        window.onload = init;
    </script>
</body>
</html>
"""

# Replace the COURSE_DATA JSON block in the HTML string
html_template = html_template.replace("%COURSE_DATA_JSON%", json.dumps(course_data, ensure_ascii=False, indent=4))

# Write the final interactive dashboard html file in root directory
dashboard_path = r"c:\Users\vicen\Documents\Libros Politica - Copy\dashboard.html"
with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print("HTML dashboard generated successfully in root workspace!")
