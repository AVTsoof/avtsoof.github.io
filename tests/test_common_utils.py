from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from avtsoof.common_utils import REPO_ROOT, data_dir


class DataDirTests(unittest.TestCase):
    def test_defaults_to_repo_data_subdir(self) -> None:
        os.environ.pop("AVTSOOF_DATA_DIR", None)
        name = f"test-default-{uuid4().hex}"
        target = data_dir(name)
        expected = REPO_ROOT / "data" / name
        self.assertEqual(expected, target)
        self.assertTrue(target.exists())
        target.rmdir()

    def test_uses_env_override_base_dir(self) -> None:
        name = f"test-env-{uuid4().hex}"
        with tempfile.TemporaryDirectory() as tmp_dir:
            os.environ["AVTSOOF_DATA_DIR"] = tmp_dir
            target = data_dir(name)
            expected = Path(tmp_dir) / name
            self.assertEqual(expected, target)
            self.assertTrue(target.exists())

    def test_blank_env_falls_back_to_repo_data_subdir(self) -> None:
        os.environ["AVTSOOF_DATA_DIR"] = "   "
        name = f"test-blank-{uuid4().hex}"
        target = data_dir(name)
        expected = REPO_ROOT / "data" / name
        self.assertEqual(expected, target)
        self.assertTrue(target.exists())
        target.rmdir()


if __name__ == "__main__":
    unittest.main()