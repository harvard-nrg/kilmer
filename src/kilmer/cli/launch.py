import sys
import tarfile
import logging
import contextlib
from pathlib import Path
import subprocess as sp

import kilmer.iproc as iproc
import kilmer.container as container
from kilmer.commons import path_with_repo

logger = logging.getLogger(__name__)

def launch(args):
    subject = args.subject
    branch = args.branch
    url = args.config.find_one(f'$.{branch}.url')
    branch_name = args.config.find_one(f'$.{branch}.branch')
    branches = Path(args.config.find_one('$.outputs.branches'))
    datasets = Path(args.config.find_one('$.inputs.datasets'))
    stages = args.config.find_one('$.iproc.stages')
    wrapper = Path(args.config.find_one('$.containers.wrapper'))
    if args.bids:
        results = Path(args.config.find_one('$.outputs.results.bids'))
    else:
        results = Path(args.config.find_one('$.outputs.results.xnat'))

    swdir = path_with_repo(branches, url, branch_name)
    outdir =  path_with_repo(results, url, branch_name)
    outdir = outdir / subject
    outdir.mkdir(parents=True, exist_ok=True)
    indir = datasets
    bidsdir = None

    # path to the iProc config file for the current subject
    cfg = Path('/input', subject, 'subject_lists', f'{subject}.cfg')

    # extract bids data if user passed --bids
    if args.bids and 'bids' not in args.mock:
        bidsdir = Path('/output', subject, 'BIDS')
        args.mock.append('bids')

    # extract any mock data to the output directory
    for m in args.mock:
        mock(datasets, subject, outdir, m)

    # run iProc for all specified stages
    for stage in stages:
        # build the iProc command
        cmd,cmdstr = iproc.build_command(cfg, stage=stage, bids=bidsdir)
        # wrap the iProc command in a container
        cmd,cmdstr = container.wrap_command(
            cmdstr,
            wrapper,
            pwd=swdir,
            mounts={
                '/n':'/n',
                indir: '/input',
                outdir: '/output'
            }
        )
        # run the command
        logger.info(f'running {cmdstr}')
        sp.check_output(cmd)

def mock(datasets, subject, outdir, mock):
    ''' Extract mock data '''
    archive = datasets / subject / 'mocks' / f'{mock}.tar.gz'
    match mock:
        case 'freesurfer':
            extract_mock_freesurfer(archive, outdir, subject)
        case 'bids':
            extract_mock_bids(archive, outdir, subject)
        case _:
            raise Exception(f'unrecognized mock {mock}')

def extract_mock_bids(archive, outdir, subject):
    ''' Extract mock BIDS data '''
    basedir = outdir / subject
    basedir.mkdir(parents=True, exist_ok=True)
    destdir = basedir / 'BIDS'
    if destdir.exists():
        logger.info(f'mock data already extracted to {destdir}')
        return
    with contextlib.chdir(basedir):
        logger.info(f'extracting {archive} to {basedir}')
        with tarfile.open(archive, 'r:gz') as tf:
            tf.extractall(filter='fully_trusted')

def extract_mock_freesurfer(archive, outdir, subject):
    ''' Extract mock FreeSurfer data '''
    basedir = outdir / subject
    basedir.mkdir(parents=True, exist_ok=True)
    fsdir = basedir / 'fs'
    if fsdir.exists():
        logger.info(f'mock data already extracted to {fsdir}')
        return
    with contextlib.chdir(basedir):
        logger.info(f'extracting {archive} to {basedir}')
        with tarfile.open(archive, 'r:gz') as tf:
            tf.extractall(filter='fully_trusted')

