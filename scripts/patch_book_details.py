import os
import re

docs_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"

book_data = {
    "etapa-03-adler-como-leer-un-libro.md": {
        "titulo_ingles": "How to Read a Book",
        "primera_publicacion": "1940",
        "edicion_recomendada": "Touchstone/Simon & Schuster / *Cómo leer un libro* (Debate)"
    },
    "etapa-04-schopenhauer-arte-tener-razon.md": {
        "titulo_ingles": "The Art of Being Right (also published as *The Art of Controversy*)",
        "primera_publicacion": "1831 (publicado póstumamente en 1864)",
        "edicion_recomendada": "Gibson Square / *El arte de tener razón* (Alianza Editorial)"
    },
    "etapa-07-platon-apologia.md": {
        "titulo_ingles": "Apology of Socrates (or *Apology*)",
        "primera_publicacion": "c. 399 a.C.",
        "edicion_recomendada": "Hackett Publishing (*Plato: Complete Works*) / *Apología de Sócrates* (Gredos)"
    },
    "etapa-08-aristoteles-politica.md": {
        "titulo_ingles": "Politics",
        "primera_publicacion": "c. 350 a.C.",
        "edicion_recomendada": "Oxford World's Classics / *Política* (Gredos)"
    },
    "etapa-09-maquiavelo-principe.md": {
        "titulo_ingles": "The Prince",
        "primera_publicacion": "1513 (escrito), 1532 (publicado)",
        "edicion_recomendada": "University of Chicago Press (trad. Harvey Mansfield) / *El Príncipe* (Alianza Editorial)"
    },
    "etapa-11-hobbes-leviatan.md": {
        "titulo_ingles": "Leviathan",
        "primera_publicacion": "1651",
        "edicion_recomendada": "Cambridge University Press (ed. Richard Tuck) / *Leviatán* (Alianza Editorial / Tecnos)"
    },
    "etapa-13-rousseau-contrato-social.md": {
        "titulo_ingles": "The Social Contract",
        "primera_publicacion": "1762",
        "edicion_recomendada": "Cambridge University Press / *El contrato social* (Alianza Editorial)"
    },
    "etapa-15-mill-sobre-la-libertad.md": {
        "titulo_ingles": "On Liberty",
        "primera_publicacion": "1859",
        "edicion_recomendada": "Oxford World's Classics / *Sobre la libertad* (Alianza Editorial)"
    },
    "etapa-17-locke-segundo-tratado.md": {
        "titulo_ingles": "Second Treatise of Government",
        "primera_publicacion": "1689",
        "edicion_recomendada": "Cambridge University Press (ed. Peter Laslett) / *Segundo Tratado sobre el Gobierno Civil* (Alianza Editorial)"
    },
    "etapa-18-tocqueville-democracia-en-america.md": {
        "titulo_ingles": "Democracy in America",
        "primera_publicacion": "Vol. I (1835), Vol. II (1840)",
        "edicion_recomendada": "University of Chicago Press (trad. Harvey Mansfield & Delba Winthrop) / *La democracia en América* (Alianza / Trotta)"
    },
    "etapa-19-pocock-momento-maquiavelico.md": {
        "titulo_ingles": "The Machiavellian Moment",
        "primera_publicacion": "1975",
        "edicion_recomendada": "Princeton University Press / *El momento maquiavélico* (Editorial Tecnos)"
    },
    "etapa-20-chang-economia-99.md": {
        "titulo_ingles": "Economics: The User's Guide",
        "primera_publicacion": "2014",
        "edicion_recomendada": "Pelican Books / *Economía: Instrucciones de uso* (Debate)"
    },
    "etapa-21-smith-riqueza-naciones.md": {
        "titulo_ingles": "The Wealth of Nations",
        "primera_publicacion": "1776",
        "edicion_recomendada": "University of Chicago Press (ed. Edwin Cannan) / *La riqueza de las naciones* (Alianza Editorial)"
    },
    "etapa-22-hegel-fenomenologia.md": {
        "titulo_ingles": "Phenomenology of Spirit",
        "primera_publicacion": "1807",
        "edicion_recomendada": "Oxford University Press (trad. A.V. Miller) / *Fenomenología del espíritu* (FCE)"
    },
    "etapa-23-marx-capital.md": {
        "titulo_ingles": "Capital: Volume I",
        "primera_publicacion": "1867",
        "edicion_recomendada": "Penguin Classics (trad. Ben Fowkes) / *El Capital: Tomo I* (Siglo XXI Editores)"
    },
    "etapa-25-mariategui-7-ensayos.md": {
        "titulo_ingles": "Seven Interpretive Essays on Peruvian Reality",
        "primera_publicacion": "1928",
        "edicion_recomendada": "University of Texas Press (trad. Marjory Urquidi) / *7 ensayos de interpretación de la realidad peruana* (Biblioteca Ayacucho / Amauta)"
    },
    "etapa-26-weber-politica-vocacion.md": {
        "titulo_ingles": "Politics as a Vocation (published in *From Max Weber*)",
        "primera_publicacion": "1919",
        "edicion_recomendada": "Hackett Publishing (*The Vocation Lectures*) / *La política como vocación* (Alianza Editorial)"
    },
    "etapa-27-foucault.md": {
        "titulo_ingles": "Discipline and Punish: The Birth of the Prison",
        "primera_publicacion": "1975",
        "edicion_recomendada": "Vintage Books / *Vigilar y castigar: Nacimiento de la prisión* (Siglo XXI Editores)"
    },
    "etapa-28-rawls-teoria-justicia.md": {
        "titulo_ingles": "A Theory of Justice",
        "primera_publicacion": "1971",
        "edicion_recomendada": "Harvard University Press (Revised Edition) / *Teoría de la justicia* (Fondo de Cultura Económica)"
    },
    "etapa-30-habermas-esfera-publica.md": {
        "titulo_ingles": "The Structural Transformation of the Public Sphere",
        "primera_publicacion": "1962",
        "edicion_recomendada": "MIT Press / *Historia y crítica de la opinión pública* (Editorial Gustavo Gili)"
    },
    "etapa-31-lenin-imperialismo.md": {
        "titulo_ingles": "Imperialism, the Highest Stage of Capitalism",
        "primera_publicacion": "1917",
        "edicion_recomendada": "International Publishers / *El imperialismo, fase superior del capitalismo* (Akal / Progreso)"
    },
    "etapa-32-gramsci-cuadernos.md": {
        "titulo_ingles": "Prison Notebooks",
        "primera_publicacion": "Escritos entre 1929-1935 (publicados póstumamente 1948-1951)",
        "edicion_recomendada": "International Publishers (trad. Quintin Hoare) / *Cuadernos de la cárcel* (Ediciones Era)"
    },
    "etapa-33-hayek-camino-servidumbre.md": {
        "titulo_ingles": "The Road to Serfdom",
        "primera_publicacion": "1944",
        "edicion_recomendada": "University of Chicago Press (Definitive Edition) / *Camino de servidumbre* (Alianza Editorial)"
    },
    "etapa-34-popper-sociedad-abierta.md": {
        "titulo_ingles": "The Open Society and Its Enemies",
        "primera_publicacion": "1945",
        "edicion_recomendada": "Princeton University Press / *La sociedad abierta y sus enemigos* (Paidós)"
    },
    "etapa-35-nozick-anarquia-estado-utopia.md": {
        "titulo_ingles": "Anarchy, State, and Utopia",
        "primera_publicacion": "1974",
        "edicion_recomendada": "Basic Books / *Anarquía, Estado y utopía* (Fondo de Cultura Económica)"
    },
    "etapa-38-rodo-ariel.md": {
        "titulo_ingles": "Ariel",
        "primera_publicacion": "1900",
        "edicion_recomendada": "University of Texas Press (trad. Margaret Sayers Peden) / *Ariel* (Colección Cátedra / Biblioteca Ayacucho)"
    },
    "etapa-39-vasconcelos-raza-cosmica.md": {
        "titulo_ingles": "The Cosmic Race",
        "primera_publicacion": "1925",
        "edicion_recomendada": "Johns Hopkins University Press (trad. Didier T. Jaén) / *La raza cósmica* (Espasa-Calpe)"
    },
    "etapa-40-paz-laberinto-soledad.md": {
        "titulo_ingles": "The Labyrinth of Solitude",
        "primera_publicacion": "1950",
        "edicion_recomendada": "Grove Press (trad. Lysander Kemp) / *El laberinto de la soledad* (Cátedra / Fondo de Cultura Económica)"
    },
    "etapa-41-galeano-venas-abiertas.md": {
        "titulo_ingles": "Open Veins of Latin America: Five Centuries of the Pillage of a Continent",
        "primera_publicacion": "1971",
        "edicion_recomendada": "Monthly Review Press (trad. Cedric Belfrage) / *Las venas abiertas de América Latina* (Siglo XXI Editores)"
    },
    "etapa-42-bueno-mito-izquierda.md": {
        "titulo_ingles": "The Myth of the Left (No official English translation)",
        "primera_publicacion": "2003",
        "edicion_recomendada": "Ediciones Pentalfa (Original en español)"
    },
    "etapa-43-echeverria-modernidad-blanquitud.md": {
        "titulo_ingles": "Modernity and Whiteness",
        "primera_publicacion": "2010",
        "edicion_recomendada": "Ediciones Era (Original en español)"
    },
    "etapa-44-dussel-1492.md": {
        "titulo_ingles": "The Invention of the Americas: Eclipse of \"the Other\" and the Myth of Modernity",
        "primera_publicacion": "1992",
        "edicion_recomendada": "Continuum (trad. Michael D. Barber) / *1492: El encubrimiento del Otro* (Plural Editores)"
    },
    "etapa-46-cusicanqui-chixinakax.md": {
        "titulo_ingles": "Ch'ixinakax utxiwa: On Decolonizing Practices and Discourses",
        "primera_publicacion": "2010",
        "edicion_recomendada": "Tinta Limón (Original en español)"
    },
    "etapa-47-freire-pedagogia-oprimido.md": {
        "titulo_ingles": "Pedagogy of the Oppressed",
        "primera_publicacion": "1968 (en manuscrito portugués), 1970 (primera publicación oficial)",
        "edicion_recomendada": "Continuum (trad. Myra Bergman Ramos) / *Pedagogía del oprimido* (Siglo XXI Editores)"
    },
    "etapa-48-gutierrez-teologia-liberacion.md": {
        "titulo_ingles": "A Theology of Liberation: History, Politics, and Salvation",
        "primera_publicacion": "1971",
        "edicion_recomendada": "Orbis Books (trad. Caridad Inda & John Eagleton) / *Teología de la liberación: Perspectivas* (CEP / Centro de Estudios y Publicaciones)"
    },
    "etapa-51-gago-potencia-feminista.md": {
        "titulo_ingles": "Feminist International: How to Change Everything",
        "primera_publicacion": "2019",
        "edicion_recomendada": "Verso Books (trad. Liz Mason-Deese) / *La potencia feminista, o el deseo de cambiarlo todo* (Tinta Limón)"
    },
    "etapa-52-segato-guerra-mujeres.md": {
        "titulo_ingles": "The War Against Women",
        "primera_publicacion": "2016",
        "edicion_recomendada": "Prometeo Libros (Original en español)"
    },
    "etapa-53-wallerstein-sistemas-mundo.md": {
        "titulo_ingles": "World-Systems Analysis: An Introduction",
        "primera_publicacion": "2004",
        "edicion_recomendada": "Duke University Press / *Análisis de sistemas-mundo: Una introducción* (Siglo XXI Editores)"
    },
    "etapa-54-mearsheimer-great-power.md": {
        "titulo_ingles": "The Tragedy of Great Power Politics",
        "primera_publicacion": "2001",
        "edicion_recomendada": "W. W. Norton & Company / *La tragedia de la política de las grandes potencias* (Malpaso)"
    },
    "etapa-55-agamben.md": {
        "titulo_ingles": "Homo Sacer: Sovereign Power and Bare Life",
        "primera_publicacion": "1995",
        "edicion_recomendada": "Stanford University Press / *Homo Sacer: El poder soberano y la nuda vida* (Pre-Textos)"
    },
    "etapa-56-fanon-condenados-tierra.md": {
        "titulo_ingles": "The Wretched of the Earth",
        "primera_publicacion": "1961",
        "edicion_recomendada": "Grove Press (trad. Richard Philcox) / *Los condenados de la tierra* (Fondo de Cultura Económica)"
    },
    "etapa-57-said-orientalismo.md": {
        "titulo_ingles": "Orientalism",
        "primera_publicacion": "1978",
        "edicion_recomendada": "Pantheon Books / *Orientalismo* (Debolsillo)"
    },
    "etapa-61-gandhi-hind-swaraj.md": {
        "titulo_ingles": "Hind Swaraj or Indian Home Rule",
        "primera_publicacion": "1909",
        "edicion_recomendada": "Cambridge University Press (ed. Anthony J. Parel) / *Hind Swaraj o el autogobierno de la India* (Navajivan Trust)"
    },
    "etapa-62-confucio-analectas.md": {
        "titulo_ingles": "The Analects of Confucius (or *The Analects*)",
        "primera_publicacion": "c. 500 - 400 a.C.",
        "edicion_recomendada": "Penguin Classics (trad. D.C. Lau) / *Analectas* (EDAF / Alianza Editorial)"
    },
    "etapa-63-sen-identidad-violencia.md": {
        "titulo_ingles": "Identity and Violence: The Illusion of Destiny",
        "primera_publicacion": "2006",
        "edicion_recomendada": "W. W. Norton & Company / *Identidad y violencia: La ilusión del destino* (Taurus)"
    },
    "etapa-64-hardt-negri-imperio.md": {
        "titulo_ingles": "Empire",
        "primera_publicacion": "2000",
        "edicion_recomendada": "Harvard University Press / *Imperio* (Paidós)"
    },
    "etapa-65-wang-hui.md": {
        "titulo_ingles": "China's New Order",
        "primera_publicacion": "2003",
        "edicion_recomendada": "Harvard University Press / *El nuevo orden de China* (Fondo de Cultura Económica)"
    },
    "etapa-66-maruyama.md": {
        "titulo_ingles": "Studies in the Intellectual History of Tokugawa Japan",
        "primera_publicacion": "1952 (en japonés)",
        "edicion_recomendada": "Princeton University Press (trad. Mikiso Hane)"
    },
    "etapa-67-ambedkar-annihilation-caste.md": {
        "titulo_ingles": "Annihilation of Caste",
        "primera_publicacion": "1936",
        "edicion_recomendada": "Verso Books (Definitive Annotated Critical Edition, ed. S. Anand)"
    },
    "etapa-71-polanyi-gran-transformacion.md": {
        "titulo_ingles": "The Great Transformation",
        "primera_publicacion": "1944",
        "edicion_recomendada": "Beacon Press / *La gran transformación* (Fondo de Cultura Económica)"
    },
    "etapa-72-esping-andersen.md": {
        "titulo_ingles": "The Three Worlds of Welfare Capitalism",
        "primera_publicacion": "1990",
        "edicion_recomendada": "Princeton University Press / *Los tres mundos del Estado del bienestar* (Institución Alfonso el Magnánimo)"
    },
    "etapa-73-filgueira-universalismo-basico.md": {
        "titulo_ingles": "Basic Universalism in Latin America",
        "primera_publicacion": "2004",
        "edicion_recomendada": "Documento de Trabajo del BID (Original en español)"
    },
    "etapa-75-williams-marxismo-literatura.md": {
        "titulo_ingles": "Marxism and Literature",
        "primera_publicacion": "1977",
        "edicion_recomendada": "Oxford University Press / *Marxismo y literatura* (Editorial Península)"
    },
    "etapa-77-bourdieu-distincion.md": {
        "titulo_ingles": "Distinction: A Social Critique of the Judgement of Taste",
        "primera_publicacion": "1979",
        "edicion_recomendada": "Harvard University Press (trad. Richard Nice) / *La distinción: Criterios y bases sociales del gusto* (Taurus)"
    },
    "etapa-79-garcia-canclini-culturas-hibridas.md": {
        "titulo_ingles": "Hybrid Cultures: Strategies for Entering and Leaving Modernity",
        "primera_publicacion": "1989",
        "edicion_recomendada": "University of Minnesota Press (trad. Christopher L. Chiappari & Silvia L. López) / *Culturas híbridas* (Grijalbo / FCE)"
    },
    "etapa-80-martin-barbero.md": {
        "titulo_ingles": "Communication, Culture and Hegemony: From the Media to Mediations",
        "primera_publicacion": "1987",
        "edicion_recomendada": "SAGE Publications (trad. Elizabeth Fox & Robert A. White) / *De los medios a las mediaciones* (Gustavo Gili / Convenio Andrés Bello)"
    },
    "etapa-81-zuboff-vigilancia.md": {
        "titulo_ingles": "The Age of Surveillance Capitalism",
        "primera_publicacion": "2019",
        "edicion_recomendada": "PublicAffairs / *La era del capitalismo de la vigilancia* (Ediciones Paidós)"
    }
}

def clean_html(text):
    # Remove existing book-details-box using robust regex that counts closing divs
    text = re.sub(r'<div class="book-details-box">.*?</div>\s*</div>\s*</div>\s*</div>\n*', '', text, flags=re.DOTALL)
    return text

print("Iniciando inyección de metadatos de libros (completo y fuera del progress box)...")
success_count = 0

# El patrón exacto de curso-progress-box que incluye la etiqueta de cierre final </div>
progress_box_pattern = r'(<div class="curso-progress-box"[^>]*>.*?<div class="g-progress">.*?</div>\s*</div>\s*</div>)'

for filename, info in book_data.items():
    filepath = os.path.join(docs_dir, filename)
    if not os.path.exists(filepath):
        print(f"[WARN] No se encontró el archivo {filename}")
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Asegurar normalización de fines de línea
    content = content.replace("\r\n", "\n")
    
    content = clean_html(content)
    
    # Preparar el bloque HTML
    html_block = f"""<div class="book-details-box">
  <div class="book-detail-item">
    <span class="book-detail-label">Título en inglés:</span>
    <span class="book-detail-val"><em>{info['titulo_ingles']}</em></span>
  </div>
  <div class="book-detail-item">
    <span class="book-detail-label">Primera publicación:</span>
    <span class="book-detail-val">{info['primera_publicacion']}</span>
  </div>
  <div class="book-detail-item">
    <span class="book-detail-label">Edición recomendada:</span>
    <span class="book-detail-val">{info['edicion_recomendada']}</span>
  </div>
</div>"""

    # Buscar el bloque curso-progress-box con regex robusto que incluye el cierre final
    match = re.search(progress_box_pattern, content, re.DOTALL)
    if match:
        matched_str = match.group(1)
        new_str = matched_str + "\n\n" + html_block
        content = content.replace(matched_str, new_str, 1)
        
        with open(filepath, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        success_count += 1
    else:
        print(f"[ERROR] No se pudo encontrar el bloque curso-progress-box en {filename}")

print(f"\nProceso finalizado. Se inyectaron metadatos en {success_count} de {len(book_data)} archivos.")
