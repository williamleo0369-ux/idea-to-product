#!/usr/bin/env python3
"""Register prediction and retrospective records without overwrites."""
import argparse
import hashlib
import re
from pathlib import Path

def digest(data):
    return hashlib.sha256(data).hexdigest()

def record(root, mode, ident, source, revision="1"):
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", ident) or not re.fullmatch(r"[a-zA-Z0-9_-]+", revision):
        raise ValueError("ID and revision must use letters, numbers, underscore or hyphen")
    data = Path(source).read_bytes()
    base = Path(root) / ".idea-to-product/experiments"
    pred = base / "predictions" / (ident + ".md")
    fingerprint = pred.with_suffix(".sha256")
    if mode == "predict":
        if pred.exists() or fingerprint.exists():
            raise FileExistsError("Prediction already registered")
        pred.parent.mkdir(parents=True, exist_ok=True)
        with pred.open("xb") as f:
            f.write(data)
        try:
            with fingerprint.open("x") as f:
                f.write(digest(data) + "\n")
        except Exception:
            pred.unlink()
            raise
        return pred
    if mode != "retro":
        raise ValueError("Unknown mode")
    original = pred.read_bytes()
    if digest(original) != fingerprint.read_text().strip():
        raise ValueError("Prediction integrity check failed; preserve files and investigate")
    target = base / "retros" / (ident + "-" + revision + ".md")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as f:
        f.write(("<!-- prediction: " + ident + "; sha256: " + digest(original) + " -->\n").encode() + data)
    return target

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["predict", "retro"])
    parser.add_argument("id")
    parser.add_argument("source", type=Path)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--revision", default="1")
    args = parser.parse_args()
    try:
        print(record(args.project, args.mode, args.id, args.source, args.revision))
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")
