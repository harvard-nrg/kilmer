import logging
import contextlib
import subprocess as sp
from pathlib import Path
from importlib.resources import files

logger = logging.getLogger(__name__)

def set_permissions(base, path, permissions):
    with contextlib.chdir(base):
        logger.info(f'chmod {path} to {permissions:#o}')
        try:
            Path(path).chmod(permissions)
        except FileNotFoundError:
            logger.info('version of iproc >= 4.0.1 being used, continuing')

def patch_files(base, patch_dir):
    logger.info(f'switching to {base}')
    with contextlib.chdir(base):
        for patch in locate_patches(patch_dir):
            logger.info(f'applying patch {patch} within {base}')
            cmd = [
                'patch',
                '-p0',
                '-i',
                patch
            ]
            sp.call(cmd)

def locate_patches(branchdir):
    ''' locate patch files in this module directory '''
    patchdir = files('kilmer.patches') / 'patches' / branchdir
    for patch in patchdir.rglob('*.patch'):
        yield patch

