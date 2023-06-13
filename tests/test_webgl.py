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
        json_file = resource_path("webgl_contours_small.json")
        output_dir = resource_path("")

        output_exf = webgl.import_data(json_file, output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(204, len(lines))
        os.remove(output_exf)

    def test_import_data_separate(self):
        json_file = resource_path("webgl_contours_separate.json")
        output_dir = resource_path("")

        output_exf = webgl.import_data(json_file, output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(378, len(lines))
        os.remove(output_exf)

    def test_import_data_missed_repeats(self):
        json_file = resource_path("webgl_contours_missed_repeats.json")
        output_dir = resource_path("")

        output_exf = webgl.import_data(json_file, output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(141, len(lines))
        os.remove(output_exf)

    def test_connected_triangles_1(self):
        triangles = [[1, 2, 3], [4, 5, 3], [4, 3, 2], [6, 5, 4], [7, 8, 1], [8, 2, 1], [9, 4, 2],
                     [9, 2, 8], [9, 10, 6], [9, 6, 4], [11, 12, 13], [7, 13, 12], [14, 8, 7], [14, 1, 2]]

        initial_triangle_index = 3
        connected_triangles = _find_connected(initial_triangle_index, triangles)

        self.assertEqual(14, len(connected_triangles[0]))

    def test_connected_triangles_2(self):
        triangles = [[1, 2, 3], [4, 5, 3], [4, 3, 2], [6, 5, 4], [7, 8, 1], [8, 2, 1], [9, 4, 2],
                     [9, 2, 8], [9, 10, 6], [9, 6, 4], [11, 12, 13], [7, 13, 12], [14, 8, 7], [14, 1, 2]]
        for index, triangle in enumerate(triangles):
            triangles[index] = [v + 250 for v in triangle]

        initial_triangle_index = 3
        connected_triangles = _find_connected(initial_triangle_index, triangles)

        self.assertEqual(14, len(connected_triangles[0]))

    def test_connected_triangles_3(self):
        triangles = [[1, 2, 3], [4, 5, 3], [4, 3, 2], [6, 5, 4], [7, 8, 1], [8, 2, 1], [9, 4, 2],
                     [9, 2, 8], [9, 10, 6], [9, 6, 4], [11, 12, 13], [7, 13, 12], [14, 8, 7], [14, 1, 2],
                     [18, 16, 19], [20, 16, 20], [21, 16, 21], [22, 16, 22], [17, 23, 18], [24, 18, 17],
                     [24, 25, 26], [27, 26, 28], [27, 26, 29], [30, 26, 30], [28, 31, 32], [15, 32, 19]]

        initial_triangle_index = 20
        connected_triangles = _find_connected(initial_triangle_index, triangles)

        self.assertEqual(12, len(connected_triangles[0]))

        initial_triangle_index = 5
        connected_triangles = _find_connected(initial_triangle_index, triangles)

        self.assertEqual(14, len(connected_triangles[0]))


def _find_connected(initial_triangle_index, triangles):
    connected_triangles = [[initial_triangle_index]]
    connected_nodes = [set(triangles[initial_triangle_index])]
    for triangle_index, triangle in enumerate(triangles):
        if triangle_index == initial_triangle_index:
            continue

        connected_triangles.append([triangle_index])
        connected_nodes.append(set(triangles[triangle_index]))

        index = 0
        while index < len(connected_triangles):
            connection_found = False
            next_index = index + 1
            base_connected_node_set = connected_nodes[index]
            while next_index < len(connected_triangles):
                current_connected_node_set = connected_nodes[next_index]
                intersection = base_connected_node_set.intersection(current_connected_node_set)
                if len(intersection):
                    connection_found = True
                    connected_triangles[index].extend(connected_triangles[next_index])
                    connected_nodes[index].update(connected_nodes[next_index])
                    del connected_triangles[next_index]
                    del connected_nodes[next_index]
                    index = 0
                    # next_index = 0
                else:
                    next_index += 1

            if not connection_found:
                index += 1

    return connected_triangles


if __name__ == '__main__':
    unittest.main()
