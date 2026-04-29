import logging
import pandas as pd
import subprocess as sp
import kilmer.iproc as iproc

logger = logging.getLogger(__name__)

def build_commands(scanlist, tasklist, resolution, outdir):
    for scan in iproc.get_multiecho_scans(scanlist, tasklist):
        sub = scan['SUBJID']
        ses = scan['SESSION_ID']
        scannum = scan['BLD']
        task = scan['TYPE']
        yield build_command(sub, ses, task, scannum, 'MNI', resolution, outdir)
        yield build_command(sub, ses, task, scannum, 'NAT', resolution, outdir)

def build_command(sub, ses, task, run, space, resolution, datadir):
    cmd = [
        'python3',
        'run_tedana.py',
        '--sub', sub,
        '--ses', ses,
        '--task', task,
        '--run', str(run),
        '--mridatadir', datadir,
        '--outname', 'tedana',
        '--space', space,
        '--resolution', resolution
    ]
    cmds = sp.list2cmdline(cmd)
    return cmd,cmds

