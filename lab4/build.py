"""Build the release artifact (tests are not included): python build.py -> dist/generic-lab4.pyz."""

import shutil
import zipapp
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
BUILD_DIR = PROJECT_DIR / "build" / "app"
DIST_DIR = PROJECT_DIR / "dist"
ARTIFACT_NAME = "generic-lab4.pyz"
PACKAGE = "generic_lab"
ENTRY_MODULE = "main.py"
ENTRY_POINT = "main:main"
INTERPRETER = "/usr/bin/env python3"
IGNORED = shutil.ignore_patterns("__pycache__", "*.pyc")


def prepare_sources() -> None:
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    BUILD_DIR.mkdir(parents=True)
    shutil.copytree(PROJECT_DIR / PACKAGE, BUILD_DIR / PACKAGE, ignore=IGNORED)
    shutil.copy2(PROJECT_DIR / ENTRY_MODULE, BUILD_DIR / ENTRY_MODULE)


def build() -> Path:
    prepare_sources()
    DIST_DIR.mkdir(exist_ok=True)
    artifact = DIST_DIR / ARTIFACT_NAME
    zipapp.create_archive(BUILD_DIR, artifact, interpreter=INTERPRETER, main=ENTRY_POINT)
    return artifact


if __name__ == "__main__":
    print(f"Built artifact: {build()}")
