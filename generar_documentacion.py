#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar la documentacion completa de Transitar en PDF.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, ListFlowable, ListItem, KeepTogether
)
from reportlab.lib import colors
import os
from datetime import datetime

# --- CONFIG ---
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Transitar_Documentacion_Completa.pdf")

# Colors
PRIMARY = HexColor("#667eea")
PRIMARY_DARK = HexColor("#5a6fd6")
SECONDARY = HexColor("#764ba2")
DARK = HexColor("#2d3748")
GRAY = HexColor("#718096")
LIGHT_BG = HexColor("#f7fafc")
WHITE = HexColor("#ffffff")
GREEN = HexColor("#48bb78")
RED = HexColor("#fc8181")
YELLOW = HexColor("#ecc94b")
BLUE_LIGHT = HexColor("#ebf4ff")
ORANGE = HexColor("#ed8936")

# --- STYLES ---
styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle(
    name='CoverTitle',
    fontName='Helvetica-Bold',
    fontSize=28,
    textColor=PRIMARY,
    alignment=TA_CENTER,
    spaceAfter=10,
    leading=34,
))

styles.add(ParagraphStyle(
    name='CoverSubtitle',
    fontName='Helvetica',
    fontSize=14,
    textColor=GRAY,
    alignment=TA_CENTER,
    spaceAfter=6,
    leading=18,
))

styles.add(ParagraphStyle(
    name='ChapterTitle',
    fontName='Helvetica-Bold',
    fontSize=22,
    textColor=PRIMARY,
    spaceBefore=20,
    spaceAfter=14,
    leading=28,
    borderWidth=0,
    borderPadding=0,
))

styles.add(ParagraphStyle(
    name='SectionTitle',
    fontName='Helvetica-Bold',
    fontSize=16,
    textColor=DARK,
    spaceBefore=16,
    spaceAfter=8,
    leading=20,
))

styles.add(ParagraphStyle(
    name='SubSection',
    fontName='Helvetica-Bold',
    fontSize=13,
    textColor=PRIMARY_DARK,
    spaceBefore=12,
    spaceAfter=6,
    leading=16,
))

styles.add(ParagraphStyle(
    name='BodyText2',
    fontName='Helvetica',
    fontSize=10.5,
    textColor=DARK,
    spaceBefore=4,
    spaceAfter=6,
    leading=15,
    alignment=TA_JUSTIFY,
))

styles.add(ParagraphStyle(
    name='CodeBlock',
    fontName='Courier',
    fontSize=8.5,
    textColor=HexColor("#2d3748"),
    backColor=HexColor("#edf2f7"),
    spaceBefore=6,
    spaceAfter=6,
    leading=12,
    leftIndent=12,
    rightIndent=12,
    borderWidth=1,
    borderColor=HexColor("#e2e8f0"),
    borderPadding=8,
))

styles.add(ParagraphStyle(
    name='Callout',
    fontName='Helvetica',
    fontSize=10,
    textColor=PRIMARY_DARK,
    backColor=BLUE_LIGHT,
    spaceBefore=8,
    spaceAfter=8,
    leading=14,
    leftIndent=12,
    rightIndent=12,
    borderWidth=1,
    borderColor=PRIMARY,
    borderPadding=10,
))

styles.add(ParagraphStyle(
    name='BulletItem',
    fontName='Helvetica',
    fontSize=10.5,
    textColor=DARK,
    spaceBefore=2,
    spaceAfter=2,
    leading=14,
    leftIndent=20,
    bulletIndent=8,
))

styles.add(ParagraphStyle(
    name='TableHeader',
    fontName='Helvetica-Bold',
    fontSize=10,
    textColor=WHITE,
    alignment=TA_CENTER,
))

styles.add(ParagraphStyle(
    name='TableCell',
    fontName='Helvetica',
    fontSize=9.5,
    textColor=DARK,
    leading=13,
))

styles.add(ParagraphStyle(
    name='FooterStyle',
    fontName='Helvetica',
    fontSize=8,
    textColor=GRAY,
    alignment=TA_CENTER,
))

# --- HELPERS ---
def chapter(title):
    return Paragraph(title, styles['ChapterTitle'])

def section(title):
    return Paragraph(title, styles['SectionTitle'])

def subsection(title):
    return Paragraph(title, styles['SubSection'])

def body(text):
    return Paragraph(text, styles['BodyText2'])

def code(text):
    return Paragraph(text.replace('\n', '<br/>').replace(' ', '&nbsp;'), styles['CodeBlock'])

def callout(text):
    return Paragraph(text, styles['Callout'])

def bullet_list(items):
    elements = []
    for item in items:
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {item}", styles['BulletItem']))
    return elements

def hr():
    return HRFlowable(width="100%", thickness=1, color=HexColor("#e2e8f0"), spaceAfter=10, spaceBefore=10)

def small_spacer():
    return Spacer(1, 6)

def med_spacer():
    return Spacer(1, 12)

# --- PAGE TEMPLATE ---
def header_footer(canvas, doc):
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(PRIMARY)
    canvas.setLineWidth(2)
    canvas.line(2*cm, A4[1] - 1.5*cm, A4[0] - 2*cm, A4[1] - 1.5*cm)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(2*cm, A4[1] - 1.3*cm, "Transitar - Documentacion Tecnica y Funcional")
    # Footer
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(A4[0]/2, 1.2*cm, f"Pagina {doc.page}")
    canvas.drawRightString(A4[0] - 2*cm, 1.2*cm, "Documento confidencial")
    canvas.restoreState()


# --- BUILD DOCUMENT ---
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        topMargin=2.2*cm,
        bottomMargin=2*cm,
        leftMargin=2*cm,
        rightMargin=2*cm,
        title="Transitar - Documentacion Completa",
        author="Lisandro / Claude Code",
    )

    story = []

    # =====================================================
    # PORTADA
    # =====================================================
    story.append(Spacer(1, 6*cm))
    story.append(Paragraph("Transitar", styles['CoverTitle']))
    story.append(Paragraph("Plataforma de Seguridad Vial", styles['CoverSubtitle']))
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="50%", thickness=2, color=PRIMARY, spaceAfter=12, spaceBefore=12))
    story.append(Paragraph("Documentacion Tecnica y Funcional Completa", styles['CoverSubtitle']))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Version: Prototipo v1.0", styles['CoverSubtitle']))
    story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d de marzo de %Y')}", styles['CoverSubtitle']))
    story.append(Paragraph("Desarrollado con: Claude Code (IA)", styles['CoverSubtitle']))
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Documento preparado para el propietario de la idea", styles['CoverSubtitle']))
    story.append(PageBreak())

    # =====================================================
    # INDICE
    # =====================================================
    story.append(chapter("Indice de Contenidos"))
    story.append(hr())
    indice = [
        "1. Introduccion: Que es Transitar",
        "2. Conceptos basicos de programacion (para principiantes)",
        "3. Tecnologias utilizadas",
        "4. Estructura del proyecto en tu computadora",
        "5. Como funciona la app: todas las pantallas",
        "6. Arquitectura tecnica del codigo",
        "7. Funciones principales de JavaScript",
        "8. Datos y estructuras de informacion",
        "9. Integraciones externas (mapas, geolocalizacion)",
        "10. Aspectos legales e institucionales en Argentina",
        "11. Como editar el proyecto vos mismo",
        "12. Proximos pasos: de prototipo a app real",
        "13. Glosario de terminos tecnicos",
    ]
    for item in indice:
        story.append(Paragraph(item, styles['BodyText2']))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 1: INTRODUCCION
    # =====================================================
    story.append(chapter("1. Introduccion: Que es Transitar"))
    story.append(hr())

    story.append(body(
        "Transitar es un <b>prototipo funcional</b> (tambien llamado \"boceto digital\" o \"mockup interactivo\") "
        "de una aplicacion movil pensada para mejorar la seguridad vial en ciudades argentinas. "
        "No es una app terminada lista para publicar en una tienda de aplicaciones, sino una "
        "<b>demostracion visual y funcional</b> que permite ver como se veria y como funcionaria la app final."
    ))

    story.append(subsection("Para que sirve este prototipo?"))
    story.extend(bullet_list([
        "<b>Mostrar la idea:</b> Permite al propietario de la idea ver como funcionaria la app en un celular, tocar botones, navegar entre pantallas y entender el flujo completo.",
        "<b>Validar el concepto:</b> Antes de invertir dinero en desarrollo profesional, se puede mostrar a posibles inversores, socios o municipios.",
        "<b>Iterar rapido:</b> Es mucho mas facil y barato cambiar cosas en un prototipo que en una app ya publicada.",
        "<b>Base para desarrollo:</b> Sirve como \"plano\" para que un equipo de desarrollo profesional sepa exactamente que construir.",
    ]))

    story.append(subsection("Que puede hacer el usuario en la app?"))
    story.extend(bullet_list([
        "<b>Registrarse</b> como conductor (con patente) o como peaton.",
        "<b>Iniciar viaje</b> con bloqueo de celular y acumulacion de puntos.",
        "<b>Canjear puntos</b> por beneficios de combustible (integracion con YPF a futuro).",
        "<b>Buscar estacionamiento</b> en un mapa real, tanto privado como medido municipal.",
        "<b>Ofrecer su cochera</b> cuando no la usa y ganar dinero.",
        "<b>Reservar y pagar</b> estacionamiento antes de llegar.",
        "<b>Chatear con el propietario</b> del estacionamiento (solo despues de pagar).",
        "<b>Reportar estadias excedidas</b> con evidencia fotografica.",
        "<b>Consultar y pagar deudas</b> de transito asociadas a su patente.",
        "<b>Llamar a emergencias</b> con un boton rapido.",
    ]))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 2: CONCEPTOS BASICOS
    # =====================================================
    story.append(chapter("2. Conceptos basicos de programacion"))
    story.append(hr())

    story.append(callout(
        "<b>Nota:</b> Este capitulo esta pensado para alguien que nunca programo. "
        "Si ya sabes que es HTML, CSS y JavaScript, podes saltarlo."
    ))

    story.append(subsection("Que es una pagina web?"))
    story.append(body(
        "Todo lo que ves en un navegador de internet (Google Chrome, Firefox, Edge, Safari) esta construido "
        "con tres lenguajes que trabajan juntos, como si fueran tres capas de una torta:"
    ))

    # Table for HTML/CSS/JS
    data = [
        [Paragraph("<b>Lenguaje</b>", styles['TableHeader']),
         Paragraph("<b>Funcion</b>", styles['TableHeader']),
         Paragraph("<b>Analogia</b>", styles['TableHeader'])],
        [Paragraph("HTML", styles['TableCell']),
         Paragraph("Define la ESTRUCTURA y el CONTENIDO. Es el esqueleto: titulos, parrafos, botones, imagenes, formularios.", styles['TableCell']),
         Paragraph("Los ladrillos y la estructura de una casa: paredes, puertas, ventanas.", styles['TableCell'])],
        [Paragraph("CSS", styles['TableCell']),
         Paragraph("Define la APARIENCIA VISUAL. Colores, tamanos, espaciados, animaciones, tipografias.", styles['TableCell']),
         Paragraph("La pintura, los muebles, la decoracion, el diseno interior de la casa.", styles['TableCell'])],
        [Paragraph("JavaScript (JS)", styles['TableCell']),
         Paragraph("Define el COMPORTAMIENTO. Que pasa cuando tocas un boton, como se calculan los puntos, como se mueve el mapa.", styles['TableCell']),
         Paragraph("La electricidad, la plomeria, el sistema de alarma: todo lo que \"funciona\" en la casa.", styles['TableCell'])],
    ]

    t = Table(data, colWidths=[2.5*cm, 6.5*cm, 6.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ]))
    story.append(t)
    story.append(med_spacer())

    story.append(subsection("Que es un archivo?"))
    story.append(body(
        "Un archivo es un documento guardado en tu computadora. Asi como un documento de Word tiene extension "
        "<b>.docx</b> y una foto tiene extension <b>.jpg</b>, los archivos de programacion tienen sus propias extensiones:"
    ))
    story.extend(bullet_list([
        "<b>.html</b> - Archivo de pagina web (contiene HTML, y puede incluir CSS y JS dentro).",
        "<b>.css</b> - Archivo de estilos visuales (solo apariencia).",
        "<b>.js</b> - Archivo de JavaScript (solo comportamiento/logica).",
        "<b>.json</b> - Archivo de datos estructurados (configuraciones, listas).",
    ]))

    story.append(callout(
        "<b>Dato clave:</b> Nuestro prototipo completo esta en UN SOLO ARCHIVO: <b>index.html</b>. "
        "Esto es intencional: al ser un unico archivo, es muy facil de compartir (lo mandas por email, WhatsApp, "
        "o lo abris haciendo doble clic). Dentro de ese archivo estan las tres capas juntas: HTML + CSS + JS."
    ))

    story.append(subsection("Que es una terminal (o consola)?"))
    story.append(body(
        "La terminal es una ventana donde podes escribir comandos de texto para darle instrucciones a tu computadora. "
        "Es como hablarle a la computadora escribiendo en vez de haciendo clic. Por ejemplo, en vez de buscar una carpeta "
        "con el Explorador de Archivos, podes escribir un comando para ir directo a ella."
    ))
    story.append(body(
        "En Windows, hay varias terminales: <b>CMD</b> (Simbolo del Sistema), <b>PowerShell</b>, y <b>Git Bash</b>. "
        "Nosotros usamos la terminal integrada en <b>Claude Code</b>, que es similar a Git Bash. "
        "No necesitas usar la terminal directamente; Claude Code la usa por vos para ejecutar comandos."
    ))

    story.append(subsection("Que es un servidor web?"))
    story.append(body(
        "Un servidor web es un programa que \"sirve\" (entrega) archivos a un navegador. Cuando visitas "
        "www.google.com, un servidor en algun lugar del mundo le envia los archivos HTML/CSS/JS a tu navegador. "
        "Para nuestro prototipo, usamos un <b>servidor local</b>: un mini-servidor que corre en TU computadora "
        "y le entrega el archivo index.html a tu navegador. Se accede escribiendo <b>http://localhost:3000</b> "
        "en el navegador (localhost significa \"mi propia computadora\", y 3000 es el \"puerto\" o puerta de entrada)."
    ))

    story.append(subsection("Que es un CDN?"))
    story.append(body(
        "CDN significa Content Delivery Network (Red de Distribucion de Contenido). Es un servicio en internet "
        "que almacena archivos publicos (como librerias de codigo) para que cualquiera los pueda usar. "
        "Nosotros usamos CDNs para cargar la libreria Leaflet (mapas) sin tener que descargarla. "
        "Es como usar una imagen de internet en vez de guardarla en tu computadora."
    ))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 3: TECNOLOGIAS UTILIZADAS
    # =====================================================
    story.append(chapter("3. Tecnologias utilizadas"))
    story.append(hr())

    story.append(body(
        "A continuacion se detallan todas las tecnologias y herramientas que se usaron para construir el prototipo:"
    ))

    tech_data = [
        [Paragraph("<b>Tecnologia</b>", styles['TableHeader']),
         Paragraph("<b>Que es</b>", styles['TableHeader']),
         Paragraph("<b>Para que la usamos</b>", styles['TableHeader']),
         Paragraph("<b>Costo</b>", styles['TableHeader'])],
        [Paragraph("HTML5", styles['TableCell']),
         Paragraph("Lenguaje estandar para crear paginas web", styles['TableCell']),
         Paragraph("Toda la estructura de las pantallas de la app", styles['TableCell']),
         Paragraph("Gratis", styles['TableCell'])],
        [Paragraph("CSS3", styles['TableCell']),
         Paragraph("Lenguaje para disenar la apariencia visual", styles['TableCell']),
         Paragraph("Colores, botones, animaciones, diseno tipo celular", styles['TableCell']),
         Paragraph("Gratis", styles['TableCell'])],
        [Paragraph("JavaScript", styles['TableCell']),
         Paragraph("Lenguaje de programacion para interactividad", styles['TableCell']),
         Paragraph("Navegacion entre pantallas, mapas, temporizadores, chat", styles['TableCell']),
         Paragraph("Gratis", styles['TableCell'])],
        [Paragraph("Leaflet.js", styles['TableCell']),
         Paragraph("Libreria de mapas interactivos de codigo abierto", styles['TableCell']),
         Paragraph("Mostrar mapas reales con pines y ubicacion del usuario", styles['TableCell']),
         Paragraph("Gratis", styles['TableCell'])],
        [Paragraph("OpenStreetMap", styles['TableCell']),
         Paragraph("Mapa mundial colaborativo y abierto (como Wikipedia de mapas)", styles['TableCell']),
         Paragraph("Proveer las imagenes del mapa (calles, ciudades, etc)", styles['TableCell']),
         Paragraph("Gratis", styles['TableCell'])],
        [Paragraph("Nominatim API", styles['TableCell']),
         Paragraph("Servicio de geocodificacion (coordenadas a direccion)", styles['TableCell']),
         Paragraph("Convertir un punto del mapa en una direccion legible", styles['TableCell']),
         Paragraph("Gratis", styles['TableCell'])],
        [Paragraph("API de Geolocalizacion", styles['TableCell']),
         Paragraph("Funcion del navegador para obtener ubicacion GPS", styles['TableCell']),
         Paragraph("Centrar el mapa en la ubicacion real del usuario", styles['TableCell']),
         Paragraph("Gratis (del navegador)", styles['TableCell'])],
        [Paragraph("Node.js", styles['TableCell']),
         Paragraph("Entorno de ejecucion de JavaScript fuera del navegador", styles['TableCell']),
         Paragraph("Correr el servidor local para previsualizar la app", styles['TableCell']),
         Paragraph("Gratis", styles['TableCell'])],
        [Paragraph("Claude Code", styles['TableCell']),
         Paragraph("Asistente de programacion con IA de Anthropic", styles['TableCell']),
         Paragraph("Escribir todo el codigo, disenar la app, probar funcionalidades", styles['TableCell']),
         Paragraph("Suscripcion", styles['TableCell'])],
    ]

    t2 = Table(tech_data, colWidths=[3*cm, 4.5*cm, 5.5*cm, 2.5*cm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ]))
    story.append(t2)

    story.append(callout(
        "<b>Importante:</b> TODAS las tecnologias usadas son gratuitas y de codigo abierto, "
        "excepto Claude Code (que es la herramienta de IA con la que se escribio el codigo). "
        "No se necesitan claves de API, licencias ni pagos adicionales para que el prototipo funcione."
    ))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 4: ESTRUCTURA DEL PROYECTO
    # =====================================================
    story.append(chapter("4. Estructura del proyecto en tu computadora"))
    story.append(hr())

    story.append(body(
        "El proyecto esta guardado en tu computadora en la siguiente ubicacion exacta:"
    ))

    story.append(code("C:\\Users\\Lisandro\\Documents\\Proyectos\\transit-app\\"))

    story.append(body(
        "Para llegar a esta carpeta, podes abrir el <b>Explorador de Archivos</b> de Windows (la carpeta amarilla "
        "en la barra de tareas) y navegar asi:"
    ))

    story.extend(bullet_list([
        "Este equipo > Disco Local (C:) > Usuarios > Lisandro > Documentos > Proyectos > transit-app",
    ]))

    story.append(subsection("Contenido de la carpeta transit-app"))

    folder_data = [
        [Paragraph("<b>Archivo/Carpeta</b>", styles['TableHeader']),
         Paragraph("<b>Que es</b>", styles['TableHeader']),
         Paragraph("<b>Lo necesitas editar?</b>", styles['TableHeader'])],
        [Paragraph("index.html", styles['TableCell']),
         Paragraph("EL ARCHIVO PRINCIPAL. Contiene TODA la app: las pantallas, los estilos, y la logica. Es el unico archivo que importa para la app.", styles['TableCell']),
         Paragraph("SI - es lo unico que necesitas tocar si queres cambiar algo de la app", styles['TableCell'])],
        [Paragraph("package.json", styles['TableCell']),
         Paragraph("Archivo de configuracion de Node.js. Define las dependencias (librerias necesarias) y comandos del proyecto.", styles['TableCell']),
         Paragraph("NO - no lo toques", styles['TableCell'])],
        [Paragraph("node_modules/", styles['TableCell']),
         Paragraph("Carpeta automatica con las librerias descargadas (como 'serve' para el servidor local). Puede tener miles de archivos - es normal.", styles['TableCell']),
         Paragraph("NO - nunca toques esta carpeta", styles['TableCell'])],
        [Paragraph(".claude/", styles['TableCell']),
         Paragraph("Carpeta de configuracion de Claude Code. Contiene el archivo launch.json para el servidor de previsualizacion.", styles['TableCell']),
         Paragraph("NO - es automatica", styles['TableCell'])],
        [Paragraph("generar_documentacion.py", styles['TableCell']),
         Paragraph("El script de Python que genero este mismo PDF que estas leyendo.", styles['TableCell']),
         Paragraph("NO - es utilitario", styles['TableCell'])],
    ]

    t3 = Table(folder_data, colWidths=[4*cm, 7*cm, 4.5*cm])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ]))
    story.append(t3)

    story.append(callout(
        "<b>Resumen:</b> Si queres modificar la app, el UNICO archivo que necesitas abrir y editar es "
        "<b>index.html</b>. Todo lo demas es infraestructura automatica que no deberias tocar."
    ))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 5: PANTALLAS DE LA APP
    # =====================================================
    story.append(chapter("5. Como funciona la app: todas las pantallas"))
    story.append(hr())

    story.append(body(
        "La app esta compuesta por multiples <b>pantallas</b> (en programacion se les dice \"screens\" o \"vistas\"). "
        "Solo una pantalla se muestra a la vez, y cuando tocas un boton, se oculta la actual y aparece otra. "
        "Es como pasar paginas de un libro, pero de forma digital."
    ))

    story.append(subsection("5.1 Pantalla de Bienvenida (welcome)"))
    story.append(body(
        "Es la primera pantalla que ve el usuario al abrir la app. Muestra el logo y nombre \"Transitar\", "
        "el slogan \"Tu aliado en seguridad vial\", y dos botones: \"Crear Cuenta\" (para registrarse) y "
        "\"Ya tengo cuenta\" (para iniciar sesion)."
    ))

    story.append(subsection("5.2 Pantalla de Registro (register)"))
    story.append(body(
        "Formulario donde el usuario se registra. Debe ingresar nombre completo, email, contrasena, "
        "y elegir su rol: <b>Conductor</b> o <b>Peaton</b>. Si elige Conductor, aparece un campo adicional "
        "para ingresar la patente del vehiculo. Al registrarse, se guarda en la variable <i>currentUser</i> "
        "y se navega al Home."
    ))

    story.append(subsection("5.3 Pantalla de Login (login)"))
    story.append(body(
        "Formulario simple con email y contrasena. Como es un prototipo, cualquier dato ingresado funciona "
        "(no hay base de datos real validando credenciales). Al hacer login, se simula un usuario conductor "
        "con datos de ejemplo."
    ))

    story.append(subsection("5.4 Pantalla Principal - Home (home)"))
    story.append(body(
        "Es el \"centro de mando\" de la app. Se adapta segun el rol del usuario:"
    ))
    story.extend(bullet_list([
        "<b>Para conductores:</b> Muestra la patente, un banner con puntos acumulados, accesos rapidos (Viaje, Estacionamiento, Deudas, Emergencia), y una barra de navegacion inferior con Inicio, Viaje, Estacionamiento, Puntos y Perfil.",
        "<b>Para peatones:</b> Muestra un perfil mas simple, sin las funciones de conduccion ni patente.",
    ]))

    story.append(subsection("5.5 Pantalla de Viaje (trip)"))
    story.append(body(
        "El conductor toca \"Iniciar Viaje\" y se activa un cronometro que cuenta el tiempo conduciendo. "
        "La idea es que durante el viaje la app bloquearia llamadas y mensajes (en la version final). "
        "Al finalizar el viaje, se suman puntos proporcionalmente al tiempo conducido sin usar el celular. "
        "Se muestra la velocidad simulada, puntos ganandose en tiempo real, y un boton grande para terminar."
    ))

    story.append(subsection("5.6 Pantalla de Puntos (points)"))
    story.append(body(
        "Muestra el historial de puntos acumulados, el nivel del usuario (Principiante, Intermedio, Experto), "
        "una barra de progreso, y la seccion de canje por beneficios de YPF (marcada como \"PROXIMAMENTE\"). "
        "Los puntos se ganan viajando sin usar el celular."
    ))

    story.append(subsection("5.7 Pantalla de Deudas (debts)"))
    story.append(body(
        "Lista las deudas de transito asociadas a la patente del conductor. Muestra multas simuladas con "
        "montos, fechas, y un boton para pagar. En la version final, esta informacion vendria del municipio."
    ))

    story.append(subsection("5.8 Pantalla de Emergencia (emergency)"))
    story.append(body(
        "Boton grande para llamar al 911 y opciones de emergencia rapida. Incluye la posibilidad de configurar "
        "contactos de emergencia que serian los unicos autorizados durante el modo viaje."
    ))

    story.append(subsection("5.9 Pantalla de Perfil (profile)"))
    story.append(body(
        "Muestra los datos del usuario, permite editarlos y cerrar sesion."
    ))
    story.append(PageBreak())

    story.append(subsection("5.10 Hub de Estacionamiento (parking-hub)"))
    story.append(body(
        "Pantalla central del sistema de estacionamiento. Ofrece dos opciones principales: "
        "<b>Buscar Estacionamiento</b> (para encontrar donde estacionar) y <b>Ofrecer Mi Espacio</b> "
        "(para publicar tu cochera). Tambien menciona que se puede buscar y pagar estacionamiento medido municipal."
    ))

    story.append(subsection("5.11 Busqueda de Estacionamiento (parking-search)"))
    story.append(body(
        "Muestra un mapa interactivo real (con Leaflet + OpenStreetMap) centrado en Buenos Aires. "
        "Aparecen marcadores de estacionamiento disponibles: cocheras privadas (con icono de casa) "
        "y estacionamiento medido (con icono de P). El usuario toca un marcador para ver el detalle."
    ))

    story.append(subsection("5.12 Detalle del Estacionamiento (parking-detail)"))
    story.append(body(
        "Muestra toda la informacion de un espacio: direccion, precio por hora, distancia, tipo "
        "(privado o medido), horario de disponibilidad, datos del propietario, calificacion, "
        "instrucciones, y un mapa con la ubicacion exacta. Solo tiene un boton: <b>Reservar y Pagar</b>. "
        "El chat NO esta disponible en esta pantalla (se habilita despues del pago)."
    ))

    story.append(subsection("5.13 Pre-pago (pre-payment)"))
    story.append(body(
        "Al tocar \"Reservar y Pagar\", se abre esta pantalla donde el conductor elige la duracion "
        "(botones rapidos de 1h, 2h, 3h, 4h o personalizado), ve el calculo automatico del costo total, "
        "elige medio de pago (Billetera Virtual o Tarjeta), y confirma la reserva. "
        "El precio se calcula multiplicando la tarifa por hora por la cantidad de horas elegidas."
    ))

    story.append(subsection("5.14 Sesion Activa de Estacionamiento (parking-session)"))
    story.append(body(
        "Despues de pagar, se muestra esta pantalla con un cronometro corriendo que muestra el tiempo "
        "estacionado, el costo acumulado, la tarifa, la hora de inicio, y la hora hasta la cual puede "
        "quedarse. Aqui SI aparecen dos botones: <b>Chatear con el propietario</b> (para comunicarse) "
        "y <b>Liberar Estacionamiento</b> (para irse)."
    ))

    story.append(callout(
        "<b>Flujo importante:</b> El chat solo se habilita DESPUES de haber pagado. "
        "Esto protege al propietario de recibir mensajes de personas que no tienen intencion de reservar."
    ))

    story.append(subsection("5.15 Chat (spot-chat)"))
    story.append(body(
        "Pantalla de mensajeria entre el conductor y el propietario del espacio. El conductor puede escribir "
        "un mensaje y enviarlo. La app simula respuestas automaticas del propietario despues de unos segundos "
        "(en la version real, seria un chat en tiempo real). Se accede SOLO desde parking-session."
    ))

    story.append(subsection("5.16 Ofrecer Mi Espacio (parking-offer)"))
    story.append(body(
        "Formulario para publicar tu cochera. El propietario ingresa la direccion, marca la ubicacion "
        "en el mapa (con un pin que puede mover), establece el precio por hora, selecciona dias y horario "
        "de disponibilidad, y agrega instrucciones opcionales. Al publicar, el espacio aparece en la seccion "
        "\"Mis Espacios Publicados\" como tarjetas clickeables."
    ))
    story.append(PageBreak())

    story.append(subsection("5.17 Detalle de Mi Cochera (my-spot-detail)"))
    story.append(body(
        "Cuando un propietario toca una de sus cocheras publicadas, se abre esta pantalla que muestra: "
        "la direccion, el horario, el precio por hora, los ingresos totales simulados, y una lista de "
        "<b>todas las reservas</b> de esa cochera con tres posibles estados:"
    ))

    status_data = [
        [Paragraph("<b>Estado</b>", styles['TableHeader']),
         Paragraph("<b>Color</b>", styles['TableHeader']),
         Paragraph("<b>Significado</b>", styles['TableHeader']),
         Paragraph("<b>Accion disponible</b>", styles['TableHeader'])],
        [Paragraph("En curso", styles['TableCell']),
         Paragraph("Verde", styles['TableCell']),
         Paragraph("El conductor esta usando la cochera dentro del horario pactado", styles['TableCell']),
         Paragraph("Ninguna (todo en orden)", styles['TableCell'])],
        [Paragraph("Excedida", styles['TableCell']),
         Paragraph("Rojo", styles['TableCell']),
         Paragraph("El conductor NO retiro su vehiculo y paso la hora pactada", styles['TableCell']),
         Paragraph("Boton: Reportar estadia excedida", styles['TableCell'])],
        [Paragraph("Finalizada", styles['TableCell']),
         Paragraph("Gris", styles['TableCell']),
         Paragraph("La reserva ya termino y el conductor se fue", styles['TableCell']),
         Paragraph("Ninguna (registro historico)", styles['TableCell'])],
    ]

    t4 = Table(status_data, colWidths=[2.5*cm, 2*cm, 5.5*cm, 5.5*cm])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ]))
    story.append(t4)

    story.append(subsection("5.18 Reporte de Estadia Excedida (overstay-report)"))
    story.append(body(
        "Al tocar \"Reportar estadia excedida\" en una reserva, se abre esta pantalla que muestra: "
        "nombre del conductor, patente, hora pactada de salida, hora actual, tiempo excedido calculado "
        "automaticamente, un boton para capturar foto como evidencia (obligatorio), y un campo para "
        "comentario opcional. Al enviar el reporte, se vuelve a la vista de esa cochera (my-spot-detail). "
        "En la version real, se notificaria al conductor y se le cobraria un recargo."
    ))

    story.append(subsection("5.19 Notificacion Push de Infraccion (infraction-alert)"))
    story.append(body(
        "Es una funcionalidad que esta construida en el codigo pero actualmente desactivada de la navegacion principal "
        "(queda para implementacion futura). Simulaba una notificacion de infraccion detectada con opcion de pago "
        "con descuento. La animacion de la notificacion push (el cartelito que baja desde arriba) sigue visible "
        "como demostracion visual."
    ))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 6: ARQUITECTURA TECNICA
    # =====================================================
    story.append(chapter("6. Arquitectura tecnica del codigo"))
    story.append(hr())

    story.append(body(
        "El archivo <b>index.html</b> tiene aproximadamente <b>5000 lineas de codigo</b> y esta organizado en tres secciones:"
    ))

    story.append(subsection("6.1 Seccion de Estilos (CSS) - Lineas ~1 a ~1200"))
    story.append(body(
        "Todo el diseno visual esta contenido dentro de una etiqueta <b>&lt;style&gt;</b>. Incluye:"
    ))
    story.extend(bullet_list([
        "<b>Variables CSS (Custom Properties):</b> Definen los colores principales de la app en un solo lugar. Si cambias el color ahi, cambia en toda la app. Estan al inicio con nombres como --primary, --secondary, --dark, etc.",
        "<b>Diseno del telefono:</b> En computadoras de escritorio, la app se muestra dentro de un marco que simula un celular (390x844 pixeles, como un iPhone). En celulares reales, ocupa toda la pantalla.",
        "<b>Componentes:</b> Cada elemento visual tiene su estilo: botones (.btn), tarjetas (.card), campos de formulario (.input-group), la barra de navegacion inferior (.bottom-nav), etc.",
        "<b>Animaciones:</b> Se definen con @keyframes. Por ejemplo, slideIn hace que las pantallas aparezcan deslizandose, pulse hace que los botones pulsen, y la notificacion push tiene un efecto de deslizamiento desde arriba.",
        "<b>Responsive Design:</b> Con @media queries se adapta el diseno segun el tamano de la pantalla.",
    ]))

    story.append(subsection("6.2 Seccion de Estructura (HTML) - Lineas ~1200 a ~3500"))
    story.append(body(
        "Contiene todas las pantallas como <b>&lt;div&gt;</b> con clase \"screen\". Cada pantalla tiene un "
        "<b>id</b> unico (como \"home\", \"trip\", \"parking-hub\") que se usa para mostrarla u ocultarla. "
        "Solo una pantalla tiene la clase \"active\" a la vez (la que se muestra)."
    ))

    story.append(body(
        "Ejemplo simplificado de como se ve una pantalla en el codigo:"
    ))

    story.append(code(
        '&lt;div id="home" class="screen"&gt;\n'
        '  &lt;div class="header"&gt;\n'
        '    &lt;h1&gt;Hola, Lisandro&lt;/h1&gt;\n'
        '  &lt;/div&gt;\n'
        '  &lt;div class="content"&gt;\n'
        '    &lt;!-- Aqui va el contenido --&gt;\n'
        '  &lt;/div&gt;\n'
        '  &lt;div class="bottom-nav"&gt;\n'
        '    &lt;!-- Barra de navegacion inferior --&gt;\n'
        '  &lt;/div&gt;\n'
        '&lt;/div&gt;'
    ))

    story.append(subsection("6.3 Seccion de Logica (JavaScript) - Lineas ~3500 a ~5000"))
    story.append(body(
        "Todo el comportamiento de la app esta dentro de una etiqueta <b>&lt;script&gt;</b>. Incluye las "
        "variables globales (datos), las funciones (acciones), y la logica de navegacion."
    ))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 7: FUNCIONES PRINCIPALES
    # =====================================================
    story.append(chapter("7. Funciones principales de JavaScript"))
    story.append(hr())

    story.append(body(
        "Una <b>funcion</b> en programacion es un bloque de codigo que realiza una tarea especifica. "
        "Se le pone un nombre y se la puede \"llamar\" (ejecutar) cuando se necesite. Es como una receta: "
        "la escribis una vez, y la podes usar cada vez que quieras hacer ese plato."
    ))

    funcs = [
        ("showScreen(screenId)", "Funcion principal de navegacion. Recibe el nombre de una pantalla (ej: 'home', 'trip') y la muestra, ocultando la anterior. Tambien inicializa los mapas si la pantalla los necesita."),
        ("setupHome()", "Configura la pantalla principal segun el rol del usuario. Si es conductor, muestra patente, viaje, etc. Si es peaton, oculta esas funciones."),
        ("toggleTrip()", "Inicia o detiene un viaje. Al iniciar, arranca un cronometro que suma puntos cada segundo. Al detener, calcula los puntos totales y muestra un resumen."),
        ("initReportMap()", "Inicializa el mapa de Leaflet en la pantalla de reporte de infracciones (funcionalidad pausada actualmente)."),
        ("initParkingSearchMap()", "Inicializa el mapa de busqueda de estacionamiento con los marcadores de cocheras privadas y medidas."),
        ("initOfferMap()", "Inicializa el mapa en la pantalla de publicar cochera, permitiendo al usuario marcar la ubicacion exacta."),
        ("placeMarker(lat, lng)", "Coloca un pin en el mapa en las coordenadas dadas y usa la API de Nominatim para obtener la direccion correspondiente (geocodificacion inversa)."),
        ("showParkingDetail(spotId)", "Recibe el ID de un estacionamiento y muestra toda su informacion en la pantalla de detalle."),
        ("openPrePayment()", "Abre la pantalla de pre-pago con los datos del estacionamiento seleccionado. Calcula el horario disponible y el precio."),
        ("updatePrePayTotal()", "Recalcula el costo total cada vez que el usuario cambia la duracion. Multiplica tarifa por hora x cantidad de horas."),
        ("setDuration(hours, el)", "Funcion de los botones rapidos de duracion (1h, 2h, 3h, 4h). Actualiza el campo de horas y recalcula el total."),
        ("confirmPrePayment()", "Procesa el pago, muestra un popup de confirmacion, e inicia la sesion de estacionamiento con el cronometro."),
        ("openSpotChat()", "Abre la pantalla de chat con el propietario. Solo accesible desde parking-session (despues del pago)."),
        ("sendChatMessage()", "Envia un mensaje en el chat y simula una respuesta automatica del propietario despues de unos segundos."),
        ("renderMySpots()", "Dibuja la lista de cocheras publicadas por el usuario en la pantalla parking-offer. Cada cochera es una tarjeta clickeable que abre el detalle."),
        ("openMySpotDetail(spotIndex)", "Abre el detalle de una cochera publicada, mostrando su informacion y todas las reservas con sus estados."),
        ("openOverstayReport(driver, patente, scheduledEnd)", "Abre la pantalla de reporte de estadia excedida con los datos del conductor que se excedio."),
        ("takeOverstayPhoto()", "Simula capturar una foto como evidencia. En la version real, abriria la camara del celular."),
        ("submitOverstayReport()", "Envia el reporte de estadia excedida (requiere foto obligatoria) y vuelve a la vista de la cochera."),
        ("showPushNotification(type)", "Muestra una notificacion animada tipo push que baja desde arriba de la pantalla (actualmente usada para demo de infracciones)."),
    ]

    for fname, fdesc in funcs:
        story.append(Paragraph(f"<b><font color='#667eea'>{fname}</font></b>", styles['BodyText2']))
        story.append(Paragraph(fdesc, styles['BulletItem']))
        story.append(small_spacer())

    story.append(PageBreak())

    # =====================================================
    # CAPITULO 8: DATOS Y ESTRUCTURAS
    # =====================================================
    story.append(chapter("8. Datos y estructuras de informacion"))
    story.append(hr())

    story.append(body(
        "La app usa <b>variables globales</b> para almacenar informacion. Una variable es como una caja "
        "con etiqueta donde guardas datos. En un prototipo, estos datos son simulados; en la app final, "
        "vendrian de una base de datos real."
    ))

    story.append(subsection("8.1 currentUser (usuario actual)"))
    story.append(body("Objeto que almacena los datos del usuario logueado:"))
    story.append(code(
        "currentUser = {\n"
        "  name: 'Lisandro',\n"
        "  email: 'lisandro@email.com',\n"
        "  role: 'conductor',    // o 'peaton'\n"
        "  patente: 'ABC 123'\n"
        "}"
    ))

    story.append(subsection("8.2 parkingSpots (estacionamientos disponibles)"))
    story.append(body("Objeto con los estacionamientos que se muestran en el mapa de busqueda:"))
    story.append(code(
        "parkingSpots = {\n"
        "  private1: {\n"
        "    name: 'Cochera de Martin',\n"
        "    address: 'Av. Corrientes 1842',\n"
        "    price: 500,    // pesos por hora\n"
        "    type: 'private',\n"
        "    lat: -34.6037, lng: -58.3816,\n"
        "    owner: 'Martin Rodriguez',\n"
        "    rating: 4.8,\n"
        "    ...\n"
        "  },\n"
        "  metered1: { ... },  // Estacionamiento medido\n"
        "  private2: { ... },  // Otra cochera privada\n"
        "}"
    ))

    story.append(subsection("8.3 publishedSpots (cocheras publicadas por el usuario)"))
    story.append(body(
        "Array (lista) de cocheras que el usuario actual ha publicado para alquilar. "
        "Cada cochera tiene un array de <b>reservaciones</b>:"
    ))
    story.append(code(
        "publishedSpots = [\n"
        "  {\n"
        "    address: 'Av. Santa Fe 2100',\n"
        "    price: 400,\n"
        "    schedule: '8:00 - 20:00',\n"
        "    lat: -34.595, lng: -58.399,\n"
        "    reservations: [\n"
        "      {\n"
        "        driver: 'Juan Perez',\n"
        "        patente: 'AB 123 CD',\n"
        "        from: '10:00',\n"
        "        to: '12:00',\n"
        "        status: 'overstay'  // excedido\n"
        "      },\n"
        "      { ... status: 'active' },\n"
        "      { ... status: 'completed' }\n"
        "    ]\n"
        "  }\n"
        "]"
    ))

    story.append(subsection("8.4 fineAmounts (montos de multas)"))
    story.append(body("Objeto que mapea tipos de infraccion a montos de multa en pesos:"))
    story.append(code(
        "fineAmounts = {\n"
        "  'Exceso de velocidad': 45000,\n"
        "  'Estacionamiento prohibido': 30000,\n"
        "  'Semaforo en rojo': 60000,\n"
        "  ...\n"
        "}"
    ))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 9: INTEGRACIONES EXTERNAS
    # =====================================================
    story.append(chapter("9. Integraciones externas"))
    story.append(hr())

    story.append(subsection("9.1 Mapas con Leaflet + OpenStreetMap"))
    story.append(body(
        "Los mapas reales de la app se implementan con dos componentes que trabajan juntos:"
    ))
    story.extend(bullet_list([
        "<b>Leaflet.js</b> es la libreria de JavaScript que dibuja el mapa interactivo en la pantalla: permite hacer zoom, mover, poner pines, y detectar toques. Se carga desde un CDN con dos lineas en el HTML.",
        "<b>OpenStreetMap (OSM)</b> es el proveedor de las imagenes del mapa (lo que se llaman \"tiles\" o baldosas). OSM es gratuito y no requiere clave de API, a diferencia de Google Maps que es pago.",
    ]))
    story.append(body(
        "Cada mapa se inicializa con coordenadas centrales (Buenos Aires: -34.6037, -58.3816), un nivel de zoom, "
        "y se le agregan marcadores (pines) con popups informativos."
    ))

    story.append(subsection("9.2 Geocodificacion con Nominatim"))
    story.append(body(
        "Cuando el usuario toca un punto en el mapa, la app necesita saber que direccion corresponde a esa ubicacion. "
        "Para eso usa la <b>API de Nominatim</b>, un servicio gratuito de OpenStreetMap que convierte coordenadas "
        "(latitud/longitud) en direcciones legibles. Por ejemplo: (-34.6037, -58.3816) se convierte en \"Av. Corrientes 1234, CABA\"."
    ))
    story.append(body(
        "Esto se llama <b>geocodificacion inversa</b> (reverse geocoding). La app hace una peticion HTTP "
        "(una solicitud a traves de internet) al servidor de Nominatim, que responde con la direccion."
    ))

    story.append(subsection("9.3 Geolocalizacion del navegador"))
    story.append(body(
        "La app usa la <b>API de Geolocalizacion</b> del navegador (navigator.geolocation) para obtener "
        "la ubicacion GPS real del usuario. Cuando el usuario lo permite, el mapa se centra en su posicion actual "
        "y aparece un circulo azul indicando donde esta. Esta funcion requiere que el usuario de permiso "
        "en el navegador y funciona mejor en dispositivos con GPS (celulares)."
    ))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 10: ASPECTOS LEGALES
    # =====================================================
    story.append(chapter("10. Aspectos legales e institucionales"))
    story.append(hr())

    story.append(body(
        "Para que la app funcione legalmente en Argentina, se necesita coordinar con varias entidades. "
        "A continuacion se detallan los <b>players</b> (actores institucionales) necesarios:"
    ))

    legal_data = [
        [Paragraph("<b>Entidad</b>", styles['TableHeader']),
         Paragraph("<b>Funcion</b>", styles['TableHeader']),
         Paragraph("<b>Para que funcionalidad</b>", styles['TableHeader'])],
        [Paragraph("DNRPA (Direccion Nacional del Registro de la Propiedad del Automotor)", styles['TableCell']),
         Paragraph("Valida que el conductor sea efectivamente el titular del vehiculo registrado con esa patente.", styles['TableCell']),
         Paragraph("Registro de conductores con patente", styles['TableCell'])],
        [Paragraph("Registro de la Propiedad Inmueble (provincial)", styles['TableCell']),
         Paragraph("Valida que quien ofrece una cochera sea propietario o tenga derecho de uso sobre el inmueble.", styles['TableCell']),
         Paragraph("Publicacion de cocheras privadas", styles['TableCell'])],
        [Paragraph("AFIP / Monotributo", styles['TableCell']),
         Paragraph("Los ingresos por alquiler de cochera deben estar declarados fiscalmente.", styles['TableCell']),
         Paragraph("Sistema de pagos entre usuarios", styles['TableCell'])],
        [Paragraph("PSP (Proveedor de Servicios de Pago) - Ej: Mercado Pago", styles['TableCell']),
         Paragraph("Procesar los pagos digitales de forma segura y regulada.", styles['TableCell']),
         Paragraph("Todas las transacciones economicas", styles['TableCell'])],
        [Paragraph("Defensa del Consumidor", styles['TableCell']),
         Paragraph("Garantizar derechos del usuario como consumidor del servicio.", styles['TableCell']),
         Paragraph("Terminos de servicio y proteccion al usuario", styles['TableCell'])],
        [Paragraph("AAIP (Agencia de Acceso a la Info Publica)", styles['TableCell']),
         Paragraph("Cumplir con la Ley de Proteccion de Datos Personales (25.326). La app maneja datos sensibles: ubicacion, patente, fotos.", styles['TableCell']),
         Paragraph("Toda la app (datos personales)", styles['TableCell'])],
        [Paragraph("SSN (Superintendencia de Seguros de la Nacion)", styles['TableCell']),
         Paragraph("Para la futura integracion con empresas de seguro y notificaciones de infracciones.", styles['TableCell']),
         Paragraph("Funcionalidad de seguros (futura)", styles['TableCell'])],
        [Paragraph("Municipios", styles['TableCell']),
         Paragraph("Cada municipio maneja su propio sistema de estacionamiento medido, multas y registros de transito.", styles['TableCell']),
         Paragraph("Estacionamiento medido, multas, infracciones", styles['TableCell'])],
    ]

    t5 = Table(legal_data, colWidths=[4*cm, 5.5*cm, 4*cm])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BG]),
    ]))
    story.append(t5)
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 11: COMO EDITAR
    # =====================================================
    story.append(chapter("11. Como editar el proyecto vos mismo"))
    story.append(hr())

    story.append(subsection("11.1 Abrir el archivo para editarlo"))
    story.append(body("Hay varias formas de abrir y editar el archivo <b>index.html</b>:"))

    story.append(Paragraph("<b>Opcion A: Con el Bloc de Notas de Windows (basico)</b>", styles['BodyText2']))
    story.extend(bullet_list([
        "Navega a C:\\Users\\Lisandro\\Documents\\Proyectos\\transit-app\\",
        "Clic derecho sobre index.html > Abrir con > Bloc de notas",
        "Edita lo que necesites y guarda con Ctrl+S",
    ]))

    story.append(Paragraph("<b>Opcion B: Con Visual Studio Code (recomendado)</b>", styles['BodyText2']))
    story.extend(bullet_list([
        "Descarga VS Code gratis desde https://code.visualstudio.com",
        "Instala y abrilo",
        "Archivo > Abrir Carpeta > navega a la carpeta transit-app",
        "Hace clic en index.html en el panel izquierdo",
        "VS Code te muestra el codigo con colores (syntax highlighting), numeros de linea, y muchas ayudas",
    ]))

    story.append(callout(
        "<b>Recomendacion:</b> Si vas a editar codigo, usa Visual Studio Code. Es gratuito, "
        "y te muestra errores, te autocompleta texto, y tiene miles de extensiones utiles. "
        "El Bloc de Notas funciona pero es mucho mas limitado."
    ))

    story.append(subsection("11.2 Ver la app en el navegador"))
    story.append(body(
        "Para ver los cambios que hagas, hay dos opciones:"
    ))

    story.append(Paragraph("<b>Opcion simple: Doble clic</b>", styles['BodyText2']))
    story.extend(bullet_list([
        "Hace doble clic en index.html y se abre en tu navegador",
        "Cada vez que hagas cambios, guarda el archivo y apreta F5 en el navegador para recargar",
        "Nota: algunos features (como mapas) pueden no funcionar bien con este metodo",
    ]))

    story.append(Paragraph("<b>Opcion profesional: Servidor local</b>", styles['BodyText2']))
    story.extend(bullet_list([
        "Abri una terminal (CMD o PowerShell) en la carpeta del proyecto",
        "Escribi: npx serve (y presiona Enter)",
        "Se abre un servidor local. Navega a http://localhost:3000 en tu navegador",
        "Los mapas y todas las funciones van a andar correctamente",
    ]))

    story.append(subsection("11.3 Cambios comunes que podes hacer"))

    story.append(Paragraph("<b>Cambiar un color:</b>", styles['BodyText2']))
    story.append(body(
        "Busca la seccion de variables CSS al inicio del archivo (lineas ~10-20). "
        "Cambia el valor hexadecimal del color. Por ejemplo:"
    ))
    story.append(code("--primary: #667eea;   /* Violeta actual */\n--primary: #e63946;   /* Cambiar a rojo */"))

    story.append(Paragraph("<b>Cambiar un texto:</b>", styles['BodyText2']))
    story.append(body(
        "Usa Ctrl+H (buscar y reemplazar) en tu editor para encontrar el texto que queres cambiar. "
        "Por ejemplo, para cambiar \"Transitar\" por otro nombre, busca \"Transitar\" y reemplazalo."
    ))

    story.append(Paragraph("<b>Cambiar un precio simulado:</b>", styles['BodyText2']))
    story.append(body(
        "Busca el objeto <i>parkingSpots</i> en el codigo JavaScript y cambia el valor de <i>price</i>."
    ))

    story.append(Paragraph("<b>Agregar un estacionamiento nuevo al mapa:</b>", styles['BodyText2']))
    story.append(body(
        "Busca <i>parkingSpots</i> y agrega un nuevo objeto siguiendo el mismo formato de los existentes. "
        "Necesitas nombre, direccion, precio, coordenadas (lat/lng), y tipo."
    ))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 12: PROXIMOS PASOS
    # =====================================================
    story.append(chapter("12. Proximos pasos: de prototipo a app real"))
    story.append(hr())

    story.append(body(
        "Actualmente tenemos un <b>prototipo web</b>. Para convertirlo en una app real descargable "
        "desde las tiendas (Google Play Store / Apple App Store), hay un camino de desarrollo. "
        "Estas son las etapas:"
    ))

    story.append(subsection("Etapa 1: Validacion del prototipo (ACTUAL)"))
    story.extend(bullet_list([
        "Mostrar el prototipo al propietario de la idea y posibles inversores",
        "Recopilar feedback y hacer ajustes al diseno",
        "Definir cuales funcionalidades son prioridad para la version 1.0",
    ]))

    story.append(subsection("Etapa 2: Desarrollo de la app real"))
    story.extend(bullet_list([
        "<b>Framework recomendado:</b> React Native o Flutter (permiten hacer UNA app que funcione en Android y iPhone al mismo tiempo)",
        "<b>Backend (servidor):</b> Se necesita un servidor en la nube que guarde los datos reales: usuarios, cocheras, reservas, pagos, etc. Opciones: Node.js + PostgreSQL, o servicios como Firebase/Supabase",
        "<b>Autenticacion real:</b> Sistema de registro con verificacion de email/telefono",
        "<b>Integracion de pagos:</b> Mercado Pago es la opcion mas comun en Argentina para procesar pagos",
        "<b>Chat en tiempo real:</b> Usar WebSockets o servicios como Firebase Realtime Database",
        "<b>Notificaciones push reales:</b> Con Firebase Cloud Messaging (FCM)",
    ]))

    story.append(subsection("Etapa 3: Integraciones institucionales"))
    story.extend(bullet_list([
        "API del DNRPA para validar patentes",
        "APIs municipales para estacionamiento medido y multas",
        "API de Mercado Pago para pagos",
        "Futura integracion con YPF para canje de puntos",
        "Futura integracion con aseguradoras (SSN)",
    ]))

    story.append(subsection("Etapa 4: Publicacion"))
    story.extend(bullet_list([
        "Cuenta de desarrollador en Google Play ($25 USD, pago unico)",
        "Cuenta de desarrollador en Apple Developer ($99 USD/ano)",
        "Testing con usuarios beta (grupo reducido de prueba)",
        "Publicacion en las tiendas",
    ]))

    story.append(callout(
        "<b>Nota sobre costos:</b> El prototipo actual costo $0 en tecnologia (todo es gratis y open source). "
        "El desarrollo de la app real requiere inversion en: equipo de desarrollo, servidores en la nube, "
        "cuentas de tiendas, y potencialmente asesoria legal para las integraciones institucionales."
    ))
    story.append(PageBreak())

    # =====================================================
    # CAPITULO 13: GLOSARIO
    # =====================================================
    story.append(chapter("13. Glosario de terminos tecnicos"))
    story.append(hr())

    glosario = [
        ("API", "Application Programming Interface. Es una forma estandarizada en que dos programas se comunican entre si. Como un menu de restaurante: vos pedis algo, y la cocina (servidor) te lo trae."),
        ("Array", "Lista ordenada de elementos. Como una lista de compras, pero en codigo. Se escribe con corchetes: [elemento1, elemento2, elemento3]."),
        ("Backend", "La parte del sistema que corre en un servidor y que el usuario no ve: base de datos, logica de negocio, autenticacion."),
        ("CDN", "Content Delivery Network. Servidores distribuidos por el mundo que almacenan archivos publicos para acceso rapido."),
        ("CSS", "Cascading Style Sheets. Lenguaje para definir la apariencia visual de una pagina web."),
        ("DOM", "Document Object Model. Es la representacion en memoria de la pagina web. JavaScript modifica el DOM para cambiar lo que se ve en pantalla."),
        ("Framework", "Conjunto de herramientas y estructuras pre-hechas que facilitan el desarrollo. Ejemplo: React Native para apps moviles."),
        ("Frontend", "La parte visual de una app que el usuario ve y toca. En nuestro caso, es todo el index.html."),
        ("Funcion", "Bloque de codigo con nombre que realiza una tarea especifica. Se puede llamar/ejecutar cuando se necesite."),
        ("Geocodificacion", "Proceso de convertir una direccion en coordenadas (lat/lng) o viceversa (inversa)."),
        ("HTML", "HyperText Markup Language. Lenguaje para definir la estructura de una pagina web."),
        ("HTTP", "HyperText Transfer Protocol. El lenguaje que usan los navegadores y servidores para comunicarse."),
        ("JavaScript", "Lenguaje de programacion que agrega interactividad a las paginas web."),
        ("JSON", "JavaScript Object Notation. Formato para almacenar e intercambiar datos. Ejemplo: {\"nombre\": \"Lisandro\", \"edad\": 25}."),
        ("Localhost", "Tu propia computadora actuando como servidor. Se accede con http://localhost."),
        ("Node.js", "Programa que permite ejecutar JavaScript fuera del navegador (en servidores o tu computadora)."),
        ("Objeto", "Estructura de datos con propiedades (como una ficha con campos). Ejemplo: {name: 'Juan', age: 30}."),
        ("Open Source", "Software cuyo codigo fuente es publico y gratuito. Cualquiera puede usarlo, modificarlo y distribuirlo."),
        ("Puerto", "Numero que identifica un servicio en una computadora. Nuestro servidor usa el puerto 3000."),
        ("Responsive", "Diseno que se adapta a distintos tamanos de pantalla (celular, tablet, computadora)."),
        ("Servidor", "Computadora o programa que recibe pedidos y devuelve respuestas (como un mozo en un restaurante)."),
        ("Variable", "Espacio en memoria con nombre donde se guarda un dato. Como una caja etiquetada."),
    ]

    for term, definition in glosario:
        story.append(Paragraph(f"<b><font color='#667eea'>{term}</font></b>", styles['BodyText2']))
        story.append(Paragraph(definition, styles['BulletItem']))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # =====================================================
    # FINAL
    # =====================================================
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("Fin del documento", styles['CoverTitle']))
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="50%", thickness=2, color=PRIMARY, spaceAfter=12, spaceBefore=12))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Documento generado automaticamente el 31 de marzo de 2026", styles['CoverSubtitle']))
    story.append(Paragraph("Desarrollo: Lisandro + Claude Code (Anthropic)", styles['CoverSubtitle']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "Este documento y el prototipo asociado son propiedad del propietario de la idea. "
        "Su distribucion requiere autorizacion previa.", styles['CoverSubtitle']
    ))

    # BUILD
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generado exitosamente: {OUTPUT_PATH}")
    print(f"Tamano: {os.path.getsize(OUTPUT_PATH) / 1024:.1f} KB")


if __name__ == "__main__":
    build_pdf()
