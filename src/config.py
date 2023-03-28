#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ config.py                 [Created: 2023-03-28 |  8:35 - AM]  #
#                                       [Updated: 2023-03-28 |  9:28 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The python config file of gitpy                                         #
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
import re
import os
import sys
import platform
import subprocess
import configparser
from time import sleep
from copy import deepcopy
from ipaddress import ip_address
from subprocess import check_output

## Third party libraries
import src.__main__ as __MAIN__
from src.args import Arguments
import src.util.github_repo as GR
from src.util.clear import clear
from src.util.exit_tool import exit_tool
from src.util.colors import Color
from src.util.help_messages import Help_Messages as HM
from src.util.internet_check import internet_check

# Main
class Configuration(object):
    '''
        The configuration class of GitPy. Where all the variables are stored.
        This class is used to parse all arguments from the 'ars.py' file (The "Arguments"' class).
    '''

    # Verbosity level: 1 = executed commands, 2 = executed commands and stdout/stderr, 
    # 3 = level 1 + 2 + more information about the execution of python functions
    verbose = 0

    program_name = 'gitpy'

    # The main version of GitPy
    VERSION = '0.0.0.1'

    # The GitPy's version from the Github's repo. Will be attributed by the 'compare_version' 
    # function from the 'github_repo.py' file
    REPO_VERSION = None

    # The version's message for the -V/--version argument
    version_message = VERSION
    version_message_verbose = '''GitPy %s
    \r
    \rCopyright (C) 2021-2023 PSociety™, All rights reserved. By Thomas Pellissier (MyMeepSQL)
    \rLicense GPLv3+: GNU GPL version 3 or later <https://www.gnu.org/licenses/gpl-3.0.html>.
    \rThis is free software; you can modify the program and share it as long as the {R}original authors
    \rappears in credit and the program is of the same license{W}.
    \r
    \rThis tool was written by Thomas Pellissier (MyMeepSQL).''' % VERSION

    # Where GitPy is installed
    DEFAULT_INSTALL_PATH = r'/opt/gitpy/'

    # For the environment variables
    gitpy_path_env_var_name = 'GITPY_INSTALL_PATH'
    gitpy_path_env_var_value = DEFAULT_INSTALL_PATH

    # The logs file
    # LOG_FILE_PATH = DEFAULT_INSTALL_PATH + r'logs'

    # The bin directory of GitPy
    BIN_PATH = r'/usr/bin/'

    # The GitPy temporary directory
    TEMP_PATH = r'/tmp/gitpy/'

    # Github's repo settings
    REPO_URL = 'https://github.com/MyMeepSQL/gitpy.git'
    REPO_BRANCH = 'master'
    REPO_MASTER_BRANCH = 'master'
    REPO_METADATA_URL = 'https://raw.githubusercontent.com/MyMeepSQL/GitPy/master/metadata.json'

    @classmethod
    def load_arguments(cls, pwd):
        '''
            Load argument and parse them to the specific function.
        '''
        # Get the arguments
        args = Arguments.get_arguments()

        # if the user run gitpy with -q/--quiet and -v/--verbose options
        if args.quiet and args.verbose:
            __MAIN__.GitPy.Banner()
            print()
            Color.pl('  {!} The -q/--quiet and -v/--verbose option are not compatible together.')
            exit_tool(1)



        # Set the verbosity level
        if args.verbose == 1:
            cls.verbose = 1

        if args.verbose == 2:
            cls.verbose = 2

        if args.verbose == 3:
            cls.verbose = 3

        # Parse the arguments
        cls.parse_informations_args(args)
        cls.first_args_to_parse(args)
        cls.parse_main_args(args, pwd)
        cls.parse_installation_args(args, pwd)
        cls.parse_miscellaneous_args(args, pwd)
        # cls.parse_test_args(args)

    @classmethod
    def first_args_to_parse(cls,args):
        '''
            Parse the first arguments that should be parsed before the others.
        '''
        if args.install_path == '0':
            __MAIN__.GitPy.Banner()
            print()
            Color.pl('  {!} You must specify a path where GitPy will be installed.')
            exit_tool(1)

    # -------------------- [ MAIN ARGUMENTS ] -------------------- #
    @classmethod
    def parse_main_args(cls, args, pwd):
        '''
            Parse all main arguments.
        '''
        if args.console:
            Color.pl('  {-} Starting the GitPy\'s console...')
            sleep(1)
            # Call the main console of GitPy
            from src.core.console import Main_Console
            Main_Console(pwd=pwd)

        if args.cli:
            Color.pl('  {!} The GitPy\'s CLI is not available yet.')
            exit_tool(1)

    # -------------------- [ INSTALLATION ARGUMENTS ] -------------------- #
    @classmethod
    def parse_installation_args(cls, args, pwd):
        '''
            Parse all installation arguments
        '''
        if args.install:
            from src.core.installer import entry_point as Installer
            Installer(args, pwd=pwd)

        if args.uninstall:
            from src.core.uninstaller import entry_point as Uninstaller
            Uninstaller(args=args, pwd=pwd)

    # -------------------- [ INFORMATIONS ARGUMENTS ] -------------------- #
    @classmethod
    def parse_informations_args(cls, args):
        '''
            Parse all informations arguments
        '''
        if args.help:
            # Show more help for wich command
            # ---------- [ Main options ] ---------- #
            if args.console:
                __MAIN__.GitPy.Banner()
                HM.option_console()
                print()
                GR.compare_version()
                exit_tool(0)
            if args.cli:
                __MAIN__.GitPy.Banner()
                HM.option_cli()
                print()
                GR.compare_version()
                exit_tool(0)

            # ---------- [ Installation options ] ---------- #
            if args.install:
                __MAIN__.GitPy.Banner()
                HM.option_install()
                print()
                GR.compare_version()
                exit_tool(0)
            if args.uninstall:
                __MAIN__.GitPy.Banner()
                HM.option_uninstall()
                print()
                GR.compare_version()
                exit_tool(0)
            if args.skip_update:
                __MAIN__.GitPy.Banner()
                HM.option_skip_update()
                print()
                GR.compare_version()
                exit_tool(0)
            if args.offline:
                __MAIN__.GitPy.Banner()
                HM.option_offline()
                print()
                GR.compare_version()
                exit_tool(0)
            if args.install_path:
                __MAIN__.GitPy.Banner()
                HM.option_install_path()
                print()
                GR.compare_version()
                exit_tool(0)

            # ---------- [ Output options ] ---------- #
            if args.quiet:
                __MAIN__.GitPy.Banner()
                HM.option_quiet()
                print()
                GR.compare_version()
                exit_tool(0)

            if args.verbose:
                __MAIN__.GitPy.Banner()
                HM.option_verbose()
                print()
                GR.compare_version()
                exit_tool(0)

            # ---------- [ Additional options ] ---------- #
            if args.no_confirm:
                __MAIN__.GitPy.Banner()
                HM.option_no_confirm()
                print()
                GR.compare_version()
                exit_tool(0)

            # ---------- [ Informations options ] ---------- #
            if args.info:
                __MAIN__.GitPy.Banner()
                HM.option_info()
                print()
                GR.compare_version()
                exit_tool(0)
            if args.version:
                __MAIN__.GitPy.Banner()
                HM.option_version()
                print()
                GR.compare_version()
                exit_tool(0)

            # ---------- [ Miscellaneous options ] ---------- #
            if args.update:
                __MAIN__.GitPy.Banner()
                HM.option_update()
                print()
                GR.compare_version()
                exit_tool(0)
            if args.force_update:
                __MAIN__.GitPy.Banner()
                HM.option_force_update()
                print()
                GR.compare_version()
                exit_tool(0)
            if args.show_env_var:
                __MAIN__.GitPy.Banner()
                HM.option_show_env_var()
                print()
                GR.compare_version()
                exit_tool(0)
            if args.remove_cache:
                __MAIN__.GitPy.Banner()
                HM.option_remove_cache()
                print()
                GR.compare_version()
                exit_tool(0)
            

            # ---- No options ---- #
            else:
                __MAIN__.GitPy.Banner()
                HM.main_help_msg()
                print()
                GR.compare_version()
                exit_tool(0)
    
        if args.info:
            from src.util.informations import Informations
            __MAIN__.GitPy.Banner()
            Informations()
            print()
            GR.compare_version()
            exit_tool(0)

        if args.version:
            if args.verbose:
                Color.pl(cls.version_message_verbose)
            else:
                Color.pl(cls.version_message)
            exit_tool(0)

    # -------------------- [ MISCELLANEOUS ARGUMENTS ] -------------------- #
    @classmethod
    def parse_miscellaneous_args(cls, args, pwd):
        '''
            Parse all miscellaneous arguments
        '''
        if args.update:
            from src.core.updater import entry_point as Updater
            Updater(args, pwd=pwd)

            # if args.regenerate_config:
            #     if os.path.isdir(cls.DEFAULT_INSTALL_PATH):
            #         if os.path.isfile(cls.DEFAULT_INSTALL_PATH):
            #             Color.pl('  {$} A configuration file is already present')
            #             choice_1=input(Color.s('  {?} Do you want to continue? [Y/n] '))

            #             if choice_1.islower() == 'y' or not choice_1:
            #                 Color.pl('  {-} Deleting old config file...')

            #                 if args.verbose:
            #                     if args.verbose > 1:
            #                         Color.pl('   {P}╰──╼{W} Python: {P}os.remove(cls.CONFIG_FILE_PATH){W}')

            #                 os.remove(cls.DEFAULT_INSTALL_PATH)

            #                 Color.pl('  {-} Generating the config file...')

            #                 if args.verbose:
            #                     if args.verbose > 1:
            #                         Color.pl('''   {P}╰──╼{W} Python: {P}with open(cls.CONFIG_FILE_PATH, 'w') as config_file:
            #                                 \r                    config_file.write(cls.CONFIG_FILE_CONTENT){W}''')

            #                 with open(cls.DEFAULT_INSTALL_PATH, 'w') as config_file:
            #                     config_file.write(cls.DEFAULT_INSTALL_PATH)

            #                 Color.pl('  {+} Config file re-generated.')
            #                 exit_tool(0)

            #             else:
            #                 Color.pl('  {*} Remove the configuration file yourself and re-run the the create config command.')
            #                 exit_tool(1)

            #         else:
            #             Color.pl('  {*} The config file was not found')
            #             sleep(0.5)
            #             Color.pl('  {-} Generating the config file...')
            #             sleep(1)

            #             if args.verbose:
            #                 if args.verbose > 1:
            #                     Color.pl('''   {P}╰──╼{W} Python: {P}with open(cls.CONFIG_FILE_PATH, 'w') as config_file:
            #                             \r                    config_file.write(cls.CONFIG_FILE_CONTENT){W}''')

            #             with open(cls.DEFAULT_INSTALL_PATH, 'w') as config_file:
            #                 config_file.write(cls.DEFAULT_INSTALL_PATH)

            #             Color.pl('  {+} Config file generated.')
            #             exit_tool(0)

            #     else:
            #         Color.pl('  {!} GitPy are not installed on your system!')
            #         Color.pl('  {*} Run {G}conpro --install{W} for install GitPy on your system')
            #         exit_tool(1)

        if args.show_env_var:
            try:
                GITPY_PATH = os.environ[cls.gitpy_path_env_var_name]
                Color.pl('%s=%s' % (cls.gitpy_path_env_var_name, GITPY_PATH))
            except KeyError:
                Color.pl('  {!} GitPy is not installed on this machine.')
                Color.pl('  {*} Because the {C}{bold}GITPY_INSTALL_PATH{W} environment variable is not set.')
                exit_tool(1)
            # if args.show_config:
            #     # Open the file in read mode
            #     with open(cls.CONFIG_FILE_PATH, "r") as config_file:
            #         # Read the file content
            #         content=config_file.read()
            #         # Prompt the file content
            #         Color.pl(content)
            #         # Close the file
            #         content=config_file.close()
        if args.remove_cache:
            from src.util.remove_python_cache import remove_python_cache
            remove_python_cache(pwd=pwd)

    # @classmethod
    # def parse_test_args(cls, args):
    #     from src.util.process import Process
    #     if args.process:
    #         if args.verbose and args.verbose > 1:
    #             cls.verbose = args.verbose
    #         Process.exists(program='pacman')
    #         Process.call(command='pacman --help', shell=True)
    #         Process.call(command='pacman --dasdd', shell=True)
    #         Process.call('git clone https://github.com/MyMeepSQL/GitPy.git', shell=True)
