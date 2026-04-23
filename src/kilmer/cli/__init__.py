import yaml
import logging
from pathlib import Path
from .setup import setup
from .launch import launch
from .validate import validate
from argparse import ArgumentParser

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', type=Path, required=True)
    subparser = parser.add_subparsers(dest='mode')
    setup_parser = subparser.add_parser('setup')
    setup_parser.add_argument('-b', '--branches', nargs='+', 
        default=['left', 'right'], choices=['left', 'right'])
    launch_parser = subparser.add_parser('launch')
    launch_parser.add_argument('-s', '--subject', required=True)
    launch_parser.add_argument('-m', '--mock', nargs='+', default=[],
        choices=['freesurfer'])
    launch_parser.add_argument('-b', '--branch', required=True)
    validate_parser = subparser.add_parser('validate')
    validate_parser.add_argument('-s', '--subject', required=True)
    validate_parser.add_argument('-r', '--reverse', action='store_true')
    validate_parser.add_argument('-o', '--output-file', type=Path,
        default='report.json')
    args = parser.parse_args()

    with open(args.config, 'rb') as fo:
        args.config = yaml.load(fo, Loader=yaml.SafeLoader)

    match args.mode:
        case 'setup':
            setup(args)
        case 'launch': 
            launch(args)
        case 'validate':
            validate(args)
