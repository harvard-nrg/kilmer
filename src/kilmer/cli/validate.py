import re
import sys
import yaml
import json
import logging
import contextlib
from tqdm import tqdm
from pathlib import Path
from sortedcontainers import SortedDict

import kilmer.compare.pdf as pdf
import kilmer.compare.nifti as nifti
from kilmer.commons import path_with_repo

logger = logging.getLogger(__name__)

def validate(args):
    subject = args.subject
    results = Path(args.config.find_one('$.outputs.results'))
    left_url = args.config.find_one('$.left.url')
    left_branch = args.config.find_one('$.left.branch')
    right_url = args.config.find_one('$.right.url')
    right_branch = args.config.find_one('$.right.branch')

    left_dir = path_with_repo(results, left_url, left_branch)
    right_dir = path_with_repo(results, right_url, right_branch)

    # reverse the direction of comparison
    if args.reverse:
        left_dir, right_dir = right_dir, left_dir

    # add subject directory
    left_dir = left_dir / subject
    right_dir = right_dir / subject

    differences = dict()

    # compare nifti files
    validate = args.config.find_one('$.validation.nifti.validate', True)
    if validate:
        logger.info('validating all NIfTI files')
        patterns = args.config.find_one(
            '$.validation.nifti.exclude',
            default=list()
        )
        diff = compare_niftis(left_dir, right_dir, patterns)
        differences['nifti'] = diff

    # compare pdf files
    validate = args.config.find_one('$.validation.pdf.validate', True)
    if validate:
        logger.info('validating all PDF files')
        diff = compare_pdfs(left_dir, right_dir)
        differences['pdf'] = diff

    # save report
    logger.info(f'saving {args.output_file}')
    with open(args.output_file, 'w') as fo:
        suffix = args.output_file.suffix
        match suffix:
            case '.yaml' | '.yml':
                fo.write(yaml.safe_dump(differences, indent=2))
            case '.json':
                fo.write(json.dumps(differences, indent=2, default=str))
            case _:
                raise Exception(f'unrecognized output file suffix {suffix}')

def compare_pdfs(left_dir, right_dir):
    diffs = SortedDict()
    with contextlib.chdir(left_dir):
        files = Path().rglob('*.pdf')
        pbar = tqdm(list(files))
        errors = 0
        for left_file in pbar:
            pbar.set_description(f'{errors} errors')
            right_file = Path(right_dir, left_file)
            left_file = left_file.absolute()
            right_file = right_file.absolute()
            logger.debug(f'comparing {left_file} to {right_file}')
            # compare left and right nifti files
            mtime = pdf.cmp(left_file, right_file)
            if mtime:
                errors += 1
                diffs[mtime] = str(left_file), str(right_file)
    return dict(diffs)

def compare_niftis(left_dir, right_dir, patterns):
    diffs = SortedDict()
    patterns = [re.compile(x) for x in patterns]
    with contextlib.chdir(left_dir):
        files = Path().rglob('*.nii.gz')
        pbar = tqdm(list(files))
        errors = 0
        for left_file in pbar:
            pbar.set_description(f'{errors} errors')
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
                errors += 1
                diffs[mtime] = str(left_file), str(right_file)
    return dict(diffs)

def compare_two_niftis(left, right):
    ''' compare two nifti files and return the left file mtime if different '''
    if not nifti.cmp(left, right):
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

