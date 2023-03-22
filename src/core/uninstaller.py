#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ uninstaller.py            [Created: 2023-03-14 | 10:25 - AM]  #
#                                       [Updated: 2023-03-14 | 12:01 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Uninstall GitPy from your system                                        #
#  Language ~ Python3                                                       #
#---[Author]----------------------------------------------------------------#
#  Thomas Pellissier (MyMeepSQL)                                            #
#  Jonas Petitpierre (Bashy)                                                #
#---[Operating System]------------------------------------------------------#
#  Developed for Linux                                                      #
#---[License]---------------------------------------------------------------#
#  GNU General Public License v3.0                                          #
#  -------------------------------                                          #
#                                                                           #
#  This program is free software; you can redistribute it and/or modify     #
#  it under the terms of the GNU General Public License as published by     #
#  the Free Software Foundation; either version 2 of the License, or        #
#  (at your option) any later version.                                      #
#                                                                           #
#  This program is distributed in the hope that it will be useful,          #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the             #
#  GNU General Public License for more details.                             #
#                                                                           #
#  You should have received a copy of the GNU General Public License along  #
#  with this program; if not, write to the Free Software Foundation, Inc.,  #
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.              #
#---------------------------------------------------------------------------#

# Imports section
import os
import sys
import shutil
import platform
import subprocess
from time import sleep

## Third party libraries
from src.__main__ import GitPy
from src.config import Configuration
from src.util.clear import clear
from src.util.colors import Color
from src.util.internet_check import internet_check
from src.util.env_var import remove_env_var
from src.util.process import Process
from src.util.remove_python_cache import remove_python_cache
from src.util.based_distro import Based_Distro as BD

# Main
class Uninstaller():
    '''
    Uninstall GitPy from your system
    '''
    # Variables
    BIN_PATH = Configuration.BIN_PATH
    TEMP_PATH = Configuration.TEMP_PATH
    VERSION = Configuration.VERSION
    gitpy_path_env_var_name = Configuration.gitpy_path_env_var_name
    # Main
    def __init__(self, args, pwd):
        # Check if the user's platform is a Linux machine or not
        if platform.system() != 'Linux':
            GitPy.Banner()
            print()
            Color.pl('  {!} You tried to run GitPy on a non-linux machine!')
            Color.pl('  {*} GitPy can be run only on a Linux kernel.')
            sys.exit(1)
        else:
            if os.getuid() != 0:
                GitPy.Banner()
                print()
                Color.pl('  {!} The GitPy Installer must be run as root.')
                Color.pl('  {*} Re-run with sudo or switch to root user.')
                sys.exit(1)
            else:
                # Distro check
                if BD.__init__() == 'Arch':
                    based_distro = 'Arch'
                    pass
                elif BD.__init__() == 'Debian':
                    based_distro = 'Debian'
                    pass
                else:
                    GitPy.Banner()
                    print()
                    Color.pl('  {!} You\'re not running Arch or Debian variant.')
                    Color.pl('  {*} GitPy can only run on Arch or Debian based distros.')
                    Color.pl('  {-} Exiting...')
                    sys.exit(1)
        if args.quiet:
            # -------------------- [ Quiet installation ] -------------------- #
            # Check if the GITPY_INSTALL_PATH environment variable is set or not
            try:
                GITPY_PATH = os.environ[self.gitpy_path_env_var_name]
                INSTALL_PATH = GITPY_PATH
            except KeyError:
                Color.pl('  {!} GitPy is not installed on this machine.')
                Color.pl('  {*} Because the {C}{bold}GITPY_INSTALL_PATH{W} environment variable is not set (in the {C}/etc/environment{W} file).')
                Color.pl('  {-} Exiting...')
                sys.exit(1)

            ## ------ [ Remove the main folder ] ------ ##
            shutil.rmtree(INSTALL_PATH)

            ## ------ [ Remove the 'gitpy' command ] ------ ##
            os.remove(self.BIN_PATH + 'gitpy')

            ## ------ [ Remove the 'GITPY_INSTALL_PAT' environment variable ] ------ ##
            remove_env_var(var_name=self.gitpy_path_env_var_name)
            # Removing the python cache
            remove_python_cache(pwd=pwd)
            sys.exit(0)            
        else:
            # -------------------- [ No quiet installation ] -------------------- #
            GitPy.Banner()
            if Configuration.verbose >= 1:
                Color.pl('\n  {*} Verbosity level: %s' % Configuration.verbose)
                if Configuration.verbose == 1:
                    Color.pl('   {G}╰──╼{W} Verbose level 1 ({C}Blue color{W}) : {&}')
                if Configuration.verbose == 2:
                    Color.pl('   {G}├──╼{W} Verbose level 1 ({C}Blue color{W}) : {&}')
                    Color.pl('   {G}╰──╼{W} Verbose level 2 ({P}Pink color{W}) . {#}')
                if Configuration.verbose == 3:
                    Color.pl('   {G}├──╼{W} Verbose level 1 ({C}Blue color{W})   : {&}')
                    Color.pl('   {G}├──╼{W} Verbose level 2 ({P}Pink color{W})   : {#}')
                    Color.pl('   {G}╰──╼{W} Verbose level 3 ({SY1}Yellow color{W}) : {§}')
            # Check if the GITPY_INSTALL_PATH environment variable is set or not
            try:
                if Configuration.verbose == 3:
                    Color.pl('  {§} Checking if the {C}{bold}GITPY_INSTALL_PATH{W} environment variable is set or not...')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.environ[self.gitpy_path_env_var_name]{W}')
                GITPY_PATH = os.environ[self.gitpy_path_env_var_name]
                INSTALL_PATH = GITPY_PATH
            except KeyError:
                Color.pl('  {!} GitPy is not installed on this machine.')
                Color.pl('  {*} Because the GITPY_INSTALL_PATH environment variable is not set (in the {C}/etc/environment{W} file).')
                Color.pl('  {-} Exiting...')
                if Configuration.verbose == 3:
                    Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                sys.exit(1)
            # Inform the user what the uninstaller will do
            Color.pl('''  {*} {underscore}This tool will{W}:
                    \r     {D}[{W}{LL}1{W}{D}]{W} Remove the {C}%s{W} folder.
                    \r     {D}[{W}{LL}2{W}{D}]{W} Remove the {C}%sgitpy{W} file.
                    \r     {D}[{W}{LL}3{W}{D}]{W} Remove the {C}{bold}%s{W} environment variable.
            ''' % (INSTALL_PATH, self.BIN_PATH, self.gitpy_path_env_var_name))
            if args.no_confirm:
                Color.pl('  {?} Do you want to continue? [Y/n] y')
                choice_1 = 'y'
            else:
                choice_1 = input(Color.s('  {?} Do you want to continue? [Y/n] '))

            # ---------- [ GitPy uninstallation ] ---------- #
            if choice_1.lower() == 'y' or not choice_1:
                try:
                    Color.pl('  {-} Uninstalling GitPy from your system...')

                    ## ------ [ Remove the main folder ] ------ ##
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Removing the {C}%s{W} folder...' % INSTALL_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(self.INSTALL_PATH){W}')
                    shutil.rmtree(INSTALL_PATH)

                    ## ------ [ Remove the 'gitpy' command ] ------ ##
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Removing the {C}%sgitpy{W} file...' % self.BIN_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.remove(self.BIN_PATH + \'gitpy\'){W}')
                    os.remove(self.BIN_PATH + 'gitpy')

                    ## ------ [ Remove the 'GITPY_INSTALL_PAT' environment variable ] ------ ##
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Removing the {C}{bold}GITPY_INSTALL_PAT{W} environment variable...')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}remove_env_var(self.gitpy_path_env_var_name){W}')
                    remove_env_var(var_name=self.gitpy_path_env_var_name)
                    Color.pl('  {*} GitPy are successfully uninstalled from your system.')
                    Color.pl('  {*} You need to restart your machine to completly remove the {C}{bold}GITPY_INSTALL_PATH{W} environment variable.')
                    choice_2 = input(Color.s('  {?} Do you want to reboot your machine now? [y/n] '))
                    if choice_2.lower() == 'y':
                        # Removing the python cache
                        remove_python_cache(pwd=pwd)
                        Color.pl('  {-} Rebooting the machine...')
                        Process.call('reboot', shell=True)
                    else:
                        # Removing the python cache
                        remove_python_cache(pwd=pwd)
                        if Configuration.verbose == 3:
                            Color.pl('  {§} Exiting with the exit code: {G}0{W}')
                            Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(0){W}')
                        sys.exit(0)
                except KeyboardInterrupt:
                    Color.pl('\n  {!} Uninstallation process interrupted.')
                    Color.pl('  {*} You must re-run the uninstalation process to uninstall GitPy correctly.')
                    Color.pl('  {-} Exiting...')
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                    sys.exit(1)
            else:
                Color.pl('  {*} Aborted')
                # Removing the python cache
                remove_python_cache(pwd=pwd)
                if Configuration.verbose == 3:
                    Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                sys.exit(1)

def entry_point(args, pwd):
    try:
        Uninstaller(args=args, pwd=pwd)
    except EOFError:
        Color.pl('\n  {*} Aborted')
        # Removing the python cache
        remove_python_cache(pwd=pwd)
        if Configuration.verbose == 3:
            Color.pl('  {#} Exiting with the exit code: {R}1{W}')
            Color.pl('   {P}╰──╼{W} Python: {P}sys.exit(1){W}')
        sys.exit(1)
    except KeyboardInterrupt:
        Color.pl('\n  {*} Aborted')
        # Removing the python cache
        remove_python_cache(pwd=pwd)
        if Configuration.verbose == 3:
            Color.pl('  {#} Exiting with the exit code: {R}1{W}')
            Color.pl('   {P}╰──╼{W} Python: {P}sys.exit(1){W}')
        sys.exit(1)
