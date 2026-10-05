#!/usr/bin/env python3
"""Portable structural checks; does not evaluate agent behavior."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
for name in ("idea-to-product", "idea-to-product-plan", "idea-to-product-design", "idea-to-product-develop"):
    p = root / "skills" / name / "SKILL.md"
    if not p.is_file():
        errors.append(f"Missing {p}")
        continue
    text = p.read_text()
    front = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not front or f"name: {name}" not in front.group(1) or "description:" not in front.group(1):
        errors.append(f"Invalid frontmatter: {p}")
    if not (p.parent / "agents" / "openai.yaml").is_file():
        errors.append(f"Missing UI metadata: {name}")
for p in root.rglob("*.md"):
    if ".git" in p.parts:
        continue
    text = p.read_text()
    if "/Users/" in text:
        errors.append(f"Machine-specific path: {p}")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if "://" in target or target.startswith("#"):
            continue
        path = (p.parent / target.split("#")[0]).resolve()
        if not path.exists() or not path.is_relative_to(root):
            errors.append(f"Broken or external local link: {p}: {target}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("PASS: four skill entrypoints, UI metadata, portable paths and local links")
