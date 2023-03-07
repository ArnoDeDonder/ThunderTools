def get_shell_type():
    try:
        ipy_str = str(type(get_ipython()))
        if 'zmqshell' in ipy_str:
            return 'JUPYTER'
        if 'terminal' in ipy_str:
            return 'IPYTHON'
    except:
        return 'TERMINAL'