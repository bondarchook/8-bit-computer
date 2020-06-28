import os
import argparse
import sys
from pathlib import Path

from generator.MicrocodeGenerator import MicrocodeGenerator
from microcode.MicrocodeSpecificationLoader import MicrocodeSpecificationLoader
from microcode.MicrocodeSpecificationValidator import MicrocodeSpecificationValidator

argument_parser = argparse.ArgumentParser()

argument_parser.add_argument("-s", "--specification", required=True, help="microcode specification")
argument_parser.add_argument("-d", "--directory", required=True, help="output directory")
argument_parser.add_argument("-n", "--name", required=False, help="ROM base name")
args = vars(argument_parser.parse_args())

print('\nMicrocode generator v1.0.\n')

spec_filename = Path(args['specification']).resolve()
out_directory = Path(args['directory']).resolve()
base_name = args['name']

if not os.path.exists(spec_filename):
    sys.exit(f'Specification file not found: {spec_filename}')

if not os.path.exists(out_directory):
    os.makedirs(out_directory, exist_ok=True)

if not base_name:
    base_name = "rom"

print(f'Specification file: {spec_filename}')
print(f'Output directory  : {out_directory}')
print(f'ROM name          : {base_name}')
print('\n')

specification = MicrocodeSpecificationLoader(spec_filename)
specification.load()

MicrocodeSpecificationValidator.validate(specification.microcode_specification)

generator = MicrocodeGenerator(out_directory, base_name, specification.microcode_specification)
generator.generate()

print('\nDone.')
