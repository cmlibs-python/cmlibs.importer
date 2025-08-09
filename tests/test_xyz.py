import os.path
import unittest

from cmlibs.importer import xyz
from cmlibs.importer.xyz import import_data
from cmlibs.importer.errors import ImporterImportInvalidInputs, ImporterImportXYZError

from shared import resource_path


class XYZ(unittest.TestCase):

    def test_parameters(self):
        parameters = xyz.parameters()
        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("XYZ", parameters["id"])
        self.assertIn("mimetype", parameters["input"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_non_existent_file(self):
        nonexistent_file = resource_path("nonexistent.file")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportInvalidInputs, import_data, nonexistent_file, output_dir)

    def test_import_data_1(self):
        point_cloud_file = resource_path("small_point_cloud_with_labels.txt")
        output_dir = resource_path("")

        output_exf = import_data(point_cloud_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(63, len(lines))
        os.remove(output_exf)

    def test_import_data_2(self):
        point_cloud_file = resource_path("xyz_2.txt")
        output_dir = resource_path("")

        output_exf = import_data(point_cloud_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(55, len(lines))
        os.remove(output_exf)

    def test_import_data_3(self):
        point_cloud_file = resource_path("xyz_1.txt")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportXYZError, import_data, point_cloud_file, output_dir)

    def test_import_data_invalid_file_1(self):
        nonexistent_file = resource_path("white_image.jpeg")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportXYZError, import_data, nonexistent_file, output_dir)

    def test_import_data_invalid_file_2(self):
        nonexistent_file = resource_path("plain_text.txt")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportXYZError, import_data, nonexistent_file, output_dir)
