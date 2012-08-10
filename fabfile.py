from fabric.api import *

"""
Base configuration
"""
env.project_name = 'universal_tutors'
env.python = 'python2.6'
env.repository_url = 'ssh://sls@slsapp.com:1234/rawjam/universal_tutors.git'

"""
Environments
"""
def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.user = 'rawjam'
    env.hosts = ['ec2-50-112-59-162.us-west-2.compute.amazonaws.com']
    env.path = '/home/rawjam/sites/%(project_name)s' % env
    env.env_path = '%(path)s/env' % env    
    env.repo_path = '%(path)s/repository' % env
    env.site_packages_path = '%(env_path)s/lib/python2.7/site-packages' % env    
    env.python = 'python2.7'

def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    env.user = 'rawjam'
    env.hosts = ['staging.rawjam.co.uk']
    env.path = '/home/rawjam/sites/%(project_name)s' % env
    env.env_path = '%(path)s/env' % env
    env.repo_path = '%(path)s/repository' % env
    env.site_packages_path = '%(env_path)s/lib/python2.6/site-packages' % env
    
"""
Branches
"""
def stable():
    """
    Work on stable branch.
    """
    env.branch = 'stable'

def master():
    """
    Work on development branch.
    """
    env.branch = 'master'

def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name
    
"""
Commands - setup
"""
def setup():
    """
    Setup a fresh virtualenv, install everything we need
    
    Does NOT perform the functions of deploy().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    
    setup_directories()
    setup_virtualenv()
    clone_repo()
    checkout_latest()
        
    install_requirements()
    install_apache_conf()
    install_nginx_conf()
    reload_webserver()
    
def refresh_configs():
    install_apache_conf()
    install_nginx_conf()
    
def refresh_requirements():
    """
    Refreshes the items in the requirements list, in case you have added additional dependences 
    after having already run the main setup process
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    
    checkout_latest()
    install_requirements()
    setup_symlinks()

def setup_directories():
    """
    Create directories necessary for deployment.
    """
    run('mkdir -p %(path)s' % env)
    run('mkdir -p %(env_path)s' % env)
    run('mkdir -p /home/rawjam/logs/' % env)
    
def setup_virtualenv():
    """
    Setup a fresh virtualenv.
    """
    run('virtualenv -p %(python)s --no-site-packages %(env_path)s;' % env)
    with prefix('source %(env_path)s/bin/activate' % env):
        run('easy_install -U setuptools; easy_install pip;' % env)

def clone_repo():
    """
    Do initial clone of the git repository.
    """
    run('git clone %(repository_url)s %(repo_path)s' % env)

def checkout_latest():
    """
    Pull the latest code on the specified branch.
    """
    run('cd %(repo_path)s; git pull origin %(branch)s' % env)

def install_requirements():
    """
    Install the required packages using pip.
    """
    with prefix('source %(env_path)s/bin/activate' % env):
        run('pip install -E %(env_path)s -r %(repo_path)s/requirements.txt' % env)

def install_apache_conf():
    """
    Install the apache site config file.
    """
    sudo('rm -fr /etc/apache2/sites-enabled/%(project_name)s.conf' % env)
    sudo('rm -fr /etc/apache2/sites-available/%(project_name)s.conf' % env)
    sudo('ln -s %(repo_path)s/%(project_name)s/configs/%(settings)s/apache.conf /etc/apache2/sites-available/%(project_name)s.conf' % env)
    sudo('ln -s /etc/apache2/sites-available/%(project_name)s.conf /etc/apache2/sites-enabled/%(project_name)s.conf' % env)
    
def install_nginx_conf():
    """
    Install the nginx site config file.
    """
    sudo('rm -fr /etc/nginx/sites-enabled/%(project_name)s.conf' % env)
    sudo('rm -fr /etc/nginx/sites-available/%(project_name)s.conf' % env)
    sudo('ln -s %(repo_path)s/%(project_name)s/configs/%(settings)s/nginx.conf /etc/nginx/sites-available/%(project_name)s.conf' % env)
    sudo('ln -s /etc/nginx/sites-available/%(project_name)s.conf /etc/nginx/sites-enabled/%(project_name)s.conf' % env)
    
def setup_symlinks():
    with prefix('source %(env_path)s/bin/activate' % env):
        run('python %(repo_path)s/%(project_name)s/configs/%(settings)s/manage.py collectstatic --noinput;' % env)
    
"""
Commands - deployment
"""
    
def deploy():
    """
    Deploy the latest version of the site to the server and restart Apache2.
    
    Does not perform the functions of load_new_data().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
        
    checkout_latest()
    setup_symlinks()
    
    # Run any South migrations
    with prefix('source %(env_path)s/bin/activate' % env):
        run('python %(repo_path)s/%(project_name)s/configs/%(settings)s/manage.py migrate;' % env)
    
    reload_modwsgi()
       
def reload_webserver():
    """
    Restart the Apache2 server.
    """
    sudo('/etc/init.d/nginx restart')
    sudo('/etc/init.d/apache2 restart')
    
def reload_modwsgi():
    run('touch %(repo_path)s/%(project_name)s/configs/%(settings)s/%(settings)s.wsgi;' % env)
    
"""
Commands - rollback
"""
def rollback(commit_id):
    """
    Rolls back to specified git commit hash or tag.
    
    There is NO guarantee we have committed a valid dataset for an arbitrary
    commit hash.
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    
    checkout_latest()
    git_reset(commit_id)
        
    reload_modwsgi()
    
def git_reset(commit_id):
    """
    Reset the git repository to an arbitrary commit hash or tag.
    """
    env.commit_id = commit_id
    run("cd %(repo_path)s; git reset --hard %(commit_id)s" % env)


"""
Commands - miscellaneous
"""
    
def clear_cache():
    """
    Restart memcache, wiping the current cache.
    """
    run('/etc/init.d/memcached restart')
    
def echo_host():
    """
    Echo the current host to the command line.
    """
    run('echo %(settings)s; echo %(hosts)s' % env)