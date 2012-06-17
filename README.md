django-bootstrap-scripts
========================

Scripts for bootstrapping your Django projects.

Minimum Django version for these scripts is **1.4**.

Requirements
------------

* Django >= 1.4
* Fabric
* django-extensions

Commands
---------

* **ini_project**: Create static (*img/*, *js/* *css/*), templates and media directories and set different variables for them.

* **show\_create\_db**: Display SQL sentences for creating an empty database for MySQL and PostgreSQL.

* **install_req**: Install all required Django packages reading a requirements files. *pip* is required.

* **create\_req\_file**: Create a requirements file for *pip*.

* **generate_static**: Run *collectstatic* and *compress* Django commands.

* **get_yui**: Download YUI compressor library.

* **gen_key**: Generate a Django secret key.

* **set\_fake\_pw**: Generate fake passwords for your users.
