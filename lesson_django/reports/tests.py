import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from reports.exporter import (
    build_document,
    collect_modules,
    find_test_files,
    parse_test_file,
)

SAMPLE = '''\
from django.test import TestCase


class FirstTests(TestCase):
    """Пример класса."""

    def setUp(self):
        self.value = 1

    def test_one(self):
        """Первый тест."""
        self.assertEqual(self.value, 1)

    def helper(self):
        return 5


class NoTestsHere:
    def method(self):
        pass
'''


class ExporterTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.app_dir = self.root / "shop"
        self.app_dir.mkdir()
        self.tests_file = self.app_dir / "tests.py"
        self.tests_file.write_text(SAMPLE, encoding="utf-8")

    def test_parse_finds_only_classes_with_tests(self):
        """Классы без test-методов не попадают в результат."""
        classes = parse_test_file(self.tests_file)
        self.assertEqual([c.name for c in classes], ["FirstTests"])

    def test_parse_reads_docstrings_and_method_names(self):
        """Читаются описания класса и теста, вспомогательные методы пропускаются."""
        cls = parse_test_file(self.tests_file)[0]
        self.assertEqual(cls.doc, "Пример класса.")
        self.assertEqual([m.name for m in cls.methods], ["test_one"])
        self.assertEqual(cls.methods[0].doc, "Первый тест.")

    def test_parse_source_is_dedented(self):
        """Код метода приходит без лишнего отступа."""
        method = parse_test_file(self.tests_file)[0].methods[0]
        self.assertTrue(method.source.startswith("def test_one(self):"))
        self.assertIn("    self.assertEqual(self.value, 1)", method.source)

    def test_parse_collects_setup(self):
        """Подготовка данных (setUp) сохраняется отдельно."""
        cls = parse_test_file(self.tests_file)[0]
        self.assertIn("self.value = 1", cls.setup_source)

    def test_find_test_files_supports_package(self):
        """Находятся и tests.py, и test*.py внутри папки tests."""
        package = self.app_dir / "tests"
        package.mkdir()
        (package / "test_extra.py").write_text(SAMPLE, encoding="utf-8")
        (package / "helpers.py").write_text("x = 1", encoding="utf-8")
        names = [p.name for p in find_test_files(self.app_dir)]
        self.assertEqual(names, ["tests.py", "test_extra.py"])

    def test_collect_modules_uses_relative_path(self):
        """Путь к файлу в отчёте считается от корня проекта."""
        modules = collect_modules([("shop", self.app_dir)], self.root)
        self.assertEqual(modules[0].path, "shop/tests.py")
        self.assertEqual(modules[0].tests_count, 1)

    def test_document_contains_test_and_cyrillic_text(self):
        """В документе есть имя теста, его описание и русский текст."""
        modules = collect_modules([("shop", self.app_dir)], self.root)
        document = build_document(modules, generated_at=datetime(2026, 1, 1, 12, 0))
        text = "\n".join(p.text for p in document.paragraphs)
        self.assertIn("test_one", text)
        self.assertIn("Первый тест.", text)
        self.assertIn("Сформировано: 01.01.2026 12:00", text)
