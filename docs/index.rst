CMLibs Importer
===============

**CMLibs Importer** is a Python package for importing different formats into Zinc.
The importer can import the following formats:

* ColonHRM
* ColonManometry
* DXF
* MBF XML
* OBJ
* PLY
* RAGP Data
* STL
* SVG
* Trimesh
* WebGL JSON

Each importer adheres to the same API:

* identifier()
* import_data(inputs, output_directory)
* import_data_into_region(region, inputs)
* parameters(parameter_name=None)
