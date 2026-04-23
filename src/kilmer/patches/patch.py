import logging
import contextlib
import subprocess as sp
from pathlib import Path
from importlib.resources import files

logger = logging.getLogger(__name__)

def patch(base, path):
    ''' patch file `path` starting from base directory `base` '''
    path = Path(path)
    with contextlib.chdir(base):
        # locate the patch file to apply
        patchfile = locate_patch_file(path)
        # apply the patch using the patch utility
        logger.info(f'applying patch {patchfile} within {base}')
        cmd = [
            'patch',
            path,
            patchfile
        ]
        sp.call(cmd)

def locate_patch_file(path):
    ''' locate a patch file in this module directory '''
    return files('kilmer.patches').joinpath(path.name + '.patch')

