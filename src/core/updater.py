#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ updater.py                [Created: 2023-03-21 |  8:32 - AM]  #
#                                       [Updated: 2023-03-21 | 10:23 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The updater of AOVPNS for download and install the latest                #
#  version of AOVPNS from the GitHub repository.                            #
#  Language ~ Python3                                                       #
#---[Author]----------------------------------------------------------------#
#  Thomas Pellissier (MyMeepSQL)                                            #
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
from requests import get

## Third party libraries
from src.config import Configuration
from src.__main__ import AOVPNS
from src.tools.packaging import version
from src.util.clear import clear
from src.util.colors import Color
from src.util.process import Process
import src.util.github_repo as GR
from src.util.internet_check import internet_check
from src.util.based_distro import Based_Distro as BD
from src.util.remove_python_cache import remove_python_cache
from src.util.create_bin_file import Create_bin_file
from src.util.env_var import set_env_var, remove_env_var

# Main
class Updater():
    '''
    The updater of AOVPNS for download and install the latest version of AOVPNS from the GitHub repository.
    '''

    # Variables
    DEFAULT_INSTALL_PATH = Configuration.DEFAULT_INSTALL_PATH
    BIN_PATH = Configuration.BIN_PATH
    TEMP_PATH = Configuration.TEMP_PATH
    INSTALL_PATH = DEFAULT_INSTALL_PATH
    VERSION = Configuration.VERSION
    REPO_VERSION = Configuration.REPO_VERSION
    REPO_METADATA_URL = Configuration.REPO_METADATA_URL

    # Environment variables
    aovpns_path_env_var_name = Configuration.aovpns_path_env_var_name
    aovpns_path_env_var_value = Configuration.DEFAULT_INSTALL_PATH

    # Github's repo settings
    REPO_URL = Configuration.REPO_URL
    REPO_BRANCH = Configuration.REPO_BRANCH
    REPO_MASTER_BRANCH = Configuration.REPO_MASTER_BRANCH

    # cp_online_ver = None

    # Main
    def __init__(self, args, pwd):
        # Check if the user's platform is a Linux machine or not
        if platform.system() != 'Linux':
            AOVPNS.Banner()
            print()
            Color.pl('  {!} You tried to run AOVPNS on a non-linux machine!')
            Color.pl('  {*} AOVPNS can be run only on a Linux kernel.')
            sys.exit(1)
        else:
            # Check if the user ran AOVPNS with root privileges or not
            if os.getuid() != 0:
                AOVPNS.Banner()
                print()
                Color.pl('  {!} The AOVPNS Updater must be run as root.')
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
                    AOVPNS.Banner()
                    print()
                    Color.pl('  {!} You\'re not running Arch or Debian variant.')
                    Color.pl('  {*} AOVPNS can only run on Arch or Debian based distros.')
                    Color.pl('  {-} Exiting...')
                    sys.exit(1)

            # aovpns main file in /usr/bin/
            aovpns_command_bin = Create_bin_file.__init__(path=self.INSTALL_PATH)

        if args.quiet:
            # -------------------- [ Quiet update ] -------------------- #
            try:
                if internet_check() == False:
                    Color.pl('Internet status: {R}Not connected{W}.')
                    Color.pl('No Internet connexion found, please check if you are connected to the Internet and retry.')
                    sys.exit(1)

                ## ---------- [ Check if the AOVPNS repositorie on GitHub are reachable or not ] ---------- ##
                GR.is_reachable(args)

                ## ---------- [ Check if the AOVPNS version is up to date or not ] ---------- ##
                rqst = get('%s' % self.REPO_METADATA_URL, timeout=5)
                fetch_sc = rqst.status_code
                if fetch_sc == 200:
                    metadata = rqst.text
                    json_data = loads(metadata)
                    cp_online_ver = json_data['version']
                    if version.parse(cp_online_ver) > version.parse(self.VERSION):
                        pass
                    else:
                        Color.pl('  {!} You already have the latest version of AOVPNS!')
                        sys.exit(1)
                sleep(0.5)

                # ---------- [ Prepare the update ] ---------- #
                # If a file called 'aovpns' already exist in /usr/bin/, inform the user and delete it
                if os.path.isfile(self.BIN_PATH + 'aovpns'):
                    os.remove(self.BIN_PATH + 'aovpns')
                # Remove the temporary directory if it already exists
                if os.path.isdir(self.TEMP_PATH):
                    shutil.rmtree(self.TEMP_PATH)
                # Create the temp folder that be use to download the latest AOVPNS version from GitHub
                # in it and install AOVPNS from this folder
                os.makedirs(self.TEMP_PATH, mode=0o777)
                # Remove the current AOVPNS instance
                shutil.rmtree(self.INSTALL_PATH)
                # Create the main folder where AOVPNS will be installed
                os.makedirs(self.INSTALL_PATH, mode=0o777)
                # Clone the latest version of AOVPNS into the temp. folder
                Process.call('git clone %s --branch %s %s' % (self.REPO_URL , self.REPO_BRANCH , self.TEMP_PATH), shell=True)
                sleep(1)

                #  ---------- [ AOVPNS Update ] ---------- #
                # Install AOVPNS by moving all the files from the temp. folder to the main folder
                shutil.copytree(src=self.TEMP_PATH, dst=self.INSTALL_PATH, dirs_exist_ok=True)
                # Update the command 'aovpns' in /usr/bin/
                with open(self.BIN_PATH + 'aovpns', 'x') as aovpns_file:
                    aovpns_file.write(aovpns_command_bin)
                # Apply rights on files
                sleep(1)
                Process.call('chmod 777 %saovpns' % self.BIN_PATH, shell=True)
                Process.call('chmod 777 -R %s' % self.INSTALL_PATH, shell=True)
                # Deleting the temporary directory
                shutil.rmtree(self.TEMP_PATH)
                sleep(1)
                # Removing the python cache
                remove_python_cache(pwd=pwd)
                sys.exit(0)
            except Exception as E:
                Color.pexception(E)
                # Color.pl(f'Exception : %s' % str(E) )
            except KeyboardInterrupt:
                Color.pl('\nUpdate process interrupted.')
                Color.pl('You must re-run the update process to update AOVPNS correctly.')
                # Removing the python cache
                remove_python_cache(pwd=pwd)
                sys.exit(1)
        else:
            # -------------------- [ No quiet installation ] -------------------- #
            AOVPNS.Banner()
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
            # Check if the AOVPNS_INSTALL_PATH environment variable is set or not
            try:
                if Configuration.verbose == 3:
                    Color.pl('  {§} Checking if the {C}{bold}AOVPNS_INSTALL_PATH{W} environment variable is set or not...')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.environ[self.aovpns_path_env_var_name]{W}')
                AOVPNS_PATH = os.environ[self.aovpns_path_env_var_name]
                self.INSTALL_PATH = AOVPNS_PATH
            except KeyError:
                Color.pl('  {!} AOVPNS is not installed on this machine.')
                Color.pl('  {*} Because the AOVPNS_INSTALL_PATH environment variable is not set (in the {C}/etc/environment{W} file).')
                Color.pl('  {-} Exiting...')
                if Configuration.verbose == 3:
                    Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                sys.exit(1)
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
                sys.exit(1)

            ## ---------- [ Check if the AOVPNS repositorie on GitHub are reachable or not ] ---------- ##
            if Configuration.verbose == 3:
                Color.pl('  {§} Check if the AOVPNS\'s repositorie are reachable or not...')
                Color.pl('   {SY1}╰──╼{W} Call the {SY1}is_reachable(){W} function.')
            GR.is_reachable(args)

            # ---- [ The info box ] ---- #
            Color.pl('''  {*} {underscore}This tool will{W}:
                    \r     {D}[{W}{LL}1{W}{D}]{W} Download the latest version of AOVPNS into {C}%s{W}.
                    \r     {D}[{W}{LL}2{W}{D}]{W} Update the current AOVPNS instance with the new one.
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
                                Color.pl('  {!} You already have the latest version of AOVPNS!')
                                if Configuration.verbose == 3:
                                    Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                                sys.exit(1)
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Python: {SY1}sleep(0.5){W}')
                    sleep(0.5)

                    # ---------- [ Prepare the update ] ---------- #
                    # If a file called 'aovpns' already exist in /usr/bin/, inform the user and delete it
                    if os.path.isfile(self.BIN_PATH + 'aovpns'):
                        if Configuration.verbose == 3:
                            Color.pl('  {§} The aovpns command already exist in {C}%s{W}' % self.BIN_PATH)
                            Color.pl('  {§} Remove it...')
                            Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.remove(self.BIN_PATH + \'aovpns\'){W})')
                        os.remove(self.BIN_PATH + 'aovpns')
                    # Remove the temporary directory if it already exists
                    if os.path.isdir(self.TEMP_PATH):
                        if args.verbose == 3:
                            Color.pl('  {§} AOVPNS\'s temporary folder detected.')
                            Color.pl('  {§} Remove it...')
                            Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(self.TEMP_PATH){W}')
                        shutil.rmtree(self.TEMP_PATH)
                    # Create the temp folder that be use to download the latest AOVPNS version from GitHub
                    # in it and install AOVPNS from this folder
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Creating temporary folder ({C}%s{W})...' % self.TEMP_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.makedirs(self.TEMP_PATH, mode=0o777){W}')
                    os.makedirs(self.TEMP_PATH, mode=0o777)
                    # Remove the current AOVPNS instance
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Deleting current AOVPNS instance...')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(%s){W}' % self.INSTALL_PATH)
                    shutil.rmtree(self.INSTALL_PATH)
                    # Create the main folder where AOVPNS will be installed
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Creating main folder ({C}%s{W})...' % self.INSTALL_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.makedirs(self.INSTALL_PATH, mode=0o777){W}')
                    os.makedirs(self.INSTALL_PATH, mode=0o777)
                    # Clone the latest version of AOVPNS into the temp. folder
                    Color.pl('  {-} Downloading the latest AOVPNS\'s version into {C}%s{W}...' % self.TEMP_PATH)
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Cloning files from GitHub to the temporary directory...')
                    Process.call('git clone %s --branch %s %s' % (self.REPO_URL , self.REPO_BRANCH , self.TEMP_PATH), shell=True)
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Python: {SY1}sleep(1){W}')
                    sleep(1)

                    #  ---------- [ AOVPNS Update ] ---------- #
                    Color.pl('  {-} Updating AOVPNS...')
                    # Install AOVPNS by moving all the files from the temp. folder to the main folder
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Copying all files from the AOVPNS\'s temporary folder to the main directory ({C}%s{W})...' % self.INSTALL_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.copytree(src=self.TEMP_PATH, dst=INSTALL_PATH, dirs_exist_ok=True){W}')
                    shutil.copytree(src=self.TEMP_PATH, dst=self.INSTALL_PATH, dirs_exist_ok=True)
                    # Update the command 'aovpns' in /usr/bin/
                    Color.pl('  {-} Updating the {G}aovpns{W} command into {C}%s{W}...' % self.BIN_PATH)
                    with open(self.BIN_PATH + 'aovpns', 'x') as aovpns_file:
                        aovpns_file.write(aovpns_command_bin)
                    # Apply rights on files
                    Color.pl('  {-} Apply rights to the new files...')
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Python: {SY1}sleep(1){W}')
                    sleep(1)
                    Process.call('chmod 777 %saovpns' % self.BIN_PATH, shell=True)
                    Process.call('chmod 777 -R %s' % self.INSTALL_PATH, shell=True)
                    # Deleting the temporary directory
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Remove the temporary directory ({C}%s{W})...' % self.TEMP_PATH)
                    shutil.rmtree(self.TEMP_PATH)
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Python: {SY1}sleep(1){W}')
                    sleep(1)
                    # Removing the python cache
                    remove_python_cache(pwd=pwd)
                    Color.pl('  {+} AOVPNS successfully updated with the version: %s' % cp_online_ver)
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Exiting with the exit code: {G}0{W}')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(0){W}')
                    sys.exit(0)
                except Exception as E:
                    Color.pexception(E)
                    # Color.pl(f'Exception : %s' % str(E) )
                    # log_writer(f'aovpns, %s' % str(E) )
                except KeyboardInterrupt:
                    Color.pl('\n  {!} Update process interrupted.')
                    Color.pl('  {!} You must re-run the update process to update AOVPNS correctly.')
                    # Removing the python cache
                    remove_python_cache(pwd=pwd)
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
        Updater(args=args, pwd=pwd)
    except EOFError:
        Color.pl('\n  {*} Aborted')
        # Removing the python cache
        remove_python_cache(pwd=pwd)
        if Configuration.verbose == 3:
            Color.pl('  {§} Exiting with the exit code: {R}1{W}')
            Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
        sys.exit(1)
    except KeyboardInterrupt:
        Color.pl('\n  {*} Aborted')
        # Removing the python cache
        remove_python_cache(pwd=pwd)
        if Configuration.verbose == 3:
            Color.pl('  {§} Exiting with the exit code: {R}1{W}')
            Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
        sys.exit(1)

