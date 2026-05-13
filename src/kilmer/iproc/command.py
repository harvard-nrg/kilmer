import subprocess as sp

def build_command(cfg, stage, overwrite=False, bids=None):
    ''' build an iProc command '''
    cmd = [
        './iProc.py',
        '--config', cfg,
        '--stage', stage,
        '--executor', 'local'
    ]
    # pass overwrite argument if requested
    if overwrite:
        cmd.append('--overwrite')
    # add bids path if one was passed in
    if bids:
        cmd.extend([
            '--bids',
            str(bids)
        ])
    cmd.append('--debug')
    cmds = sp.list2cmdline(cmd)
    return cmd,cmds

