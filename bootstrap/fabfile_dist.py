import os
import fileinput
import shutil
import time
from fabric.api import local, task, cd, run, env, get, lcd
from fabric.colors import red, green

#-------
# Tasks
#--------
@task
def ls_remote():
    """
    List remote default directory
    Usage: fab ls_remote -H <host> -u <user>
    """
    with cd('.'):
        run('ls -l')

@task
def create_project(name='myproject', app='main'):
    """
    Create a project with a default application
    """
    local('django-admin.py startproject {0}'.format(name))
    with lcd(name):
        local('python manage.py startapp {0}'.format(app))

@task
def ini_project(name, yui_file='./jars/yui.jar'):
    """
    Set different variables, create static directories and configure compressor
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
            print("\t'compressor',\n\t'django_extensions',")
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
    Usage: fab show_create_db:mysql,dbname
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
    """
    Install all required Django packages reading a requirement file
    """
    local('pip install -r requirements/project.txt')

@task
def create_req_file():
    """
    Create a requirements file for pip
    """
    local('pip freeze > requirements/project.txt')

@task
def generate_static():
    """
    Run collectstatic and compress Django commands
    """
    local('python manage.py collectstatic --noinput && python manage.py compress --force')

@task
def get_yui(version='2.4.7', target='./jars/'):
    """
    Download YUI compressor library
    """
    yui_file = 'http://yui.zenfs.com/releases/yuicompressor/yuicompressor-{0}.zip'.format(version)
    yui_dest = '{0}/yuicompressor-{1}.zip'.format(target, version)
    download_file(yui_file, yui_dest)

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

@task
def backup_mysql(name, user, passwd, dest_dir='/tmp/'):
    """
    Backup your MysQL database and save it to your local machine
    """
    timestamp = int(time.time())
    dest_file = '{0}{1}-{2}.sql'.format(dest_dir, name, timestamp)
    cmd = 'mysqldump {0} -u {1} -p{2} > {3}'.format(name,
                                                    user,
                                                    passwd,
                                                    dest_file)
    run(cmd)
    get(dest_file)

@task
def del_pyc():
    """
    Delete *.pyc of your project
    """
    local('find . -name \*.pyc | xargs rm')

@task
def create_gmail_file(f='/tmp/google.csv'):
    """
    Create a csv file importable by GMail or Google Docs
    """
    local('python manage.py export_emails --format=google {0}'.format(f))

#-------------------
# Useful functions
#-------------------

def download_file(url, dest='.'):
    import urllib
    urllib.urlretrieve(url, dest)
