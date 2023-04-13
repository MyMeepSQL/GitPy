#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ installer.py              [Created: 2023-03-07 | 10:27 - AM]  #
#                                       [Updated: 2023-04-10 | 14:30 - PM]  #
#---[Info]------------------------------------------------------------------#
#  The installer of GitPy for install GitPy and the                         #
#  dependencies                                                             #
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
import shutil
import platform
import pkg_resources
from time import sleep

## Third party libraries
from src.util.github_repo import GitHub_Repo
from src.__main__ import GitPy
from src.config import Configuration
from src.util.colors import Color
from src.util.process import Process
from src.util.exit_tool import exit_tool
from src.util.env_var import set_env_var
from src.util.based_distro import Based_Distro
from src.util.internet_check import internet_check
from src.util.remove_python_cache import remove_python_cache
from src.util.if_package_exists import package_exists
from src.util.create_bin_file import Create_bin_file
from src.util.check_path import check_folder_path

# Main
class Installer():
    '''
        The installer of GitPy
    '''

    # Variables
    DEFAULT_INSTALL_PATH = Configuration.DEFAULT_INSTALL_PATH
    BIN_PATH = Configuration.BIN_PATH
    TEMP_PATH = Configuration.TEMP_PATH
    INSTALL_PATH = DEFAULT_INSTALL_PATH
    NOTIFICATION_CONFIG_FILE = Configuration.DEFAULT_NOTIFICATION_CONFIG_FILE_PATH
    PROGRAM_NAME = Configuration.PROGRAM_NAME

    # Environment variables
    ## The GitPy's install path
    gitpy_install_path_env_var_name = Configuration.gitpy_install_path_env_var_name
    gitpy_install_path_env_var_value = Configuration.gitpy_install_path_env_var_value

    ## The News Version Notification's config file
    gitpy_path_notification_config_file_env_var_name = Configuration.gitpy_notification_config_file_env_var_name
    gitpy_path_notification_config_file_env_var_value = Configuration.gitpy_notification_config_file_env_var_value

    # Packages list for Arch based distros (pacman)
    arch_package_list = [
        'python-pip',
        'git',
        'curl',
        'wget',
    ]
    # Packages list for Debian based distros (apt)
    debian_package_list = [
        'python3-pip',
        'git',
        'curl',
        'wget',
    ]
    # pip package list 
    pip_package_name_list = [
        'rich',
        'gnureadline',
        'python-crontab',
    ]

    # Github's repo settings
    REPO_CLONE_URL = Configuration.REPO_CLONE_URL
    REPO_BRANCH = Configuration.REPO_BRANCH
    REPO_MASTER_BRANCH = Configuration.REPO_MASTER_BRANCH

    # Main
    def __init__(self, args, pwd):

        self.pwd = pwd

        # Check if the user's platform is a Linux machine or not
        if platform.system() != 'Linux':
            Color.pl(GitPy.Banner())
            print()
            Color.pl('  {!} You tried to run GitPy on a non-linux machine!')
            Color.pl('  {*} GitPy can be run only on a Linux kernel.')
            exit_tool(1,pwd=self.pwd)

        else:
            if os.getuid() != 0:
                Color.pl(GitPy.Banner())
                print()
                Color.pl('  {!} The GitPy Installer must be run as root.')
                Color.pl('  {*} Re-run with sudo or switch to root user.')
                exit_tool(1,pwd=self.pwd)
            else:
                # Distro check
                if Based_Distro() == 'Arch':
                    based_distro = 'Arch'
                    pass

                elif Based_Distro() == 'Debian':
                    based_distro = 'Debian'
                    pass

                else:
                    Color.pl(GitPy.Banner())
                    print()
                    Color.pl('  {!} You\'re not running Arch or Debian variant.')
                    Color.pl('  {*} GitPy can only run on Arch or Debian based distros.')
                    exit_tool(1,pwd=self.pwd)

        if args.skip_update:
            UPDATE_SYSTEM_SKIPED='(Skipped)'

        else:
            UPDATE_SYSTEM_SKIPED=''
            
        if args.install_path:
            self.INSTALL_PATH = ''.join(args.install_path).strip()
            self.INSTALL_PATH = check_folder_path(self.INSTALL_PATH,self.PROGRAM_NAME)
            self.gitpy_install_path_env_var_value = self.INSTALL_PATH
            self.gitpy_path_notification_config_file_env_var_value = self.INSTALL_PATH + 'config/new_version_notification.conf'
            
        # gitpy main file in /usr/bin/
        gitpy_command_bin = Create_bin_file.__init__(path=self.INSTALL_PATH)

        # Main
        if args.quiet:
            # -------------------- [ Quiet installation ] -------------------- #
            try:
                ## System update
                if args.skip_update:
                    pass

                else:
                    sleep(0.5)
                    if based_distro == 'Arch':
                        Process.call('pacman -Syy')

                    elif based_distro == 'Debian':
                        Process.call('apt update')
                    sleep(1)

                ## Tools installation
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

                ## PIP package
                for pip_package_name in self.pip_package_name_list:
                    try:
                        pkg_resources.get_distribution(pip_package_name)

                    except pkg_resources.DistributionNotFound:
                        Process.call('pip install %s' % pip_package_name, shell=True)

                ## GitPy installation
                if os.path.isdir(self.INSTALL_PATH):
                    shutil.rmtree(self.INSTALL_PATH)

                    if os.path.isdir(self.TEMP_PATH):
                        shutil.rmtree(self.TEMP_PATH)

                ## GitPy files
                ### Create the main folder in /usr/share/
                os.makedirs(self.INSTALL_PATH, mode=0o777)    # Create the main directory of GitPy

                ### Create the temp folder that be use to download the latest GitPy version from GitHub
                ### in it and install GitPy from this folder
                os.makedirs(self.TEMP_PATH, mode=0o777)

                ### Clone the latest version of GitPy into the temp. folder
                Process.call('git clone %s --verbose --branch %s %s' % (self.REPO_CLONE_URL , self.REPO_BRANCH , self.TEMP_PATH), shell=True)

                ### Install GitPy by moving all the files from the temp. folder to the main folder
                shutil.copytree(src=self.TEMP_PATH, dst=self.INSTALL_PATH, dirs_exist_ok=True)

                ### Create the command 'gitpy' in /usr/bin
                # If a file called 'gitpy' already exist, inform the user and delete it
                if os.path.isfile(self.BIN_PATH + 'gitpy'):
                    os.remove(self.BIN_PATH + 'gitpy')
                else:
                    pass

                # Create and write the 'gitpy' file into /usr/bin/
                with open(self.BIN_PATH + 'gitpy', 'x') as gitpy_file:
                    gitpy_file.write(gitpy_command_bin)

                ### Apply rights on files
                sleep(1)
                Process.call('chmod 777 %sgitpy' % self.BIN_PATH, shell=True)
                Process.call('chmod 777 -R %s' % self.INSTALL_PATH, shell=True)
                # Deleting the temporary directory
                shutil.rmtree(self.TEMP_PATH)
                sleep(1)
                # Create the environment variable

                ## The environment variable is used to know where GitPy is installed
                set_env_var(var_name=self.gitpy_install_path_env_var_name, var_value=self.gitpy_install_path_env_var_value)

                ## The environment variable is used to know where the News Version Notification config file is
                set_env_var(var_name=self.gitpy_path_notification_config_file_env_var_name, var_value=self.gitpy_path_notification_config_file_env_var_value)
    
            except KeyboardInterrupt:
                Color.pl('\n  {!} Installation process interrupted.')
                Color.pl('  {!} You must re-run the installation process to install GitPy correctly.')  
                # Exit and removing the python cache
                exit_tool(1,pwd=self.pwd)

        else:
            # -------------------- [ No quiet installation ] -------------------- #
            Color.pl(GitPy.Banner())
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
                exit_tool(1,pwd=self.pwd)

            if Configuration.verbose == 3:
                Color.pl('  {§} Check if the GitPy\'s repositorie are reachable or not...')
                Color.pl('   {SY1}╰──╼{W} Call the {SY1}is_reachable(){W} function.')

            ## Check if the GitPy repositorie on GitHub are reachable or not
            GitHub_Repo.is_reachable(args)

            # The info box
            Color.pl('''  {*} {underscore}This tool will{W}:
                    \r     {D}[{W}{LL}1{W}{D}]{W} Update your system. %s
                    \r     {D}[{W}{LL}2{W}{D}]{W} Install python-pip.
                    \r     {D}[{W}{LL}3{W}{D}]{W} Create the GitPy's folder in {C}%s{W}.
                    \r     {D}[{W}{LL}4{W}{D}]{W} Create the GitPy's temporary folder in {C}%s{W} and clone the GitPy files, from GitHub, into it.
                    \r     {D}[{W}{LL}5{W}{D}]{W} Move the GitPy's files from {C}%s{W} into {C}%s{W}.
                    \r     {D}[{W}{LL}6{W}{D}]{W} Create and install the command {G}gitpy{W} into {C}%s{W}.
                    \r     {D}[{W}{LL}7{W}{D}]{W} Apply all rights on the new files in {C}%s{W} and {C}%sgitpy{W}.
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
                choice_1 = 'y'

            else:
                choice_1 = input(Color.s('  {?} Do you want to continue? [Y/n] '))

            if choice_1.lower() == 'y' or not choice_1:
                try:
                    # System update
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

                    # Tools installation
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

                    ## PIP package
                    for pip_package_name in self.pip_package_name_list:
                        try:
                            pkg_resources.get_distribution(pip_package_name)
                            Color.pl('  {*} PIP\'s package \'%s\' already intsalled.' % pip_package_name)

                        except pkg_resources.DistributionNotFound:
                            Color.pl('  {-} Installing \'%s\' PIP\'s package...' % pip_package_name)
                            Process.call('pip install %s' % pip_package_name, shell=True)

                    # GitPy installation
                    if os.path.isdir(self.INSTALL_PATH):
                        Color.pl('  {$} A GitPy instance already exist in {C}%s{W}.' % self.INSTALL_PATH)

                        if args.no_confirm:
                            Color.pl('  {?} Do you want to replace it? [Y/n] y')
                            choice_2 = 'y'

                        else:
                            choice_2 = input(Color.s('  {?} Do you want to replace it? [Y/n] '))

                        if choice_2.lower() == 'y' or not choice_2:
                            Color.pl('  {-} Deleting current GitPy files...')
                            
                            if Configuration.verbose == 3:
                                Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(%s){W}' % self.INSTALL_PATH)

                            shutil.rmtree(self.INSTALL_PATH)

                            if os.path.isdir(self.TEMP_PATH):
                                if Configuration.verbose  == 3:
                                    Color.pl('  {§} GitPy\'s temporary folder detected.')
                                    Color.pl('  {§} Remove it...')
                                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(self.TEMP_PATH){W}')

                                shutil.rmtree(self.TEMP_PATH)

                        else:
                            Color.pl('  {!} You must remove the current GitPy files by yourself for continue the install process!')
                            # Exit and removing the python cache
                            exit_tool(1,pwd=self.pwd)

                    ## GitPy files
                    Color.pl('  {-} Installing GitPy files...')

                    ### Create the main directory of GitPy
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Creating main folder ({C}%s{W})...' % self.INSTALL_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.makedirs(INSTALL_PATH, mode=0o777){W}')

                    os.makedirs(self.INSTALL_PATH, mode=0o777)    

                    ### Create the temp folder that be use to download the latest GitPy version from GitHub
                    ### in it and install GitPy from this folder
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Creating temporary folder ({C}%s{W})...' % self.TEMP_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.makedirs(self.TEMP_PATH, mode=0o777){W}')

                    os.makedirs(self.TEMP_PATH, mode=0o777)

                    ### Clone the latest version of GitPy into the temp. folder
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Cloning files from GitHub to the temporary directory...')
                    Process.call('git clone %s --verbose --branch %s %s' % (self.REPO_CLONE_URL , self.REPO_BRANCH , self.TEMP_PATH), shell=True)

                    ### Install GitPy by moving all the files from the temp. folder to the main folder
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Copying all files from the GitPy\'s temporary folder to the main directory ({C}%s{W})...' % self.INSTALL_PATH)
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}shutil.copytree(src=self.TEMP_PATH, dst=INSTALL_PATH, dirs_exist_ok=True){W}')
                    shutil.copytree(src=self.TEMP_PATH, dst=self.INSTALL_PATH, dirs_exist_ok=True)

                    ### Create the command 'gitpy' in /usr/bin
                    ### If a file called 'gitpy' already exist, inform the user and delete it
                    if os.path.isfile(self.BIN_PATH + 'gitpy'):
                        if Configuration.verbose == 3:
                            Color.pl('  {§} The gitpy command already exist in {C}%s{W}' % self.BIN_PATH)
                            Color.pl('  {§} Remove it...')
                            Color.pl('   {SY1}╰──╼{W} Python: {SY1}os.remove(self.BIN_PATH + \'gitpy\'){W})')
                        os.remove(self.BIN_PATH + 'gitpy')

                    else:
                        pass

                    # Create the command 'gitpy' in /usr/bin/
                    Color.pl('  {-} Create the {G}gitpy{W} command into {C}%s{W}...' % self.BIN_PATH)

                    # Create and write the 'gitpy' file into /usr/bin/
                    with open(self.BIN_PATH + 'gitpy', 'x') as gitpy_file:
                        gitpy_file.write(gitpy_command_bin)

                    ### Apply rights on files
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
                        Color.pl('  {#} Python: {SY1}sleep(1){W}')

                    sleep(1)

                    # Create the environment variable
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Create the {C}{bold}%s{W} environment variable...' % self.gitpy_install_path_env_var_name)
                        Color.pl('  {§} Call the {P}set_env_var(){W} function.')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}set_env_var(name=self.gitpy_install_path_env_var_name, value=self.gitpy_install_path_env_var_value){W}')

                        ## The environment variable is used to know where GitPy is installed
                        set_env_var(var_name=self.gitpy_install_path_env_var_name, var_value=self.gitpy_install_path_env_var_value)

                    if Configuration.verbose == 3:
                        Color.pl('  {§} Create the {C}{bold}%s{W} environment variable...' % self.gitpy_path_notification_config_file_env_var_name)
                        Color.pl('  {§} Call the {P}set_env_var(){W} function.')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}set_env_var(name=self.gitpy_path_notification_config_file_env_var_name, value=self.gitpy_path_notification_config_file_env_var_value){W}')

                        ## The environment variable is used to know where the News Version Notification config file is
                        set_env_var(var_name=self.gitpy_path_notification_config_file_env_var_name, var_value=self.gitpy_path_notification_config_file_env_var_value)
                    
                    # -------------------- [ FINISH ] -------------------- #
                    Color.pl('  {+} GitPy are successfully installed on your system.')
                    Color.pl('  {*} You need to restart your machine to use GitPy normaly.')
                    reboot = input(Color.s('  {?} Do you want to reboot your machine now? [y/n] '))

                    if reboot.lower() == 'y':
                        # Removing the python cache
                        remove_python_cache(pwd=pwd)
                        Color.pl('  {-} Rebooting the machine...')
                        Process.call('reboot', shell=True)

                    else:
                        Color.pl('  {*} Now you can run the command {G}gitpy{W} anywhere in the terminal.')
                        # Exit and removing the python cache
                        exit_tool(0,pwd=self.pwd)

                except KeyboardInterrupt:
                    Color.pl('\n  {!} Installation process interrupted.')
                    Color.pl('  {*} You must re-run the installation process to install GitPy correctly.')
                    # Exit and removing the python cache
                    exit_tool(1,pwd=self.pwd)

            else:
                Color.pl('  {*} Aborted')
                # Exit and removing the python cache
                exit_tool(1,pwd=self.pwd)

def entry_point(args, pwd):
    try:
        Installer(args=args, pwd=pwd)

    except EOFError:
        Color.pl('\n  {*} Aborted')
        # Exit and removing the python cache
        exit_tool(1,pwd=pwd)
        
    except KeyboardInterrupt:
        Color.pl('\n  {*} Aborted')
        # Exit and removing the python cache
        exit_tool(1,pwd=pwd)
