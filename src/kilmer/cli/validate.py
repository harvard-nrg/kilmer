import re
import sys
import yaml
import json
import filecmp
import logging
import contextlib
from pathlib import Path
from collections import defaultdict
from sortedcontainers import SortedDict

import kilmer.compare.nifti as nifti
from kilmer.commons import path_with_repo

logger = logging.getLogger(__name__)

def validate(args):
    subject = args.subject
    results = Path(args.config['outputs']['results'])
    left_url = args.config['left']['url']
    left_branch = args.config['left']['branch']
    right_url = args.config['right']['url']
    right_branch = args.config['right']['branch']

    left_dir = path_with_repo(results, left_url, left_branch)
    right_dir = path_with_repo(results, right_url, right_branch)

    # reverse the direction of comparison
    if args.reverse:
        left_dir, right_dir = right_dir, left_dir

    # compare all nifti files
    differences = dict()
    patterns = args.config['validation']['nifti']['exclude']
    diff = compare_niftis(patterns, left_dir, right_dir)
    differences['nifti'] = diff

    # save report
    with open(args.output_file, 'w') as fo:
        suffix = args.output_file.suffix
        match suffix:
            case '.yaml' | '.yml':
                fo.write(yaml.safe_dump(differences, indent=2))
            case '.json':
                fo.write(json.dumps(differences, indent=2, default=str))
            case _:
                raise Exception(f'unrecognized output file suffix {suffix}')

def compare_niftis(patterns, left_dir, right_dir):
    diffs = SortedDict()
    patterns = [re.compile(x) for x in patterns]
    with contextlib.chdir(left_dir):
        for left_file in Path().rglob('*.nii.gz'):
            # exclude any files matching provided patterns
            if exclude(left_file.absolute(), patterns):
                continue
            # expand both files to absolute paths
            right_file = Path(right_dir, left_file)
            left_file = left_file.absolute()
            right_file = right_file.absolute()
            logger.debug(f'comparing {left_file} to {right_file}')
            # compare left and right nifti files
            mtime = compare_two_niftis(left_file, right_file)
            # using a SortedDict keyed on mtime keeps the files sorted
            if mtime:
                diffs[mtime] = str(left_file), str(right_file)
    return dict(diffs)

def compare_two_niftis(left, right):
    ''' compare two nifti files and return the left file mtime if different '''
    if not nifti.cmp(left, right):
        logger.warning(f'{left} != {right}')
        mtime = left.stat(follow_symlinks=False).st_mtime
        return mtime
    logger.debug(f'{left} == {right}')
    return False

def exclude(s, patterns):
    ''' helper to exclude files based on regular expression '''
    s = str(s)
    for pattern in patterns:
        if pattern.match(s):
            return True
    return False

