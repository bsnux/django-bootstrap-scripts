import os
from fabric.api import local, task, cd, run, env
from fabric.colors import red, green

env.hosts = ['bsnux.com']
env.user = 'bsnux'

code_dir = '/home/bsnux/webapps/'

@task
def ini_project(name):
    """
    fab ini_project:name=myproject
    """
    settings_file = name + '/settings.py'
    import fileinput
    for line in fileinput.input(settings_file, inplace=1):
        if line.startswith('MEDIA_URL = '):
            cad = "MEDIA_URL = '/media/'"
            print(line.replace(line, cad))
        elif line.startswith('# Django settings'):
            cad = "import os\nPROJECT_ROOT = os.path.dirname(os.path.realpath(__file__)) + '{0}/'".format(name)
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
        else:
            print line,
    for line in fileinput.input(settings_file, inplace=1):
        if not line.startswith('#'):
            print line,
    os.mkdir('{0}/static'.format(name))
    os.mkdir('{0}/static_collected'.format(name))
    os.mkdir('{0}/media'.format(name))

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
    local('python manage.py collectstatic && python manage.py compress')
