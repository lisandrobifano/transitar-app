const fs = require("fs");
const path = require("path");
const globalModules = require("child_process").execSync("npm root -g").toString().trim();
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, LevelFormat, PageNumber, PageBreak
} = require(path.join(globalModules, "docx"));

const PRIMARY = "667EEA";
const DARK = "2D3748";
const GRAY = "718096";
const LIGHT_BG = "F0F4FF";
const WHITE = "FFFFFF";

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Arial", size: 22, color: DARK } }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: PRIMARY },
        paragraph: { spacing: { before: 120, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: DARK },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 1 }
      },
    ]
  },
  numbering: {
    config: [
      {
        reference: "steps",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "Paso %1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 500 } }, run: { bold: true, color: PRIMARY } }
        }]
      },
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 360 } } }
        }]
      },
      {
        reference: "bullets2",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 360 } } }
        }]
      },
      {
        reference: "bullets3",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 360 } } }
        }]
      },
      {
        reference: "bullets4",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 360 } } }
        }]
      },
      {
        reference: "bullets5",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 360 } } }
        }]
      },
      {
        reference: "bullets6",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 360 } } }
        }]
      },
      {
        reference: "bullets7",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 360 } } }
        }]
      },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1200, right: 1200, bottom: 1200, left: 1200 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: PRIMARY, space: 4 } },
          children: [
            new TextRun({ text: "Transitar", font: "Arial", bold: true, size: 18, color: PRIMARY }),
            new TextRun({ text: "  |  Hoja de Ruta del Proyecto", font: "Arial", size: 18, color: GRAY }),
          ]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0", space: 4 } },
          children: [
            new TextRun({ text: "Documento confidencial | Marzo 2026 | ", size: 16, color: GRAY }),
            new TextRun({ text: "Pagina ", size: 16, color: GRAY }),
            new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GRAY }),
          ]
        })]
      })
    },
    children: [
      // TITULO
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
        children: [new TextRun({ text: "TRANSITAR", size: 48, bold: true, color: PRIMARY, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 40 },
        children: [new TextRun({ text: "Plataforma de Seguridad Vial para Ciudades Argentinas", size: 24, color: GRAY })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 300 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: PRIMARY, space: 8 } },
        children: [new TextRun({ text: "Hoja de Ruta - Pasos a seguir desde abril 2026", size: 22, bold: true, color: DARK })]
      }),

      // ESTADO ACTUAL
      new Paragraph({
        shading: { fill: LIGHT_BG, type: ShadingType.CLEAR },
        spacing: { after: 200 },
        indent: { left: 200, right: 200 },
        children: [
          new TextRun({ text: "Estado actual: ", bold: true, size: 22 }),
          new TextRun({ text: "Prototipo funcional terminado (boceto interactivo en HTML/CSS/JS). ", size: 22 }),
          new TextRun({ text: "Idea en tramite de patentamiento. ", bold: true, size: 22, color: "48BB78" }),
          new TextRun({ text: "Proximo objetivo: validar la idea con actores institucionales clave y definir el plan de negocio.", size: 22 }),
        ]
      }),

      // PASO 1
      new Paragraph({ numbering: { reference: "steps", level: 0 }, spacing: { before: 200, after: 80 },
        children: [new TextRun({ text: "Reunirse con la Municipalidad de La Plata", size: 24, bold: true })]
      }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Contactar:", bold: true }), new TextRun(" Secretaria de Movilidad Urbana y Espacio Publico."),
        ]
      }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Objetivo:", bold: true }), new TextRun(" Presentar el prototipo, explorar interes en integrar el sistema de estacionamiento medido municipal y el registro de infracciones de transito. Consultar sobre APIs o sistemas digitales que ya tengan en uso."),
        ]
      }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Tambien consultar:", bold: true }), new TextRun(" Direccion de Transito y Transporte (calle 7 entre 56 y 57) para validacion de multas y patentes a nivel local. Preguntar si tienen convenios con DNRPA."),
        ]
      }),

      // PASO 2
      new Paragraph({ numbering: { reference: "steps", level: 0 }, spacing: { before: 200, after: 80 },
        children: [new TextRun({ text: "Reunirse con el DNRPA (Registro Automotor)", size: 24, bold: true })]
      }),
      new Paragraph({ numbering: { reference: "bullets2", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Contactar:", bold: true }), new TextRun(" Direccion Nacional de los Registros Nacionales de la Propiedad del Automotor y de Creditos Prendarios (Ministerio de Justicia)."),
        ]
      }),
      new Paragraph({ numbering: { reference: "bullets2", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Objetivo:", bold: true }), new TextRun(" Consultar el proceso para acceder a la base de datos de titulares de vehiculos. Necesitamos validar que el conductor que se registra sea el titular de la patente declarada. Preguntar por APIs de consulta o convenios para apps de transito."),
        ]
      }),

      // PASO 3
      new Paragraph({ numbering: { reference: "steps", level: 0 }, spacing: { before: 200, after: 80 },
        children: [new TextRun({ text: "Reunirse con el Registro de la Propiedad Inmueble (Prov. de Buenos Aires)", size: 24, bold: true })]
      }),
      new Paragraph({ numbering: { reference: "bullets3", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Contactar:", bold: true }), new TextRun(" Direccion Provincial del Registro de la Propiedad, sede La Plata (calle 46 entre 7 y 8)."),
        ]
      }),
      new Paragraph({ numbering: { reference: "bullets3", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Objetivo:", bold: true }), new TextRun(" Consultar como validar que quien ofrece una cochera es propietario o tiene derecho legal sobre el inmueble (propietario o inquilino con autorizacion). Explorar certificados digitales de dominio."),
        ]
      }),

      // PASO 4
      new Paragraph({ numbering: { reference: "steps", level: 0 }, spacing: { before: 200, after: 80 },
        children: [new TextRun({ text: "Consultar con abogado especialista en derecho digital y transito", size: 24, bold: true })]
      }),
      new Paragraph({ numbering: { reference: "bullets4", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Objetivo:", bold: true }), new TextRun(" Definir la estructura legal de la empresa (SAS es la opcion mas agil para startups en Argentina). Revisar cumplimiento de Ley de Proteccion de Datos Personales (25.326) y regulaciones de la AAIP. Evaluar responsabilidades legales por las funcionalidades de denuncia y cobro."),
        ]
      }),
      new Paragraph({ numbering: { reference: "bullets4", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Tambien:", bold: true }), new TextRun(" Redactar Terminos y Condiciones de uso de la app y Politica de Privacidad (obligatorio antes de publicar)."),
        ]
      }),

      // PASO 5
      new Paragraph({ numbering: { reference: "steps", level: 0 }, spacing: { before: 200, after: 80 },
        children: [new TextRun({ text: "Contactar un Proveedor de Servicios de Pago (Mercado Pago)", size: 24, bold: true })]
      }),
      new Paragraph({ numbering: { reference: "bullets5", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Contactar:", bold: true }), new TextRun(" Equipo de desarrolladores de Mercado Pago (developers.mercadopago.com.ar) para solicitar acceso al entorno de pruebas (sandbox)."),
        ]
      }),
      new Paragraph({ numbering: { reference: "bullets5", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Objetivo:", bold: true }), new TextRun(" Integrar pagos reales: reserva de cocheras, pago de estacionamiento medido, y cobro de multas. Mercado Pago maneja la regulacion financiera (PSP autorizado por BCRA). Definir comisiones y modelo de revenue."),
        ]
      }),

      // PASO 6
      new Paragraph({ numbering: { reference: "steps", level: 0 }, spacing: { before: 200, after: 80 },
        children: [new TextRun({ text: "Contactar AFIP / Monotributo para la actividad economica", size: 24, bold: true })]
      }),
      new Paragraph({ numbering: { reference: "bullets6", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Objetivo:", bold: true }), new TextRun(" Dar de alta la actividad de intermediacion digital para los propietarios que alquilan cocheras. Definir si los propietarios necesitan estar inscriptos para facturar, o si la app actua como intermediario con facturacion propia."),
        ]
      }),

      // PASO 7
      new Paragraph({ numbering: { reference: "steps", level: 0 }, spacing: { before: 200, after: 80 },
        children: [new TextRun({ text: "Armar equipo de desarrollo para la app real", size: 24, bold: true })]
      }),
      new Paragraph({ numbering: { reference: "bullets7", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Perfiles necesarios:", bold: true }), new TextRun(" 1 desarrollador mobile (React Native o Flutter), 1 desarrollador backend (Node.js o Python), 1 disenador UX/UI. Opcionalmente: un project manager."),
        ]
      }),
      new Paragraph({ numbering: { reference: "bullets7", level: 0 }, spacing: { after: 40 },
        children: [
          new TextRun({ text: "Con el prototipo actual:", bold: true }), new TextRun(" el equipo ya tiene un plano detallado de que construir (todas las pantallas, flujos y funcionalidades estan definidas en el boceto). Esto ahorra semanas de diseno inicial."),
        ]
      }),

      // RESUMEN VISUAL
      new Paragraph({ spacing: { before: 300, after: 120 },
        children: [new TextRun({ text: "Resumen de actores clave", size: 28, bold: true, color: PRIMARY })]
      }),

      // Table
      new Table({
        width: { size: 9840, type: WidthType.DXA },
        columnWidths: [3200, 3200, 3440],
        rows: [
          new TableRow({
            children: ["Actor / Entidad", "Para que", "Prioridad"].map(h =>
              new TableCell({
                width: { size: 3200, type: WidthType.DXA },
                shading: { fill: PRIMARY, type: ShadingType.CLEAR },
                margins: { top: 60, bottom: 60, left: 100, right: 100 },
                borders: { top: { style: BorderStyle.SINGLE, size: 1, color: PRIMARY }, bottom: { style: BorderStyle.SINGLE, size: 1, color: PRIMARY }, left: { style: BorderStyle.SINGLE, size: 1, color: PRIMARY }, right: { style: BorderStyle.SINGLE, size: 1, color: PRIMARY } },
                children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, color: WHITE, size: 20 })] })]
              })
            )
          }),
          ...([
            ["Municipalidad de La Plata", "Estacionamiento medido, infracciones, convenio local", "ALTA"],
            ["DNRPA", "Validar titularidad de vehiculos por patente", "ALTA"],
            ["Registro Propiedad Inmueble PBA", "Validar titularidad/derecho sobre inmuebles", "ALTA"],
            ["Abogado (derecho digital)", "Estructura legal, datos personales, T&C", "ALTA"],
            ["Mercado Pago", "Procesar pagos digitales (cocheras, multas)", "MEDIA"],
            ["AFIP", "Encuadre fiscal de la actividad", "MEDIA"],
            ["Equipo de desarrollo", "Construir la app real a partir del prototipo", "MEDIA"],
            ["YPF (futuro)", "Integracion de canje de puntos por combustible", "BAJA"],
            ["SSN / Aseguradoras (futuro)", "Notificacion de infracciones a seguros", "BAJA"],
          ]).map(([actor, para, prio]) =>
            new TableRow({
              children: [
                new TableCell({
                  width: { size: 3200, type: WidthType.DXA },
                  margins: { top: 50, bottom: 50, left: 100, right: 100 },
                  borders: { top: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" }, bottom: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" }, left: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" }, right: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" } },
                  children: [new Paragraph({ children: [new TextRun({ text: actor, bold: true, size: 20 })] })]
                }),
                new TableCell({
                  width: { size: 3200, type: WidthType.DXA },
                  margins: { top: 50, bottom: 50, left: 100, right: 100 },
                  borders: { top: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" }, bottom: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" }, left: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" }, right: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" } },
                  children: [new Paragraph({ children: [new TextRun({ text: para, size: 20 })] })]
                }),
                new TableCell({
                  width: { size: 3440, type: WidthType.DXA },
                  margins: { top: 50, bottom: 50, left: 100, right: 100 },
                  shading: { fill: prio === "ALTA" ? "FED7D7" : prio === "MEDIA" ? "FEFCBF" : "F0FFF4", type: ShadingType.CLEAR },
                  borders: { top: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" }, bottom: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" }, left: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" }, right: { style: BorderStyle.SINGLE, size: 1, color: "E2E8F0" } },
                  children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: prio, bold: true, size: 20, color: prio === "ALTA" ? "E53E3E" : prio === "MEDIA" ? "D69E2E" : "48BB78" })] })]
                }),
              ]
            })
          )
        ]
      }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  const out = path.join(__dirname, "Transitar_Hoja_de_Ruta.docx");
  fs.writeFileSync(out, buffer);
  console.log("Word generado:", out);
  console.log("Tamano:", (buffer.length / 1024).toFixed(1), "KB");
});
