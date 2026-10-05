import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("record", ROOT / "skills/idea-to-product/scripts/record.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class RecordTests(unittest.TestCase):
    def test_records_preserve_prediction_and_reject_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "draft.md"
            src.write_text("original expectation")
            pred = module.record(tmp, "predict", "design-01", src)
            src.write_text("actual evidence")
            with self.assertRaises(FileExistsError):
                module.record(tmp, "predict", "design-01", src)
            retro = module.record(tmp, "retro", "design-01", src)
            self.assertEqual(pred.read_text(), "original expectation")
            self.assertIn("actual evidence", retro.read_text())
            with self.assertRaises(FileExistsError):
                module.record(tmp, "retro", "design-01", src)

    def test_modified_or_missing_prediction_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "draft.md"
            src.write_text("original")
            with self.assertRaises(FileNotFoundError):
                module.record(tmp, "retro", "missing", src)
            pred = module.record(tmp, "predict", "plan-01", src)
            pred.write_text("changed after result")
            with self.assertRaises(ValueError):
                module.record(tmp, "retro", "plan-01", src)
            self.assertFalse((Path(tmp) / ".idea-to-product/experiments/retros").exists())

    def test_path_traversal_is_rejected(self):
        with self.assertRaises(ValueError):
            module.record(".", "predict", "../escape", "unused")
