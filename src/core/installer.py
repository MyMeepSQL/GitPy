#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ installer.py              [Created: 2023-03-07 | 10:27 - AM]  #
#                                       [Updated: 2023-03-14 |  9:21 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The installer of AOVPNS for install AOVPNS and the                       #
#  dependencies                                                             #
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
import pkg_resources
from time import sleep

## Third party libraries
import src.util.github_repo as GR
from src.__main__ import AOVPNS
from src.config import Configuration
from src.util.clear import clear
from src.util.colors import Color
from src.util.process import Process
from src.util.env_var import set_env_var
from src.util.based_distro import Based_Distro as BD
from src.util.internet_check import internet_check
from src.util.remove_python_cache import remove_python_cache
from src.util.if_package_exists import package_exists
from src.util.create_bin_file import Create_bin_file
from src.util.check_path import check_folder_path

# Main
class Installer():
    '''
    The installer of AOVPNS
    '''
    # Variables
    DEFAULT_INSTALL_PATH = Configuration.DEFAULT_INSTALL_PATH
    BIN_PATH = Configuration.BIN_PATH
    TEMP_PATH = Configuration.TEMP_PATH
    INSTALL_PATH = DEFAULT_INSTALL_PATH
    # Environment variables
    aovpns_path_env_var_name = Configuration.aovpns_path_env_var_name
    aovpns_path_env_var_value = Configuration.DEFAULT_INSTALL_PATH

    # Packages list for Arch based distros (pacman)
    arch_package_list = [
        'python-pip',
        'git',
        'curl',
        'wget',
        'openvpn',
        'openssl',
        'ca-certificates',
        'iptables',
    ]
    # Packages list for Debian based distros (apt)
    debian_package_list = [
        'python3-pip',
        'git',
        'curl',
        'wget'
        'openvpn',
        'openssl',
        'ca-certificates'
        'iptables',
        'gnupg'
    ]
    # pip package list 
    pip_package_name_list = [
        'rich',
        'gnureadline'
    ]

    # Github's repo settings
    REPO_URL = Configuration.REPO_URL
    REPO_BRANCH = Configuration.REPO_BRANCH
    REPO_MASTER_BRANCH = Configuration.REPO_MASTER_BRANCH

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
            if os.getuid() != 0:
                AOVPNS.Banner()
                print()
                Color.pl('  {!} The AOVPNS Installer must be run as root.')
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
        if args.skip_update:
            UPDATE_SYSTEM_SKIPED='(Skipped)'
        else:
            UPDATE_SYSTEM_SKIPED=''
        if args.install_path:
            self.INSTALL_PATH = ''.join(args.install_path).strip()
            self.INSTALL_PATH = check_folder_path(self.INSTALL_PATH)
            self.aovpns_path_env_var_value = self.INSTALL_PATH
            
        # aovpns main file in /usr/bin/
        aovpns_command_bin = Create_bin_file.__init__(path=self.INSTALL_PATH)

        # Main
        if args.quiet:
            # -------------------- [ Quiet installation ] -------------------- #
            try:
                # ---------- [ System update ] ---------- #
                if args.skip_update:
                    pass
                else:
                    sleep(0.5)
                    if based_distro == 'Arch':
                        Process.call('pacman -Syy')
                    elif based_distro == 'Debian':
                        Process.call('apt update')
                    sleep(1)

                # ---------- [ Tools installation ] ---------- #
                if based_distro == 'Arch':
                    for arch_package_name in self.arch_package_list:
                        if package_exists(package=arch_package_name):
                            pass
                        else:
                            Process.call('pacman --needed --noconfirm -q -S %s'% arch_package_name, shell=True)
                elif based_distro == 'Debian':
                    for debian_package_name in self.debian_package_list:
                        if package_exists(package=debian_package_name):
                            pass
                        else:
                            Process.call('apt install -qqq-y %s'% debian_package_name, shell=True)

                ## ------ [ PIP package ] ------ ##
                for pip_package_name in self.pip_package_name_list:
                    try:
                        pkg_resources.get_distribution(pip_package_name)
                    except pkg_resources.DistributionNotFound:
                        Process.call('pip install %s' % pip_package_name, shell=True)

                # ---------- [ AOVPNS installation ] ---------- #
                if os.path.isdir(self.INSTALL_PATH):
                    shutil.rmtree(self.INSTALL_PATH)
                    if os.path.isdir(self.TEMP_PATH):
                        shutil.rmtree(self.TEMP_PATH)

                ## ------ [ AOVPNS files ] ------ ##
                ### ---- [ Create the main folder in /usr/share/ ] ---- ###
                os.makedirs(self.INSTALL_PATH, mode=0o777)    # Create the main directory of AOVPNS

                ### ---- [ Create the temp folder that be use to download the latest AOVPNS version from GitHub
                #          in it and install AOVPNS from this folder                                            ] ---- ###
                os.makedirs(self.TEMP_PATH, mode=0o777)

                ### ---- [ Clone the latest version of AOVPNS into the temp. folder ] ---- ###
                Process.call('git clone %s --verbose --branch %s %s' % (self.REPO_URL , self.REPO_BRANCH , self.TEMP_PATH), shell=True)

                ### ---- [ Install AOVPNS by moving all the files from the temp. folder to the main folder ] ---- ###
                shutil.copytree(src=self.TEMP_PATH, dst=self.INSTALL_PATH, dirs_exist_ok=True)

                ### ---- [ Create the command 'aovpns' in /usr/bin ] ---- ###
                # If a file called 'aovpns' already exist, inform the user and delete it
                if os.path.isfile(self.BIN_PATH + 'aovpns'):
                    os.remove(self.BIN_PATH + 'aovpns')
                else:
                    pass

                # Create and write the 'aovpns' file into /usr/bin/
                with open(self.BIN_PATH + 'aovpns', 'x') as aovpns_file:
                    aovpns_file.write(aovpns_command_bin)

                ### ---- [ Apply rights on files ] ---- ###
                sleep(1)
                Process.call('chmod 777 %saovpns' % self.BIN_PATH, shell=True)
                Process.call('chmod 777 -R %s' % self.INSTALL_PATH, shell=True)
                # Deleting the temporary directory
                shutil.rmtree(self.TEMP_PATH)
                sleep(1)
                # Create the environment variable
                set_env_var(var_name=self.aovpns_path_env_var_name, var_value=self.aovpns_path_env_var_value)
            except KeyboardInterrupt:
                Color.pl('\n  {!} Installation process interrupted.')
                # Removing the python cache
                remove_python_cache(pwd=pwd)
                Color.pl('  {!} You must re-run the installation process to install AOVPNS correctly.')
                Color.pl('  {*} Exiting...')
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
            if Configuration.verbose == 3:
                Color.pl('  {§} Check if the AOVPNS\'s repositorie are reachable or not...')
                Color.pl('   {SY1}╰──╼{W} Call the {SY1}is_reachable(){W} function.')

            ## ---------- [ Check if the AOVPNS repositorie on GitHub are reachable or not ] ---------- ##
            GR.is_reachable(args)

            # ---- [ The info box ] ---- #
            Color.pl('''  {*} {underscore}This tool will{W}:
                    \r     {D}[{W}{LL}1{W}{D}]{W} Update your system. %s
                    \r     {D}[{W}{LL}2{W}{D}]{W} Install python-pip.
                    \r     {D}[{W}{LL}3{W}{D}]{W} Create the AOVPNS's folder in {C}%s{W}.
                    \r     {D}[{W}{LL}4{W}{D}]{W} Create the AOVPNS's temporary folder in {C}%s{W} and clone the AOVPNS files, from GitHub, into it.
                    \r     {D}[{W}{LL}5{W}{D}]{W} Move the AOVPNS's files from {C}%s{W} into {C}%s{W}.
                    \r     {D}[{W}{LL}6{W}{D}]{W} Create and install the command {G}aovpns{W} into {C}%s{W}.
                    \r     {D}[{W}{LL}7{W}{D}]{W} Apply all rights on the new files in {C}%s{W} and {C}%saovpns{W}.
            ''' %
                (
                UPDATE_SYSTEM_SKIPED,
                self.INSTALL_PATH,
                self.TEMP_PATH,
                self.TEMP_PATH,
                self.INSTALL_PATH,
                self.BIN_PATH,
                self.INSTALL_PATH,
                self.BIN_PATH
                )
            )
            if args.no_confirm:
                Color.pl('  {?} Do you want to continue? [Y/n] y')
                choice_1='y'
            else:
                choice_1=input(Color.s('  {?} Do you want to continue? [Y/n] '))
            if choice_1.lower() == 'y' or not choice_1:
                try:
                    # ---------- [ System update ] ---------- #
                    if args.skip_update:
                        Color.pl('  {*} System update skiped.')
                        pass
                    else:
                        Color.pl('  {-} Updating your system...')
                        if Configuration.verbose == 3:
                            Color.pl('  {§} Python: {SY1}sleep(0.5){W}')
                        sleep(0.5)
                        if based_distro == 'Arch':
                            Process.call('pacman -Syy')
                        elif based_distro == 'Debian':
                            Process.call('apt update')
                        if Configuration.verbose == 3:
                                Color.pl('  {§} Python: {SY1}sleep(1){W}')
                        sleep(1)

                    # ---------- [ Tools installation ] ---------- #
                    if based_distro == 'Arch':
                        for arch_package_name in self.arch_package_list:
                            if package_exists(package=arch_package_name):
                                Color.pl('  {*} The package \'%s\' are already installed.' % arch_package_name)
                            else:
                                Color.pl('  {-} Installing \'%s\' package...' % arch_package_name)
                                Process.call('pacman --needed --noconfirm -v -S %s'% arch_package_name, shell=True)
                    elif based_distro == 'Debian':
                        for debian_package_name in self.debian_package_list:
                            if package_exists(package=debian_package_name):
                                Color.pl('  {*} The package \'%s\' are already installed.' % debian_package_name)
                            else:
                                Color.pl('  {-} Installing \'%s\' package...' % debian_package_name)
                                Process.call('apt install -y %s'% debian_package_name, shell=True)

                    ## ------ [ PIP package ] ------ ##
                    for pip_package_name in self.pip_package_name_list:
                        try:
                            pkg_resources.get_distribution(pip_package_name)
                            Color.pl('  {*} PIP\'s package \'%s\' already intsalled.' % pip_package_name)
                        except pkg_resources.DistributionNotFound:
                            Color.pl('  {-} Installing \'%s\' PIP\'s package...' % pip_package_name)
                            Process.call('pip install %s' % pip_package_name, shell=True)

                    # ---------- [ AOVPNS installation ] ---------- #
                    if os.path.isdir(self.INSTALL_PATH):
                        Color.pl('  {$} A AOVPNS instance already exist in %s.' % self.INSTALL_PATH)
                        if args.no_confirm:
                            Color.pl('  {?} Do you want to replace it? [Y/n] y')
                            choice_2 = 'y'
                        else:
                            choice_2 = input(Color.s('  {?} Do you want to replace it? [Y/n] '))
                        if choice_2.lower() == 'y' or not choice_2:
                            Color.pl('  {-} Deleting current AOVPNS files...')
                            if Configuration.verbose == 3:
                                Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(%s){W}' % self.INSTALL_PATH)
                            shutil.rmtree(self.INSTALL_PATH)
                            if os.path.isdir(self.TEMP_PATH):
                                if Configuration.verbose  == 3:
                                    Color.pl('  {§} AOVPNS\'s temporary folder detected.')
                                    Color.pl('  {§} Remove it...')
                                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(self.TEMP_PATH){W}')
                                shutil.rmtree(self.TEMP_PATH)
                        else:
                            Color.pl('  {!} You must remove the current AOVPNS files by yourself for continue the install process!')
                            Color.pl('  {*} Exiting...')
                            # Removing the python cache
                            remove_python_cache(pwd=pwd)
                            if Configuration.verbose == 3:
                                Color.pl(' {§} Exiting with the exit code: {R}1{W}')
                                Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                            sys.exit(1)

                    ## ------ [ AOVPNS files ] ------ ##
                    Color.pl('  {-} Installing AOVPNS files...')

                    ### ---- [ Create the main folder in /usr/share/ ] ---- ###
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Creating main folder ({C}%s{W})...' % self.INSTALL_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.makedirs(INSTALL_PATH, mode=0o777){W}')
                    os.makedirs(self.INSTALL_PATH, mode=0o777)    # Create the main directory of AOVPNS

                    ### ---- [ Create the temp folder that be use to download the latest AOVPNS version from GitHub
                    #          in it and install AOVPNS from this folder                                            ] ---- ###
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Creating temporary folder ({C}%s{W})...' % self.TEMP_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.makedirs(self.TEMP_PATH, mode=0o777){W}')
                    os.makedirs(self.TEMP_PATH, mode=0o777)

                    ### ---- [ Clone the latest version of AOVPNS into the temp. folder ] ---- ###
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Cloning files from GitHub to the temporary directory...')
                    Process.call('git clone %s --verbose --branch %s %s' % (self.REPO_URL , self.REPO_BRANCH , self.TEMP_PATH), shell=True)

                    ### ---- [ Install AOVPNS by moving all the files from the temp. folder to the main folder ] ---- ###
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Copying all files from the AOVPNS\'s temporary folder to the main directory ({C}%s{W})...' % self.INSTALL_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.copytree(src=self.TEMP_PATH, dst=INSTALL_PATH, dirs_exist_ok=True){W}')
                    shutil.copytree(src=self.TEMP_PATH, dst=self.INSTALL_PATH, dirs_exist_ok=True)

                    ### ---- [ Create the command 'aovpns' in /usr/bin ] ---- ###
                    # If a file called 'aovpns' already exist, inform the user and delete it
                    if os.path.isfile(self.BIN_PATH + 'aovpns'):
                        if Configuration.verbose == 3:
                            Color.pl('  {§} The aovpns command already exist in {C}%s{W}' % self.BIN_PATH)
                            Color.pl('  {§} Remove it...')
                            Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.remove(self.BIN_PATH + \'aovpns\'){W})')
                        os.remove(self.BIN_PATH + 'aovpns')
                    else:
                        pass
                    # Create the command 'aovpns' in /usr/bin/
                    Color.pl('  {-} Create the {G}aovpns{W} command into {C}%s{W}...' % self.BIN_PATH)

                    # Create and write the 'aovpns' file into /usr/bin/
                    with open(self.BIN_PATH + 'aovpns', 'x') as aovpns_file:
                        aovpns_file.write(aovpns_command_bin)

                    ### ---- [ Apply rights on files ] ---- ###
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
                        Color.pl('  {#} Python: {SY1}sleep(1){W}')
                    sleep(1)
                    # Create the environment variable
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Create the {C}{bold}AOVPNS_INSTALL_PATH{W} environment variable...')
                        Color.pl('  {§} Call the {P}set_env_var(){W} function.')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}set_env_var(name=self.aovpns_path_env_var_name, value=self.aovpns_path_env_var_value){W}')
                    set_env_var(var_name=self.aovpns_path_env_var_name, var_value=self.aovpns_path_env_var_value)

                    # -------------------- [ FINISH ] -------------------- #
                    Color.pl('  {+} AOVPNS are successfully installed on your system.')
                    Color.pl('  {*} You need to restart your machine to use AOVPNS normaly.')
                    choice_3 = input(Color.s('  {?} Do you want to reboot your machine now? [y/n] '))
                    if choice_3.lower() == 'y':
                        # Removing the python cache
                        remove_python_cache(pwd=pwd)
                        Color.pl('  {-} Rebooting the machine...')
                        Process.call('reboot', shell=True)
                    else:
                        # Removing the python cache
                        remove_python_cache(pwd=pwd)
                        Color.pl('  {*} Now you can run the command {G}aovpns{W} anywhere in the terminal.')
                        if Configuration.verbose == 3:
                            Color.pl('  {§} Exiting with the exit code: {G}0{W}')
                            Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(0){W}')
                        sys.exit(0)
                except KeyboardInterrupt:
                    Color.pl('\n  {!} Installation process interrupted.')
                    Color.pl('  {*} You must re-run the installation process to install AOVPNS correctly.')
                    Color.pl('  {-} Exiting...')
                    # Removing the python cache
                    remove_python_cache(pwd=pwd)
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                    sys.exit(1)
            else:
                Color.pl('  {*} Aborted')
                if Configuration.verbose == 3:
                    Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                sys.exit(1)

def entry_point(args, pwd):
    try:
        Installer(args=args, pwd=pwd)
    except EOFError:
        Color.pl('\n  {*} Aborted')
        # Removing the python cache
        remove_python_cache(pwd=pwd)
        if Configuration.verbose == 3:
            Color.pl('  {§} Exiting with the exit code: {R}1{W}')
            Color.pl('    {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
        sys.exit(1)
    except KeyboardInterrupt:
        Color.pl('\n  {*} Aborted')
        # Removing the python cache
        remove_python_cache(pwd=pwd)
        if Configuration.verbose == 3:
            Color.pl('  {§} Exiting with the exit code: {R}1{W}')
            Color.pl('    {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
        sys.exit(1)
