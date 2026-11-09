"""Сбор тестов из файлов проекта и запись их в Word-документ (.docx).

Модуль не зависит от Django: ему достаточно путей к приложениям.
Пути приложений ему передаёт management-команда export_tests.
"""
import ast
import textwrap
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

SETUP_NAMES = ("setUp", "setUpTestData", "setUpClass")
CODE_FONT = "Consolas"


@dataclass
class MethodInfo:
    name: str
    doc: str
    source: str


@dataclass
class ClassInfo:
    name: str
    doc: str
    setup_source: str = ""
    methods: list = field(default_factory=list)


@dataclass
class ModuleInfo:
    app: str
    path: str
    classes: list = field(default_factory=list)

    @property
    def tests_count(self):
        return sum(len(c.methods) for c in self.classes)


def _function_source(lines, node):
    """Текст функции вместе с декораторами, без общего отступа."""
    first = min([node.lineno] + [d.lineno for d in node.decorator_list])
    return textwrap.dedent("\n".join(lines[first - 1:node.end_lineno]))


def parse_test_file(path):
    """Возвращает классы с методами test*, найденные в файле."""
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    classes = []
    for node in ast.parse(text).body:
        if not isinstance(node, ast.ClassDef):
            continue
        info = ClassInfo(name=node.name, doc=ast.get_docstring(node) or "")
        setup_parts = []
        for item in node.body:
            if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if item.name.startswith("test"):
                info.methods.append(
                    MethodInfo(
                        name=item.name,
                        doc=ast.get_docstring(item) or "",
                        source=_function_source(lines, item),
                    )
                )
            elif item.name in SETUP_NAMES:
                setup_parts.append(_function_source(lines, item))
        if info.methods:
            info.setup_source = "\n\n".join(setup_parts)
            classes.append(info)
    return classes


def find_test_files(app_dir):
    """tests.py и все test*.py внутри пакета tests/ приложения."""
    app_dir = Path(app_dir)
    files = []
    single = app_dir / "tests.py"
    if single.is_file():
        files.append(single)
    package = app_dir / "tests"
    if package.is_dir():
        files.extend(sorted(package.rglob("test*.py")))
    return files


def collect_modules(targets, base_dir):
    """targets: пары (название приложения, путь к его папке)."""
    base_dir = Path(base_dir).resolve()
    modules = []
    for label, app_dir in targets:
        for test_file in find_test_files(app_dir):
            classes = parse_test_file(test_file)
            if classes:
                relative = Path(test_file).resolve().relative_to(base_dir)
                modules.append(
                    ModuleInfo(app=label, path=relative.as_posix(), classes=classes)
                )
    return modules


def _set_font(run, name, size=None, color=None, bold=None):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    if size:
        run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    if bold is not None:
        run.font.bold = bold


def _shade(paragraph, fill="F2F2F2"):
    properties = paragraph._p.get_or_add_pPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:color"), "auto")
    shading.set(qn("w:fill"), fill)
    properties.append(shading)


def _add_code(document, source):
    """Код: моноширинный шрифт, серый фон, по абзацу на строку."""
    for line in source.splitlines() or [""]:
        paragraph = document.add_paragraph()
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.line_spacing = 1.0
        _shade(paragraph)
        _set_font(paragraph.add_run(line), CODE_FONT, size=9)
    document.add_paragraph().paragraph_format.space_after = Pt(2)


def _add_caption(document, text):
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(2)
    paragraph.paragraph_format.keep_with_next = True
    _set_font(paragraph.add_run(text), "Calibri", size=10, color=(0x59, 0x59, 0x59), bold=True)


def _add_summary_table(document, modules):
    table = document.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    for cell, text in zip(table.rows[0].cells, ("Приложение", "Класс тестов", "Тестов")):
        cell.text = ""
        _set_font(cell.paragraphs[0].add_run(text), "Calibri", bold=True)
    for module in modules:
        for cls in module.classes:
            row = table.add_row().cells
            row[0].text = module.app
            row[1].text = cls.name
            row[2].text = str(len(cls.methods))
            row[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.rows[0].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER


def build_document(modules, title="Тесты Django-проекта", generated_at=None):
    """Собирает Word-документ со всеми тестами."""
    generated_at = generated_at or datetime.now()
    document = Document()

    normal = document.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    document.add_heading(title, level=0)
    total = sum(m.tests_count for m in modules)
    document.add_paragraph(f"Сформировано: {generated_at:%d.%m.%Y %H:%M}")
    document.add_paragraph(f"Всего тестов: {total}")

    document.add_heading("Сводка", level=1)
    _add_summary_table(document, modules)

    for module in modules:
        document.add_heading(f"Приложение {module.app}", level=1)
        document.add_paragraph(f"Файл: {module.path}")
        for cls in module.classes:
            document.add_heading(cls.name, level=2)
            if cls.doc:
                document.add_paragraph(cls.doc)
            if cls.setup_source:
                _add_caption(document, "Подготовка данных")
                _add_code(document, cls.setup_source)
            for method in cls.methods:
                document.add_heading(method.name, level=3)
                if method.doc:
                    document.add_paragraph(method.doc)
                _add_code(document, method.source)
    return document
