import logging
import contextlib
import subprocess as sp
from pathlib import Path

logger = logging.getLogger(__name__)

def venv(d, name=None, requirements=None):
    ''' create a python venv within directory {d} '''
    if not name:
        name = '.venv'
    with contextlib.chdir(d):
        cwd = Path.cwd()
        venvdir = Path(name)
        if not venvdir.exists():
            logger.info(f'creating venv {name} in {d}')
            cmd = [
                'python3.11',
                '-m', 'venv',
                venvdir
            ]
            cmdstr = sp.list2cmdline(cmd)
            # create venv 
            logger.info(f'running: {cmdstr}')
            sp.call(cmd)
        # upgrade pip
        cmd = [
            venvdir / 'bin' / 'pip',
            'install',
            '--upgrade', 'pip'
        ]
        cmdstr = sp.list2cmdline(cmd)
        logger.info(f'running {cmdstr}')
        sp.call(cmd)
        if requirements:
            cmd = [
                venvdir / 'bin' / 'pip',
                'install',
                '-r', requirements
            ]
        else:
            cmd = [
                venvdir / 'bin' / 'pip',
                'install',
                '.'
            ]
        cmdstr = sp.list2cmdline(cmd)
        logger.info(f'running {cmdstr}')
        sp.call(cmd)
        return Path(cwd, name)
