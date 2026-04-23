import subprocess as sp

def build_command(cfg, stage):
    ''' build an iProc command '''
    cmd = [
        './iProc.py',
        '--config', cfg,
        '--stage', stage,
        '--executor', 'local',
        '--debug'
    ]
    cmds = sp.list2cmdline(cmd)
    return cmd,cmds

