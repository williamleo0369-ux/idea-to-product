#!/usr/bin/env python3
"""Install all four skills without overwriting existing destinations."""
import argparse
import os
from pathlib import Path
import shutil
import tempfile

NAMES = ("idea-to-product", "idea-to-product-plan", "idea-to-product-design", "idea-to-product-develop")

def install(source, destination):
    source, destination = Path(source), Path(destination)
    for name in NAMES:
        if not (source / name / "SKILL.md").is_file():
            raise ValueError(f"Missing source skill: {name}")
    conflicts = [name for name in NAMES if os.path.lexists(destination / name)]
    if conflicts:
        raise FileExistsError("Existing skills; nothing installed: " + ", ".join(conflicts))
    destination.mkdir(parents=True, exist_ok=True)
    created = []
    with tempfile.TemporaryDirectory(prefix=".idea-to-product-install-", dir=destination) as tmp:
        staged = Path(tmp)
        for name in NAMES:
            shutil.copytree(source / name, staged / name)
        try:
            for name in NAMES:
                target = destination / name
                target.mkdir()  # exclusive creation, including protection from concurrent installs
                created.append(target)
                shutil.copytree(staged / name, target, dirs_exist_ok=True)
        except Exception:
            for target in reversed(created):
                shutil.rmtree(target)
            raise
    return [destination / name for name in NAMES]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    default = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"
    parser.add_argument("--dest", type=Path, default=default)
    args = parser.parse_args()
    try:
        for path in install(Path(__file__).resolve().parents[1] / "skills", args.dest):
            print(f"Installed: {path}")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Installation stopped: {error}\n")
