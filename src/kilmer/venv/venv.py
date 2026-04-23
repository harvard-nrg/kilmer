import logging
import contextlib
import subprocess as sp
from pathlib import Path

logger = logging.getLogger(__name__)

def venv(d, install=True):
    ''' create a python venv named .venv within directory {d} '''
    with contextlib.chdir(d):
        cwd = Path.cwd()
        venvd = Path('.venv')
        if not venvd.exists():
            logger.info(f'creating .venv in {d}')
            cmd = [
                'python3.11',
                '-m', 'venv',
                str(venvd)
            ]
            cmdstr = sp.list2cmdline(cmd)
            # create venv 
            logger.info(f'running: {cmdstr}')
            sp.call(cmd)
        # upgrade pip
        cmd = [
            '.venv/bin/pip',
            'install',
            '--upgrade', 'pip'
        ]
        cmdstr = sp.list2cmdline(cmd)
        logger.info(f'running {cmdstr}')
        sp.call(cmd)
        if install:
            # install the current python package
            cmd = [
                '.venv/bin/pip',
                'install',
                '.'
            ]
            cmdstr = sp.list2cmdline(cmd)
            logger.info(f'running {cmdstr}')
            sp.call(cmd)
        return Path(cwd, '.venv')
