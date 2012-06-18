import os
import fileinput
import shutil
from fabric.api import local, task, cd, run, env
from fabric.colors import red, green

env.hosts = ['bsnux.com']
env.user = 'bsnux'

code_dir = '/home/bsnux/webapps/'

@task
def ini_project(name, yui_file='./jars/yui.jar'):
    """
    fab ini_project:name=myproject
    """
    settings_file = name + '/settings.py'
    # Copy original 'settings.py' before starting, just in case
    shutil.copy2(settings_file, settings_file + ".original")
    # Replacing important variables
    for line in fileinput.input(settings_file, inplace=1):
        if line.startswith('MEDIA_URL = '):
            cad = "MEDIA_URL = '/media/'"
            print(line.replace(line, cad))
        elif line.startswith('# Django settings'):
            cad = "import os\nPROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))"
            print(line)
            print(cad)
        elif line.startswith('MEDIA_ROOT = '):
            cad = "MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')"
            print(line.replace(line, cad))
        elif line.startswith('STATIC_ROOT = '):
            cad = "STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_collected/')"
            print(line.replace(line, cad))
        elif line.startswith('STATICFILES_DIRS = ('):
            cad = "\tos.path.join(PROJECT_ROOT, 'static/'),"
            print(line)
            print(cad)
        elif line.startswith('TEMPLATE_DIRS = ('):
            cad = "\tos.path.join(PROJECT_ROOT, 'templates/'),"
            print(line)
            print(cad)
        elif line.startswith('TIME_ZONE = '):
            cad = "TIME_ZONE = 'Europe/Madrid'"
            print(line.replace(line, cad))
        elif line.find("'django.contrib.staticfiles.finders.AppDirectoriesFinder'") != -1:
            print(line)
            print("\t'compressor.finders.CompressorFinder',")
        elif line.find("'django.contrib.staticfiles'") != -1:
            print(line)
            print("\t'compressor',")
        else:
            print line,
    # Deleting lines with comments
    for line in fileinput.input(settings_file, inplace=1):
        if not line.startswith('#'):
            print line,
    # Adding 'compressor' configuration
    f = open(settings_file, 'a')
    f.write("\nCOMPRESS_YUI_BINARY = '{0}'\n".format(yui_file))
    f.write('\nCOMPRESS_JS_FILTERS = [\n')
    f.write("\t'compressor.filters.yui.YUIJSFilter',\n")
    f.write(']\n')
    f.write('\nCOMPRESS_CSS_FILTERS = [\n')
    f.write("\t'compressor.filters.yui.YUICSSFilter',\n")
    f.write(']\n')
    f.close()
    # Creating static, media and templates files
    os.mkdir('{0}/static'.format(name))
    os.mkdir('{0}/static/js'.format(name))
    os.mkdir('{0}/static/css'.format(name))
    os.mkdir('{0}/static/img'.format(name))
    os.mkdir('{0}/static_collected'.format(name))
    os.mkdir('{0}/media'.format(name))
    os.mkdir('{0}/templates'.format(name))

@task
def show_create_db(engine, name):
    """
    fab show_create_db:mysql,dbname
    """
    if engine == 'mysql':
        create_str = 'CREATE DATABASE {0} DEFAULT CHARACTER SET utf8;'.format(name)
        per_str = "GRANT ALL PRIVILEGES ON {0}.* TO '{0}'@'localhost' IDENTIFIED BY '{0}';".format(name)
    elif engine == 'postgresql':
       create_str = "CREATE ROLE {0} LOGIN ENCRYPTED PASSWORD '{0}' NOINHERIT VALID UNTIL '{0}'".format(name)
       per_str = "CREATE DATABASE {0} WITH ENCODING='UTF8' OWNER={0};".format(name)
    else:
        print(red('Error: Use mysql or postgresql'))
    if engine == 'mysql' or engine == 'postgresql':
        print(green('Execute these commands:'))
        print(create_str)
        print(per_str)

@task
def install_req():
    local('pip install -r requirements/project.txt')

@task
def create_req_file():
    local('pip freeze > requirements/project.txt')

@task
def ls_remote():
    with cd(code_dir):
        run('ls -l')

@task
def generate_static():
    local('python manage.py collectstatic --noinput && python manage.py compress --force')

@task
def get_yui(version='2.4.7', target='./jars/'):
    import urllib
    url = 'http://yui.zenfs.com/releases/yuicompressor/yuicompressor-{0}.zip'.format(version)
    urllib.urlretrieve (url, '{0}/yuicompressor-{1}.zip'.format(target, version))

@task
def gen_key():
    """
    Generates a new Django secret key
    """
    local('python manage.py generate_secret_key')

@task
def set_fake_pw():
    """
    Reset all use passwords to a fake value
    """
    local('python manage.py set_fake_passwords')
