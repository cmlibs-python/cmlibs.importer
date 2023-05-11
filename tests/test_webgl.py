import os.path
import unittest

from cmlibs.importer import webgl
from cmlibs.importer.errors import ImporterImportInvalidInputs

from shared import resource_path


class WebGLJSON(unittest.TestCase):

    def test_parameters(self):
        parameters = webgl.parameters()

        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("WebGLJSON", parameters["id"])
        self.assertEqual(1, len(parameters["input"]))
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_nonexistent_json(self):
        json_file = resource_path("nonexistent.json")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportInvalidInputs, webgl.import_data, json_file, output_dir)

    def test_import_data(self):
        json_file = resource_path("webgl_contours.json")
        output_dir = resource_path("")

        output_exf = webgl.import_data(json_file, output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(240210, len(lines))
        os.remove(output_exf)


if __name__ == '__main__':
    unittest.main()
