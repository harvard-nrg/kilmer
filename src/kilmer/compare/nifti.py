import logging
import filecmp

logger = logging.getLogger(__name__)

def cmp(a, b):
    ''' 
    Compare two NIfTI files {a} and {b} and return True if they are the same
    or False if they are different.

    If both input files are symlinks, return True if both links point to the 
    same file. If both input files are real files, return True if both files 
    exist and contents are identical.
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
    return filecmp.cmp(a, b, shallow=False)
