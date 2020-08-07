from os import listdir, path, remove
from shutil import rmtree, copyfile
from argparse import ArgumentParser
from subprocess import call
from distutils.dir_util import copy_tree

# Build options to target specific OS
parser = ArgumentParser(description='Build options.')
parser.add_argument('-o', '--os', default='win')
parser.add_argument('-a', '--arch', default='x64')
args = vars(parser.parse_args())
os = args['os']
arch = args['arch']

# Checks arguments
if os != 'win' and os != 'macos' and os != 'linux':
    print('Supported systems are: win, macos, linux.')
    quit()
if arch != 'x86' and arch != 'x64':
    print('Supported architectures are: x86, x64')
    quit()

# Installs dependencies
if not path.isdir('./node_modules'):
    call('npm i', shell=True)
if not path.isdir('./../portfolio/node_modules'):
    call('npm i', shell=True, cwd='../portfolio')
if not path.isdir('./../truck-forge/node_modules'):
    call('npm i', shell=True, cwd='../truck-forge')

# Builds clients
call('npm run build', shell=True, cwd='../portfolio')
call('npm run build --prod', shell=True, cwd='../truck-forge')

# Removes previous built client
if path.isdir('./public'):
    rmtree('./public')

# Copies built clients to server
call('mkdir public', shell=True)
copy_tree('./../portfolio/build', './public/portfolio')
copy_tree('./../truck-forge/dist/truck-forge', './public/truck-forge')
copy_tree('./../ietm-forge-old/public', './public/ietm-forge-old')
copy_tree('./../mpu-cloud-old/public', './public/mpu-cloud-old')
copy_tree('./../mpu-cloud-old/storage', './public/mpu-cloud-old/storage')

# Compiles server
command = 'pkg . --targets=node12-{}-{}'.format(os, arch)
call(command, shell=True)

# Creates and fills /build folder
if path.isdir('./build'):
    rmtree('./build')
call('mkdir build', shell=True)
copyfile('./../mpu-cloud-old/data.db', './build/mpu-cloud-old-data.db') # important mpu-cloud-old file
copyfile('./config.json', './build/config.json')
if os == 'win':
    copyfile('./archive-projects.exe', './build/portfolio.exe')
    remove('./archive-projects.exe')
else:
    print('\nWARNING: Copy archive-projects file to /build folder.')

print('\nBuilding is finished.\n')
