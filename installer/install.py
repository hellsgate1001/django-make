"""Strangemother djangomaker.

This is an alpha - So a lot of items are missing to use.
Currently this does:
    + Pip wrapping and depencancy automation.
    + configutation parsing mapped to config/default.conf etc...
Current Not implemented:

Features: 
    + config fallthough - With fallthough of command-line/piping/config/user
    + logging with colors
    + alpha of a pip wrapper (easier api wrapper) - Currently install
    
Usage:
    install.py [options] [--] [<name>]
    install.py -h | --help
    
Arguments:
    <name>            Name of the application or project.
    <verbosity>       level of output for printing
    <email>           User register admin email address
    <database>        name of the database
    <file>            Name of the input configuration file

Options:
    -h --help                Show this screen.
    --version                Show version.
    -n --name=<name>         Name of the project [default: <name>]
    -a --admin               Admin name default will be the [default: user]
    -e --email               Admin email address
    -c --config=<file>       provide a configuration file for automation and 
                             silent installations
    -v --verbose             Say more [default: 1]
    -t --template            Collection path of the templating dir
                             [default: templates]
    -i --install             auto install the required packages without
    -w --wide-name           Use the provided NAME on dir, name, db-name
                             without specifying all individually.
                             prompt [default: False]
    -m --make-config         Write changes and complete to a file
                             for use later with --config [default: <name>.conf
    -q --quiet               Say less
    -s --sandbox             Do not allow external package requests [default: False]
    -p --proxy               Add a pip proxy string e.g 'http://user:pass@realm:port'
    -r --requirements        Provide a requirements file for package installs
    --db-engine              Which database Engine add 'postgresql_psycopg2', 
                             'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    --db-name                Name of the database. [default: <database>]
    --db-user                Database user for the application
    --db-password            The password of the database user
    --db-host                Databases accessible host [default: localhost]
    --db-port                Databases accessible post.
    -d --dir                 Install your project into a specified
                             directory, [default: ../<name>]
    --pip-install-option     Extra options required for pip as a 
                             string of commands (use like --pip-install-option="--install-
                             scripts=/usr/local/bin")
    
    
    
"""
# Default dependancies
import sys
import os
import pdb
from utils import pip_install, confirm
import re
import json
from pprint import pprint

arguments = None
parsed_config = {}

# These are some examples of configs you can edit.
configs = (
           ('default', 'config/default.conf',),
           ('dev', 'config/development.conf',),
           ('production', 'config/production.conf',),
        )

__version__ = 'v0.1 <ZZ>< Pi'

# A list of real imports for use with aut importing of required
# scripts
map_package = (
            ('termcolor', 'from termcolor import colored', ),
            ('docopt', 'from docopt import docopt', ),
            ('fabric', 'from fabric.api import settings, run', ),
            ('clint', 'from clint import resources', ),
            ('yolk', 'import yolk', ),
            # ('virtualenv', '',),
    )

# Contains a transient list of missing files. This will be updated
# at will by the script.
missing_packages = []

# Ensire the fundamental none core dependencies exist
try:
    print 'Checking core dependancies'
    import pip
    from docopt import docopt
except ImportError, ie:
    print """This installer cannot run without the following 
    packages docopt, pip Run the following commands:
    
    pip install docopt pip
    
    After this, all installs should be optionally automatic.
    ---
    """, ie
    sys.exit()

def arg(name):
    return arguments['--%s' % name]

def have(name):
    ''' simple check for the package return true or false'''
    if name in missing_packages: return False
    
    try:
        exec('import %s' %name)
        return True 
    except ImportError, ie:
        return False


# Log script The simplest for for use before advanced override
def log(*args, **kargs):
    a = [str(x) for x in args]
    color = kargs.get('color', None)
    s = ''. join(a)
    dangle_print = True if s.endswith('\,') else False
    
    s = s[:-2] if dangle_print else s
    
    if color is not None:
        try:
            try: from termcolor import colored
            except ImportError, ie: pip_install('termcolor')
             
            print colored(s, color=color),
            if not dangle_print:
                print ''
        except NameError, e:
            print "Print Error: '%s'" % e
            print s,
            if not dangle_print:
                print ''
    else: 
        print s

def get_arg_setting(name, default=None):
    '''Collect an argument from an argument dict formatted 
    for Docopts and (currently) variable name in the  <tag>
    format not the CAPS format.'''
    arg_name ='--%s' % name 
    if arg_name in arguments:
        n = arguments[arg_name]
        log('Found %s argument \'%s\'' % (arg_name, n), color='blue')
        reobj = re.compile("[<](.*)[>]", re.IGNORECASE)
        if reobj.search(n):
            log('Reading argument pointer %s' % n, color='blue')
            if n in arguments:
                val=arguments[n]
                log('Found %s = %s' % (n, val,),color='blue')
                if val == None:
                    print 'Retaining', val
                    return default
                return val
        else:
            log('%s isn\'t a pointer' % name)
        return n
    return default

def get_config_setting(field):
    global parsed_config
    if field in parsed_config:
        val = parsed_config[field]
        log('Parsed field %s = \'%s\'' % (field, val), color='blue')
        return val
    return None

def get_setting(field, prompt=None):
    '''Provide a setting using fallthough of
    command line arguments, config file settings, user input.'''
    global arguments
    # collect config from files.
    config_name = get_config_setting(field)
    
    # Fetch name from arguments passed
    name = get_arg_setting(field, config_name)
    
    # fetch piped
    val = name
    
    if prompt is None and name is None:
        prompt = 'Please provide configuration \'%s\': ' % (field)
        val = raw_input(prompt)
    return val
    
    

def install(exec_string, name):
    log('checking %s... \,' % name, color='yellow')
    try:
        exec(exec_string)
        file_location = ''
        try:
            exec('import %s\nfile_location= %s.__file__' % (name, name))
            log('%s location: %s' % (name, file_location) )
        except ImportError, ie:
            log("Could not check file locations. %s" % ie)
        if name in missing_packages:
            missing_packages.remove(name)
    except ImportError, e:
        log('Installing: \'%s\'' % exec_string, color='yellow')
        missing(name)
        ins = install_package(name)
        if ins:
            log('Installed %s' % name, color='green')
        else: 
            log('Package %s not installed' % name, color='red')
        return ins
    
    
def missing(name):
    '''Store a missing package'''
    log("Missing package: %s" % name, color='red')
    missing_packages.append(name)
    return missing_packages

    
def install_package(*args, **kargs):
    '''Provide a string, an iterable or pass values to the 
    *args. Each a url or endoint used by pip
    '''
    v = True
    for url in args:
        log('installing %s' % url, color='yellow')
        confirm('Would you like to install package \'%s\'' % url, True)
        v = pip_install(url)
        # To not have a horrible big in the future, if one package
        # fails the entire procedure reports False
    return v


def depend_on(name, callback, *args, **kargs):
    ''' Supply the package name of which
    the next functionality will depend upon.
    if the pakcage hasn't been indicated as collected, the
    install script will do it's best to install it.
    '''
    for x in map_package:
        if x[0] == name:
            log('Checking dependancy %s' % name, color='yellow')
            install(x[1], x[0])
    callback(*args, **kargs)


# Config parsing routines
def parse_config():
    global parsed_config
    o = {}
    for name, path in configs:
        # Loop though receiver objects.
        log('Parsing config file %s' % name, color='yellow')
        if os.path.exists(path):
            json_data=open(path)
            data = json.load(json_data)
            
            json_data.close()
            if data != '': 
                o.update(data)
            else: 
                log('config file %s is empty. Ignoring' % name, 
                    color='blue')
        else: log('Missing config file \'%s\': %s' % (name, path), 
                  color='red')    
    parsed_config.update(o)
    return parsed_config
    
def write_config(name, value):
    '''not implemented'''
    pass
        
def get_config():
    '''retrieve a config file either pipped, passed or default 
    file'''
    log('Running config', color='blue')
    return parse_config()

def confirm_with_setting(question, default=None, yesno=False,
                         lock=True):
    '''A confirmation question to the user, first interjected with
    local settings. Including Config or pipped.
    yesno is True if you would like a yes no question
    To stop the user from cancelling
    yesno: if the question should return True/False
    lock: The user cannot skip the question
    '''

def do_mysql(self):

    print "---"
    print "Read mysql data"
    
    
    u = get_setting('db_username')
    p = get_setting('db_password')
    db_name = get_setting('db_name')
    
    log('checking mysql (creating table if required)', color='yellow')
    ms = '''mysql -u%s -p%s -e "show databases; 
            create database if not exists %s"''' % (u, p, db_name)
    os.system(ms)
    
    ms = 'mysql -u%s -p%s -e "show databases like \'%s\'"' % (u,
                                                              p,
                                                              db_name)

def django_sync_database(self):
    inp = confirm('Continue to sync database?')
    if inp == False: sys.exit(0)
    os.system('cd %s;python manage.py syncdb' % path)
    os.system('cd %s;python manage.py migrate' % path)
    os.system('cd %s;python manage.py validate' % path)

def django_runserver():
    if inp == False: sys.exit(0)
    os.system('cd %s;python manage.py runserver 0.0.0.0:8008' % path)


## INSTALLATION ROUTINE
print "Performing install."
    
# Fetch the requirements.txt ? 
    # From pip, from config

def run_args():

    print 'run install'
    global arguments
    arguments = docopt(__doc__, version=__version__)
    config = depend_on('clint', get_config)
    
    log('Checking all dependancies', color='yellow')
    
    for pkg in map_package:
        install(pkg[1], pkg[0])
    
    make_database = get_setting('make_db')
    if make_database:
        do_mysql()
    
    django_sync_database()
    inp = confirm('run server?')
    

    
if __name__ == '__main__':
    depend_on('docopt', run_args)
    
    
    