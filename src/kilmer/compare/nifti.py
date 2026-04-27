import logging
import filecmp
import subprocess as sp

logger = logging.getLogger(__name__)

def cmp(a, b, try_zdiff=True):
    ''' 
    Compare two NIfTI files {a} and {b} and return True if they are the same
    or False if they are different.

    If both input files are symlinks, return True if both links point to the 
    same file. If both input files are real files, return True if both files 
    exist and contents are identical.

    If filecmp says the files are different, pass try_zdiff=True to test files
    equality using zdiff.
    '''
    if a.is_symlink() and b.is_symlink():
        a = a.readlink()
        b = b.readlink()
        if a == b:
            return True
        return False
    if not a.exists():
        logger.warning(f'file not found {a}')
        return False
    if not b.exists():
        logger.warning(f'file not found {b}')
        return False
    result = filecmp.cmp(a, b, shallow=False)
    if not result and try_zdiff:
        return zdiff(a, b)
    return result

def zdiff(a, b):
    ''' run zdiff '''
    cmd = [
        'zdiff',
        a,
        b
    ]
    cmds = sp.list2cmdline(cmd)
    logger.debug(f'running {cmds}')
    returncode = sp.call(cmd, stdout=sp.DEVNULL)
    if returncode == 0:
        return True
    return False

