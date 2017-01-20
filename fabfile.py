import yaml
import sys
from fabric.api import run

def get_jupyterlab_config(config):
    hosts = config['hosts']
    return hosts['jupyterlab']

def load_config(path):
    with open(path) as raw_config:
        config = yaml.load_config(raw_config)
        setup_jupyterlab(config)
        

def lab():
    print "Hello"

if __name__ == "__main__":
    conf = sys.argv[1]
    load_config(conf)