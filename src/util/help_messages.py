#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ help_messages.py          [Created: 2023-02-21 | 10:26 - AM]  #
#                                       [Updated: 2023-02-28 |  9:12 - AM]  #
#---[Info]------------------------------------------------------------------#
#  All help messages for AOVPNS                                             #
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
from time import sleep

## Third party libraries
import src.config as config
from src.args import Arguments
from src.util.colors import Color

# Main
class Help_Messages():
    '''
    All help messages for: the 'aovpns' command, the main console and the CLI environment.
    '''
    def main_help_msg():
        '''
        The help message of the aovpns command (aovpns -h/--help)
        '''
        Color.pl('''
        \r{SB2}{bold}VPN options{W}:
        \r============

        \r  Options                              Description
        \r  -------                              -----------
        \r       --console                       Start the main console of AOVPNS.
        \r       --cli                           Start the CLI environment of AOVPNS.

        \r{SB2}{bold}Installation options{W}:
        \r=====================

        \r  Options                             DescriptionAOVPNS
        \r  -------                             -----------
        \r       --install                [+]   Install AOVPNS with all depencies on your system.
        \r       --uninstall              [+]   Uninstall AOVPNS from your system.
 
        \r       --skip-update                  Skip the system update phase during the installation of AOVPNS.
        \r       --offline                      Install AOVPNS with the local file already downloaded
        \r                                      (default: {G}download new files from GitHub{W}).
        \r  -iP, --install-path [PATH]          Chose where the AOVPNS will be install on the system
        \r                                      (default: {G}%s{W}).

        \r{SB2}{bold}Output options{W}:
        \r===============

        \r  Options                             Description
        \r  -------                             -----------
        \r  -q,  --quiet                        Prevent header from displaying. {O}Warning{W}: bypass any "Are your sure?"
        \r                                      message!
        \r  -v [LEVEL], --verbose [LEVEL]       Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).

        \r{SB2}{bold}Additional options{W}:
        \r===================

        \r  Options                             Description
        \r  -------                             -----------
        \r  -y,  --no-confirm                   Bypass any and all "Are you sure?" messages.

        \r{SB2}{bold}Informations options{W}:
        \r=====================

        \r  Options                             Description
        \r  -------                             -----------
        \r       --info                         Show more informations about AOVPNS and exit.
        \r  -h,  --help                   [+]   Show this help message and exit or show more help for a option.
        \r  -V,  --version                      Show program's version and exit.

        \r{SB2}{bold}Miscellaneous options{W}:
        \r======================

        \r  Options                             Description
        \r  -------                             -----------
        \r  -u,  --update                 [+]   Update the AOVPNS directly from GitHub.
        \r       --show-config                  Prompt the content of the config file.
        \r       --show-env-var                 Prompt the value of the {C}{bold}AOVPNS_INSTALL_PATH{W} environment variable.
        \r       --remove-cache           [+]   Delete python cache from the AOVPNS directory.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns <OPTIONS>

        \r  Others
        \r  ------
        \r  Report all bugs to <thomas.pellissier.pro@proton.me> or open an issue at <https://github.com/MyMeepSQL/aovpns/issues>.
        \r  The options with the [+] mean that it may require additional option(s).
        \r  If you want more details about a command, run: {G}aovpns --help <OPTION>{W}''' % config.Configuration.DEFAULT_INSTALL_PATH)


    # -------------------- [ Main options ] -------------------- #
    def option_cli():
        '''
        The help message for the --cli option
        '''
        Color.pl('''
        \r{SB2}{bold}CLI option{W}:
        \r===========

        \r  Category
        \r  --------
        \r  Main options

        \r  Description
        \r  -----------
        \r  Start the CLI environment of AOVPNS. The CLI environment of AOVPNS
        \r  work like a shell, you can use the command like you do in a shell.
        \r  Inspired by the Metasploit Framework.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns --cli''')

    def option_console():
        '''
        The help message for the --console option
        '''
        Color.pl('''
        \r{SB2}{bold}Console option{W}:
        \r===============

        \r  Category
        \r  --------
        \r  Main options

        \r  Description
        \r  -----------
        \r  Start the main console of AOVPNS. This console work like a choice
        \r  menu console. Inspired by the Social Engineering Toolkit (SET).

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns --console''')


    # -------------------- [ Installation options ] -------------------- #
    def option_install():
        '''
        The help message for the --install option
        '''
        Color.pl('''
        \r{SB2}{bold}Install option{W}:
        \r===============

        \r  Category
        \r  --------
        \r  Installation options

        \r  Description
        \r  -----------
        \r  Install AOVPNS on your system with all of his depencies.

        \r  Options                         Description
        \r  -------                         -----------
        \r              --skip-update       Skip the system update phase during the installation of AOVPNS.
        \r  -y,         --noconfirm         Bypass any and all "Are you sure?" messages.
        \r  -q,         --quiet             Prevent header from displaying. {O}Warning{W}: bypass any "Are your sure?"
        \r                                  message!
        \r  -v [LEVEL], --verbose [LEVEL]   Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns --install [OPTIONS]''')

    def option_uninstall():
        '''
        The help message for the --uninstall option
        '''
        Color.pl('''
        \r{SB2}{bold}Uninstall option{W}:
        \r=================

        \r  Category
        \r  --------
        \r  Installation options

        \r  Description
        \r  -----------
        \r  Remove AOVPNS from your system (do not remove depencies)

        \r  Options                         Description
        \r  -------                         -----------
        \r  -y,         --noconfirm         Bypass any and all "Are you sure?" messages.
        \r  -q,         --quiet             Prevent header from displaying. {O}Warning{W}: bypass any "Are your sure?"
        \r                                  message!
        \r  -v [LEVEL], --verbose [LEVEL]   Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns --uninstall [OPTIONS]''')

    def option_skip_update():
        '''
        The help message for the --skip-update option
        '''
        Color.pl('''
        \r{SB2}{bold}Skip update option{W}:
        \r===================

        \r  Category
        \r  --------
        \r  Installation options

        \r  Description
        \r  -----------
        \r  Do no ask "Are your sure?" every time a choice appears.

        \r  Options           Description
        \r  -------           -----------
        \r  --install         Install AOVPNS with all depencies on your system.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns --install --skip-update''')

    def option_offline():
        '''
        The help message for the --offline option
        '''
        Color.pl('''
        \r{SB2}{bold}Offline option{W}:
        \r===============

        \r  Category
        \r  --------
        \r  Installation options

        \r  Description
        \r  -----------
        \r  Install AOVPNS from the local files (do not download anything).
        \r  By default, the installaiton process will download the latest 
        \r  version of AOVPNS from the GitHub repository.

        \r  Options           Description
        \r  -------           -----------
        \r  --install         Install AOVPNS with all depencies on your system.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns --install --offline''')

    def option_install_path():
        '''
        The help message for the --install-path option
        '''
        Color.pl('''
        \r{SB2}{bold}Install Path option{W}:
        \r====================

        \r  Category
        \r  --------
        \r  Installation options

        \r  Description
        \r  -----------
        \r  You can specify the path where AOVPNS will be installed.
        \r  By default, AOVPNS will be installed in %s.

        \r  Options           Description
        \r  -------           -----------
        \r  --install         Install AOVPNS with all depencies on your system.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns --install -iP <PATH>
        \r    or
        \r  aovpns --install --install-path <PATH>''' % config.Configuration.DEFAULT_INSTALL_PATH)


    # -------------------- [ Output options ] -------------------- #
    def option_quiet():
        '''
        The help message for the -q/--quiet option
        '''
        Color.pl('''
        \r{SB2}{bold}Quiet option{W}:
        \r===================

        \r  Category
        \r  --------
        \r  Output option

        \r  Description
        \r  -----------
        \r  No output given and bypass all "Are you sure?" style message.

        \r  Options           Description
        \r  -------           -----------
        \r      --install     Install AOVPNS with all depencies on your system.
        \r      --uninstall   Uninstall AOVPNS from your system.
        \r  -u, --update      Update the AOVPNS directly from GitHub.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns <OPTIONS> -q
        \r    or
        \r  aovpns <OPTIONS> --quiet''')

    def option_verbose():
        '''
        The help message for the -v/--verbose option
        '''
        Color.pl('''
        \r{SB2}{bold}Verbose option{W}:
        \r===============

        \r  Category
        \r  --------
        \r  Output option

        \r  Description
        \r  -----------
        \r  Prompt more informations during the execution of the script.
        \r  The default value of the verbose level is 0. If you use the -v 
        \r  without any value, the verbose level will be set to 1 (const).

        \r  Options           Description
        \r  -------           -----------
        \r      --install     Install AOVPNS with all depencies on your system.
        \r      --uninstall   Uninstall AOVPNS from your system.
        \r  -u, --update      Update the AOVPNS directly from GitHub.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Verbosity level
        \r  ---------------
        \r  0: No verbose
        \r  1: Display the command executed
        \r  2: Display the command executed and the output
        \r  3: Display the command executed and the output, and display more informations
        \r     about the excecusion of python functions.

        \r  Usage
        \r  -----
        \r  aovpns <OPTIONS> -v [LEVEL]
        \r    or
        \r  aovpns <OPTIONS> --verbose [LEVEL]''')


    # -------------------- [ Additional options ] -------------------- #
    def option_no_confirm():
        '''
        The help message for the -y/--no-confirm option
        '''
        Color.pl('''
        \r{SB2}{bold}No confirmation option{W}:
        \r=======================

        \r  Category
        \r  --------
        \r  Additional options

        \r  Description
        \r  -----------
        \r  Do no ask "Are your sure?" every time a choice appears.

        \r  Options           Description
        \r  -------           -----------
        \r      --install     Install AOVPNS with all depencies on your system.
        \r      --uninstall   Uninstall AOVPNS from your system.
        \r  -u, --update      Update the AOVPNS directly from GitHub.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns <OPTIONS> -y
        \r    or
        \r  aovpns <OPTIONS> --no-confirm''')


    # -------------------- [ Informations options ] -------------------- #
    def option_info():
        '''
        The help message for the --info option
        '''
        Color.pl('''
        \r{SB2}{bold}Information option{W}:
        \r===================

        \r  Category
        \r  --------
        \r  Informations options

        \r  Description
        \r  -----------
        \r  Show all informations about AOVPNS. Version, owner, etc.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns --info''')


    # -------------------- [ Miscellaneous options ] -------------------- #
    def option_update():
        '''
        The help message for the -u/--update option
        '''
        Color.pl('''
        \r{SB2}{bold}Force Update option{W}:
        \r====================

        \r  Category
        \r  --------
        \r  Miscellaneous options

        \r  Description
        \r  -----------
        \r  Download and update the current instance of AOVPNS on the machine with
        \r  the latest stable version of AOVPNS from its repository.

        \r  Options                         Description
        \r  -------                         -----------
        \r  -y,         --noconfirm         Bypass any and all "Are you sure?" messages.
        \r  -q,         --quiet             Prevent header from displaying. {O}Warning{W}: bypass any "Are your sure?"
        \r                                  message!
        \r  -v [LEVEL], --verbose [LEVEL]   Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns -U [OPTIONS]
        \r    or
        \r  aovpns --update [OPTIONS]''')

    def option_force_update():
        '''
        The help message for the -fu/--force-update option
        '''
        Color.pl('''
        \r{SB2}{bold}Update option{W}:
        \r==============

        \r  Category
        \r  --------
        \r  Miscellaneous options

        \r  Description
        \r  -----------
        \r  Update AOVPN even if the AOVPNS' instance version on the machine is 
        \r  already the latest.

        \r  Options        Description
        \r  -------        -----------
        \r  -u,  --update  Update the AOVPNS directly from GitHub.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns -u -fu [OPTIONS]
        \r    or
        \r  aovpns -u --force-update [OPTIONS]
        \r    or
        \r  aovpns --update -fu [OPTIONS]
        \r    or
        \r  aovpns --update --force-update [OPTIONS]''')

    def option_show_env_var():
        '''
        The help message for the --show-env-var option
        '''
        Color.pl('''
        \r{SB2}{bold}Show env var option{W}:
        \r====================

        \r  Category
        \r  --------
        \r  Miscellaneous options

        \r  Description
        \r  -----------
        \r  Show the value of the {C}{bold}AOVPNS_INSTALL_PATH{W} environment variable.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns --show-env-var''')

    def option_remove_cache():
        '''
        The help message for the --remove-cache option 
        '''
        Color.pl('''
        \r{SB2}{bold}Remove cache option{W}:
        \r====================

        \r  Category
        \r  --------
        \r  Miscellaneous options

        \r  Description
        \r  -----------
        \r  Delete all __pycache__ directories and .pyc files of AOVPNS.

        \r  Options                         Description
        \r  -------                         -----------
        \r  -v [LEVEL], --verbose [LEVEL]   Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  aovpns --remove-cache [OPTIONS]''')


    # -------------------- [ Consoles ] -------------------- #
    def console_help_message():
        '''
        The main help message of the main console (not the CLI one)
        '''
        Color.pl('''
        \r{SB2}{bold}Core options{W}:
        \r=============
        
        \r  Options        Description
        \r  -------        -----------
        \r  88, back       Goes back one menu.

        \r{SB2}{bold}Global options{W}:
        \r===============

        \r  Options        Description
        \r  -------        -----------
        \r  help           Show this help message.
        \r  version        Show the version of AOVPNS.
        \r  info           Show more informations about AOVPNS.
        \r  verbose  [+]   Verbosity level: 1-3 (default: {G}0{W})
        \r  99, exit       Exit the console.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Report all bugs to <thomas.pellissier.pro@proton.me> or open an issue at <https://github.com/MyMeepSQL/aovpns/issues>.''')

    def CLI_env_main_help_msg():
        '''
        The main help message of the CLI environment
        '''
        Color.pl('''
        \r {SB2}{bold}Core commands{W}
        \r =============

        \r    Commands        Description
        \r    --------        -----------
        \r    set     [+]     Set a value to the module's variables (run {G}help set{W} for more
        \r                    informations).
        \r    run             Run the loaded module.
        \r    options         Displays global options for current loaded module
        \r    clear           Clear the terminal prompt.
        \r    reset   [+]     Reset the current loaded module' variables
        \r    unload          Unload the current module.
        \r    use     [+]     Load a module for type of conversion.
        \r    show    [+]     Displays all modules.
        \r    help    [+]     Show this help message.
        \r    whoami          Show the your current user.
        \r    version         Show version of AOVPNS.
        \r    exit            Exit the AOVPNS's CLI environment.

        \r {SB2}{bold}Miscellaneous commands{W}
        \r ======================

        \r    Command         Description
        \r    -------         -----------
        \r    update  [+]     Update the current instance of AOVPNS on the machine with the latest
        \r                    stable version of AOVPNS from its repository.

        \r    The commands with the [+] mean that it may require additional arguments.
        \r    If you want more details about a command, run: {G}help <COMMAND>{W}''')
