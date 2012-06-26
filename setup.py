from distutils.core import setup

license_text = open('LICENSE.txt').read()

VERSION = __import__("bootstrap").__version__

setup(
    name = 'django-bootstrap-scripts',
    version = VERSION,
    url = 'http://github.com/bsnux/django-bootstrap-scripts',
    author = 'Arturo Fernandez',
    author_email = 'arturo@bsnux.com',
    license = license_text,
    packages = ['bootstrap'],
    data_files=[('', ['LICENSE.txt'])],
    description = 'Scripts for bootstrapping Django projects',
    install_requires=[
        'Fabric==1.4.2',
        'django-extensions==0.9',
    ],
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content']
)
