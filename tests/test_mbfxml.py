import csv
import os.path
import unittest

from opencmiss.importer import mbfxml
from opencmiss.importer.errors import OpenCMISSImportInvalidInputs
from opencmiss.importer.mbfxml import import_data

from tests.shared import resource_path


class MBFXML(unittest.TestCase):

    def test_parameters(self):
        parameters = mbfxml.parameters()

        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("MBFXML", parameters["id"])
        self.assertEqual(1, len(parameters["input"]))
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_nonexistent_xml(self):
        xml_file = resource_path("nonexistent.xml")
        output_dir = resource_path("")

        self.assertRaises(OpenCMISSImportInvalidInputs, import_data, xml_file, output_dir)

    def test_import_data(self):
        xml_file = resource_path("mbf_contours.xml")
        output_dir = resource_path("")

        output_exf = import_data(xml_file, output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(230, len(lines))
        os.remove(output_exf)


if __name__ == '__main__':
    unittest.main()
