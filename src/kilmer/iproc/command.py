import subprocess as sp

def build_command(cfg, stage, bids=None):
    ''' build an iProc command '''
    cmd = [
        './iProc.py',
        '--config', cfg,
        '--stage', stage,
        '--executor', 'local'
    ]
    # add bids path if one was passed in
    if bids:
        cmd.extend([
            '--bids',
            bids
        ])
    cmd.append('--debug')
    cmds = sp.list2cmdline(cmd)
    return cmd,cmds

