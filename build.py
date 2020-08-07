from os import listdir, path, remove
from shutil import rmtree, copyfile
from argparse import ArgumentParser
from subprocess import call
from distutils.dir_util import copy_tree

# Build options to target specific OS
parser = ArgumentParser(description='Build options.')
parser.add_argument('-o', '--os', default='win')
parser.add_argument('-a', '--arch', default='x64')
parser.add_argument('-i', '--npm_install', default='false')
args = vars(parser.parse_args())
os = args['os']
arch = args['arch']
npm_install = args['npm_install']

# Checks arguments
if os != 'win' and os != 'macos' and os != 'linux':
    print('Supported systems are: win, macos, linux.')
    quit()
if arch != 'x86' and arch != 'x64':
    print('Supported architectures are: x86, x64')
    quit()

# Install dependencies
if npm_install == 'true':
    call('npm i', shell=True)
    call('npm i', shell=True, cwd='../portfolio')
    call('npm i', shell=True, cwd='../truck-forge')

# Builds clients
call('npm run build', shell=True, cwd='../portfolio')
call('npm run build --prod', shell=True, cwd='../truck-forge')

# Removes previous built client
if path.isdir('./public'):
    rmtree('./public')

# Creates folders to store web sites
call('mkdir public', shell=True)
call('mkdir portfolio', shell=True, cwd='public')
call('mkdir truck-forge', shell=True, cwd='public')

# Copies built client to server (portfolio)
for item in listdir('./../portfolio/build'):
    old_path = './../portfolio/build/{}'.format(item)
    new_path = './public/portfolio/{}'.format(item)
    if path.isfile(old_path) or path.islink(old_path):
        copyfile(old_path, new_path)
    elif path.isdir(old_path):
        copy_tree(old_path, new_path)

# Copies built client to server (truck-forge)
copy_tree('./../truck-forge/dist/truck-forge', './public/truck-forge')

# Compiles server
command = 'pkg . --targets=node12-{}-{}'.format(os, arch)
call(command, shell=True)

# Copies exec and config to /build folder
if path.isdir('./build'):
    rmtree('./build')
call('mkdir build', shell=True)
copyfile('./config.json', './build/config.json')
if os == 'win':
    copyfile('./archive-projects.exe', './build/portfolio.exe')
    remove('./archive-projects.exe')
else:
    print('\nWARNING: Copy archive-projects file to /build folder.')

print('\nBuilding is finished.\n')
