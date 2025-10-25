import os.path
import unittest

from cmlibs.importer import xyzvalue
from cmlibs.importer.xyzvalue import import_data
from cmlibs.importer.errors import ImporterImportInvalidInputs, ImporterImportXYZValueError

from shared import resource_path


class XYZValue(unittest.TestCase):

    def test_parameters(self):
        parameters = xyzvalue.parameters()
        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("XYZValue", parameters["id"])
        self.assertIn("mimetype", parameters["input"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_non_existent_file(self):
        nonexistent_file = resource_path("nonexistent.file")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportInvalidInputs, import_data, nonexistent_file, output_dir)

    def test_import_data_1(self):
        point_cloud_file = resource_path("xyz_value_headerless.txt")
        output_dir = resource_path("")

        output_exf = import_data(point_cloud_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(163, len(lines))
        os.remove(output_exf)

    def test_import_data_2(self):
        point_cloud_file = resource_path("xyz_value_header.txt")
        output_dir = resource_path("")

        output_exf = import_data(point_cloud_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(193, len(lines))
        os.remove(output_exf)

    def test_import_data_3(self):
        point_cloud_file = resource_path("xyz_value_multi_string_fields.dat")
        output_dir = resource_path("")

        output_exf = import_data(point_cloud_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(97, len(lines))
        os.remove(output_exf)

    def test_import_data_invalid_value(self):
        point_cloud_file = resource_path("xyz_value_header_bad_value.txt")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportXYZValueError, import_data, point_cloud_file, output_dir)

    def test_import_data_invalid_file_1(self):
        nonexistent_file = resource_path("white_image.jpeg")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportXYZValueError, import_data, nonexistent_file, output_dir)

    def test_import_data_invalid_file_2(self):
        nonexistent_file = resource_path("plain_text.txt")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportXYZValueError, import_data, nonexistent_file, output_dir)
