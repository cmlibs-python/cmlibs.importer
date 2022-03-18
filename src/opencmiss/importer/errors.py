
class OpenCMISSImportError(Exception):
    pass


class OpenCMISSImportMBFXMLError(OpenCMISSImportError):
    pass


class OpenCMISSImportFileNotFoundError(OpenCMISSImportError):
    pass


class OpenCMISSImportGeneFileError(OpenCMISSImportError):
    pass
