import os.path
import unittest

from opencmiss.importer import colonhrm
from opencmiss.importer.colonhrm import import_data
from opencmiss.importer.errors import OpenCMISSImportInvalidInputs, OpenCMISSImportColonHRMError

from tests.shared import resource_path


class ColonHRM(unittest.TestCase):

    def test_parameters(self):
        parameters = colonhrm.parameters()
        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("ColonHRM", parameters["id"])
        self.assertIn("mimetype", parameters["input"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data(self):
        hrm_file = resource_path("hrm_stim_colon.txt")
        output_dir = resource_path("")

        output_exf = import_data(hrm_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(566, len(lines))
        os.remove(output_exf)

    def test_import_data_no_hrm_file(self):
        nonexistent_file = resource_path("nonexistent.file")
        output_dir = resource_path("")

        self.assertRaises(OpenCMISSImportInvalidInputs, import_data, nonexistent_file, output_dir)

    def test_import_data_invalid_hrm_file_1(self):
        nonexistent_file = resource_path("white_image.jpeg")
        output_dir = resource_path("")

        self.assertRaises(OpenCMISSImportColonHRMError, import_data, nonexistent_file, output_dir)

    def test_import_data_invalid_hrm_file_2(self):
        nonexistent_file = resource_path("plain_text.txt")
        output_dir = resource_path("")

        self.assertRaises(OpenCMISSImportColonHRMError, import_data, nonexistent_file, output_dir)
