import os.path
import unittest

from cmlibs.importer import pointcloud
from cmlibs.importer.pointcloud import import_data
from cmlibs.importer.errors import ImporterImportInvalidInputs, ImporterImportPointCloudError

from shared import resource_path


class PointCloud(unittest.TestCase):

    def test_parameters(self):
        parameters = pointcloud.parameters()
        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("PointCloud", parameters["id"])
        self.assertIn("mimetype", parameters["input"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_non_existent_file(self):
        nonexistent_file = resource_path("nonexistent.file")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportInvalidInputs, import_data, nonexistent_file, output_dir)

    def test_import_data_1(self):
        point_cloud_file = resource_path("point_cloud_1.csv")
        output_dir = resource_path("")

        output_exf = import_data(point_cloud_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(35, len(lines))
        os.remove(output_exf)

    def test_import_data_2(self):
        point_cloud_file = resource_path("point_cloud_2.csv")
        output_dir = resource_path("")

        output_exf = import_data(point_cloud_file, output_dir)
        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(27, len(lines))
        os.remove(output_exf)

    def test_import_data_3(self):
        point_cloud_file = resource_path("point_cloud_3.csv")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportPointCloudError, import_data, point_cloud_file, output_dir)

    def test_import_data_4(self):
        point_cloud_file = resource_path("point_cloud_4.csv")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportPointCloudError, import_data, point_cloud_file, output_dir)

    def test_import_data_invalid_file_1(self):
        nonexistent_file = resource_path("white_image.jpeg")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportPointCloudError, import_data, nonexistent_file, output_dir)

    def test_import_data_invalid_file_2(self):
        nonexistent_file = resource_path("plain_text.txt")
        output_dir = resource_path("")

        self.assertRaises(ImporterImportPointCloudError, import_data, nonexistent_file, output_dir)
