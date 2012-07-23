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