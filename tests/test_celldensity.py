import os.path
import unittest

from cmlibs.importer import celldensity
from cmlibs.importer.celldensity import import_data
from cmlibs.importer.errors import ImporterImportInvalidInputs, ImporterImportCellDensityError

from tests.shared import resource_path


class CellDensity(unittest.TestCase):

    def test_parameters(self):
        parameters = celldensity.parameters()
        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("CellDensity", parameters["id"])
        self.assertIn("mimetype", parameters["input"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_non_existent_file(self):
        nonexistent_file = resource_path("nonexistent.file")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportInvalidInputs, import_data, nonexistent_file, output_dir)

    def test_import_data(self):
        cell_density_file = resource_path("cell_density.csv")
        output_dir = resource_path("")

        output_exf = import_data(cell_density_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(41, len(lines))
        os.remove(output_exf)

    def test_import_data_invalid_file_1(self):
        nonexistent_file = resource_path("white_image.jpeg")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportCellDensityError, import_data, nonexistent_file, output_dir)

    def test_import_data_invalid_file_2(self):
        nonexistent_file = resource_path("plain_text.txt")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportCellDensityError, import_data, nonexistent_file, output_dir)
