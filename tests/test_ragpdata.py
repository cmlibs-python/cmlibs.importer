import csv
import os.path
import unittest

import mbfxml2ex.exceptions
from mbfxml2ex.app import read_xml
from mbfxml2ex.zinc import load

from opencmiss.utils.zinc.field import create_field_finite_element
from opencmiss.zinc.context import Context
from opencmiss.zinc.field import Field

from opencmiss.importer import ragpdata
from opencmiss.importer.errors import OpenCMISSImportInvalidInputs
from opencmiss.importer.ragpdata import import_data

from tests.shared import resource_path


class RAGPData(unittest.TestCase):

    def test_parameters(self):
        parameters = ragpdata.parameters()

        keys = set(parameters.keys())
        exp_keys = {"version", "id", "inputs", "output", "title", "description"}

        self.assertEqual(exp_keys, keys)
        self.assertEqual("RAGPData", parameters["id"])
        self.assertEqual(2, len(parameters["inputs"]))
        self.assertIn("mimetype", parameters["output"])

    def test_read_bad_markers(self):
        image_file = resource_path("white_image.jpeg")
        self.assertRaises(mbfxml2ex.exceptions.MBFXMLFormat, read_xml, image_file)

    def test_read_bad_csv(self):
        image_file = resource_path("white_image.jpeg")
        with open(image_file) as f:
            csv_reader = csv.DictReader(f)

            try:
                for row in csv_reader:
                    print(row)
            except UnicodeDecodeError as e:
                self.assertEqual("'utf-8' codec can't decode byte 0xff in position 0: invalid start byte", str(e))

    def test_read_no_markers(self):
        nonexistent_file = resource_path("nonexistent.file")
        self.assertRaises(mbfxml2ex.exceptions.MBFXMLFile, read_xml, nonexistent_file)

    def test_read_no_csv(self):
        nonexistent_file = resource_path("nonexistent.file")
        self.assertRaises(FileNotFoundError, open, nonexistent_file)

    def test_read_markers(self):
        xml_file = resource_path("gene_locations.xml")
        contents = read_xml(xml_file)

        self.assertEqual(4, len(contents))

    def test_read_gene_values(self):
        EXPECTED_GENES = ["Ache", "Actb", "Adra1a"]
        csv_file = resource_path("gene_v_location.csv")
        with open(csv_file) as f:
            csv_reader = csv.DictReader(f)

            for row in csv_reader:
                gene = row[""]
                self.assertIn(gene, EXPECTED_GENES)
                del row[""]
                self.assertEqual(4, len(row))

    def test_content_in_context(self):
        xml_file = resource_path("gene_locations.xml")
        contents = read_xml(xml_file)
        context = Context("Gene")
        region = context.getDefaultRegion()
        field_module = region.getFieldmodule()
        load(region, contents, None)

        csv_file = resource_path("gene_v_location.csv")
        with open(csv_file) as f:
            csv_reader = csv.DictReader(f)

            for row in csv_reader:
                gene = row[""]
                del row[""]

                gene_field = create_field_finite_element(field_module, gene, 1, type_coordinate=False)
                data_points = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
                data_template = data_points.createNodetemplate()
                data_template.defineField(gene_field)

                point_iter = data_points.createNodeiterator()
                data_point = point_iter.next()
                while data_point.isValid():
                    field_cache = field_module.createFieldcache()
                    field_cache.setNode(data_point)
                    marker = field_module.findFieldByName("marker_name")
                    cell_name = marker.evaluateString(field_cache)

                    try:
                        gene_expression_value = float(row[cell_name])
                        data_point.merge(data_template)
                        gene_field.assignReal(field_cache, gene_expression_value)
                    except ValueError:
                        pass

                    data_point = point_iter.next()

        output_exf = resource_path("gene_data.exf")
        region.writeFile(output_exf)
        self.assertTrue(os.path.isfile(output_exf))
        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(97, len(lines))
        os.remove(output_exf)

    def test_import_data_nonexistent_xml(self):
        xml_file = resource_path("nonexistent.xml")
        csv_file = resource_path("gene_v_location.csv")
        output_dir = resource_path("")

        self.assertRaises(OpenCMISSImportInvalidInputs, import_data, [xml_file, csv_file], output_dir)

    def test_import_data_nonexistent_csv(self):
        xml_file = resource_path("gene_locations.xml")
        csv_file = resource_path("nonexistent.csv")
        output_dir = resource_path("")

        self.assertRaises(OpenCMISSImportInvalidInputs, import_data, [xml_file, csv_file], output_dir)

    def test_import_data(self):
        xml_file = resource_path("gene_locations.xml")
        csv_file = resource_path("gene_v_location.csv")
        output_dir = resource_path("")

        output_exf = import_data([xml_file, csv_file], output_dir)

        self.assertTrue(os.path.isfile(output_exf))

        with open(output_exf) as f:
            lines = f.readlines()

        self.assertEqual(97, len(lines))
        os.remove(output_exf)


if __name__ == '__main__':
    unittest.main()
