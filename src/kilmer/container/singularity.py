import subprocess as sp

def wrap_command(cmd, wrapper, mounts, app=None, pwd=None):
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
    # add bind mounts if any were specified
    for dst,src in iter(mounts.items()):
        scmd.extend([
            '--bind', f'{src}:{dst}'
        ])
    # add app argument if one was specified
    if app:
        scmd.extend([
            '--app', app
        ])
    scmd.append(str(wrapper))
    scmd.append(cmd)
    scmds = sp.list2cmdline(scmd)
    return scmd,scmds
    
