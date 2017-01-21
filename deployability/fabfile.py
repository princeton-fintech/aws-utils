import yaml
import sys
from os import path
from fabric.api import run
from fabric.api import cd

CONDA_INSTALLER = 'Anaconda2-4.2.0-Linux-x86_64.sh'
CONDA_SHASUM = 'beee286d24fb37dd6555281bba39b3deb5804baec509a9dc5c69185098cf661a'
CONDA_DIR = '~/anaconda2'

def get_jupyterlab_config(config):
    hosts = config['hosts']
    return hosts['jupyterlab']

def load_config(path):
    with open(path) as raw_config:
        config = yaml.load_config(raw_config)
        setup_jupyterlab(config)

def isdir_remote(path):
    result = run('python -c "import os;print os.path.isdir(os.path.expanduser(\'{}\'))"'.format(path))
    return bool(result)

def conda_installed():
    current_conda_path = run('which conda')
    return 'which' not in current_conda_path
        

def download_anaconda():
    if conda_installed():
        print "Anaconda is already installed."
        return
    if not isdir_remote("~/.deploy"):
        run('mkdir ~/.deploy')
    with cd('~/.deploy'):
        # Delete existing installer and download fresh copy
        run('rm -f {}'.format(CONDA_INSTALLER))
        run('wget https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh')
        shasum = run('sha256sum {}'.format(CONDA_INSTALLER))
        shasum = shasum.split(' ')[0]
        if CONDA_SHASUM != shasum:
            run('rm -f {}'.format(CONDA_INSTALLER))
            raise Exception("{} is inconsistent...aborting installation!".format(CONDA_INSTALLER))

def install_anaconda():
    if conda_installed():
        print "Anaconda is already installed."
        return
    with cd ('~/.deploy'):
        run('bash {} -b'.format(CONDA_INSTALLER))
        run('source ~/.bash_profile')

def install_jupyterlab():
    if not conda_installed():
        print "conda is not installed - install Anaconda or check your .bashrc"
        return
    run('conda install -c conda-forge jupyterlab')

def deploy_anaconda():
    download_anaconda()
    install_anaconda()
    install_jupyterlab()