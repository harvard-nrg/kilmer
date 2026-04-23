import subprocess as sp

def wrap_command(cmd, wrapper, mounts, pwd=None):
    ''' wrap command {cmd} in a singularity run command '''
    scmd = [
        'singularity',
        'run'
    ]
    # override the working directory within the container
    if pwd:
        scmd.extend([
            '--pwd', str(pwd)
        ])
    # specify any bind mounts
    for a,b in iter(mounts.items()):
        scmd.extend([
            '--bind', f'{a}:{b}'
        ])
    scmd.append(str(wrapper))
    scmd.append(cmd)
    scmds = sp.list2cmdline(scmd)
    return scmd,scmds
    
