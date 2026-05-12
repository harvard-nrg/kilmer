import subprocess as sp

def wrap_command(cmd, wrapper, mounts, mode='run', app=None, pwd=None):
    ''' wrap command {cmd} in a singularity run command '''
    scmd = [
        'singularity',
        mode
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
    # append command to run
    match cmd:
        case list():
            scmd.extend(cmd)
        case str():
            scmd.append(cmd)
        case _:
            raise Exception(f'unexpected command type: {cmd}')
    scmds = sp.list2cmdline(scmd)
    return scmd,scmds
    
