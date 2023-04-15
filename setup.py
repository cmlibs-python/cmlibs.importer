import io

from setuptools import setup


def readfile(filename, split=False):
    with io.open(filename, encoding="utf-8") as stream:
        if split:
            return stream.read().split("\n")
        return stream.read()


readme = readfile("README.rst", split=True)

requires = ['cmlibs.importer']

setup(
    name='opencmiss.importer',
    version="0.4.2",
    description='OpenCMISS Import functions.',
    long_description='\n'.join(readme),
    long_description_content_type='text/x-rst',
    classifiers=["Development Status :: 7 - Inactive"],
    license='Apache Software License',
    license_files=("LICENSE",),
    install_requires=requires,
)