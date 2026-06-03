import os
import re

etapas_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"

# Define the dictionary of justifications
justifications = {
    # PHASE 0
    "etapa-03-adler-como-leer-un-libro": {
        "type": "selective",
        "why_only_these": "Los capítulos 1 a 4 y la sección analítica (Caps. 5-7, 11) explican la distinción fundamental entre adquirir información y aumentar la comprensión, establecen las bases de los cuatro niveles de lectura (elemental, inspeccional, analítica y sintópica) y detallan las reglas prácticas indispensables para desmenuzar activamente el argumento de un autor.",
        "why_skip_rest": "El resto del volumen se dispersa en pautas metodológicas hiperespecíficas sobre cómo abordar géneros literarios particulares, como la poesía lírica, obras teatrales clásicas, novelas de ficción o tratados de matemáticas puras. Si bien son útiles para una formación humanística general, carecen de relevancia para el objetivo de este programa de estudio, que se enfoca en la apropiación analítica de tratados de teoría social.",
        "why_read_complete": "Leer la obra completa es aconsejable si deseas perfeccionar tu técnica lectora en áreas fuera de la teoría del Estado (como la literatura de ficción, la poesía o la divulgación científica) o si quieres dominar la lectura sintópica para realizar investigaciones académicas comparativas complejas."
    },
    "etapa-04-schopenhauer-arte-tener-razon": {
        "type": "complete",
        "why_complete": "Al ser un tratado sumamente breve y directo (aproximadamente 100 páginas), su lectura íntegra es necesaria para captar el flujo deductivo y la ironía cínica con la que Schopenhauer describe las 38 estratagemas dialécticas de la retórica adversarial.",
        "why_no_select": "Cada estratagema es un caso de estudio lógico independiente. Saltar alguna impediría tener el catálogo completo de falacias retóricas para el análisis de debates políticos en vivo.",
        "if_selective": "Enfócate en la base conceptual del prólogo (la distinción entre verdad objetiva y victoria dialéctica) y en las estratagemas más comunes de la discusión política contemporánea: #1 (ampliación), #2 (homonimia), #8 (provocar la cólera), #18 (interrupción), #30 (ad verecundiam) y #38 (ad hominem)."
    },
    # PHASE 1
    "etapa-08-aristoteles-politica": {
        "type": "selective",
        "why_only_these": "Libro I (Caps. 1-2, 3-7), Libro III (Caps. 1-9) y Libro VII (Caps. 1-3, 13-14). Contiene la fundamentación del ser humano como *zoon politikon* (animal político), la legitimación clásica de la esclavitud, la tipología formal de las seis formas de gobierno y el diseño moral y físico de la *polis* ideal.",
        "why_skip_rest": "Los libros IV, V, VI y VIII son estudios empíricos descriptivos de las poleis griegas de su época, descripciones de revoluciones específicas de la antigüedad y de la educación musical y gimnástica que carecen de peso conceptual directo para la teoría política del Estado contemporáneo.",
        "why_read_complete": "Es indispensable para historiadores del pensamiento clásico y de las instituciones antiguas, ya que permite comprender el método inductivo y comparado de Aristóteles a través del análisis de las constituciones reales de más de 150 ciudades-estado de la antigüedad."
    },
    "etapa-09-maquiavelo-principe": {
        "type": "complete",
        "why_complete": "Es una obra maestra literaria y conceptual sumamente corta. Su brevedad permite asimilar el método realista crudo y la argumentación continua sobre la conquista, conservación y pérdida de los principados en el Renacimiento italiano.",
        "why_no_select": "Omitir capítulos rompería el hilo argumental deductivo que vincula la tipología de principados con la milicia y los consejos finales al soberano sobre cómo conservar su poder.",
        "if_selective": "Enfócate en los capítulos 15 a 19 (las virtudes morales del príncipe, si es mejor ser amado o temido, y la evitación del odio) y el capítulo 25 (el papel de la *fortuna* y la *virtù* en la política humana)."
    },
    "etapa-11-hobbes-leviatan": {
        "type": "selective",
        "why_only_these": "Parte I (Caps. 6, 10, 11, 13, 14-15, 16) y Parte II (Caps. 17-19, 21, 26, 29-30). Sientan las bases de la antropología materialista (el miedo a la muerte violenta como motor racional), el experimento mental del estado de naturaleza, la creación del soberano por contrato social, y los límites de la obediencia del súbdito.",
        "why_skip_rest": "Las Partes III (\"De un Estado cristiano\") y IV (\"Del reino de las tinieblas\") representan casi dos tercios del libro. Consisten en exégesis bíblicas minuciosas del Antiguo y Nuevo Testamento con el fin de neutralizar el poder de la Iglesia Romana frente al monarca inglés, debates teológicos ajenos a la teoría constitucional contemporánea.",
        "why_read_complete": "Es sumamente valioso para comprender la relación histórica entre teología y política (teología política). Permite desmitificar la idea de que Hobbes era un ateo secular y entender cómo estructuraba su justificación racional del absolutismo sobre bases cristianas reformadas."
    },
    "etapa-13-rousseau-contrato-social": {
        "type": "selective",
        "why_only_these": "Libros I, II y III completos, y Libro IV capítulos 1-2 y 8. Estructuran la soberanía popular indivisible, la distinción entre Estado y Gobierno, la formulación de la voluntad general y la propuesta de la \"religión civil\".",
        "why_skip_rest": "La mayor parte del Libro IV se detiene en un exhaustivo análisis descriptivo de las instituciones de la antigua República Romana (comicios, tribunado, censura, dictadura) que Rousseau copia de Montesquieu, lo cual resulta tedioso y desvía la atención de la teoría pura del pacto.",
        "why_read_complete": "Es aconsejable para investigadores de la recepción del republicanismo clásico en el siglo XVIII y para comprender cómo Rousseau intentaba operativizar sus teorías abstractas en instituciones del mundo real a partir de ejemplos históricos."
    },
    "etapa-15-mill-sobre-la-libertad": {
        "type": "selective",
        "why_only_these": "*Sobre la libertad* se lee completo debido a su brevedad e importancia fundamental. De *El utilitarismo*, se seleccionan los primeros capítulos para sentar las bases morales del principio de mayor felicidad (utilidad social) como sustento de las libertades que Mill defiende.",
        "why_skip_rest": "Los capítulos finales de *El utilitarismo* (Caps. 3 a 5) se adentran en debates técnicos de la filosofía moral victoriana sobre el origen psicológico de la idea de justicia y controversias éticas con pensadores intuicionistas británicos de su época.",
        "why_read_complete": "Permite asimilar de forma integral la filosofía moral de Mill y entender cómo intentaba conciliar el rigor consecuencialista de Bentham con una defensa cualitativa y humanista de la individualidad, la libertad y la justicia distributiva."
    },
    "etapa-17-locke-segundo-tratado": {
        "type": "selective",
        "why_only_these": "Capítulos 1 a 5, 7 a 12, y 19. Exponen los derechos naturales pre-políticos (vida, libertad y propiedad), la justificación de la propiedad privada por el trabajo mezclado, los fines del gobierno civil limitado y el derecho moral y jurídico de rebelión popular.",
        "why_skip_rest": "Los capítulos intermedios analizan las relaciones de subordinación familiar y dinástica en oposición directa a las teorías patriarcalistas de Robert Filmer (que Locke ya demolió en el Primer Tratado). También detallan normas sobre el derecho militar de conquista de su época que no alteran el marco de su teoría constitucional y liberal del Estado.",
        "why_read_complete": "Es sumamente útil para estudiantes avanzados de derecho internacional e historia colonial, ya que los capítulos sobre conquista y usurpación exponen la justificación lockeana del imperialismo inglés del siglo XVII y la legitimación jurídica de la apropiación territorial colonial."
    },
    "etapa-18-constant-libertad": {
        "type": "complete",
        "why_complete": "Es un ensayo/conferencia brevísimo (aproximadamente 20 páginas). Su lectura completa de corrido es indispensable para comprender la distinción sociológica entre la libertad antigua (participación política) y la libertad moderna (independencia privada).",
        "why_no_select": "Debido a su naturaleza sintética y a su brevedad, cada párrafo forma parte de un único argumento deductivo que contrasta la escala material y moral del mundo antiguo y moderno.",
        "if_selective": "Al ser un texto tan corto, no se recomienda una lectura selectiva. No obstante, si se requiere un repaso rápido, concéntrese en la comparación directa entre el comercio moderno y la guerra antigua en la sección media."
    },
    "etapa-19-tocqueville-democracia-en-america": {
        "type": "selective",
        "why_only_these": "Volumen I (Parte II, Caps. 5, 7, 8) y Volumen II (Parte II, Caps. 1-4; Parte IV, Caps. 6-7). Analizan la dinámica de la igualdad y advierten sobre los peligros de la soberanía popular ilimitada: la tiranía de la mayoría sobre las ideas disidentes, y el despotismo blando burocrático-paternalista.",
        "why_skip_rest": "La obra completa es una vasta enciclopedia que abunda en descripciones empíricas de la geografía del valle del Misisipi, estadísticas de la administración judicial de Nueva Inglaterra de 1831, el sistema de correos y las costumbres norteamericanas del siglo XIX, pasajes de carácter puramente histórico.",
        "why_read_complete": "Ofrece un retrato sociológico e historiográfico monumental del nacimiento de los Estados Unidos y un análisis profundo del impacto moral, cultural y religioso del igualitarismo sobre la sociedad civil moderna."
    },
    "etapa-20-pocock-momento-maquiavelico": {
        "type": "selective",
        "why_only_these": "Parte I (Caps. 1-3), Parte II (Caps. 6-7) y Parte III (Caps. 12-13). Establecen la metodología de la Escuela de Cambridge (lenguajes políticos), sitúan a Maquiavelo en su crisis florentina y trazan el traspaso del republicanismo a Inglaterra a través de James Harrington.",
        "why_skip_rest": "El volumen supera las 600 páginas y se adentra en análisis extremadamente pormenorizados de crónicas florentinas menores, disputas teológicas locales sobre las profecías del monje Savonarola, y la evolución jurídica del derecho común inglés bajo la monarquía Estuardo que desvían del hilo conductor.",
        "why_read_complete": "Es indispensable para investigadores del republicanismo atlántico, ya que detalla la transición intelectual del humanismo cívico renacentista hacia la fundación constitucional de los Estados Unidos en 1776."
    },
    "etapa-21-pateman-mills-contrato": {
        "type": "selective",
        "why_only_these": "Carole Pateman (Caps. 1 y 6) y Charles W. Mills (Cap. 1). Exponen las tesis centrales: el contrato original de la filosofía política tiene dos dimensiones ocultas (una social y una sexual, de dominación masculina), y el \"contrato racial\" como una estructura de dominación supremacista blanca real.",
        "why_skip_rest": "Los capítulos restantes de ambas obras profundizan en contratos laborales/de gestación específicos o en debates ontológicos locales sobre la blanquitud que resultan secundarios para comprender la crítica conceptual al contractualismo liberal clásico de Hobbes, Locke y Rousseau.",
        "why_read_complete": "Ambas obras completas son hitos de la teoría crítica contemporánea. Su lectura íntegra es recomendada para quienes investiguen las intersecciones del derecho contractual, la filosofía feminista de la reproducción social y la sociología del racismo estructural."
    },
    # PHASE 2
    "etapa-22-chang-economia-99": {
        "type": "selective",
        "why_only_these": "10 Capítulos Clave (1, 2, 4, 7, 12, 13, 17, 19, 22, 23). Desmontan las falacias principales del libre mercado ortodoxo (aranceles, derrame, capital humano puro, desregulación financiera, y la intervención estatal e industrial exitosa).",
        "why_skip_rest": "La obra está estructurada bajo un formato periodístico de divulgación rápida (*23 cosas que no te cuentan sobre el capitalismo*). Leer las 23 cosas completas genera redundancias conceptuales, ya que varios capítulos repiten el mismo argumento crítico usando otros ejemplos.",
        "why_read_complete": "Es útil para lectores no especializados en economía que quieran contar con un repertorio completo de anécdotas y datos históricos sobre el funcionamiento real del comercio global, las corporaciones y los mercados financieros."
    },
    "etapa-23-smith-riqueza-naciones": {
        "type": "selective",
        "why_only_these": "Libro I (Caps. 1-3, 5-8), Libro IV (Caps. 1-2, 9) y Libro V (Cap. 1). Analizan la productividad de la división del trabajo (fábrica de alfileres), el precio natural y de mercado, la mano invisible contra el mercantilismo y los deberes mínimos de financiación del Estado.",
        "why_skip_rest": "La obra consta de más de mil páginas y contiene extensos capítulos de digresión histórica y estadística del siglo XVIII, como tablas sobre fluctuaciones del precio del trigo en Inglaterra desde el año 1200, la regulación arancelaria del arenque escocés o el mantenimiento de faros portuarios.",
        "why_read_complete": "Es una lectura fundamental para historiadores de la economía que deseen examinar la transición del feudalismo al capitalismo mercantil y la génesis empírica detallada de la ciencia económica clásica."
    },
    "etapa-24-ricardo-economia-politica": {
        "type": "selective",
        "why_only_these": "Capítulos I (\"Sobre el valor\") y II (\"Sobre la renta\"). Contienen el corazón teórico del valor-trabajo clásica y el conflicto distributivo insoluble entre terratenientes (renta), capitalistas (beneficios) y trabajadores (salarios).",
        "why_skip_rest": "El resto de la obra aborda impuestos específicos del siglo XIX, patentes británicas, el patrón oro, y subsidios agrícolas locales ingleses, temas de interés exclusivo para historiadores de la economía que carecen del valor atemporal de su teoría general de la distribución.",
        "why_read_complete": "Es fundamental para comprender en detalle la teoría del comercio internacional a través de la ventaja comparativa (desarrollada en los capítulos posteriores) y la evolución del pensamiento clásico británico sobre la hacienda pública."
    },
    "etapa-25-hegel-fenomenologia": {
        "type": "selective",
        "why_only_these": "Fenomenología (Sección Dominio y Servidumbre) y Filosofía del Derecho (Sociedad Civil y Estado). Sientan las bases de la dialéctica del amo y el esclavo (el reconocimiento intersubjetivo por el trabajo) y la superación ética del egoísmo individual en el Estado racional.",
        "why_skip_rest": "El corpus hegeliano es monumental y abarca la lógica especulativa abstracta, la filosofía de la naturaleza y la teología. Exigir la lectura de ambas obras completas consumiría semestres enteros de exégesis filosófica no orientada a la teoría política y social.",
        "why_read_complete": "Es aconsejable para filósofos dedicados al idealismo alemán que busquen reconstruir el sistema metafísico completo de Hegel y el despliegue fenomenológico de la conciencia hacia el Saber Absoluto."
    },
    "etapa-26-marx-capital": {
        "type": "selective",
        "why_only_these": "Capítulos 1 a 4, 6 y 7, 10 y 24-25. Deconstruyen la mercancía, el fetichismo, la transformación del dinero en capital, la extracción de plusvalía (explotación) en el proceso de producción, la lucha por la jornada laboral y la violencia originaria campesina.",
        "why_skip_rest": "El primer tomo tiene cerca de 800 páginas. Marx dedica cientos de páginas a detallados informes oficiales de inspectores de fábricas victorianas del siglo XIX (con largas listas de accidentes de calderas y horas de comida) y a complejas derivaciones matemáticas repetitivas.",
        "why_read_complete": "Es una experiencia intelectual incomparable para entender el método dialéctico materialista aplicado. Ofrece una radiografía exhaustiva de la dinámica de acumulación de capital y las contradicciones de clase en el siglo XIX."
    },
    "etapa-28-federici-caliban-bruja": {
        "type": "selective",
        "why_only_these": "Capítulos 2 y 4. El Capítulo 2 es el núcleo de su redefinición marxista-feminista de la acumulación originaria (el cercamiento de las tierras comunales y la división sexual del trabajo). El Capítulo 4 deconstruye la caza de brujas como violencia estatal para quebrar la autonomía de las mujeres.",
        "why_skip_rest": "Los capítulos 1, 3 y 5 profundizan en las luchas de los herejes medievales y la transposición de la caza de brujas a las colonias. Estos temas ya se abordan de manera transversal en otras etapas, por lo que la selección concentra su gran aportación teórica.",
        "why_read_complete": "Ofrece un panorama detallado de la historia social europea, desvelando cómo la violencia del nacimiento del capitalismo afectó de forma diferenciada a los cuerpos de las mujeres y la resistencia campesina."
    },
    "etapa-29-mariategui-7-ensayos": {
        "type": "selective",
        "why_only_these": "Ensayos II (\"El problema del indio\") y III (\"El problema de la tierra\"). Contienen el núcleo de la reinterpretación socialista andina de Mariátegui, argumentando que el problema del indígena no es pedagógico o moral, sino una cuestión material y agraria de despojo territorial feudal.",
        "why_skip_rest": "Los ensayos restantes abordan la literatura peruana colonial, la instrucción pública del siglo XIX y la religión, temas que, aunque valiosos para la historia cultural peruana, resultan secundarios frente a su análisis de economía política y propiedad agraria.",
        "why_read_complete": "Es una obra cumbre del pensamiento latinoamericano. Leerla completa es fundamental para entender la síntesis mariateguista sobre literatura, educación, religión y geopolítica regional desde el Sur global."
    },
    # PHASE 3
    "etapa-30-weber-politica-vocacion": {
        "type": "complete",
        "why_complete": "Es una transcripción de conferencia breve (~70 páginas) donde Weber condensa conceptos que en sus tratados mayores toman cientos de páginas, tales como la definición del Estado como monopolio de la violencia legítima y las éticas de convicción y responsabilidad.",
        "why_no_select": "Al ser una conferencia de síntesis verbal directa, cada sección es un eslabón conceptual lógico. Saltar pasajes rompería el argumento deductivo sobre la naturaleza del político profesional.",
        "if_selective": "Si necesitas repasar de forma ultrarrápida, concéntrate en la definición inicial del monopolio estatal y las últimas 15 páginas sobre la tensión entre las éticas de la convicción y la responsabilidad."
    },
    "etapa-31-foucault": {
        "type": "selective",
        "why_only_these": "*Vigilar y castigar* (Parte I y Parte III, Cap. 3) y *Nacimiento de la biopolítica* (Lecciones 1-2). Muestran la transición del suplicio soberano a la disciplina panóptica normalizadora, y definen la gubernamentalidad neoliberal como racionalidad competitiva de subjetivación.",
        "why_skip_rest": "*Vigilar y castigar* completo se detiene en minuciosas y tediosas crónicas sobre la legislación carcelaria francesa del siglo XIX. El resto de las lecciones de *Nacimiento de la biopolítica* se adentran en debates del ordoliberalismo alemán que desvían del marco conceptual universal.",
        "why_read_complete": "Ambos libros completos son indispensables para sociólogos. Ofrecen un análisis genealógico exhaustivo del nacimiento de las instituciones de encierro modernas (manicomios, escuelas, prisiones) y la evolución del liberalismo económico europeo."
    },
    "etapa-32-arendt-condicion-humana": {
        "type": "selective",
        "why_only_these": "Capítulos II (\"La esfera pública y la privada\") y V (\"Acción\"). Estructuran la distinción espacial que prefigura la teoría de la esfera pública contemporánea y definen la acción, la pluralidad, la natalidad y el perdón como las únicas actividades puramente políticas de la vita activa.",
        "why_skip_rest": "Las secciones sobre \"Labor\" (Capítulo III) y \"Trabajo\" (Capítulo IV) se extienden en debates con la teoría del valor de Marx y discusiones fenomenológicas sobre objetos y trabajo manual. El Capítulo VI aborda la revolución científica (Galileo, telescopio), de carácter más metafísico.",
        "why_read_complete": "Permite asimilar el diagnóstico existencial arendtiano sobre la modernidad en su totalidad: cómo la entronización del consumo y el trabajo degradaron la acción deliberativa y allanaron el camino al totalitarismo burocrático."
    },
    "etapa-33-schmitt-concepto-politico": {
        "type": "complete",
        "why_complete": "*El concepto de lo político* (~60 páginas) define progresivamente lo político a partir de la distinción amigo/enemigo y la guerra como presupuesto. Debe leerse completo para captar el decisionismo y el realismo político schmittiano sin caricaturizaciones.",
        "why_no_select": "Su brevedad e intensidad conceptual exigen una lectura continua. Se complementa con el Capítulo I de *Teología política* sobre la soberanía y la excepción.",
        "if_selective": "Concéntrese en las secciones 2, 3 y 4 de *El concepto de lo político* donde se detalla la distinción amigo/enemigo frente a otras esferas humanas (moral, estética, economía)."
    },
    "etapa-34-rawls-teoria-justicia": {
        "type": "selective",
        "why_only_these": "Capítulos I, II y III, más secciones selectas de IV y VIII. Definen la justicia como equidad, formulan los dos principios de justicia (libertad y diferencia) y construyen el experimento mental del velo de ignorancia en la posición original.",
        "why_skip_rest": "Rawls dedica una parte sustancial de las 600 páginas de su libro a detalladas demostraciones lógicas de economía del bienestar de los años 70 y discusiones formalistas sobre la psicología kantiana del desarrollo que oscurecen la potencia de la posición original.",
        "why_read_complete": "Es el tratado de filosofía política anglosajona más importante del siglo XX. Su lectura íntegra es recomendada para quienes deseen estudiar en profundidad el liberalismo igualitario y la justificación institucional del Estado social de derecho."
    },
    "etapa-35-berlin-dos-conceptos": {
        "type": "complete",
        "why_complete": "Es un ensayo sintético brevísimo (~60 páginas) fundacional del liberalismo de posguerra. Su lectura íntegra es obligatoria para comprender la distinción pura entre libertad negativa (ausencia de interferencia) y libertad positiva (autorrealización y autogobierno).",
        "why_no_select": "Al ser un texto redactado originalmente como conferencia académica, carece de secciones descriptivas u ornamentales, manteniendo un ritmo argumental de alta densidad conceptual.",
        "if_selective": "Si requiere un repaso rápido, concéntrese en las primeras 20 páginas donde define la libertad negativa y en las secciones sobre el peligro del despotismo paternalista encarnado en la libertad positiva."
    },
    "etapa-36-pettit-skinner-republicanismo": {
        "type": "selective",
        "why_only_these": "Philip Pettit (Caps. 1 y 2) y Quentin Skinner (Cap. 1). Establecen la libertad como no-dominación frente al binario liberal de Berlin y ofrecen la reconstrucción histórica del surgimiento del concepto de \"persona libre\" en el derecho romano y el republicanismo inglés.",
        "why_skip_rest": "El resto del libro de Pettit se adentra en el diseño detallado de agencias gubernamentales anglosajonas de los años 90. La obra de Skinner se extiende en minuciosos debates historiográficos y consideraciones de historia literaria que no aportan a la teoría conceptual.",
        "why_read_complete": "Ambas obras completas estructuran el renacimiento neorrepublicano contemporáneo. Se recomiendan para investigadores que busquen alternativas constitucionales reales al modelo liberal pluralista tradicional."
    },
    "etapa-37-habermas-esfera-publica": {
        "type": "selective",
        "why_only_these": "Capítulos I, II y Capítulo Final. Ofrecen la genealogía sociohistórica del nacimiento de la esfera pública burguesa en el siglo XVIII y exponen la posterior refeudalización y deconstrucción del espacio público burgués bajo el capitalismo de consumo de masas.",
        "why_skip_rest": "Los capítulos intermedios se hunden en un denso examen del derecho administrativo y constitucional alemán del siglo XIX, la evolución de las leyes de partidos en Weimar y disputas jurídicas que alejan al estudiante de la teoría del espacio crítico.",
        "why_read_complete": "Es una obra fundamental de la sociología de la comunicación. Ofrece un panorama histórico sumamente rico sobre el desarrollo de la prensa, los cafés literarios y la opinión pública en la modernidad europea."
    },
    "etapa-38-laclau-mouffe-hegemonia": {
        "type": "selective",
        "why_only_these": "Laclau & Mouffe (Cap. 3 de *Hegemonía y estrategia socialista*) y Chantal Mouffe (*Deliberative Democracy or Agonistic Pluralism?*). Exponen el núcleo de la transición de la hegemonía gramsciana al análisis del discurso postestructuralista y el agonismo democrático frente a Habermas.",
        "why_skip_rest": "Los primeros capítulos consisten en una minuciosa revisión historiográfica del pensamiento socialista del siglo XIX (Kautsky, Bernstein), e intelectuales marxistas ya superados. La segunda mitad del libro aborda debates sobre movimientos sociales de los años 80 desactualizados.",
        "why_read_complete": "Es la obra fundacional de la teoría del discurso y el postmarxismo. Su lectura completa es obligatoria para entender la justificación teórica del populismo de izquierda y la ontología de lo político contingente."
    },
    "etapa-39-lenin-imperialismo": {
        "type": "complete",
        "why_complete": "Es un folleto de agitación teórica de unas 120 páginas. Debe leerse completo para captar cómo Lenin articula los cinco rasgos estructurales del imperialismo a partir de la concentración del capital monopolístico y financiero en los albores del siglo XX.",
        "why_no_select": "Su brevedad e importancia para la teoría del sistema-mundo contemporánea exigen una lectura íntegra, evitando esquemas simplificados que omiten el debate sobre la aristocracia obrera.",
        "if_selective": "Concéntrese en el Capítulo VII, donde Lenin resume sistemáticamente los cinco rasgos fundamentales que definen la etapa superior del capitalismo."
    },
    "etapa-40-gramsci-cuadernos": {
        "type": "selective",
        "why_only_these": "Notas sobre Intelectuales, Hegemonía y Estado. Se focaliza en la ampliación del concepto de Estado (sociedad política + sociedad civil), la distinción entre hegemonía y coerción, y el papel de los intelectuales orgánicos en la construcción de bloques históricos.",
        "why_skip_rest": "Los *Cuadernos* son una colección fragmentaria y desordenada escrita bajo la censura fascista. Gramsci escribe reflexiones sobre la literatura italiana de folletín, análisis gramaticales, o notas de lectura de revistas jesuitas de su época que resultan irrelevantes para la teoría contemporánea.",
        "why_read_complete": "Una lectura de los *Cuadernos* completos revela la inmensa cultura enciclopédica de Gramsci y la forma en que pensaba la revolución cultural, el folklore popular y la historia de los intelectuales de forma global."
    },
    "etapa-41-hayek-camino-servidumbre": {
        "type": "selective",
        "why_only_these": "Capítulos 1, 3, 5, 7, 9. Concentran la tesis epistémica y liberal de Hayek: el mercado como un transmisor descentralizado de información y cómo cualquier intento de planificación central económica allana el camino para el totalitarismo y la pérdida de libertades.",
        "why_skip_rest": "Los capítulos omitidos se concentran en debates de política exterior de la Sociedad de las Naciones de los años 40, discusiones coyunturales sobre el federalismo interestatal de posguerra en Europa y polémicas contra figuras del partido laborista británico ya olvidadas.",
        "why_read_complete": "Es uno de los libros más influyentes del pensamiento político y económico del siglo XX. Leerlo completo permite comprender de forma detallada la defensa ética de la libertad individual frente al colectivismo y la socialdemocracia."
    },
    "etapa-42-menger-economia-politica": {
        "type": "selective",
        "why_only_these": "Capítulo III (\"La teoría del valor\"). Contiene la formulación conceptual pura del subjetivismo metodológico y la utilidad marginal decreciente. Menger expone la célebre tabla de necesidades y desarticula de forma lógica la paradoja del agua y los diamantes.",
        "why_skip_rest": "El resto de los capítulos abordan la teoría de los bienes de órdenes superiores (I y II), del intercambio mercantil (V), del precio puro (VI), y el origen del dinero (VIII). Aunque valiosos para un economista, no añaden conceptos filosóficos adicionales al subjetivismo del valor.",
        "why_read_complete": "Permite comprender de forma sistemática la revolución marginalista austriaca de 1871 y la fundamentación epistemológica de la economía de mercado y la acción humana frente a los clásicos clásicos."
    },
    "etapa-43-popper-sociedad-abierta": {
        "type": "selective",
        "why_only_these": "Volumen II (Caps. 11-17, 23-24) y Volumen I (Caps. 1, 5, 6, 10). Concentran la demoledora crítica al historicismo y al determinismo económico de Hegel y Marx, el asalto al utopismo colectivista de Platón y las bases de la paradoja de la tolerancia.",
        "why_skip_rest": "La obra completa supera las mil páginas. Popper dedica enormes y engorrosas notas al pie de página (que superan la extensión del texto) a debatir traducciones gramaticales de Platón y disputas filológicas que oscurecen la tesis política y sociológica pura.",
        "why_read_complete": "Es una obra monumental de la epistemología de la sociedad liberal. Su lectura íntegra es recomendada para comprender el racionalismo crítico y la defensa de la reforma social gradual frente a las revoluciones holistas."
    },
    "etapa-44-nozick-anarquia-estado-utopia": {
        "type": "selective",
        "why_only_these": "Capítulos 1 a 3, y Capítulos 7 y 8. Formulan la fundamentación moral de los derechos individuales absolutos, la justificación del Estado mínimo, y contienen su célebre deconstrucción de la justicia distributiva de Rawls (Wilt Chamberlain).",
        "why_skip_rest": "La tercera parte de la obra (\"Utopía\") se sumerge en modelos lógicos abstractos sobre la viabilidad de comunidades utópicas voluntarias, y la primera parte abunda en discusiones técnicas sobre teoría económica de las indemnizaciones de seguros que distraen del debate.",
        "why_read_complete": "Es la obra cumbre del libertarismo filosófico. Leerla completa es de gran valor para entender la justificación ética y utópica de una sociedad de mercado libre absoluto fundada sobre el principio de propiedad de sí mismo."
    },
    "etapa-45-keynes-teoria-general": {
        "type": "selective",
        "why_only_these": "Capítulo 24 (\"Notas finales sobre la filosofía social a que podría conducir la Teoría General\"). Keynes sintetiza de forma clara cómo sus descubrimientos técnicos exigen una reforma política del capitalismo, justificando el Estado del bienestar y la socialización de la inversión.",
        "why_skip_rest": "La *Teoría general* es una de las obras de economía matemática más densas de la historia intelectual. La mayor parte del libro aborda ecuaciones contables, la tasa de interés marginal de eficiencia del capital y debates técnicos incomprensibles para el estudiante de filosofía política.",
        "why_read_complete": "Es indispensable para economistas y estudiosos del capitalismo democrático, ya que fundamenta la macroeconomía moderna y la justificación de la intervención contracíclica del Estado para evitar el desempleo involuntario."
    },
    "etapa-46-hardin-ostrom-comunes": {
        "type": "selective",
        "why_only_these": "Garrett Hardin (*La tragedia de los comunes*, completo) y Elinor Ostrom (Capítulo 1 de *Governing the Commons*). Ofrecen la definición conceptual de la tragedia de los comunes y el posterior desmontaje de la política ortodoxa estatal/privada a través del autogobierno comunal.",
        "why_skip_rest": "El resto de la obra de Ostrom consiste en extensos y detallados estudios de caso locales (riego en Valencia, gestión forestal en Japón, o agua en California) que, si bien prueban empíricamente sus tesis, no aportan nuevas categorías conceptuales a la teoría política general.",
        "why_read_complete": "Es fundamental para investigadores en políticas públicas, sociología ambiental y economía institucional que busquen comprender los principios de diseño de instituciones duraderas para la gestión de recursos de uso común."
    },
    "etapa-47-fraser-honneth-redistribucion": {
        "type": "selective",
        "why_only_these": "Nancy Fraser (Capítulo I: \"Redistribución o reconocimiento\") y Axel Honneth (Capítulo II: \"La redistribución como reconocimiento\"). Contienen el núcleo del debate bidimensional (Fraser) frente al monismo moral del reconocimiento hegeliano (Honneth).",
        "why_skip_rest": "El resto de la obra consiste en réplicas y contrarréplicas extremadamente complejas y técnicas de carácter puramente filosófico (Capítulo III y IV) que resultan redundantes con las tesis centrales presentadas en los primeros dos capítulos.",
        "why_read_complete": "Es uno de los debates de teoría crítica más importantes del siglo XXI. Su lectura íntegra es recomendada para comprender las tensiones entre la justicia económica redistributiva y la justicia cultural de la identidad."
    },
    # PHASE 4 (Latin American)
    "etapa-50-rodo-ariel": {
        "type": "complete",
        "why_complete": "Es un ensayo modernista muy breve (~80 páginas). Su lectura íntegra es clave para comprender el idealismo de la juventud latinoamericana frente al utilitarismo utilitario sajón, formulado a partir de los personajes de Shakespeare.",
        "why_no_select": "Al ser una pieza de alta oratoria modernista, la fuerza reside en la retórica del maestro Próspero a sus discípulos, lo que exige una lectura fluida de su estructura dramática.",
        "if_selective": "Si la prosa modernista resulta agotadora, puede leerse únicamente el capítulo primero y el capítulo final donde se sintetiza la comparación espiritual de América Latina y EE.UU."
    },
    "etapa-51-vasconcelos-raza-cosmica": {
        "type": "selective",
        "why_only_these": "Prólogo y Ensayo Central. Concentran la polémica tesis de la \"raza cósmica\" (la quinta raza iberoamericana mestiza como síntesis espiritual del futuro) en contraposición directa a las teorías racistas del determinismo biológico europeo de la época.",
        "why_skip_rest": "La segunda parte del libro consiste en crónicas de viajes personales del autor por diversos países sudamericanos en los años 20 que carecen de densidad teórica y no aportan valor a la tesis de la identidad latinoamericana.",
        "why_read_complete": "Es una pieza clave del nacionalismo cultural mexicano posrevolucionario. Leer la obra completa ofrece un panorama detallado de la mentalidad mística y de la utopía de la latinidad que pretendía construir el autor."
    },
    "etapa-52-paz-laberinto-soledad": {
        "type": "selective",
        "why_only_these": "Capítulos 1 a 4. Estructuran los ensayos de corte socio-existencial y psicoanalítico sobre el \"pachuco\" de frontera, el papel de las máscaras de la hermeticidad y la desconfianza del mexicano, y el trauma histórico y decolonial de la Malinche.",
        "why_skip_rest": "La segunda parte del libro contiene reflexiones poéticas y literarias de corte ensayístico sobre el día de muertos, descripciones estéticas del arte de la época colonial mexicana, y crónicas personales de la Revolución Mexicana que desvían del núcleo sociológico.",
        "why_read_complete": "Es una obra cumbre del ensayo mexicano. Ofrece un retrato existencial e histórico profundo del carácter nacional y una meditación lírica sobre la modernidad de México."
    },
    "etapa-53-galeano-venas-abiertas": {
        "type": "complete",
        "why_complete": "Es una narrativa histórica y de economía política muy accesible. Se lee completa porque su fuerza reside en la acumulación de datos históricos sobre el saqueo de recursos naturales desde la colonización hasta el siglo XX.",
        "why_no_select": "Cada capítulo detalla el despojo de una materia prima distinta (oro, azúcar, café, petróleo). Omitir secciones restaría impacto a su tesis global sobre la división internacional del trabajo.",
        "if_selective": "Concéntrese en la primera sección (\"La pobreza del hombre como resultado de la riqueza de la tierra\") y en el capítulo sobre la estructura contemporánea del despojo multinacional."
    },
    "etapa-54-bueno-mito-izquierda": {
        "type": "selective",
        "why_only_these": "Capítulos sobre las seis generaciones de izquierda y la crítica a la izquierda indefinida (~150 pp). Sientan las bases del Materialismo Filosófico aplicado a la deconstrucción del mito unitario de la izquierda política.",
        "why_skip_rest": "El resto del libro aborda debates técnicos ontológicos y controversias de la filosofía de la ciencia específicas del sistema de Gustavo Bueno que resultan excesivamente complejas para una primera aproximación de teoría del Estado.",
        "why_read_complete": "Es fundamental para comprender el sistema del Materialismo Filosófico español en su vertiente política. Permite asimilar la crítica detallada al humanismo ingenuo y al cosmopolitismo social."
    },
    "etapa-55-echeverria-modernidad-blanquitud": {
        "type": "selective",
        "why_only_these": "Capítulos sobre el \"ethos barroco\" y la \"blanquitud\" colonial. Definen la asimilación del capitalismo moderno no como blanqueamiento racial puro, sino como una blanquitud civilizatoria de normalización conductual.",
        "why_skip_rest": "Los capítulos restantes se detienen en análisis estéticos de la pintura colonial quiteña del siglo XVII e interpretaciones de la modernidad barroca barroco-mestiza que resultan de interés primordial para los estudios culturales de arte.",
        "why_read_complete": "Es una de las contribuciones teóricas más originales del marxismo crítico latinoamericano. Su lectura completa ofrece un panorama exhaustivo de la cuádruple articulación del ethos de la modernidad capitalista."
    },
    "etapa-56-dussel-1492": {
        "type": "selective",
        "why_only_these": "Conferencias 1 a 5. Estructuran la tesis del \"encubrimiento del Otro\" como el nacimiento del mito de la modernidad eurocéntrica, contrastando el descubrimiento cartográfico con la invasión y despojo existencial del indio.",
        "why_skip_rest": "Las conferencias finales se adentran en debates específicos con la teología de la liberación y cartas históricas de colonizadores que resultan reiterativas respecto a la fundamentación ontológica de la alteridad de las primeras lecciones.",
        "why_read_complete": "Es la mejor introducción al pensamiento decolonial y a la filosofía de la liberación de Dussel. Leer la obra completa permite comprender su propuesta de un diálogo intercultural hacia la Transmodernidad."
    },
    "etapa-57-quijano-colonialidad": {
        "type": "selective",
        "why_only_these": "Paper *Colonialidad del poder, eurocentrismo y América Latina* (completo, ~40 páginas). Es el paper fundacional del giro decolonial, articulando cómo el patrón de poder global moderno se basa en la clasificación racial de la población.",
        "why_skip_rest": "Al ser un ensayo autocontenido de gran rigor conceptual, su lectura íntegra es necesaria. Se evitan compilaciones masivas posteriores del autor que repiten los mismos postulados teóricos en diversos artículos.",
        "why_read_complete": "Permite asimilar el origen del concepto de colonialidad del poder en su formulación pura y comprender su diferencia crítica con el colonialismo jurídico y administrativo tradicional."
    },
    "etapa-59-freire-pedagogia-oprimido": {
        "type": "selective",
        "why_only_these": "Capítulos 1 y 2. Definen la contradicción opresor-oprimido, el concepto de \"educación bancaria\" (acumulación pasiva de contenidos) frente a la \"educación liberadora\" basada en el diálogo crítico y la concientización.",
        "why_skip_rest": "Los capítulos 3 y 4 se concentran en la metodología práctica de la alfabetización de adultos en el Nordeste brasileño de los años 60 y en consideraciones de acción comunitaria que resultan muy específicas de la pedagogía de campo.",
        "why_read_complete": "Es una obra de referencia mundial en educación y teoría crítica. Su lectura íntegra es recomendada para comprender la dimensión ético-política del diálogo revolucionario y la deconstrucción de la dominación interiorizada."
    },
    "etapa-60-gutierrez-teologia-liberacion": {
        "type": "selective",
        "why_only_these": "Introducción, Parte I y Parte IV. Exponen la reformulación de la teología como reflexión crítica desde la praxis de los oprimidos, fundamentan el pecado estructural e institucional y formulan la opción preferencial por los pobres.",
        "why_skip_rest": "El resto del volumen se detiene en debates del Concilio Vaticano II, exégesis bíblicas extensas de los Profetas y del libro de Job, y debates eclesiásticos latinoamericanos de los años 70 de carácter puramente pastoral.",
        "why_read_complete": "Es la obra fundacional de la Teología de la Liberación. Leerla completa permite comprender en profundidad la reconciliación teológica e intelectual entre el marxismo humanista y la fe cristiana en América Latina."
    },
    # PHASE 5
    "etapa-64-gago-potencia-feminista": {
        "type": "selective",
        "why_only_these": "Introducción y Capítulos Clave (Huelga, Cuerpo-Territorio, Deuda y Neoliberalismo). Definen la huelga feminista como un cartógrafo de la explotación neoliberal y la deuda como dispositivo de dominación material sobre el cuerpo-territorio.",
        "why_skip_rest": "Los capítulos restantes recopilan crónicas de calle detalladas de Buenos Aires en 2017 y manifiestos coyunturales específicos de activismo de la asamblea *Ni Una Menos* que tienen un gran valor de registro histórico pero añaden redundancia teórica.",
        "why_read_complete": "Es una pieza clave del feminismo materialista y decolonial del Sur global. Leer la obra completa ofrece un análisis situado sobre la mutación del trabajo informal y las finanzas populares bajo el neoliberalismo extractivista."
    },
    "etapa-65-segato-guerra-mujeres": {
        "type": "selective",
        "why_only_these": "Introducción y Capítulos sobre Mandato de Masculinidad, Pedagogía de la Crueldad y Ciudad Juárez. Explican la soberanía estatal informal ejercida mediante la violencia expresiva sobre el cuerpo femenino como territorio.",
        "why_skip_rest": "La segunda mitad del libro es una antología de conferencias breves leídas en congresos y dictámenes judiciales específicos en Guatemala que repiten de forma oral los mismos postulados teóricos explicados al comienzo del volumen.",
        "why_read_complete": "Ofrece un análisis antropológico forense profundo del patriarcado como estructura fundacional de la violencia humana y una clave interpretativa para comprender las nuevas formas de guerra no estatal de la modernidad tardía."
    },
    "etapa-66-wallerstein-sistemas-mundo": {
        "type": "selective",
        "why_only_these": "Capítulos sobre el marco analítico del sistema-mundo. Sientan la partición trilateral del trabajo global (centro, periferia y semiperiferia) y analizan la dinámica histórica de los Estados hegemónicos frente al mercado mundial.",
        "why_skip_rest": "Las secciones finales de esta obra introductoria se detienen en debates académicos sobre la reestructuración metodológica de las ciencias sociales del siglo XXI que desvían la atención de la teoría de la acumulación global.",
        "why_read_complete": "Es la mejor introducción sintética al método del análisis de sistemas-mundo desarrollado por el autor. Leer el volumen completo es muy aconsejable para dominar las bases macrohistóricas de la globalización capitalista."
    },
    "etapa-67-mearsheimer-great-power": {
        "type": "selective",
        "why_only_these": "Capítulos sobre el Realismo Ofensivo. Detallan las cinco premisas del comportamiento estatal en un entorno de anarquía internacional pura, por qué los Estados buscan la hegemonía regional y la competencia de seguridad inevitable.",
        "why_skip_rest": "La mayor parte del libro consiste en extensas y minuciosas reconstrucciones históricas de las alianzas diplomáticas europeas del siglo XIX (sistema bismarckiano) y balances de tanques y ejércitos de la Guerra Fría que resultan redundantes para la teoría pura.",
        "why_read_complete": "Es el tratado moderno más importante de la escuela del realismo ofensivo en relaciones internacionales. Su lectura completa ofrece una validación histórica exhaustiva de cómo las grandes potencias compiten por la supervivencia."
    },
    "etapa-69-fanon-condenados-tierra": {
        "type": "selective",
        "why_only_these": "Capítulos 1 (\"Sobre la violencia\"), 3 (\"Desventuras de la conciencia nacional\") y 5 (\"Guerra colonial y trastornos mentales\"). Contienen su teoría de la violencia catártica descolonizadora, su advertencia sobre la burguesía nacional parasitaria y los informes psiquiátricos reales del trauma colonial.",
        "why_skip_rest": "Los capítulos intermedios profundizan en la organización del campesinado local y en debates sobre la cultura nacional que repiten las tesis expuestas en los capítulos 1 y 3 en clave puramente organizativa de la Argelia de 1961.",
        "why_read_complete": "Es la obra cumbre de la descolonización global. Leerla completa es fundamental para comprender el compromiso político y psiquiátrico de Fanon frente al imperio colonial francés y el nacimiento del Tercer Mundo."
    },
    "etapa-70-said-orientalismo": {
        "type": "selective",
        "why_only_these": "Capítulo I (\"Conocer al Oriental\") y Capítulos II-III (Evolución y Actualidad). Definen el orientalismo como un dispositivo geopolítico y literario de representación que subyuga al \"Otro\" mediante el nexo conocimiento-poder foucaultiano.",
        "why_skip_rest": "Las secciones omitidas se detienen en análisis literarios detallados de diarios de viaje de escritores románticos franceses y poetas victorianos del siglo XIX, pasajes de interés para la filología y la crítica literaria comparada.",
        "why_read_complete": "Es la obra fundacional de los estudios poscoloniales. Su lectura completa es recomendada para quienes busquen comprender de forma exhaustiva cómo la erudición y la literatura europea construyeron la hegemonía colonial en el plano cultural."
    },
    "etapa-72-chibber-teoria-poscolonial": {
        "type": "selective",
        "why_only_these": "Capítulos clave. Ofrecen la contraposición materialista y universalista al poscolonialismo de Said y Spivak, argumentando que el capitalismo no requiere un sujeto eurocéntrico homogéneo para explotar, sino que se adapta perfectamente a las diferencias locales.",
        "why_skip_rest": "El resto del libro consiste en detallados debates historiográficos y controversias metodológicas específicas con los miembros del grupo de *Estudios Subalternos* de la India (Guha, Chakrabarty) que resultan muy locales y técnicos.",
        "why_read_complete": "Es una de las críticas marxistas y materialistas más potentes al giro culturalista poscolonial. Su lectura íntegra es muy aconsejable para comprender la vigencia del universalismo de la Ilustración y la teoría de la clase social."
    },
    "etapa-73-mbembe-necropolitica": {
        "type": "selective",
        "why_only_these": "Ensayo Central Necropolítica. Condensa su gran tesis: el poder soberano en la modernidad tardía y colonial no se define solo por regular la vida (biopolítica), sino por el poder de decidir quién vive y quién debe morir, creando zonas de muerte en vida.",
        "why_skip_rest": "Las conferencias y ensayos que suelen acompañar a esta obra recopilan reflexiones estéticas y estilísticas sobre la identidad africana que, aunque poéticas, no añaden rigor al aparato analítico de la biopolítica destructiva.",
        "why_read_complete": "Permite comprender de forma íntegra la genealogía espacial de la soberanía necropolítica y su aplicación a conflictos geopolíticos contemporáneos, campos de detención modernos y el control fronterizo algorítmico."
    },
    "etapa-76-gandhi-hind-swaraj": {
        "type": "complete",
        "why_complete": "Es un diálogo filosófico brevísimo (~100 páginas) escrito en 1909. Su lectura completa es indispensable para captar su crítica radical a la civilización moderna industrial de Occidente y su formulación del autogobierno espiritual y político (*swaraj*).",
        "why_no_select": "Debido a su estructura de diálogo platónico entre un editor (Gandhi) y un lector escéptico, saltar capítulos rompería la progresión lógica de su defensa de la no-violencia activa (*satyagraha*).",
        "if_selective": "Al ser un texto tan ágil y breve, no se recomienda una lectura selectiva. No obstante, concéntrese en los capítulos sobre la naturaleza de la civilización moderna y la crítica a los ferrocarriles y la medicina occidental."
    },
    "etapa-77-confucio-analectas": {
        "type": "selective",
        "why_only_these": "Libros I, II, IV, VII, XII y XV. Contienen las nociones morales constitutivas de *Ren* (benevolencia/humanidad), *Li* (rito/conducta apropiada), el rol del *Junzi* (el caballero noble) y la piedad filial como cimiento del orden social y gubernamental.",
        "why_skip_rest": "Las *Analectas* son recopilaciones asistemáticas de frases breves. Los libros omitidos describen cómo Confucio se sentaba a comer (no hablaba en la comida), el largo de las mangas de sus túnicas, o el tono de voz exacto ante duques locales, detalles folclóricos.",
        "why_read_complete": "Ofrece un panorama completo de la moral tradicional y del ritualismo clásico de la dinastía Zhou, fundamental para comprender la matriz del pensamiento social y cultural chino en su totalidad."
    },
    "etapa-78-sen-identidad-violencia": {
        "type": "complete",
        "why_complete": "Es una obra breve (~200 páginas) y sumamente fluida. Su lectura íntegra es necesaria para captar su crítica a las teorías de choque de civilizaciones y la justificación del multiculturalismo basado en la libertad individual y las identidades múltiples.",
        "why_no_select": "Cada capítulo aborda un plano del reduccionismo identitario (religión, economía, globalización). Omitir secciones impediría captar cómo Sen responde a la violencia contemporánea de forma integral.",
        "if_selective": "Concéntrese en los Capítulos 1 (la ilusión del destino identitario único), 3 (el confinamiento civilizatorio contra Huntington) y 8 (el multiculturalismo plural frente al monoculturalismo plural)."
    },
    "etapa-79-hardt-negri-imperio": {
        "type": "selective",
        "why_only_these": "Capítulos 1, 2, 3 y 4.3. Estructuran la tesis central: la transición del imperialismo de los Estados-nación a un Imperio global descentralizado en red, y formulan al nuevo sujeto subversivo constitutivo (la multitud).",
        "why_skip_rest": "La obra completa supera las 500 páginas de prosa posmoderna muy densa. Dedica extensos capítulos a herméticas digresiones filosóficas sobre Spinoza, debates jurídicos norteamericanos abstractos y análisis literarios que restan agilidad al estudio.",
        "why_read_complete": "Es la obra cumbre del postmarxismo autonomista de inicios del siglo XXI. Leerla completa permite asimilar en detalle la genealogía del derecho imperial, la soberanía biopolítica y la ontología de la multitud en el capitalismo global."
    },
    "etapa-80-wang-hui": {
        "type": "selective",
        "why_only_these": "Capítulos \"El nuevo orden de China\" y \"El neoliberalismo\". Explican cómo el Partido-Estado chino integró la economía de mercado global neoliberal sin desmantelar la soberanía del partido, trazando su vía alternativa de capitalismo de Estado.",
        "why_skip_rest": "El resto del volumen se detiene en extensas reconstrucciones histórico-filosóficas de intelectuales de las dinastías Qing y Ming, disputas historiográficas sobre la reforma agraria de los años 50 y polémicas locales que oscurecen la tesis geopolítica.",
        "why_read_complete": "Es una de las mejores claves interpretativas sobre la modernidad china contemporánea y el debate de la Nueva Izquierda asiática frente a la globalización capitalista."
    },
    "etapa-81-maruyama": {
        "type": "selective",
        "why_only_these": "Capítulos 1 y 3. Ofrecen la clave conceptual para comprender la Restauración Meiji como una modernización nacional incompleta y cómo sus tensiones latentes pavimentaron el camino para el posterior ultranacionalismo militarista japonés.",
        "why_skip_rest": "El resto de la obra se halla dedicado a análisis filológicos muy específicos del neoconfucianismo japonés del período Edo frente a la escuela del aprendizaje nacional (*Kokugaku*) que resultan de interés puramente regional.",
        "why_read_complete": "Es un hito de la historia intelectual de Japón. Su lectura completa ofrece un análisis exhaustivo del surgimiento de la subjetividad moderna japonesa y la ideología del Estado imperial de posguerra."
    },
    "etapa-82-ambedkar-annihilation-caste": {
        "type": "complete",
        "why_complete": "Es un discurso de unas 100 páginas de gran potencia conceptual e histórica. Su lectura completa es obligatoria para comprender la deconstrucción radical del sistema de castas hindú y su crítica al reformismo paternalista de Gandhi.",
        "why_no_select": "Al haber sido redactado originalmente como un discurso único para la Conferencia por la Reforma de las Castas, su estructura argumental lógica y forense exige una lectura íntegra.",
        "if_selective": "Al ser un texto breve, no se recomienda una lectura parcial. Si se requiere un repaso rápido, concéntrese en las secciones donde Ambedkar detalla las justificaciones religiosas y teológicas de las castas."
    },
    # PHASE 6
    "etapa-86-polanyi-gran-transformacion": {
        "type": "selective",
        "why_only_these": "Capítulos Clave (principalmente del 3 al 6, y del 11 al 14). Abordan el núcleo teórico: la invención de las mercancías ficticias (tierra, trabajo y dinero) y el concepto del \"doble movimiento\" (la autorregulación mercantil y la reacción de autodefensa social).",
        "why_skip_rest": "El libro contiene extensos y densos capítulos sobre la Ley de Pobres inglesa de Speenhamland de 1795, la Ley de Speenhamland de Gilbert y debates presupuestarios e historiográficos parlamentarios de los siglos XVIII y XIX que resultan sumamente específicos.",
        "why_read_complete": "Es una obra maestra de la historia económica y la sociología histórica. Leerla completa es fundamental para comprender los orígenes institucionales del colapso del liberalismo del siglo XIX y la emergencia de los fascismos de entreguerras."
    },
    "etapa-87-esping-andersen": {
        "type": "selective",
        "why_only_these": "Capítulos 1 y 2. Introducen de forma teórica los tres mundos del bienestar capitalista (socialdemócrata, corporativista y liberal), desarrollando los conceptos cardinales de desmercantilización y desfamiliarización del bienestar social.",
        "why_skip_rest": "Los capítulos restantes consisten en minuciosos análisis empíricos econométricos e históricos basados en datos comparativos de jubilaciones, licencias médicas y empleo público de los países de la OCDE en las décadas de 1970 y 1980.",
        "why_read_complete": "Es el tratado fundacional de la política social contemporánea. Leer la obra completa ofrece un panorama exhaustivo de las alianzas de clase y la formación institucional de los sistemas de protección social occidentales."
    },
    # PHASE 7
    "etapa-90-horkheimer-adorno-industria-cultural": {
        "type": "selective",
        "why_only_these": "Capítulo \"La industria cultural: Ilustración como engaño de masas\" en *Dialéctica de la Ilustración*. Define la racionalidad instrumental aplicada al arte de masas, la alienación del ocio y cómo el cine y la radio mercantilizan la conciencia del sujeto moderno.",
        "why_skip_rest": "El resto del libro aborda el antisemitismo, exégesis mitológicas de la *Odisea* de Homero y reflexiones metafísicas complejas del materialismo filosófico de la Escuela de Frankfurt que distraen del análisis de la cultura de masas.",
        "why_read_complete": "Es la obra fundacional de la Teoría Crítica. Leer el volumen completo ofrece una comprensión profunda sobre la autodestrucción de la racionalidad de la Ilustración y la emergencia del totalitarismo moderno."
    },
    "etapa-91-williams-marxismo-literatura": {
        "type": "selective",
        "why_only_these": "Capítulos sobre Hegemonía, Culturas Dominantes/Residuales/Emergentes y Estructuras del Sentir. Concentran los conceptos claves que definen la aportación del materialismo cultural a la sociología del poder y el análisis de la ideología.",
        "why_skip_rest": "El primer tercio del libro aborda discusiones de lingüística saussuriana clásica y semiótica teórica de los años 70 que hoy resultan superadas, y la parte final se enfoca en el análisis formal e histórico de la teoría literaria del drama británico.",
        "why_read_complete": "Permite asimilar el modelo teórico de Raymond Williams de forma integral y comprender su propuesta de un marxismo cultural no reduccionista que analiza el arte y la literatura como prácticas materiales."
    },
    "etapa-93-bourdieu-distincion": {
        "type": "selective",
        "why_only_these": "Capítulos seleccionados sobre Habitus y Espacio de Capitales. Exponen la teoría de cómo las preferencias y el gusto estético sirven como marcas invisibles pero rígidas de distinción de clase y reproducción de capital social.",
        "why_skip_rest": "El volumen completo supera las 600 páginas e incluye cientos de tablas sociológicas empíricas que recopilan los hábitos de compra franceses de champú, pan y revistas de 1963, y la inclinación estética de obreros metalúrgicos de la época.",
        "why_read_complete": "Ofrece un panorama sociológico y etnográfico monumental sobre la sociedad francesa y una demostración empírica de cómo la dominación de clase se inscribe en el cuerpo, el gusto y las prácticas cotidianas."
    },
    "etapa-97-zuboff-vigilancia": {
        "type": "selective",
        "why_only_these": "Capítulos seleccionados sobre Excedente Conductual y Asimetría de Información. Sientan el marco analítico de cómo el capitalismo informático extrae datos del comportamiento humano para modificarlos a gran escala con fines de lucro.",
        "why_skip_rest": "Zuboff repite y amplía este mismo marco conceptual básico a lo largo de 700 páginas apoyándose en docenas de estudios de caso anecdóticos (como juguetes inteligentes conectados a internet y asistentes domésticos virtuales) que generan redundancia.",
        "why_read_complete": "Es el retrato crítico más completo de la economía de datos de Silicon Valley. Leer el volumen completo es recomendado para quienes deseen estudiar en detalle la infraestructura tecnológica de la gubernamentalidad digital."
    }
}

patched_count = 0

for filename, data in justifications.items():
    filepath = os.path.join(etapas_dir, filename + ".md")
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # We want to replace the old justification block
    # The old block could have header:
    # "## Justificación de la lectura seleccionada" or "## Justificaciónde la lectura seleccionada"
    # or similar.
    # We'll use a regex to find the start of the justification header up to ## Tareas (or ## tareas)
    
    just_pattern = re.compile(r'##\s*Justificación.*?(##\s*Tareas|##\s*tareas)', re.DOTALL | re.IGNORECASE)
    
    # Format the new justification block based on book type
    if data["type"] == "selective":
        justification_md = f"""## Justificación de la lectura seleccionada

* **¿Por qué leer solo esta selección?** {data['why_only_these']}
* **¿Por qué omitir el resto en una primera lectura?** {data['why_skip_rest']}
* **¿Por qué vale la pena leer el libro completo?** {data['why_read_complete']}

"""
    else: # complete
        justification_md = f"""## Justificación de la lectura completa

* **¿Por qué leer este libro completo?** {data['why_complete']}
* **¿Por qué no se seleccionan capítulos?** {data['why_no_select']}
* **Si decides hacer una lectura selectiva:** {data['if_selective']}

"""
    
    # Try to replace the old block
    match = just_pattern.search(content)
    if match:
        # We replace the matched block, keeping the Tareas header
        replacement = justification_md + match.group(1)
        new_content = content[:match.start()] + replacement + content[match.end():]
        print(f"Replacing existing justification in {filename}")
    else:
        # Locate ## Tareas and insert before it
        tareas_pos = content.find("## Tareas")
        if tareas_pos == -1:
            tareas_pos = content.lower().find("## tareas")
            
        if tareas_pos == -1:
            print(f"Warning: Could not find '## Tareas' in {filename}")
            continue
            
        new_content = content[:tareas_pos] + justification_md + content[tareas_pos:]
        print(f"Inserting new justification in {filename}")
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    patched_count += 1

print(f"Patched {patched_count} files in total.")
