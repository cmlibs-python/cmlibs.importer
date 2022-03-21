import argparse
import os.path
import sys

from opencmiss.importer import ragpdata


def available_importers():
    return [
        ragpdata.identifier(),
    ]


def import_data(importer, inputs, working_directory):
    outputs = None
    if importer == ragpdata.identifier():
        outputs = ragpdata.import_data(inputs, working_directory)

    return outputs


def main():
    parser = argparse.ArgumentParser(description='Import data into OpenCMISS-Zinc.')
    parser.add_argument("-o", "--output", help='output directory.')
    parser.add_argument("-l", "--list", help="list available importers", action='store_true')

    args = parser.parse_args()
    if args.list:
        print("Available importers:")
        for id_ in available_importers():
            print(f" - {id_}")
    else:
        if args.output and not os.path.isdir(args.output):
            sys.exit(1)


if __name__ == "__main__":
    main()
