import logging
import filecmp
import tempfile
from pathlib import Path
import subprocess as sp

logger = logging.getLogger(__name__)

def cmp(a, b):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        tmpdir_a = tmpdir / 'a'
        tmpdir_b = tmpdir / 'b'
        tmpdir_a.mkdir()
        tmpdir_b.mkdir()
        pdf_to_png(a, tmpdir_a)
        pdf_to_png(b, tmpdir_b)
        logger.debug(f'diffing {a} and {b}')
        dircmp = filecmp.dircmp(tmpdir_a, tmpdir_b)
        if dircmp.diff_files or dircmp.left_only or dircmp.right_only:
            return True
        return False

def pdf_to_png(path, outdir):
    cmd = [
        'pdftoppm',
        '-png',
        path,
        outdir / path.stem
    ]
    logger.debug(f'converting {path} to png')
    cmds = sp.list2cmdline(cmd)
    logger.debug(f'running {cmds}')
    sp.check_output(cmd)

