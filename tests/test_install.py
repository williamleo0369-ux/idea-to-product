import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

class InstallTests(unittest.TestCase):
    def test_installs_self_contained_package(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / "skills"
            paths = installer.install(ROOT / "skills", dest)
            self.assertEqual(len(paths), 4)
            self.assertTrue((dest / "idea-to-product/references/calibration.md").is_file())
            for path in paths:
                self.assertEqual((path / "SKILL.md").read_bytes(), (ROOT / "skills" / path.name / "SKILL.md").read_bytes())

    def test_conflict_preserves_existing_and_creates_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            existing = dest / "idea-to-product-design"
            existing.mkdir()
            (existing / "keep.txt").write_text("user work")
            with self.assertRaises(FileExistsError):
                installer.install(ROOT / "skills", dest)
            self.assertEqual((existing / "keep.txt").read_text(), "user work")
            self.assertEqual([p.name for p in dest.iterdir()], ["idea-to-product-design"])

    def test_failed_copy_rolls_back_owned_destinations(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            original = installer.shutil.copytree
            def fail_on_publish(src, target, *args, **kwargs):
                if kwargs.get("dirs_exist_ok"):
                    raise OSError("simulated copy failure")
                return original(src, target, *args, **kwargs)
            with patch.object(installer.shutil, "copytree", side_effect=fail_on_publish):
                with self.assertRaises(OSError):
                    installer.install(ROOT / "skills", dest)
            self.assertEqual(list(dest.iterdir()), [])

if __name__ == "__main__":
    unittest.main()
