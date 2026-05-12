import logging
import filecmp
import tempfile
from pathlib import Path
import subprocess as sp
import kilmer.container as container

logger = logging.getLogger(__name__)

def cmp(a, b, wrapper=None):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        tmpdir_a = tmpdir / 'a'
        tmpdir_b = tmpdir / 'b'
        tmpdir_a.mkdir()
        tmpdir_b.mkdir()
        pdf_to_png(a, tmpdir_a, wrapper=wrapper)
        pdf_to_png(b, tmpdir_b, wrapper=wrapper)
        logger.debug(f'diffing {a} and {b}')
        dircmp = filecmp.dircmp(tmpdir_a, tmpdir_b)
        if dircmp.diff_files or dircmp.left_only or dircmp.right_only:
            return True
        return False

def pdf_to_png(path, outdir, wrapper=None):
    cmd = [
        'pdftoppm',
        '-png',
        path,
        outdir / path.stem
    ]
    cmds = sp.list2cmdline(cmd)
    # wrap in container if specified
    if wrapper:
        cmd,cmds = container.wrap_command(
            cmd,
            wrapper,
            mode='exec',
            mounts={
                path: path,
                outdir: outdir
            }
        )
    logger.debug(f'converting {path} to png')
    logger.debug(f'running {cmds}')
    sp.check_output(cmd)

