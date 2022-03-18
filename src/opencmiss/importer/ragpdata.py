import csv

from mbfxml2ex.app import read_xml
from mbfxml2ex.exceptions import MBFXMLFormat
from mbfxml2ex.zinc import load
from opencmiss.zinc.context import Context
from opencmiss.zinc.field import Field

from opencmiss.importer.errors import OpenCMISSImportMBFXMLError, OpenCMISSImportFileNotFoundError, OpenCMISSImportGeneFileError
from opencmiss.utils.zinc.field import create_field_finite_element


def import_data(marker_file, gene_data_file, output_exf):
    try:
        contents = read_xml(marker_file)
    except MBFXMLFormat:
        raise OpenCMISSImportMBFXMLError("Marker file is not a valid MBF XML file.")

    context = Context("Gene")
    region = context.getDefaultRegion()
    field_module = region.getFieldmodule()
    load(region, contents, None)

    try:
        with open(gene_data_file) as f:
            csv_reader = csv.DictReader(f)

            try:
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
            except UnicodeDecodeError:
                raise OpenCMISSImportGeneFileError("Gene CSV file not valid.")

        region.writeFile(output_exf)
    except FileNotFoundError:
        raise OpenCMISSImportFileNotFoundError("Gene CSV file not found.")


def identifier():
    return "ragpdata"


def parameters():
    return {
        "version": "0.1.0",
        "id": identifier(),
        "inputs": [
            {
                "mimetype": "application/vnd.mbfbioscience.metadata+xml",
            },
            {
                "mimetype": "text/x.vnd.sparc.gene-v-sample+csv",
            }
        ],
        "outputs": [
            {
                "mimetype": "text/x.vnd.abi.exf+plain",
            }
        ]
    }
