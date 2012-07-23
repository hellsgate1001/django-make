django-make
===========

Django make will apply a set of build scripts for getting a django
application hosted from an empty box to production.

Yep, another build script with current features:

+ Installer folder / install.py
    
    An app to run all the boilerplate required for a new project.
    + project creation much like django-admin startproject
        + basic apps installed including:
            + south
            + admin
            + django-admin-tools
            + django-cms
            + django-extensions
            + django-debug-toolbar
            
    + auto PIP, installing all dependencies
    + Initial proect templating 
    + database setup, sync, migrations, supporting:
        + mysql
        + sqlite3 
        
    + deployment to one/all of the following:
        + WSGI
        + Dev (with dev media setup)
        + cherrypy
        
Why am I building this:

I'm a python developer - go figure. I love Django but I don't love 
deployments. I must deploy offsite, of which is handled by an engineer; of which in turn
is handled by myself over a remote desktop or a camera pointing 
at a CRT with me trying to yelp over the sound of background servers
220 miles away. A this point they don't know what a python is or what the 
where f*ck django has his guitar. Couple that with my eggs, a pip bundle, 
some south migrations and a git in the middle, it's no wonder why 
my collegues think I'm a foreign language. 

Let's make it easy - both for me as a developer wanting to have a 
ready site in minutes.

Great for:

+ Testbed websites for creating sites as quick as you think of them.
+ Personal deployement strategy for new websites.
+ Creating installation routines for remote deployment
+ Creating installers for third-party deployment
+ All apps are made in the same manor. 
+ Never miss a step. 

Toolset:
    
    # Pip install
    >>> from utils import *
    >>> pip_install('yolk')
    # installs yolk
   
    # Confirm dialog
    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True
    
    # DictClass for turning objects into class style
    >>> x = DictClass({'name': 'Fishy', 'word':'w00t!'})
    >>> x.name
    'Fishy'
    
    # Get Setting functionality. Providing full waterfall fallthough
    # of values using: Config File JSON, argument settings, user input
    >>> name = get_setting('site_name', prompt="What's the site name? ")
    # Fallthrough
    'project name'
    
    
    
Config files are JSON mapped variables using variable names
matching arguments and application settings.
    
    # Supply tuple, tuple of configs.
    >>> configs = (
               ('default', 'config/default.conf',),
               ('dev', 'config/development.conf',),
               ('production', 'config/production.conf',),
            )
    >>> parse_config()
    {} # config object of all settings
    

Library handling - for matching and collecting using PIP missing 
packages.
Map packages is a working progress paradim; supply the PIP 
package and the import string required for required functionality
off the application.
On initial script load and install 

    # A list of real imports for use with aut importing of required
    # scripts
    >>> map_package = (
            ('termcolor', 'from termcolor import colored', ),
            ('docopt', 'from docopt import docopt', ),
            ('fabric', 'from fabric.api import settings, run', ),
            ('clint', 'from clint import resources', ),
            ('yolk', 'import yolk', ),
    )

    # If package is installed
    >>> have('yolk')
    True # False
    
