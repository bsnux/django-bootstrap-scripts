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

3. Create your Django project with a *fabfile* with this content:

    `from bootstrap import fabfile`


Commands
---------

See a complete list executing:

    $ fab -l
