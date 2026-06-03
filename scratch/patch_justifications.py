import os
import re

etapas_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"

justifications = {
    "etapa-03-adler-como-leer-un-libro": {
        "why_only_these": (
            "* **Capítulos 1 a 4 y Sección Analítica (Caps. 5-7, 11):** Sientan los cimientos prácticos "
            "de los cuatro niveles de lectura (elemental, inspeccional, analítica y sintópica). Introducen "
            "la diferencia crítica entre asimilar información pasivamente y forzar la comprensión activa "
            "a través de reglas sistemáticas para desmenuzar las ideas del autor."
        ),
        "why_not_complete": (
            "El resto del volumen se dispersa en pautas metodológicas hiperespecíficas sobre cómo abordar "
            "géneros literarios particulares, como la poesía lírica, obras teatrales clásicas, novelas de ficción "
            "o tratados de matemáticas puras. Si bien son útiles para una formación humanística general, carecen "
            "de relevancia para el objetivo de este programa de estudio, que se enfoca en la apropiación analítica "
            "de tratados densos de teoría social, económica y del Estado."
        )
    },
    "etapa-08-aristoteles-politica": {
        "why_only_these": (
            "* **Libro I (Caps. 1-2, 3-7):** Establece el fundamento antropológico y teleológico del ser humano "
            "como *zoon politikon* (animal político), analiza la *oikos* (el hogar) y contiene su controvertida "
            "e influyente teoría de la esclavitud natural.\n"
            "* **Libro III (Caps. 1-9):** Define la noción pura de ciudadanía, la virtud cívica y la famosa "
            "clasificación formal de las seis formas de gobierno (monarquía/tiranía, aristocracia/oligarquía, "
            "politeia/democracia).\n"
            "* **Libro VII (Caps. 1-3, 13-14):** Expone los requisitos morales, demográficos e institucionales "
            "indispensables para fundar la *polis* ideal."
        ),
        "why_not_complete": (
            "Los libros IV, V, VI y VIII consisten principalmente en detallados inventarios históricos y "
            "descripciones de la inestabilidad política de las poleis de su época (clasificaciones minuciosas "
            "de cómo se desmoronaban las tiranías locales en el siglo IV a.C.) y largas reflexiones sobre la "
            "educación musical y gimnástica de los jóvenes. Omitir estas secciones nos permite enfocarnos en el "
            "aparato conceptual sistemático de la filosofía política clásica."
        )
    },
    "etapa-11-hobbes-leviatan": {
        "why_only_these": (
            "* **Parte I (Caps. 6, 10, 11, 13, 14-15, 16):** Contiene el corazón de la antropología materialista "
            "de Hobbes, su teorización del estado de naturaleza como una guerra civil permanente y el papel del "
            "miedo a la muerte violenta como catalizador de la racionalidad política.\n"
            "* **Parte II (Caps. 17-19, 21, 26, 29-30):** Explica la generación del soberano por medio del pacto "
            "social, la indivisibilidad de la soberanía, el concepto puro de representación y la libertad negativa "
            "del súbdito en los silencios de la ley."
        ),
        "why_not_complete": (
            "El *Leviatán* está compuesto por cuatro partes, siendo la Parte III (\"De un Estado cristiano\") "
            "y la Parte IV (\"Del reino de las tinieblas\") casi dos tercios del volumen completo. En ellas, "
            "Hobbes se detiene en un exhaustivo escrutinio bíblico y teológico con el único fin de neutralizar "
            "el poder temporal de la Iglesia Católica y de los sectores puritanos de su época. Aunque históricamente "
            "fascinantes, carecen de peso teórico para comprender las bases constitucionales del Estado moderno."
        )
    },
    "etapa-13-rousseau-contrato-social": {
        "why_only_these": (
            "* **Libros I, II y III:** Estructuran el andamiaje filosófico central de la soberanía popular indivisible, "
            "la conceptualización de la voluntad general frente a la voluntad de todos, y la diferenciación teórica "
            "crucial entre el Estado (soberano) y el Gobierno (ejecutor).\n"
            "* **Libro IV (Caps. 1-2, 8):** Expone las condiciones para la toma de decisiones colectivas y la controvertida "
            "formulación de la \"religión civil\" como pegamento moral de la república."
        ),
        "why_not_complete": (
            "La mayor parte del Libro IV está dedicada a una minuciosa e histórica reconstrucción de la maquinaria "
            "administrativa y las asambleas de votación de la antigua República Romana (los comicios por curias, "
            "centurias y tribus, y la institución de la censura y la dictadura). Rousseau introduce este extenso "
            "análisis para ofrecer ejemplos empíricos de autogobierno clásico, pero oscurece la teoría pura del "
            "pacto social y resulta de valor meramente historiográfico."
        )
    },
    "etapa-15-mill-sobre-la-libertad": {
        "why_only_these": (
            "* **Sobre la libertad (Completo):** Al ser un ensayo sintético de unas cien páginas, su lectura íntegra "
            "es obligatoria para asimilar los límites de la autoridad social sobre el individuo.\n"
            "* **El utilitarismo (Caps. 1 y 2):** Introduce el criterio moral de la utilidad general como base moral "
            "de las libertades que Mill defiende en su obra política, definiendo la felicidad en términos cualitativos."
        ),
        "why_not_complete": (
            "Los capítulos finales de *El utilitarismo* (Caps. 3 a 5) se adentran en debates técnicos de la filosofía "
            "moral victoriana sobre el origen psicológico de la idea de justicia y controversias éticas con pensadores "
            "intuicionistas británicos de su época. Para fines de teoría política y del Estado, los dos primeros "
            "capítulos bastan para fijar el marco ético consecuencialista."
        )
    },
    "etapa-17-locke-segundo-tratado": {
        "why_only_these": (
            "* **Capítulos 1 a 5:** Exponen las bases iusnaturalistas del Estado moderno (estado de naturaleza e "
            "igualdad moral), diferencian el estado de naturaleza del estado de guerra y formulan la clásica teoría "
            "del valor y la apropiación por mezcla del trabajo.\n"
            "* **Capítulos 7 a 12:** Estructuran la sociedad política civil, los fines legítimos del gobierno limitado y "
            "la primacía del poder legislativo.\n"
            "* **Capítulo 19:** Legítima filosófica y jurídicamente el derecho de rebelión popular y de disolución "
            "del gobierno en caso de tiranía o usurpación."
        ),
        "why_not_complete": (
            "Los capítulos intermedios del Segundo Tratado (Caps. 6, 13 a 18) analizan de forma redundante las "
            "relaciones de subordinación familiar y dinástica en oposición directa a las teorías patriarcalistas de "
            "Robert Filmer (que ya demolió línea por línea en el Primer Tratado). También detallan normas sobre el "
            "derecho militar de conquista de su época que no alteran el marco de su teoría constitucional y liberal "
            "del Estado."
        )
    },
    "etapa-19-tocqueville-democracia-en-america": {
        "why_only_these": (
            "* **Volumen I (Parte II, Caps. 5, 7, 8):** Analiza la dinámica sociopolítica americana, advirtiendo sobre "
            "los peligros de la soberanía popular ilimitada y la temida tiranía de la mayoría sobre las minorías e ideas disidentes.\n"
            "* **Volumen II (Parte II, Caps. 1-4; Parte IV, Caps. 6-7):** Explora cómo la igualdad democrática alimenta el "
            "individualismo apático y el retraimiento privado, allanando el camino para el surgimiento de un \"despotismo blando\" "
            "o burocrático-paternalista."
        ),
        "why_not_complete": (
            "La obra completa es un compendio enciclopédico de dos macizos tomos que abunda en descripciones empíricas "
            "de la geografía del valle del Misisipi, estadísticas de la administración judicial de Nueva Inglaterra de 1831, "
            "el sistema carcelario, y las dinámicas postales del siglo XIX. Estas secciones descriptivas, aunque históricamente "
            "valiosas, dificultan la apropiación ágil de la teoría general sobre las tendencias morales y políticas de la democracia."
        )
    },
    "etapa-20-pocock-momento-maquiavelico": {
        "why_only_these": (
            "* **Parte I (Caps. 1-3):** Introduce las bases metodológicas de la escuela de Cambridge sobre los \"lenguajes "
            "políticos\" y la conceptualización de la virtud cívica de raíz aristotélica.\n"
            "* **Parte II (Caps. 6-7):** Aborda el corazón de la obra: Maquiavelo en su contexto florentino y el dilema de "
            "mantener una república virtuosa en el tiempo frente a la inestabilidad de la fortuna.\n"
            "* **Parte III (Caps. 12-13):** Trazará el traspaso del republicanismo a Inglaterra a través de James Harrington."
        ),
        "why_not_complete": (
            "El volumen supera las 600 páginas y se adentra en análisis extremadamente pormenorizados de crónicas florentinas "
            "menores, disputas teológicas locales sobre las profecías del monje Savonarola, y la evolución jurídica del derecho "
            "común inglés bajo la monarquía Estuardo. Para captar la tesis del \"hilo republicano atlántico\" que une a Florencia, "
            "Inglaterra y la fundación constitucional estadounidense, la selección elegida contiene la columna vertebral lógica."
        )
    },
    "etapa-22-chang-economia-99": {
        "why_only_these": (
            "* **10 Capítulos Clave (1, 2, 4, 7, 12, 13, 17, 19, 22, 23):** Desmontan las falacias principales del libre mercado "
            "ortodoxo. Abordan temas cardinales como el proteccionismo histórico, la falsedad del derrame, la falacia del "
            "capital humano puro en la educación, la inevitabilidad de la planificación estatal encubierta, y la necesidad de "
            "someter el mercado financiero al control democrático."
        ),
        "why_not_complete": (
            "La obra de Chang está diseñada bajo un formato de divulgación ágil y periodística (*23 cosas que no te cuentan sobre "
            "el capitalismo*). Leer las 23 cosas completas genera redundancias conceptuales, ya que varios capítulos repiten "
            "la misma tesis crítica empleando distintos ejemplos. La selección optimiza el tiempo de estudio para adquirir el "
            "herramental de economía crítica esencial."
        )
    },
    "etapa-23-smith-riqueza-naciones": {
        "why_only_these": (
            "* **Libro I (Caps. 1-3, 5-8):** Analiza la productividad de la división del trabajo (fábrica de alfileres), "
            "el valor de cambio y los componentes del precio (renta, salarios y beneficios).\n"
            "* **Libro IV (Caps. 1-2, 9):** Explica la crítica al proteccionismo mercantilista y es donde aparece el pasaje "
            "original de la \"mano invisible\".\n"
            "* **Libro V (Cap. 1):** Delimita las funciones legítimas que el soberano debe financiar (defensa, justicia, "
            "infraestructura y educación básica para evitar la idiotización del obrero)."
        ),
        "why_not_complete": (
            "La obra de Smith consta de más de mil páginas y contiene vastos capítulos de digresión histórica y estadística "
            "coyuntural del siglo XVIII, tales como detalladas tablas sobre las fluctuaciones del precio del trigo en Inglaterra "
            "desde el año 1200, la regulación arancelaria del comercio de arenques escoceses, o el mantenimiento de los faros "
            "marítimos. Esto tiene valor para la historia de la economía, pero oscurece la teoría pura del nacimiento del capitalismo."
        )
    },
    "etapa-25-hegel-fenomenologia": {
        "why_only_these": (
            "* **Fenomenología del Espíritu (Sección Dominio y Servidumbre):** Contiene la dialéctica del amo y el esclavo, "
            "el núcleo de la autoconstitución mutua por el trabajo y el reconocimiento intersubjetivo, matriz de la teoría crítica.\n"
            "* **Filosofía del Derecho (Secciones sobre Sociedad Civil y Estado):** Analiza al Estado como la realización racional "
            "y superación ética del egoísmo atomizado de la sociedad civil."
        ),
        "why_not_complete": (
            "El corpus hegeliano es monumental y su prosa hermética abarca la lógica especulativa abstracta, la filosofía de "
            "la naturaleza y la teología de la religión. Exigir la lectura de ambas obras completas consumiría semestres enteros "
            "de exégesis filosófica. La selección extrae estrictamente las piezas políticas y sociales que impactaron en el "
            "marxismo y en la teoría social contemporánea."
        )
    },
    "etapa-26-marx-capital": {
        "why_only_these": (
            "* **Capítulos 1 a 4:** Deconstruyen el valor de uso y cambio de la mercancía, el misterio del dinero y la teoría "
            "del fetichismo de la mercancía.\n"
            "* **Capítulos 6 y 7:** Definen conceptualmente el secreto de la explotación: la venta de la fuerza de trabajo y la "
            "extracción de plusvalía en el proceso de producción.\n"
            "* **Capítulo 10 y Capítulos 24-25:** Exponen la lucha material por el límite de la jornada laboral y la historia de "
            "la violencia originaria que expropió a los campesinos de sus medios de producción."
        ),
        "why_not_complete": (
            "El primer tomo de *El Capital* tiene cerca de 800 páginas en sus ediciones estándar. Marx dedica cientos de páginas "
            "a detallados informes oficiales de inspectores de fábricas victorianas del siglo XIX (con largas listas de accidentes "
            "de calderas y horas de comida de niños trabajadores textiles) y a complejas derivaciones matemáticas repetitivas. "
            "La selección conserva el andamiaje sociológico, histórico e intelectual del texto intacto."
        )
    },
    "etapa-27-harvey-reading-marx": {
        "why_only_these": (
            "* **Videoclases correspondientes a los Caps. 1, 4 y 24:** Harvey ejerce como un decodificador indispensable para "
            "los pasajes teóricamente más complejos del Libro I de *El Capital*, guiando al estudiante a través de la teoría del "
            "valor y la posterior dinámica de la acumulación por desposesión."
        ),
        "why_not_complete": (
            "El curso completo de Harvey contiene más de 13 videoclases largas que cubren exhaustivamente las 800 páginas del "
            "Libro I. Para un programa de teoría del Estado y del poder político que ya cuenta con una amplia variedad de autores, "
            "dedicar 40 horas adicionales de análisis empírico decimonónico es pedagógicamente ineficiente. La selección optimiza "
            "la guía sobre los núcleos teóricos."
        )
    },
    "etapa-31-foucault": {
        "why_only_these": (
            "* **Vigilar y castigar (Parte I y Parte III, Cap. 3):** Contrasta el suplicio físico soberano con la sutil normalización "
            "disciplinaria. Explica el panóptico como modelo arquitectónico del autocontrol moderno.\n"
            "* **Nacimiento de la biopolítica (Lecciones 1-2):** Sienta las bases de la biopolítica y define la gubernamentalidad "
            "neoliberal no como ideología, sino como una técnica de conducción basada en fabricar la competencia y la subjetividad "
            "del \"empresario de sí mismo\"."
        ),
        "why_not_complete": (
            "El libro *Vigilar y castigar* completo se detiene en minuciosas y a menudo tediosas crónicas sobre la legislación carcelaria "
            "francesa del siglo XIX, planos detallados de orfanatos reformatorios locales y reglamentaciones penales menores. El resto "
            "de las lecciones de *Nacimiento de la biopolítica* se adentran en debates históricos del ordoliberalismo alemán de posguerra. "
            "La selección rescata las innovaciones conceptuales universales."
        )
    },
    "etapa-34-rawls-teoria-justicia": {
        "why_only_these": (
            "* **Capítulos I a III:** Definen la justicia como equidad, formulan los dos principios de justicia (libertad y diferencia) "
            "y construyen el célebre experimento mental del velo de ignorancia en la posición original.\n"
            "* **Secciones selectas de IV y VIII:** Abordan la estabilidad institucional y la justificación moral y psicológica "
            "de una sociedad justa y democrática."
        ),
        "why_not_complete": (
            "Rawls dedica una parte sustancial de las 600 páginas de su libro a detalladas demostraciones lógicas de economía del "
            "bienestar, derivaciones estadísticas de la teoría de la elección racional de los años 70 y discusiones formalistas "
            "sobre la psicología kantiana del desarrollo. Estos pasajes técnicos, hoy en día secundarios, oscurecen la potencia "
            "ética de la posición original."
        )
    },
    "etapa-37-habermas-esfera-publica": {
        "why_only_these": (
            "* **Capítulos I y II:** Ofrecen la genealogía sociohistórica del nacimiento de la esfera pública burguesa en los cafés "
            "londinenses y salones franceses del siglo XVIII, basada en el diálogo crítico y racional libre de dominación estatal.\n"
            "* **Capítulo Final:** Expone la deconstrucción y \"refeudalización\" de esta esfera bajo el capitalismo tardío y el "
            "consumo de masas."
        ),
        "why_not_complete": (
            "Los capítulos intermedios del libro se hunden en un denso examen del derecho administrativo y constitucional alemán "
            "del siglo XIX, la evolución técnica de las leyes de partidos en Weimar, y controversias jurídicas hiperlocales de la "
            "Europa de posguerra. Estos temas resultan obsoletos y alejan al estudiante de la teoría del espacio público."
        )
    },
    "etapa-40-gramsci-cuadernos": {
        "why_only_these": (
            "* **Notas sobre Intelectuales, Hegemonía y Estado:** Se focaliza en la ampliación del concepto de Estado (sociedad "
            "política + sociedad civil), la distinción entre hegemonía y coerción, y el papel de los intelectuales orgánicos en "
            "la construcción de bloques históricos."
        ),
        "why_not_complete": (
            "Los *Cuadernos de la cárcel* son una colección desordenada y fragmentaria de miles de notas escritas bajo la censura "
            "del fascismo y sin intenciones de publicación inmediata. Gramsci escribe extensas reflexiones sobre la literatura popular "
            "italiana de folletín del siglo XIX, minuciosos análisis gramaticales de dialectos locales, o notas de lectura de revistas "
            "jesuitas de su época. Una antología teórica sistemática es fundamental."
        )
    },
    "etapa-41-hayek-camino-servidumbre": {
        "why_only_these": (
            "* **Capítulos 1, 3, 5, 7, 9:** Concentran la tesis epistémica y liberal de Hayek: el mercado como un transmisor "
            "descentralizado de información (sistema de precios) y cómo cualquier intento estatal de planificación central de la "
            "economía allana inevitablemente el camino para la pérdida de libertades políticas y civiles."
        ),
        "why_not_complete": (
            "Los capítulos omitidos se concentran en debates de política exterior de la Sociedad de las Naciones de los años 40, "
            "discusiones coyunturales sobre el federalismo interestatal de posguerra en Europa y polémicas directas contra figuras "
            "menores del partido laborista británico del siglo XX. La selección conserva el argumento atemporal sobre la libertad "
            "y el conocimiento."
        )
    },
    "etapa-43-popper-sociedad-abierta": {
        "why_only_these": (
            "* **Volumen II (Caps. 11-17, 23-24):** Concentra la demoledora crítica al historicismo y al determinismo económico de "
            "Hegel y Marx, y expone su concepción racionalista crítica de la sociedad abierta.\n"
            "* **Volumen I (Caps. 1, 5, 6, 10):** Sienta las bases de la paradoja de la tolerancia y el asalto al utopismo aristocrático-colectivista "
            "de Platón."
        ),
        "why_not_complete": (
            "La obra completa supera las mil páginas. Popper dedica enormes y engorrosas notas al pie de página (que en muchas ediciones "
            "tienen más extensión que el cuerpo del texto) a debatir traducciones gramaticales del griego antiguo con filólogos de su "
            "época e interpretaciones metafísicas de la dialéctica hegeliana. La selección permite concentrarse en la tesis política "
            "y sociológica pura."
        )
    },
    "etapa-44-nozick-anarquia-estado-utopia": {
        "why_only_these": (
            "* **Capítulos 1 a 3:** Formulan la fundamentación moral de los derechos individuales absolutos y la justificación "
            "del Estado mínimo o ultramínimo.\n"
            "* **Capítulos 7 y 8:** Contienen la célebre deconstrucción de la justicia distributiva pautada de Rawls por medio "
            "del famoso experimento mental de Wilt Chamberlain (la propiedad de sí mismo)."
        ),
        "why_not_complete": (
            "La tercera parte de la obra (\"Utopía\") se sumerge en modelos lógicos altamente abstractos sobre la viabilidad de "
            "comunidades utópicas voluntarias, y la primera parte abunda en discusiones técnicas sobre teoría económica de las "
            "indemnizaciones de seguros y compensaciones de monopolios de la fuerza. Omitir estas partes permite centrarse en el "
            "careo Rawls-Nozick."
        )
    },
    "etapa-52-paz-laberinto-soledad": {
        "why_only_these": (
            "* **Capítulos 1 a 4:** Estructuran los ensayos de corte socio-existencial y psicoanalítico sobre el \"pachuco\" "
            "de frontera, el papel de las máscaras de la hermeticidad y la desconfianza del mexicano, y el trauma histórico y "
            "decolonial de la Malinche."
        ),
        "why_not_complete": (
            "La segunda parte del libro contiene reflexiones poéticas y literarias de corte ensayístico sobre el día de muertos, "
            "descripciones estéticas del arte de la época colonial mexicana, y crónicas personales de la Revolución Mexicana. "
            "Aunque hermosas literariamente, carecen de la densidad conceptual e identitaria que define a los primeros cuatro capítulos."
        )
    },
    "etapa-60-gutierrez-teologia-liberacion": {
        "why_only_these": (
            "* **Introducción, Parte I y Parte IV:** Exponen la reformulación de la teología clásica como una reflexión crítica "
            "desde la praxis histórica de los oprimidos, fundamentan la noción de pecado estructural e institucionalizado, y "
            "formulan la opción preferencial por los pobres."
        ),
        "why_not_complete": (
            "El resto del volumen se detiene en pormenorizados análisis documentales del Concilio Vaticano II, exégesis bíblicas "
            "extensas de los textos del Antiguo Testamento y debates eclesiológicos sobre la estructura del clero latinoamericano "
            "de los años 70. Omitir estas partes prioriza la dimensión teórica y sociopolítica de la obra."
        )
    },
    "etapa-64-gago-potencia-feminista": {
        "why_only_these": (
            "* **Introducción y Capítulos Clave (Huelga, Cuerpo-Territorio, Deuda y Neoliberalismo):** Definen la articulación "
            "materialista de la huelga feminista como un cartógrafo del despojo, la conexión del cuerpo-territorio y la deuda "
            "como mecanismo de explotación."
        ),
        "why_not_complete": (
            "Los capítulos restantes recopilan crónicas de calle pormenorizadas, debates internos del colectivo de activistas "
            "de Buenos Aires en 2017 y manifiestos coyunturales específicos. Aunque útiles como registro del activismo, añaden "
            "redundancia al andamiaje de su teoría feminista y de la reproducción social."
        )
    },
    "etapa-65-segato-guerra-mujeres": {
        "why_only_these": (
            "* **Introducción y Capítulos sobre Mandato de Masculinidad, Pedagogía de la Crueldad y Ciudad Juárez:** Explican "
            "cómo la soberanía estatal informal se ejerce por medio de la violencia expresiva e instrumental sobre el cuerpo "
            "de las mujeres, y deconstruyen el mandato de masculinidad corporativo."
        ),
        "why_not_complete": (
            "La segunda mitad del libro es una antología de conferencias orales breves leídas en simposios de antropología forense, "
            "transcripciones de entrevistas periodísticas cortas y dictámenes judiciales específicos presentados en Guatemala. "
            "La lectura de la primera parte concentra de forma sistemática sus contribuciones teóricas originales."
        )
    },
    "etapa-66-wallerstein-sistemas-mundo": {
        "why_only_these": (
            "* **Capítulos sobre el marco analítico del sistema-mundo:** Sientan la clásica partición trilateral del trabajo "
            "global entre el centro geográfico del capital, la periferia exportadora de materias primas y la semiperiferia amortiguadora, "
            "y analizan la evolución de los Estados hegemónicos."
        ),
        "why_not_complete": (
            "El resto de la obra introductoria e historiográfica se detiene en debates académicos sobre la reestructuración futura "
            "de las ciencias sociales hacia el siglo XXI y discusiones epistemológicas con la escuela francesa de los *Annales* "
            "que desvían la atención de la teoría de la acumulación global y la geopolítica contemporánea."
        )
    },
    "etapa-67-mearsheimer-great-power": {
        "why_only_these": (
            "* **Capítulos sobre el Realismo Ofensivo:** Detallan las cinco premisas del comportamiento de los Estados en un "
            "entorno de anarquía internacional pura, por qué los Estados buscan la hegemonía regional y la inevitabilidad de "
            "la competencia de poder."
        ),
        "why_not_complete": (
            "La mayor parte de este libro consiste en minuciosas y extensas reconstrucciones históricas de las alianzas diplomáticas "
            "europeas del siglo XIX (como el sistema bismarckiano), balances cuantitativos de tropas y tanques durante las Guerras "
            "Mundiales, y tablas empíricas de poder industrial. La teoría racional del realismo ofensivo queda fijada en las lecturas seleccionadas."
        )
    },
    "etapa-70-said-orientalismo": {
        "why_only_these": (
            "* **Capítulo I (Conocer al Oriental) y Capítulos II-III (Evolución y Actualidad):** Definen el orientalismo como un "
            "dispositivo de representación geopolítica que sirve para subyugar y colonizar al \"Otro\" mediante el nexo "
            "conocimiento-poder."
        ),
        "why_not_complete": (
            "La obra abunda en minuciosos análisis filológicos y de crítica literaria de diarios de viaje de poetas románticos "
            "franceses e ingleses olvidados del siglo XIX y exégesis de novelas imperiales victorianas. Estas partes resultan de "
            "interés primordial para la teoría de la literatura comparada, pero resultan secundarias para la teoría geopolítica."
        )
    },
    "etapa-73-mbembe-necropolitica": {
        "why_only_these": (
            "* **Ensayo Central Necropolítica:** Condensa la tesis fundamental: cómo la soberanía en la modernidad tardía y colonial "
            "consiste en decidir quién debe vivir y quién debe morir, creando zonas de \"muerte en vida\" (como las plantaciones o los "
            "campos de refugiados)."
        ),
        "why_not_complete": (
            "Las obras extendidas de Mbembe de donde se suele extraer este ensayo se dispersan en digresiones líricas y poéticas "
            "sobre el arte contemporáneo, la identidad africana e improvisaciones teóricas que no alteran el modelo analítico de "
            "su tesis sobre la muerte soberana."
        )
    },
    "etapa-77-confucio-analectas": {
        "why_only_these": (
            "* **Libros I, II, IV, VII, XII y XV:** Formulan las nociones morales constitutivas de *Ren* (benevolencia/humanidad), "
            "*Li* (rito/conducta apropiada), el rol del *Junzi* (el caballero noble) y la piedad filial como cimiento del orden social "
            "y gubernamental."
        ),
        "why_not_complete": (
            "Las *Analectas* son una recopilación fragmentaria y desordenada de frases breves. Varios de los libros omitidos describen "
            "con excesiva minucia cómo Confucio se sentaba a comer (no hablaba mientras comía), la longitud de las mangas de sus túnicas, "
            "o el tono de voz exacto que empleaba ante determinados duques locales. Tienen valor histórico-etnográfico pero no filosófico."
        )
    },
    "etapa-79-hardt-negri-imperio": {
        "why_only_these": (
            "* **Capítulos 1, 2, 3 y 4.3:** Estructuran la tesis central: la transición del imperialismo centrado en los Estados-nación "
            "a un Imperio global descentralizado y en red sin centro geográfico, y formulan el sujeto constitutivo de la \"multitud\"."
        ),
        "why_not_complete": (
            "La obra completa supera las 500 páginas de prosa posmoderna muy densa. Dedica extensos capítulos a herméticas digresiones "
            "filosóficas sobre Spinoza, debates jurídicos norteamericanos abstractos y análisis literarios redundantes que restan "
            "agilidad al estudio de la tesis geopolítica."
        )
    },
    "etapa-80-wang-hui": {
        "why_only_these": (
            "* **Capítulos El nuevo orden de China y El neoliberalismo:** Explican cómo el Partido-Estado chino integró de forma "
            "soberana la economía de mercado global neoliberal sin desmantelar la soberanía del partido, trazando su vía alternativa."
        ),
        "why_not_complete": (
            "El resto del volumen se detiene en extensas reconstrucciones histórico-filosóficas de intelectuales y poetas de las "
            "dinastías Qing y Ming, disputas historiográficas sobre la reforma agraria de los años 50 y debates intelectuales locales "
            "que oscurecen la tesis de economía política del capitalismo de Estado."
        )
    },
    "etapa-81-maruyama": {
        "why_only_these": (
            "* **Capítulos 1 y 3:** Ofrecen la clave conceptual para comprender la Restauración Meiji como una modernización nacional "
            "incompleta y cómo sus tensiones latentes pavimentaron el camino para el posterior ultranacionalismo militarista japonés."
        ),
        "why_not_complete": (
            "El resto de la obra se halla dedicado a análisis filológicos muy específicos del neoconfucianismo japonés del período "
            "Edo frente a la escuela del aprendizaje nacional (*Kokugaku*). Son estudios de historia intelectual que no alteran el "
            "andamiaje del fascismo japonés que se estudia en esta etapa."
        )
    },
    "etapa-86-polanyi-gran-transformacion": {
        "why_only_these": (
            "* **Capítulos Clave (principalmente del 3 al 6, y del 11 al 14):** Abordan el núcleo teórico: la invención de las "
            "\"mercancías ficticias\" (tierra, trabajo y dinero) y el concepto del \"doble movimiento\" (la autorregulación mercantil "
            "y la reacción de autodefensa social)."
        ),
        "why_not_complete": (
            "El libro contiene extensos y densos capítulos sobre la Ley de Pobres inglesa de Speenhamland de 1795, la Ley de Speenhamland "
            "de Gilbert y debates presupuestarios e historiográficos parlamentarios de los siglos XVIII y XIX que resultan sumamente "
            "específicos e inmanejables para la adquisición de la teoría general del Estado social."
        )
    },
    "etapa-87-esping-andersen": {
        "why_only_these": (
            "* **Capítulos 1 y 2:** Introducen de forma teórica los tres mundos del bienestar capitalista (socialdemócrata, corporativista "
            "y liberal), desarrollando los conceptos cardinales de desmercantilización y desfamiliarización del bienestar social."
        ),
        "why_not_complete": (
            "Los capítulos restantes consisten en minuciosos análisis empíricos econométricos e históricos basados en datos comparativos "
            "de jubilaciones, licencias médicas y empleo público de los países de la OCDE en las décadas de 1970 y 1980. Aunque valiosos "
            "para el especialista, son datos históricos fechados."
        )
    },
    "etapa-91-williams-marxismo-literatura": {
        "why_only_these": (
            "* **Capítulos sobre Hegemonía, Culturas Dominantes/Residuales/Emergentes y Estructuras del Sentir:** Concentran "
            "los conceptos claves que definen la aportación del materialismo cultural a la sociología del poder y el análisis de la ideología."
        ),
        "why_not_complete": (
            "El primer tercio del libro aborda discusiones de lingüística saussuriana clásica y semiótica teórica de los años 70 "
            "que hoy resultan superadas, y la parte final se enfoca en el análisis formal e histórico de la teoría literaria del drama "
            "británico, alejándose del análisis sociopolítico de la cultura."
        )
    },
    "etapa-93-bourdieu-distincion": {
        "why_only_these": (
            "* **Capítulos seleccionados sobre Habitus y Espacio de Capitales:** Exponen la teoría de cómo las preferencias "
            "y el gusto estético sirven como marcas invisibles pero rígidas de distinción de clase y reproducción de capital social."
        ),
        "why_not_complete": (
            "El volumen completo supera las 600 páginas e incluye cientos de tablas sociológicas empíricas que recopilan los hábitos "
            "de compra franceses de champú, pan y revistas de 1963, y la inclinación estética de obreros metalúrgicos frente a la pequeña "
            "burguesía parisina de la época. Son datos históricos redundantes para captar los conceptos sociológicos clave."
        )
    },
    "etapa-97-zuboff-vigilancia": {
        "why_only_these": (
            "* **Capítulos seleccionados sobre Excedente Conductual y Asimetría de Información:** Sientan el marco analítico de cómo "
            "el capitalismo informático extrae datos del comportamiento humano para modificarlos a gran escala con fines de lucro."
        ),
        "why_not_complete": (
            "Zuboff repite y amplía este mismo marco conceptual básico a lo largo de 700 páginas apoyándose en docenas de estudios de "
            "caso anecdóticos (como juguetes inteligentes conectados a internet y asistentes domésticos virtuales). La lectura selectiva "
            "evita la fatiga de la redundancia empírica."
        )
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
        
    if "## Justificación de la lectura seleccionada" in content:
        print(f"Skipping {filename} (already has justification)")
        continue
        
    # Find ## Tareas
    tareas_pos = content.find("## Tareas")
    if tareas_pos == -1:
        # try case variations
        tareas_pos = content.lower().find("## tareas")
        
    if tareas_pos == -1:
        print(f"Warning: Could not find '## Tareas' in {filename}")
        continue
        
    # Format the justification markdown block
    justification_md = f"""## Justificación de la lectura seleccionada

* **¿Por qué leer solo estos capítulos?**
    {data['why_only_these']}
* **¿Por qué no el libro completo?** {data['why_not_complete']}

"""
    
    new_content = content[:tareas_pos] + justification_md + content[tareas_pos:]
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Successfully patched {filename}")
    patched_count += 1

print(f"Patched {patched_count} files in total.")
