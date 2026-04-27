import sys
import json
import logging
from pathlib import Path
import subprocess as sp

from kilmer.git import clone
from kilmer.venv import venv
from kilmer.commons import path_with_repo
from kilmer.patches import patch

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
        patch(branch_dir, 'modules_rocky8.sh')
        # create a venv and install the branch
        create_venv_and_install(
            branch_dir
        )

def create_venv_and_install(d):
    outdir = venv(d)
    return outdir

def clone_repo(url, branch, base):
    outdir = path_with_repo(base, url, branch)
    clone(
        url,
        branch,
        outdir
    )
    return outdir
