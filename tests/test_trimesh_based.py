import os.path
import unittest

from opencmiss.importer.errors import OpenCMISSImportInvalidInputs
from opencmiss.importer.obj import import_data
from opencmiss.importer import stl
from opencmiss.importer import ply
from opencmiss.importer import obj
from opencmiss.importer import svg
from opencmiss.importer import dxf

from tests.shared import resource_path


class Trimesh(unittest.TestCase):

    def test_parameters(self):
        parameters = obj.parameters()

        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("OBJ", parameters["id"])
        self.assertEqual(1, len(parameters["input"]))
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_nonexistent_xml(self):
        non_file = resource_path("nonexistent.xml")
        output_dir = resource_path("")

        self.assertRaises(OpenCMISSImportInvalidInputs, import_data, non_file, output_dir, )

    def test_parameters_stl(self):
        parameters = stl.parameters()

        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("STL", parameters["id"])
        self.assertEqual(1, len(parameters["input"]))
        self.assertEqual("model/stl", parameters["input"]["mimetype"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_stl(self):
        stl_file = resource_path("cylinder.stl")
        output_dir = resource_path("")

        output_exf = stl.import_data(stl_file, output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(3594, len(lines))
        os.remove(output_exf)

    def test_parameters_ply(self):
        parameters = ply.parameters()

        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("PLY", parameters["id"])
        self.assertEqual(1, len(parameters["input"]))
        self.assertEqual("text/plain", parameters["input"]["mimetype"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_ply(self):
        stl_file = resource_path("bunny.ply")
        output_dir = resource_path("")

        output_exf = ply.import_data(stl_file, output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(138502, len(lines))
        os.remove(output_exf)

    def test_parameters_obj(self):
        parameters = obj.parameters()

        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("OBJ", parameters["id"])
        self.assertEqual(1, len(parameters["input"]))
        self.assertEqual("model/obj", parameters["input"]["mimetype"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_obj(self):
        stl_file = resource_path("wallhole.obj")
        output_dir = resource_path("")

        output_exf = obj.import_data(stl_file, output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(893, len(lines))
        os.remove(output_exf)

    def test_parameters_dxf(self):
        parameters = dxf.parameters()

        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("DXF", parameters["id"])
        self.assertEqual(1, len(parameters["input"]))
        self.assertEqual("image/vnd.dxf", parameters["input"]["mimetype"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_dxf(self):
        stl_file = resource_path("wrench.dxf")
        output_dir = resource_path("")

        output_exf = dxf.import_data(stl_file, output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(849, len(lines))
        os.remove(output_exf)

    def test_parameters_svg(self):
        parameters = svg.parameters()

        keys = set(parameters.keys())
        exp_keys = {"version", "id", "input", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("SVG", parameters["id"])
        self.assertEqual(1, len(parameters["input"]))
        self.assertEqual("image/svg+xml", parameters["input"]["mimetype"])
        self.assertIn("mimetype", parameters["output"])

    def test_import_data_svg(self):
        stl_file = resource_path("mil.svg")
        output_dir = resource_path("")

        output_exf = svg.import_data(stl_file, output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(726065, len(lines))
        os.remove(output_exf)


if __name__ == '__main__':
    unittest.main()
