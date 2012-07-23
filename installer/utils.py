    
from pip.commands.install import InstallCommand
from pip.locations import build_prefix, src_prefix
from pip.log import logger

class DictClass(object):

    def __init__(self, o):
        self.o = o
            
    def __getattr__(self, name):
        if name not in self.o:
            self.o[name] = None
        
        return self.o[name]

def confirm(prompt=None, resp=False, lock=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """
    
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if lock:
            if ans.lower() not in ['y', 'yes', 'ys', 'no', 'n']:
                print 'Please enter yes or no.'
                continue
            
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False
           
def pip_install(*args, **kargs):
    
    o = {'install_options': None, 
    'verbose': 0, 
    'index_url': 'http://pypi.python.org/simple/', 
    'target_dir': None, 
    'global_options': None, 
    'force_reinstall': None, 
    'default_vcs': '', 
    'ignore_installed': None, 
    'use_user_site': None, 
    'upgrade': None, 
    'requirements': [], 
    'log': None, 
    'no_index': False, 
    'no_download': None,
    'build_dir': build_prefix,
    'extra_index_urls': [], 
    'find_links': [], 
    'editables': [], 
    'mirrors': [], 
    'src_dir': src_prefix, 
    'download_cache': None, 
    'download_dir': None, 
    'no_install': None, 
    'use_mirrors': False, 
    'proxy': '', 'log_explicit_levels': False, 
    'exists_action': [], 
    'require_venv': False, 
    'no_input': False, 
    'quiet': 0, 
    'timeout': 15, 
    'skip_requirements_regex': '', 
    'log_file': '/home/jay/.pip/pip.log', 
    'ignore_dependencies': False
    }
    
    # oo = o.update(kargs)
    ins = InstallCommand()
    x= DictClass(o)
    
    def logger_consumer(rendered):
        print rendered
    
    logger.consumers.append((4, logger_consumer))
    
    val = ins.run(x, args)
    
    print 'return', val
    