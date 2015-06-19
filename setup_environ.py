#!/usr/bin/env python

import os, sys, argparse, subprocess

def run_cmd(cmd):
    subprocess.check_call(cmd, shell=True, executable='/bin/bash')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Setup Django Python environment.')
    parser.add_argument('--deploy', '-d', choices=['development', 'production'], default='development',
                        help='deployment type')
    args = parser.parse_args()
    args.deploy = args.deploy.lower()

    site = os.path.basename(os.getcwd())
    path = os.path.join(os.getcwd(), site)
    requirements = 'requirements/%s.txt'%args.deploy
    settings = '%s.settings.%s'%(site, args.deploy)

    commands = [
        'virtualenv --no-site-packages environ',
        'echo -e \'\nexport DJANGO_SETTINGS_MODULE=%s\n\' >> environ/bin/activate'%settings,
        'echo -e \'export PYTHONPATH=%s:$PYTHONPATH\n\' >> environ/bin/activate'%path,
        'source environ/bin/activate; pip install -r %s'%requirements
    ]
    for cmd in commands:
        run_cmd(cmd)

    if os.path.exists('patches'):
        for patch in os.listdir('patches'):
            cmd = 'patch -p0 -d environ/lib/python2.7/site-packages < patches/%s'%patch
            run_cmd(cmd)

    if args.deploy == 'development':
        commands = [
            'curl http://nodejs.org/dist/node-latest.tar.gz | tar xz',
            'cd node-v*; source ../environ/bin/activate; ./configure --prefix=$VIRTUAL_ENV',
            'cd node-v*; source ../environ/bin/activate; make install',
            'rm -rf node-v*',
            'source environ/bin/activate; npm -g install phantomjs',
            'source environ/bin/activate; npm -g install knockout.validation --save',
        ]
        for cmd in commands:
            run_cmd(cmd)
