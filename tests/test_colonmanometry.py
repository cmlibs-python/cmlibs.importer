import os.path
import unittest

from cmlibs.importer import colonmanometry
from cmlibs.importer.colonmanometry import import_data
from cmlibs.importer.errors import ImporterImportInvalidInputs, ImporterImportColonManometryError

from tests.shared import resource_path


class ColonManometry(unittest.TestCase):

    def test_parameters(self):
        parameters = colonmanometry.parameters()
        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("ColonManometry", parameters["id"])
        self.assertIn("mimetype", parameters["input"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data(self):
        hrm_file = resource_path("colon_manometry.csv")
        output_dir = resource_path("")

        output_exf = import_data(hrm_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(955, len(lines))
        os.remove(output_exf)

    def test_import_data_small(self):
        hrm_file = resource_path("colon_manometry_small.csv")
        output_dir = resource_path("")

        output_exf = import_data(hrm_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(47, len(lines))
        os.remove(output_exf)

    def test_import_data_no_manometry_file(self):
        nonexistent_file = resource_path("nonexistent.file")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportInvalidInputs, import_data, nonexistent_file, output_dir)

    def test_import_data_invalid_manometry_file_1(self):
        nonexistent_file = resource_path("white_image.jpeg")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportColonManometryError, import_data, nonexistent_file, output_dir)

    def test_import_data_invalid_manometry_file_2(self):
        nonexistent_file = resource_path("plain_text.txt")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportColonManometryError, import_data, nonexistent_file, output_dir)
