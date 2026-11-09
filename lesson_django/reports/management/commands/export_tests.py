from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Собирает все тесты проекта и записывает их в Word-файл (.docx)."

    def add_arguments(self, parser):
        parser.add_argument(
            "-o",
            "--output",
            default="tests_report.docx",
            help="Имя выходного файла (по умолчанию tests_report.docx).",
        )
        parser.add_argument(
            "--app",
            action="append",
            dest="app_labels",
            help="Взять тесты только этого приложения. Можно указать несколько раз.",
        )

    def handle(self, *args, **options):
        try:
            from reports.exporter import build_document, collect_modules
        except ImportError as error:
            raise CommandError(
                "Не хватает пакета python-docx. Установите: pip install python-docx"
            ) from error

        base_dir = Path(settings.BASE_DIR).resolve()
        wanted = options["app_labels"]
        targets = []
        for config in apps.get_app_configs():
            app_dir = Path(config.path).resolve()
            # Только приложения самого проекта: без django.contrib и сторонних пакетов.
            if base_dir not in app_dir.parents or "site-packages" in app_dir.parts:
                continue
            if wanted and config.label not in wanted:
                continue
            targets.append((config.label, app_dir))

        modules = collect_modules(targets, base_dir)
        if not modules:
            raise CommandError("Тесты не найдены.")

        output = Path(options["output"])
        build_document(modules).save(output)

        total = sum(module.tests_count for module in modules)
        self.stdout.write(
            self.style.SUCCESS(f"Готово: тестов {total}, файл {output.resolve()}")
        )
