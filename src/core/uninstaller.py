#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ uninstaller.py            [Created: 2023-03-14 | 10:25 - AM]  #
#                                       [Updated: 2023-04-10 | 14:55 - PM]  #
#---[Info]------------------------------------------------------------------#
#  Uninstall GitPy from your system                                         #
#  Language ~ Python3                                                       #
#---[Authors]---------------------------------------------------------------#
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
from src.util.colors import Color
from src.util.exit_tool import exit_tool
from src.util.env_var import remove_env_var
from src.util.process import Process
from src.util.remove_python_cache import remove_python_cache
from src.util.based_distro import Based_Distro

# Main
class Uninstaller():
    '''
        Uninstall GitPy from your system
    '''

    # Variables
    BIN_PATH = Configuration.BIN_PATH
    TEMP_PATH = Configuration.TEMP_PATH
    VERSION = Configuration.VERSION
    INSTALL_PATH = None

    # Environment variables
    ## The GitPy's install path
    gitpy_install_path_env_var_name = Configuration.gitpy_install_path_env_var_name

    ## The News Version Notification's config file
    gitpy_notification_config_file_env_var_name = Configuration.gitpy_notification_config_file_env_var_name


    # Main
    def __init__(self, args, pwd):

        Color.pl(GitPy.Banner())
        print()

        # Check if the user's platform is a Linux machine or not
        if Configuration.verbose == 3:
            Color.pl('  {§} Checking if the user\'s platform is a Linux machine or not...')
            Color.pl('   {SY1}├──╼{W} Python: {SY1}platform.system() != Linux{W}')
            sleep(0.2)

        if platform.system() != 'Linux':
            if Configuration.verbose == 3:
                Color.pl('   {SY1}├──╼{W} The user\'s platform is {R}%s{W}' % platform.system())
                Color.pl('   {SY1}╰──╼{W} The user\'s platform is not a Linux machine.')
                sleep(0.2)

            Color.pl('  {!} You tried to run GitPy on a non-linux machine!')
            Color.pl('  {*} GitPy can be run only on a Linux kernel.')

            # Exit and removing the python cache
            exit_tool(1,pwd=pwd)

        else:
            if Configuration.verbose == 3:
                Color.pl('   {SY1}╰──╼{W} The user\'s platform is {C}%s{W}' % platform.system())
                sleep(0.2)

            if os.getuid() != 0:                
                Color.pl('  {!} The GitPy Uninstaller must be run as root.')
                Color.pl('  {*} Re-run with sudo or switch to root user.')

                # Exit and removing the python cache
                exit_tool(1,pwd=pwd)

            else:
                # Distro check
                if Based_Distro() == 'Arch':
                    based_distro = 'Arch'
                    pass

                elif Based_Distro() == 'Debian':
                    based_distro = 'Debian'
                    pass

                else:
                    Color.pl('  {!} You\'re not running Arch or Debian variant.')
                    Color.pl('  {*} GitPy can only run on Arch or Debian based distros.')
                    
                    # Exit and removing the python cache
                    exit_tool(1,pwd=pwd)

        if args.quiet: # -------------------- [ Quiet uninstallation ] -------------------- #

            # Check if the GITPY_INSTALL_PATH environment variable is set or not
            try:
                GITPY_PATH = os.environ[self.gitpy_install_path_env_var_name]
                self.INSTALL_PATH = GITPY_PATH

            except KeyError:
                Color.pl('GitPy is not installed on this machine.')
                Color.pl('Because the {C}{bold}%s{W} environment variable is not set.' % self.gitpy_install_path_env_var_name)
                # Exit and removing the python cache
                exit_tool(1,pwd=pwd)

            # Remove the main folder
            shutil.rmtree(self.INSTALL_PATH)

            #Remove the 'gitpy' command
            os.remove(self.BIN_PATH + 'gitpy')

            # Remove the GITPY_INSTALL_PAT environment variable 
            remove_env_var(var_name=self.gitpy_install_path_env_var_name)

            # Remove the GITPY_NOTIFICATION_CONFIG_FILE_PATH environment variable 
            # remove_env_var(var_name=self.gitpy_notification_config_file_env_var_name)

            # Exit and removing the python cache
            exit_tool(0,pwd=pwd)

        else: # -------------------- [ No quiet uninstallation ] -------------------- #
            Color.pl(GitPy.Banner())
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
                    Color.pl('  {§} Checking if the {C}{bold}%s{W} environment variable is set or not...' % self.gitpy_install_path_env_var_name)
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.environ[self.gitpy_install_path_env_var_name]{W}')
                GITPY_PATH = os.environ[self.gitpy_install_path_env_var_name]
                self.INSTALL_PATH = GITPY_PATH

            except KeyError:
                Color.pl('\n  {!} GitPy is not installed on this machine.')
                Color.pl('  {*} Because the {C}{bold}%s{W} environment variable is not set.' % self.gitpy_install_path_env_var_name)
                # Exit and removing the python cache
                exit_tool(1,pwd=pwd)

            # Inform the user what the uninstaller will do
            Color.pl('''  {*} {underscore}This tool will{W}:
                    \r     {D}[{W}{LL}1{W}{D}]{W} Remove the {C}%s{W} folder.
                    \r     {D}[{W}{LL}2{W}{D}]{W} Remove the {C}%sgitpy{W} file.
                    \r     {D}[{W}{LL}3{W}{D}]{W} Remove the {C}{bold}%s{W} environment variable.
                    ''' % (
                self.INSTALL_PATH,
                self.BIN_PATH,
                self.gitpy_install_path_env_var_name,
                # self.gitpy_notification_config_file_env_var_name
                )
            )

            if args.no_confirm:
                Color.pl('  {?} Do you want to continue? [Y/n]: y')
                choice_1 = 'y'
            else:
                choice_1 = input(Color.s('  {?} Do you want to continue? [Y/n]: '))

            # ---------- [ GitPy uninstallation ] ---------- #
            if choice_1.lower() == 'y' or not choice_1:
                try:
                    Color.pl('  {-} Uninstalling GitPy from your system...')

                    ## ------ [ Remove the main folder ] ------ ##
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Removing the {C}%s{W} folder...' % self.INSTALL_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(self.self.INSTALL_PATH){W}')
                    shutil.rmtree(self.INSTALL_PATH)

                    ## ------ [ Remove the 'gitpy' command ] ------ ##
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Removing the {C}%sgitpy{W} file...' % self.BIN_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.remove(self.BIN_PATH + \'gitpy\'){W}')
                    os.remove(self.BIN_PATH + 'gitpy')

                    ## ------ [ Remove the 'GITPY_INSTALL_PATH' environment variable ] ------ ##
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Removing the {C}{bold}GITPY_INSTALL_PAT{W} environment variable...')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}remove_env_var(self.gitpy_install_path_env_var_name){W}')

                    remove_env_var(var_name=self.gitpy_install_path_env_var_name)

                    Color.pl('  {*} GitPy are successfully uninstalled from your system.')
                    Color.pl('  {*} You need to restart your machine to completly remove the {C}{bold}%s{W} environment variable.' % 
                        self.gitpy_install_path_env_var_name
                    )
                    choice_2 = input(Color.s('  {?} Do you want to reboot your machine now? [y/n]: '))
                    if choice_2.lower() == 'y':
                        # Removing the python cache
                        remove_python_cache(pwd=pwd)
                        Color.pl('  {-} Rebooting the machine...')
                        Process.call('reboot', shell=True)
                    else:
                        # Exit and removing the python cache
                        exit_tool(0,pwd=pwd)

                except KeyboardInterrupt:
                    Color.pl('\n  {!} Uninstallation process interrupted.')
                    Color.pl('  {*} You must re-run the uninstalation process to uninstall GitPy correctly.')
                    # Exit and removing the python cache
                    exit_tool(1,pwd=pwd)

            else:
                Color.pl('  {*} Aborted')
                # Exit and removing the python cache
                exit_tool(1,pwd=pwd)

def entry_point(args, pwd):
    try:
        Uninstaller(args=args, pwd=pwd)

    except EOFError:
        Color.pl('\n  {*} Aborted')
        # Exit and removing the python cache
        exit_tool(1,pwd=pwd)

    except KeyboardInterrupt:
        Color.pl('\n  {*} Aborted')
        # Exit and removing the python cache
        exit_tool(1,pwd=pwd)
