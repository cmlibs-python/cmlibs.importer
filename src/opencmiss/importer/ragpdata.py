import csv
import os.path

from mbfxml2ex.app import read_xml
from mbfxml2ex.exceptions import MBFXMLFormat
from mbfxml2ex.zinc import load

from opencmiss.utils.zinc.field import create_field_finite_element
from opencmiss.zinc.context import Context
from opencmiss.zinc.field import Field
from opencmiss.zinc.status import OK as ZINC_OK

from opencmiss.importer.base import valid
from opencmiss.importer.errors import OpenCMISSImportMBFXMLError, OpenCMISSImportGeneFileError, OpenCMISSImportInvalidInputs, OpenCMISSImportUnknownParameter


def import_data(inputs, output_directory):
    if not valid(inputs, parameters("inputs")):
        raise OpenCMISSImportInvalidInputs(f"Invalid imports given to importer: {identifier()}")

    marker_file = inputs[0]
    gene_data_file = inputs[1]
    output = None

    try:
        contents = read_xml(marker_file)
    except MBFXMLFormat:
        raise OpenCMISSImportMBFXMLError("Marker file is not a valid MBF XML file.")

    context = Context("Gene")
    region = context.getDefaultRegion()
    field_module = region.getFieldmodule()
    load(region, contents, None)

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

    output_exf = os.path.join(output_directory, identifier() + ".exf")
    result = region.writeFile(output_exf)
    if result == ZINC_OK:
        output = output_exf

    return output


def identifier():
    return "ragpdata"


def parameters(parameter_name=None):
    importer_parameters = {
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
        "output": {
            "mimetype": "text/x.vnd.abi.exf+plain",
        }
    }

    if parameter_name is not None:
        if parameter_name in importer_parameters:
            return importer_parameters[parameter_name]
        else:
            raise OpenCMISSImportUnknownParameter(f"Importer '{identifier()}' does not have parameter: {parameter_name}")

    return importer_parameters
