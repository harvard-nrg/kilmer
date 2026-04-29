import sys
import json
import logging
from pathlib import Path
import subprocess as sp

from kilmer.git import clone
from kilmer.venv import venv
from kilmer.commons import path_with_repo
from kilmer.patches import patch_files, set_permissions

logger = logging.getLogger(__name__)

def setup(args):
    for branch in args.branches:
        url = args.config.find_one(f'$.{branch}.url')
        branch_name = args.config.find_one(f'$.{branch}.branch')
        branches_dir = args.config.find_one('$.outputs.branches')
        # clone the repository
        branch_dir = clone_repo(
            url,
            branch_name,
            branches_dir
        )
        # patch any files that need patching
        patch_dir = branch_dir.relative_to(branches_dir)
        patch_files(branch_dir, patch_dir)
        set_permissions(branch_dir, 'iProc_p4_sbatch_combined_ME.py', 0o755)
        # create iproc venv and install the current branch
        create_venv_and_install(
            branch_dir
        )
        # create a tedana venv and install requirements
        create_venv_and_install(
            branch_dir,
            name='.tedana',
            requirements='tedana-requirements.txt'
        )

def create_venv_and_install(d, name=None, requirements=None):
    outdir = venv(d, name=name, requirements=requirements)
    return outdir

def clone_repo(url, branch, base):
    outdir = path_with_repo(base, url, branch)
    clone(
        url,
        branch,
        outdir
    )
    return outdir
