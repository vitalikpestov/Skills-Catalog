/**
 * DOCX Generation Helpers
 *
 * Reusable building blocks for generating design spec documents.
 * Battle-tested with Cyrillic text.
 *
 * Usage:
 *   const h = require('./docx-helpers');
 *   const doc = new Document({
 *     styles: h.defaultStyles,
 *     numbering: h.defaultNumbering,
 *     sections: [{ children: [
 *       h.heading("Section Title"),
 *       h.para("Body text"),
 *       h.bullet("List item"),
 *       h.makeTable(["Col1", "Col2"], [["a", "b"]], [4680, 4680]),
 *     ]}]
 *   });
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, ExternalHyperlink,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak
} = require("docx");

// ─── Color Constants ───
const TEAL = "0D9488";
const DARK = "111827";
const GRAY = "6B7280";
const LIGHT_TEAL = "F0FDFA";

// ─── Table Helpers ───
const BORDER = { style: BorderStyle.SINGLE, size: 1, color: "D1D5DB" };
const BORDERS = { top: BORDER, bottom: BORDER, left: BORDER, right: BORDER };
const CELL_MARGINS = { top: 60, bottom: 60, left: 100, right: 100 };
const TABLE_WIDTH = 9360; // US Letter, 1" margins

function headerCell(text, width) {
  return new TableCell({
    borders: BORDERS,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: "E5E7EB", type: ShadingType.CLEAR },
    margins: CELL_MARGINS,
    children: [new Paragraph({
      children: [new TextRun({ text, bold: true, font: "Arial", size: 20 })],
    })],
  });
}

function cell(text, width, opts = {}) {
  return new TableCell({
    borders: BORDERS,
    width: { size: width, type: WidthType.DXA },
    shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined,
    margins: CELL_MARGINS,
    children: [new Paragraph({
      children: [new TextRun({
        text, font: "Arial", size: 20,
        bold: opts.bold, color: opts.color,
      })],
    })],
  });
}

function makeTable(headers, rows, colWidths) {
  return new Table({
    width: { size: TABLE_WIDTH, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({ children: headers.map((h, i) => headerCell(h, colWidths[i])) }),
      ...rows.map(r => new TableRow({
        children: r.map((c, i) => {
          if (typeof c === "object" && c._cell) return c._cell;
          return cell(String(c), colWidths[i]);
        }),
      })),
    ],
  });
}

// ─── Text Helpers ───
function heading(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({
    heading: level,
    children: [new TextRun({
      text, font: "Arial", bold: true,
      color: level === HeadingLevel.HEADING_1 ? TEAL : DARK,
    })],
  });
}

function h2(text) { return heading(text, HeadingLevel.HEADING_2); }
function h3(text) { return heading(text, HeadingLevel.HEADING_3); }

function para(text, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after || 120 },
    children: [new TextRun({
      text, font: "Arial", size: opts.size || 22,
      bold: opts.bold, italic: opts.italic,
      color: opts.color || DARK,
    })],
  });
}

function bullet(text, ref = "bullets") {
  return new Paragraph({
    numbering: { reference: ref, level: 0 },
    children: [new TextRun({ text, font: "Arial", size: 22 })],
  });
}

function numberedItem(text, ref = "numbers") {
  return new Paragraph({
    numbering: { reference: ref, level: 0 },
    children: [new TextRun({ text, font: "Arial", size: 22 })],
  });
}

function spacer() {
  return new Paragraph({ spacing: { after: 80 }, children: [] });
}

function link(text, url) {
  return new Paragraph({
    spacing: { after: 100 },
    children: [new ExternalHyperlink({
      children: [new TextRun({
        text, font: "Arial", size: 22,
        color: "2563EB", underline: { type: "single" },
      })],
      link: url,
    })],
  });
}

function pageBreak() { return new PageBreak(); }

// ─── Default Styles ───
const defaultStyles = {
  default: { document: { run: { font: "Arial", size: 22 } } },
  paragraphStyles: [
    {
      id: "Heading1", name: "Heading 1",
      basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 36, bold: true, font: "Arial", color: TEAL },
      paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 },
    },
    {
      id: "Heading2", name: "Heading 2",
      basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 28, bold: true, font: "Arial", color: DARK },
      paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 },
    },
    {
      id: "Heading3", name: "Heading 3",
      basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 24, bold: true, font: "Arial", color: DARK },
      paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 },
    },
  ],
};

// ─── Default Numbering ───
const defaultNumbering = {
  config: [
    {
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "\u2022",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } },
      }],
    },
    {
      reference: "numbers",
      levels: [{
        level: 0, format: LevelFormat.DECIMAL, text: "%1.",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } },
      }],
    },
  ],
};

// ─── Standard Header/Footer ───
function makeHeader(projectName, version) {
  return new Header({
    children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({
        text: `${projectName} — ТЗ ${version}`,
        font: "Arial", size: 18, color: GRAY,
      })],
    })],
  });
}

function makeFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ text: "Стр. ", font: "Arial", size: 18, color: GRAY }),
        new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: GRAY }),
      ],
    })],
  });
}

// ─── Exports ───
module.exports = {
  // Colors
  TEAL, DARK, GRAY, LIGHT_TEAL,
  // Table
  headerCell, cell, makeTable, TABLE_WIDTH,
  // Text
  heading, h2, h3, para, bullet, numberedItem, spacer, link, pageBreak,
  // Document setup
  defaultStyles, defaultNumbering, makeHeader, makeFooter,
  // Re-exports for convenience
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, ExternalHyperlink,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak,
};
