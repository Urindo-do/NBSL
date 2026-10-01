const fs = require('fs');
const path = require('path');
const d = require('docx');
const {Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, HeadingLevel, BorderStyle, ShadingType, PageBreak, Footer, PageNumber,
  LevelFormat, VerticalAlign, TableLayoutType} = d;
// 사용법: node build.js <content.js 경로> <출력 docx 경로>
// content.js의 이미지 경로는 content.js가 있는 폴더 기준 상대경로로 쓴다.
const contentPath = path.resolve(process.argv[2] || 'content.js');
const outPath = path.resolve(process.argv[3] || 'report.docx');
const BASE = path.dirname(contentPath);
const C = require(contentPath);
const P = f => path.resolve(BASE, f);
const dims = {};

const BODY = '함초롬바탕', HEAD = '함초롬돋움';
const font = f => ({ascii: f, eastAsia: f, hAnsi: f, cs: f});
const CONTENT_W = 9638; // DXA (A4 - 좌우 20 mm)


(async () => {
// 이미지 크기 미리 읽기
const sharp = require('sharp');
const files = [];
for (const b of C.body) { if (b.t === 'fig') files.push(b.img); if (b.t === 'photos') b.items.forEach(it => files.push(it.img)); }
for (const f of files) { const m = await sharp(P(f)).metadata(); dims[P(f)] = [m.width, m.height]; }

// ---------- 1st pass: numbering ----------
let ch = 0, h2 = 0, h3 = 0; const num = {}; const figCount = {}, tabCount = {};
for (const b of C.body) {
  if (b.t === 'h1') { ch++; h2 = 0; b.n = `${ch}.`; }
  else if (b.t === 'h2') { h2++; h3 = 0; b.n = `${ch}.${h2}`; }
  else if (b.t === 'h3') { h3++; b.n = `${ch}.${h2}.${h3}`; }
  else if (b.t === 'fig') { figCount[ch] = (figCount[ch] || 0) + 1; num['f:' + b.key] = `그림 ${ch}-${figCount[ch]}`; b.label = num['f:' + b.key]; }
  else if (b.t === 'photos') { for (const it of b.items) { figCount[ch] = (figCount[ch] || 0) + 1; num['f:' + it.key] = `그림 ${ch}-${figCount[ch]}`; it.label = num['f:' + it.key]; } }
  else if (b.t === 'table') { tabCount[ch] = (tabCount[ch] || 0) + 1; num['t:' + b.key] = `표 ${ch}-${tabCount[ch]}`; b.label = num['t:' + b.key]; }
}
const sub = s => s.replace(/\{([ft]):(\w+)\}/g, (m, k, key) => {
  const v = num[k + ':' + key]; if (!v) throw new Error('unknown ref ' + m); return v; });

// ---------- helpers ----------
const run = (text, o = {}) => new TextRun({text, font: font(o.f || BODY), size: o.size || 22, bold: o.bold, color: o.color});
const para = (text, o = {}) => new Paragraph({
  children: [run(sub(text), o)], alignment: o.align || AlignmentType.JUSTIFIED,
  spacing: {line: o.line || 384, after: o.after ?? 120, before: o.before || 0},
  indent: o.indent, keepNext: o.keepNext});
function imgSize(file, maxW, maxH) {
  const [w, h] = dims[P(file)]; let W = maxW, H = Math.round(maxW * h / w);
  if (H > maxH) { H = maxH; W = Math.round(maxH * w / h); }
  return {width: W, height: H};
}
const image = (file, maxW, maxH) => new ImageRun({type: file.endsWith('.png') ? 'png' : 'jpg',
  data: fs.readFileSync(P(file)), transformation: imgSize(file, maxW, maxH)});
const caption = (text) => new Paragraph({alignment: AlignmentType.CENTER, spacing: {before: 60, after: 200, line: 276},
  children: [run(sub(text), {size: 19})]});
const NB = {style: BorderStyle.NONE, size: 0, color: 'FFFFFF'};
const noBorders = {top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB};
const LINE = {style: BorderStyle.SINGLE, size: 4, color: '808080'};

let olId = 0; const numberingConfigs = [];
const out = [];

function heading(b) {
  const lv = {h1: HeadingLevel.HEADING_1, h2: HeadingLevel.HEADING_2, h3: HeadingLevel.HEADING_3}[b.t];
  const size = {h1: 28, h2: 24, h3: 22}[b.t];
  const title = b.t === 'h1' ? `${b.n} ${b.x}` : `${b.n} ${b.x}`;
  return new Paragraph({heading: lv, keepNext: true,
    spacing: {before: b.t === 'h1' ? 360 : 220, after: 120, line: 300},
    children: [new TextRun({text: title, font: font(HEAD), size, bold: true})]});
}

let firstH1 = true;
C.body.forEach((b, i) => { if (b.t === 'p' && C.body[i + 1] && C.body[i + 1].t === 'table') b.keepNext = true; });
for (const b of C.body) {
  if (b.t === 'h1') {
    firstH1 = false; out.push(heading(b));
  }
  else if (b.t === 'h2' || b.t === 'h3') out.push(heading(b));
  else if (b.t === 'p') out.push(para(b.x, {keepNext: b.keepNext}));
  else if (b.t === 'ol') {
    const ref = 'ol' + (++olId);
    numberingConfigs.push({reference: ref, levels: [{level: 0, format: LevelFormat.DECIMAL, text: '%1)',
      alignment: AlignmentType.LEFT, style: {paragraph: {indent: {left: 500, hanging: 340}}}}]});
    for (const it of b.items) out.push(new Paragraph({numbering: {reference: ref, level: 0},
      spacing: {line: 360, after: 60}, children: [run(sub(it))]}));
    out.push(new Paragraph({spacing: {after: 60}, children: []}));
  }
  else if (b.t === 'fig') {
    out.push(new Paragraph({alignment: AlignmentType.CENTER, keepNext: true, spacing: {before: 120},
      children: [image(b.img, b.w, 330)]}));
    out.push(caption(`${b.label}. ${b.cap}`));
  }
  else if (b.t === 'photos') {
    if (b.items.length === 1) {
      const it = b.items[0];
      out.push(new Paragraph({alignment: AlignmentType.CENTER, keepNext: true, spacing: {before: 120},
        children: [image(it.img, 340, 250)]}));
      out.push(caption(`${it.label}. ${it.cap}`));
    } else {
      const cw = Math.floor(CONTENT_W / 2);
      const cells = b.items.map(it => new TableCell({width: {size: cw, type: WidthType.DXA}, borders: noBorders,
        verticalAlign: VerticalAlign.BOTTOM, children: [
          new Paragraph({alignment: AlignmentType.CENTER, keepNext: true, children: [image(it.img, 300, 225)]}),
          new Paragraph({alignment: AlignmentType.CENTER, spacing: {before: 60, after: 60, line: 276},
            children: [run(`${it.label}. ${it.cap}`, {size: 19})]})]}));
      out.push(new Table({width: {size: cw * 2, type: WidthType.DXA}, columnWidths: [cw, cw], borders: noBorders,
        layout: TableLayoutType.FIXED, alignment: AlignmentType.CENTER, rows: [new TableRow({cantSplit: true, children: cells})]}));
      out.push(new Paragraph({spacing: {after: 120}, children: []}));
    }
  }
  else if (b.t === 'table') {
    out.push(new Paragraph({alignment: AlignmentType.CENTER, keepNext: true, spacing: {before: 160, after: 80},
      children: [run(`${b.label}. ${sub(b.cap)}`, {size: 19})]}));
    const tw = b.cols.reduce((a, c) => a + c, 0);
    const mk = (texts, head) => new TableRow({cantSplit: true, tableHeader: head, children: texts.map((t, i) => new TableCell({
      width: {size: b.cols[i], type: WidthType.DXA},
      borders: {top: LINE, bottom: LINE, left: LINE, right: LINE},
      shading: head ? {type: ShadingType.CLEAR, color: 'auto', fill: 'E8EDF3'} : undefined,
      margins: {top: 60, bottom: 60, left: 100, right: 100}, verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({alignment: head ? AlignmentType.CENTER : AlignmentType.LEFT, spacing: {line: 300},
        children: [run(t, {size: 19, bold: head, f: head ? HEAD : BODY})]})]}))});
    out.push(new Table({width: {size: tw, type: WidthType.DXA}, columnWidths: b.cols, alignment: AlignmentType.CENTER,
      layout: TableLayoutType.FIXED, rows: [mk(b.head, true), ...b.rows.map(r => mk(r, false))]}));
    out.push(new Paragraph({spacing: {after: 160}, children: []}));
  }
}
// references
out.push(new Paragraph({children: [new PageBreak()]}));
out.push(new Paragraph({heading: HeadingLevel.HEADING_1, spacing: {after: 160},
  children: [new TextRun({text: '참고문헌', font: font(HEAD), size: 28, bold: true})]}));
C.refs.forEach((r, i) => out.push(new Paragraph({spacing: {after: 100, line: 300}, indent: {left: 520, hanging: 520},
  children: [run(`[${i + 1}]\t${r}`, {size: 19})], tabStops: [{type: 'left', position: 520}]})));

// ---------- cover ----------
const cover = [];
cover.push(new Paragraph({spacing: {before: 2600, after: 200}, alignment: AlignmentType.CENTER,
  children: [run('실습 보고서', {f: HEAD, size: 26, color: '555555'})]}));
cover.push(new Paragraph({spacing: {after: 240}, alignment: AlignmentType.CENTER,
  children: [run(C.cover.title, {f: HEAD, size: 40, bold: true})]}));
cover.push(new Paragraph({spacing: {after: 1800}, alignment: AlignmentType.CENTER,
  children: [run(C.cover.subtitle, {f: HEAD, size: 22, color: '444444'})]}));
const iw = [2200, 4200];
const infoRow = (a, b2) => new TableRow({children: [a, b2].map((t, i) => new TableCell({width: {size: iw[i], type: WidthType.DXA},
  borders: {top: LINE, bottom: LINE, left: LINE, right: LINE}, margins: {top: 80, bottom: 80, left: 120, right: 120},
  shading: i === 0 ? {type: ShadingType.CLEAR, color: 'auto', fill: 'F0F0F0'} : undefined,
  children: [new Paragraph({alignment: i === 0 ? AlignmentType.CENTER : AlignmentType.LEFT, children: [run(t, {size: 21, f: i === 0 ? HEAD : BODY})]})]}))});
const members = [];
for (let i = 0; i < C.cover.members; i++) members.push(['조원' + (i + 1), '이름 [        ]   학번 [            ]']);
cover.push(new Table({width: {size: 6400, type: WidthType.DXA}, columnWidths: iw, alignment: AlignmentType.CENTER,
  layout: TableLayoutType.FIXED, rows: [...C.cover.info, ...members].map(([a, b2]) => infoRow(a, b2))}));

// ---------- TOC (static) ----------
const toc = [new Paragraph({spacing: {after: 240}, children: [new TextRun({text: '목차', font: font(HEAD), size: 28, bold: true})]})];
for (const b of C.body) {
  if (b.t === 'h1') toc.push(new Paragraph({spacing: {before: 140, after: 40}, children: [run(`${b.n} ${b.x}`, {f: HEAD, size: 22, bold: true})]}));
  if (b.t === 'h2') toc.push(new Paragraph({indent: {left: 440}, spacing: {after: 30}, children: [run(`${b.n} ${b.x}`, {size: 21})]}));
}
toc.push(new Paragraph({spacing: {before: 140}, children: [run('참고문헌', {f: HEAD, size: 22, bold: true})]}));
toc.push(new Paragraph({children: [new PageBreak()]}));

const page = {size: {width: 11906, height: 16838}, margin: {top: 1134, bottom: 850, left: 1134, right: 1134, footer: 425}};
const footer = new Footer({children: [new Paragraph({alignment: AlignmentType.CENTER,
  children: [new TextRun({children: [PageNumber.CURRENT], font: font(BODY), size: 18})]})]});

const doc = new Document({
  creator: 'NBSL', title: C.cover.title,
  styles: {default: {document: {run: {font: font(BODY), size: 22}}},
    paragraphStyles: [
      {id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: {font: font(HEAD), size: 28, bold: true}, paragraph: {outlineLevel: 0}},
      {id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: {font: font(HEAD), size: 24, bold: true}, paragraph: {outlineLevel: 1}},
      {id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: {font: font(HEAD), size: 22, bold: true}, paragraph: {outlineLevel: 2}},
    ]},
  numbering: {config: numberingConfigs},
  sections: [
    {properties: {page}, children: cover},
    {properties: {page: {...page, pageNumbers: {start: 1}}}, footers: {default: footer}, children: [...toc, ...out]},
  ]});
const buf = await Packer.toBuffer(doc);
fs.writeFileSync(outPath, buf); console.log('wrote', outPath, buf.length);
fs.writeFileSync(outPath.replace(/\.docx$/, '.labels.json'), JSON.stringify(num, null, 1));

})().catch(e => { console.error(e); process.exit(1); });
