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
    results = Path(args.config.find_one('$.outputs.results'))
    wrapper = Path(args.config.find_one('$.containers.wrapper'))
    stages = args.config.find_one('$.iproc.stages')

    swdir = path_with_repo(branches, url, branch_name)
    outdir =  path_with_repo(results, url, branch_name)
    outdir = outdir / subject
    outdir.mkdir(parents=True, exist_ok=True)
    indir = datasets

    # path to the iProc config file for the current subject
    cfg = Path('/input', subject, 'subject_lists', f'{subject}.cfg')

    # extract any mock data to the output directory
    for m in args.mock:
        mock(datasets, subject, outdir, m)

    # run iProc for all specified stages
    for stage in stages:
        # build the iProc command
        cmd,cmdstr = iproc.build_command(cfg, stage=stage)
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
        case _:
            raise Exception(f'unrecognized mock {mock}')

def extract_mock_freesurfer(archive, outdir, subject):
    ''' Extract mock FreeSurfer data '''
    basedir = outdir / subject
    basedir.mkdir(parents=True, exist_ok=True)
    fsdir = basedir / 'fs'
    if fsdir.exists():
        logger.info(f'mock data already extracted {fsdir}')
        return
    with contextlib.chdir(basedir):
        logger.info(f'extracting {archive} to {basedir}')
        with tarfile.open(archive, 'r:gz') as tf:
            tf.extractall(filter='fully_trusted')

