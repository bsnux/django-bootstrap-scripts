django-bootstrap-scripts
========================

Scripts for bootstrapping your Django projects.

Minimum Django version for these scripts is **1.4**.

Requirements
------------

* Fabric
* Django >= 1.4
* django-extensions

Usage
-----

1. Clone this project
2. Install this package:

    `$ cd django-bootstrap-scripts`

    `$ python setup.py install`

3. Create your Django project with a *fabfile.py* with this content:

    `from bootstrap.fabfile_dist import *`

4. Optional: You can use your own *fabfile* per project:

    * Add following lines to your *fabfile.py*:

            try:
                from fabfile_project import *
            except:
                pass

    * Create a new *fabfile_project.py* and use it as your regular *fabfile.py*

Commands
---------

See a complete list executing:

    $ fab -l
