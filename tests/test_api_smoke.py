"""Offline API regression checks: no AI API key or network calls needed."""
import importlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

SOURCE = Path(__file__).resolve().parents[1] / "web" / "api" / "src"
sys.path.insert(0, str(SOURCE))


class ApiSmokeTests(unittest.TestCase):
    def test_import_and_public_profiles_without_gemini_key(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
            module = importlib.import_module("api.main")
            sample = pd.DataFrame({"searched_profile": ["Data Analyst", "Data Engineer"]})
            with patch.object(module, "load_parquet_data", return_value=sample):
                self.assertEqual(module.get_profiles(), ["Data Analyst", "Data Engineer"])

    def test_ai_endpoint_returns_unavailable_without_key(self):
        from api import main
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
            request = main.RoadmapGenerateRequest(profile="Data Analyst", skills=["SQL"])
            with self.assertRaises(main.HTTPException) as error:
                main.generate_roadmap(request)
            self.assertEqual(error.exception.status_code, 503)

    def test_filename_is_confined_to_output_dir(self):
        from api import main
        with tempfile.TemporaryDirectory() as path:
            with patch.object(main, "OUTPUT_DIR", path):
                name = main.roadmap_file_path("../../private")
                self.assertEqual(Path(name).parent, Path(path))
                self.assertFalse(".." in Path(name).name)
                self.assertEqual(Path(name).name, "roadmap_private.md")
                with self.assertRaises(main.HTTPException):
                    main.roadmap_file_path("...")

    def test_generation_remains_usable_when_storage_is_read_only(self):
        from api import main
        request = main.RoadmapGenerateRequest(profile="Data Analyst", skills=["SQL"])
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-value"}):
            with patch.object(main, "generate_roadmap_with_llm", return_value="# Test roadmap"):
                with patch.object(main, "os") as mocked_os:
                    mocked_os.makedirs.side_effect = OSError("Read-only filesystem")
                    response = main.generate_roadmap(request)
        self.assertEqual(response.markdown, "# Test roadmap")


if __name__ == "__main__":
    unittest.main()
