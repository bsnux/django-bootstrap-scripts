import os
from distutils.core import setup

license_text = open('LICENSE.txt').read()

setup(
    name = 'django-bootstrap-scripts',
    version = '0.9',
    url = 'http://github.com/bsnux/django-bootstrap-scripts',
    author = 'Arturo Fernandez',
    author_email = 'arturo@bsnux.com',
    license = license_text,
    data_files=[('', ['LICENSE.txt'])],
    description = 'Scripts for bootstrapping Django projects',
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content']
)
