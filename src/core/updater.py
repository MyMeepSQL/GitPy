#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ updater.py                [Created: 2023-03-21 |  8:32 - AM]  #
#                                       [Updated: 2023-03-21 | 10:23 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The updater of GitPy for download and install the latest                #
#  version of GitPy from the GitHub repository.                            #
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
from json import loads
from time import sleep

## Third party libraries
from src.config import Configuration
from src.__main__ import GitPy
from src.tools.packaging import version
from src.tools.requests import get
from src.util.clear import clear
from src.util.colors import Color
from src.util.process import Process
import src.util.github_repo as GR
from src.util.exit_tool import exit_tool
from src.util.internet_check import internet_check
from src.util.based_distro import Based_Distro as BD
from src.util.remove_python_cache import remove_python_cache
from src.util.create_bin_file import Create_bin_file
from src.util.env_var import set_env_var, remove_env_var

# Main
class Updater():
    '''
    The updater of GitPy for download and install the latest version of GitPy from the GitHub repository.
    '''

    # Variables
    DEFAULT_INSTALL_PATH = Configuration.DEFAULT_INSTALL_PATH
    BIN_PATH = Configuration.BIN_PATH
    TEMP_PATH = Configuration.TEMP_PATH
    INSTALL_PATH = DEFAULT_INSTALL_PATH
    VERSION = Configuration.VERSION

    # Environment variables
    ## The GitPy's install path
    gitpy_install_path_env_var_name = Configuration.gitpy_install_path_env_var_name
    ## The News Version Notification's config file
    gitpy_install_path_env_var_value = Configuration.gitpy_install_path_env_var_value

    # Github's repo settings
    REPO_URL = Configuration.REPO_URL
    REPO_BRANCH = Configuration.REPO_BRANCH
    REPO_MASTER_BRANCH = Configuration.REPO_MASTER_BRANCH
    REPO_VERSION = Configuration.REPO_VERSION
    REPO_METADATA_URL = Configuration.REPO_METADATA_URL

    # cp_online_ver = None

    # Main
    def __init__(self, args, pwd):
        # Check if the user's platform is a Linux machine or not
        if platform.system() != 'Linux':
            GitPy.Banner()
            print()
            Color.pl('  {!} You tried to run GitPy on a non-linux machine!')
            Color.pl('  {*} GitPy can be run only on a Linux kernel.')
            # Exit and removing the python cache
            exit_tool(1,pwd=pwd)
        else:
            # Check if the user ran GitPy with root privileges or not
            if os.getuid() != 0:
                GitPy.Banner()
                print()
                Color.pl('  {!} The GitPy Updater must be run as root.')
                Color.pl('  {*} Re-run with sudo or switch to root user.')
                # Exit and removing the python cache
                exit_tool(1,pwd=pwd)
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
                    # Exit and removing the python cache
                    exit_tool(1,pwd=pwd)

            # gitpy main file in /usr/bin/
            gitpy_command_bin = Create_bin_file.__init__(path=self.INSTALL_PATH)

        if args.quiet:
            # -------------------- [ Quiet update ] -------------------- #
            try:
                if internet_check() == False:
                    Color.pl('Internet status: {R}Not connected{W}.')
                    Color.pl('No Internet connexion found, please check if you are connected to the Internet and retry.')
                    # Exit and removing the python cache
                    exit_tool(1,pwd=pwd)

                ## ---------- [ Check if the GitPy repositorie on GitHub are reachable or not ] ---------- ##
                GR.is_reachable(args)

                ## ---------- [ Check if the GitPy version is up to date or not ] ---------- ##
                rqst = get('%s' % self.REPO_METADATA_URL, timeout=5)
                fetch_sc = rqst.status_code
                if fetch_sc == 200:
                    metadata = rqst.text
                    json_data = loads(metadata)
                    cp_online_ver = json_data['version']
                    if version.parse(cp_online_ver) > version.parse(self.VERSION):
                        pass
                    else:
                        Color.pl('  {!} You already have the latest version of GitPy!')
                        # Exit and removing the python cache
                        exit_tool(1,pwd=pwd)
                sleep(0.5)

                # ---------- [ Prepare the update ] ---------- #
                # If a file called 'gitpy' already exist in /usr/bin/, inform the user and delete it
                if os.path.isfile(self.BIN_PATH + 'gitpy'):
                    os.remove(self.BIN_PATH + 'gitpy')
                # Remove the temporary directory if it already exists
                if os.path.isdir(self.TEMP_PATH):
                    shutil.rmtree(self.TEMP_PATH)
                # Create the temp folder that be use to download the latest GitPy version from GitHub
                # in it and install GitPy from this folder
                os.makedirs(self.TEMP_PATH, mode=0o777)
                # Remove the current GitPy instance
                shutil.rmtree(self.INSTALL_PATH)
                # Create the main folder where GitPy will be installed
                os.makedirs(self.INSTALL_PATH, mode=0o777)
                # Clone the latest version of GitPy into the temp. folder
                Process.call('git clone %s --branch %s %s' % (self.REPO_URL , self.REPO_BRANCH , self.TEMP_PATH), shell=True)
                sleep(1)

                #  ---------- [ GitPy Update ] ---------- #
                # Install GitPy by moving all the files from the temp. folder to the main folder
                shutil.copytree(src=self.TEMP_PATH, dst=self.INSTALL_PATH, dirs_exist_ok=True)
                # Update the command 'gitpy' in /usr/bin/
                with open(self.BIN_PATH + 'gitpy', 'x') as gitpy_file:
                    gitpy_file.write(gitpy_command_bin)
                # Apply rights on files
                sleep(1)
                Process.call('chmod 777 %sgitpy' % self.BIN_PATH, shell=True)
                Process.call('chmod 777 -R %s' % self.INSTALL_PATH, shell=True)
                # Deleting the temporary directory
                shutil.rmtree(self.TEMP_PATH)
                sleep(1)
                # Exit and removing the python cache
                exit_tool(0,pwd=pwd)
            except Exception as E:
                Color.pexception(E)
                # Color.pl(f'Exception : %s' % str(E) )
            except KeyboardInterrupt:
                Color.pl('\nUpdate process interrupted.')
                Color.pl('You must re-run the update process to update GitPy correctly.')
                # Exit and removing the python cache
                exit_tool(1,pwd=pwd)
        else:
            # -------------------- [ No quiet installation ] -------------------- #
            GitPy.Banner()
            print()
            if Configuration.verbose >= 1:
                Color.pl('  {*} Verbosity level: %s' % Configuration.verbose)
                if Configuration.verbose == 1:
                    Color.pl('   {G}╰──╼{W} Verbose level 1 ({C}Blue color{W}) : {&}')
                if Configuration.verbose == 2:
                    Color.pl('   {G}├──╼{W} Verbose level 1 ({C}Blue color{W}) : {&}')
                    Color.pl('   {G}╰──╼{W} Verbose level 2 ({P}Pink color{W}) : {#}')
                if Configuration.verbose == 3:
                    Color.pl('   {G}├──╼{W} Verbose level 1 ({C}Blue color{W})   : {&}')
                    Color.pl('   {G}├──╼{W} Verbose level 2 ({P}Pink color{W})   : {#}')
                    Color.pl('   {G}╰──╼{W} Verbose level 3 ({SY1}Yellow color{W}) : {§}')
            # Check if the GITPY_INSTALL_PATH environment variable is set or not
            try:
                if Configuration.verbose == 3:
                    Color.pl('  {§} Checking if the {C}{bold}GITPY_INSTALL_PATH{W} environment variable is set or not...')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.environ[self.gitpy_install_path_env_var_name]{W}')
                GITPY_PATH = os.environ[self.gitpy_install_path_env_var_name]
                self.INSTALL_PATH = GITPY_PATH
            except KeyError:
                Color.pl('  {!} GitPy is not installed on this machine.')
                Color.pl('  {*} Because the GITPY_INSTALL_PATH environment variable is not set (in the {C}/etc/environment{W} file).')
                # Exit and removing the python cache
                exit_tool(1,pwd=pwd)
            # Check if the use are connected to the Internet network with the internet_check() function
            Color.pl('  {-} Checking for internet connexion...')
            if Configuration.verbose == 3:
                Color.pl('  {§} Call the {P}internet_check(){W} function.')
                Color.pl('   {SY1}╰──╼{W} Python: {SY1}request.urlopen(host, timeout=10){W}')
            if internet_check() == True:
                Color.pl('  {+} Internet status: {G}Connected{W}.')
                pass
            else:
                Color.pl('  {+} Internet status: {R}Not connected{W}.')
                Color.pl('  {!} No Internet connexion found, please check if you are connected to the Internet and retry.')
                # Exit and removing the python cache
                exit_tool(1,pwd=pwd)

            ## ---------- [ Check if the GitPy repositorie on GitHub are reachable or not ] ---------- ##
            if Configuration.verbose == 3:
                Color.pl('  {§} Check if the GitPy\'s repositorie are reachable or not...')
                Color.pl('   {SY1}╰──╼{W} Call the {SY1}is_reachable(){W} function.')
            GR.is_reachable(args)

            # ---- [ The info box ] ---- #
            Color.pl('''  {*} {underscore}This tool will{W}:
                    \r     {D}[{W}{LL}1{W}{D}]{W} Download the latest version of GitPy into {C}%s{W}.
                    \r     {D}[{W}{LL}2{W}{D}]{W} Update the current GitPy instance with the new one.
                    \r     {D}[{W}{LL}3{W}{D}]{W} Apply all rights on the new files.
            ''' % self.TEMP_PATH)
            if args.no_confirm:
                Color.pl('  {?} Do you want to continue? [Y/n] y')
                choice_1 = 'y'
            else:
                choice_1 = input(Color.s('  {?} Do you want to continue? [Y/n] '))
            if choice_1 == 'y' or choice_1 == 'Y' or not choice_1:
                try:
                    Color.pl('  {-} Fetching metadata...')
                    rqst = get('%s' % self.REPO_METADATA_URL, timeout=5)
                    fetch_sc = rqst.status_code
                    if fetch_sc == 200:
                        metadata = rqst.text
                        json_data = loads(metadata)
                        cp_online_ver = json_data['version']
                        if not args.force_update:
                            if version.parse(cp_online_ver) > version.parse(self.VERSION):
                                Color.pl('  {*} A new update are avalable : %s (current: %s)' % (cp_online_ver, self.VERSION))
                            else:
                                Color.pl('  {!} You already have the latest version of GitPy!')
                                # Exit and removing the python cache
                                exit_tool(1,pwd=pwd)
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Python: {SY1}sleep(0.5){W}')
                    sleep(0.5)

                    # ---------- [ Prepare the update ] ---------- #
                    # If a file called 'gitpy' already exist in /usr/bin/, inform the user and delete it
                    if os.path.isfile(self.BIN_PATH + 'gitpy'):
                        if Configuration.verbose == 3:
                            Color.pl('  {§} The gitpy command already exist in {C}%s{W}' % self.BIN_PATH)
                            Color.pl('  {§} Remove it...')
                            Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.remove(self.BIN_PATH + \'gitpy\'){W})')
                        os.remove(self.BIN_PATH + 'gitpy')
                    # Remove the temporary directory if it already exists
                    if os.path.isdir(self.TEMP_PATH):
                        if args.verbose == 3:
                            Color.pl('  {§} GitPy\'s temporary folder detected.')
                            Color.pl('  {§} Remove it...')
                            Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(self.TEMP_PATH){W}')
                        shutil.rmtree(self.TEMP_PATH)
                    # Create the temp folder that be use to download the latest GitPy version from GitHub
                    # in it and install GitPy from this folder
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Creating temporary folder ({C}%s{W})...' % self.TEMP_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.makedirs(self.TEMP_PATH, mode=0o777){W}')
                    os.makedirs(self.TEMP_PATH, mode=0o777)
                    # Remove the current GitPy instance
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Deleting current GitPy instance...')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(%s){W}' % self.INSTALL_PATH)
                    shutil.rmtree(self.INSTALL_PATH)
                    # Create the main folder where GitPy will be installed
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Creating main folder ({C}%s{W})...' % self.INSTALL_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.makedirs(self.INSTALL_PATH, mode=0o777){W}')
                    os.makedirs(self.INSTALL_PATH, mode=0o777)
                    # Clone the latest version of GitPy into the temp. folder
                    Color.pl('  {-} Downloading the latest GitPy\'s version into {C}%s{W}...' % self.TEMP_PATH)
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Cloning files from GitHub to the temporary directory...')
                    Process.call('git clone %s --branch %s %s' % (self.REPO_URL , self.REPO_BRANCH , self.TEMP_PATH), shell=True)
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Python: {SY1}sleep(1){W}')
                    sleep(1)

                    #  ---------- [ GitPy Update ] ---------- #
                    Color.pl('  {-} Updating GitPy into {C}%s{W}...' % self.INSTALL_PATH)
                    # Install GitPy by moving all the files from the temp. folder to the main folder
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Copying all files from the GitPy\'s temporary folder to the main directory ({C}%s{W})...' % self.INSTALL_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.copytree(src=self.TEMP_PATH, dst=INSTALL_PATH, dirs_exist_ok=True){W}')
                    shutil.copytree(src=self.TEMP_PATH, dst=self.INSTALL_PATH, dirs_exist_ok=True)
                    # Update the command 'gitpy' in /usr/bin/
                    Color.pl('  {-} Updating the {G}gitpy{W} command into {C}%s{W}...' % self.BIN_PATH)
                    with open(self.BIN_PATH + 'gitpy', 'x') as gitpy_file:
                        gitpy_file.write(gitpy_command_bin)
                    # Apply rights on files
                    Color.pl('  {-} Apply rights to the new files...')
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Python: {SY1}sleep(1){W}')
                    sleep(1)
                    Process.call('chmod 777 %sgitpy' % self.BIN_PATH, shell=True)
                    Process.call('chmod 777 -R %s' % self.INSTALL_PATH, shell=True)
                    # Deleting the temporary directory
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Remove the temporary directory ({C}%s{W})...' % self.TEMP_PATH)
                    shutil.rmtree(self.TEMP_PATH)
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Python: {SY1}sleep(1){W}')
                    sleep(1)
                    Color.pl('  {*} GitPy successfully updated with the version: %s' % cp_online_ver)
                    # Exit and removing the python cache
                    exit_tool(0,pwd=pwd)
                except Exception as E:
                    Color.pexception(E)
                    # Color.pl(f'Exception : %s' % str(E) )
                except KeyboardInterrupt:
                    Color.pl('\n  {!} Update process interrupted.')
                    Color.pl('  {!} You must re-run the update process to update GitPy correctly.')
                    # Exit and removing the python cache
                    exit_tool(1,pwd=pwd)
            else:
                Color.pl('  {*} Aborted')
                # Exit and removing the python cache
                exit_tool(1,pwd=pwd)

def entry_point(args, pwd):
    try:
        Updater(args=args, pwd=pwd)
    except EOFError:
        Color.pl('\n  {*} Aborted')
        # Exit and removing the python cache
        exit_tool(1,pwd=pwd)
    except KeyboardInterrupt:
        Color.pl('\n  {*} Aborted')
        # Exit and removing the python cache
        exit_tool(1,pwd=pwd)

