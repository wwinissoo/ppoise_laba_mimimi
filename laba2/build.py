"""Сборка исполняемого артефакта: python build.py → dist/culinary-lab2.pyz."""

import shutil
import zipapp
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
BUILD_DIR = PROJECT_DIR / "build" / "app"
DIST_DIR = PROJECT_DIR / "dist"
ARTIFACT_NAME = "culinary-lab2.pyz"
PACKAGES = ("culinary", "cli")
MODULES = ("main.py",)
ENTRY_POINT = "main:main"
INTERPRETER = "/usr/bin/env python3"
IGNORED = shutil.ignore_patterns("__pycache__", "*.pyc")


def prepare_sources():
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    BUILD_DIR.mkdir(parents=True)
    for package in PACKAGES:
        shutil.copytree(PROJECT_DIR / package, BUILD_DIR / package, ignore=IGNORED)
    for module in MODULES:
        shutil.copy2(PROJECT_DIR / module, BUILD_DIR / module)


def build():
    prepare_sources()
    DIST_DIR.mkdir(exist_ok=True)
    artifact = DIST_DIR / ARTIFACT_NAME
    zipapp.create_archive(BUILD_DIR, artifact, interpreter=INTERPRETER, main=ENTRY_POINT)
    return artifact


if __name__ == "__main__":
    print(f"Собран артефакт: {build()}")
