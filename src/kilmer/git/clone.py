import logging
import subprocess as sp

logger = logging.getLogger(__name__)

def clone(url, branch, outdir):
    ''' clone a specific branch from a git repository '''
    if outdir.exists():
        return outdir
    cmd = [
        'git',
        'clone',
        '--single-branch',
        '--branch', branch,
        url,
        outdir
    ]
    cmdstr = sp.list2cmdline(cmd)
    logger.info(f'running {cmdstr}')
    sp.call(cmd)
    return outdir
