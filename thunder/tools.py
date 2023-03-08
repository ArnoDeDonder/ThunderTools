import getpass
import socket


def get_shell_type():
    try:
        ipy_str = str(type(get_ipython()))
        if 'zmqshell' in ipy_str:
            return 'JUPYTER'
        if 'terminal' in ipy_str:
            return 'IPYTHON'
    except:
        return 'TERMINAL'
    
    
def get_system_user():
    return getpass.getuser()


def get_system_name():
    return socket.gethostname()