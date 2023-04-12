#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ help_messages.py          [Created: 2023-02-21 | 10:26 - AM]  #
#                                       [Updated: 2023-04-10 | 13:34 - PM]  #
#---[Info]------------------------------------------------------------------#
#  All help messages for GitPy                                              #
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
from time import sleep

## Third party libraries
from src.util.colors import Color

# Main
class Help_Messages():
    '''
        All help messages for: the 'gitpy' command, the main console and the CLI environment.
    '''

    
    def main_help_msg():
        '''
            The help message of the gitpy command (gitpy -h/--help)
        '''
        from src.config import Configuration

        return '''
        \r{SB2}{bold}Main options{W}:
        \r=============

        \r  Options                                  Description
        \r  -------                                  -----------
        \r              --console                    Start the main console of GitPy.
        \r              --cli                        Start the CLI environment of GitPy.

        \r{SB2}{bold}Installation options{W}:
        \r=====================

        \r  Options                                  Description
        \r  -------                                  -----------
        \r              --install              [+]   Install GitPy with all depencies on your system.
        \r              --uninstall            [+]   Uninstall GitPy from your system.
        
        \r              --skip-update                Skip the system update phase during the installation of GitPy.
        \r              --offline                    Install GitPy with the local file already downloaded
        \r                                           (default: {G}download new files from GitHub{W}).
        \r  -iP [PATH], --install-path [PATH]        Chose where GitPy will be install on the system
        \r                                           (default: {G}%s{W}).

        \r{SB2}{bold}Repository options{W}:
        \r===================

        \r  Options                                  Description
        \r  -------                                  -----------
        \r  -cr,        --check-repo                 Check if the repository in the notification config file have a new 
        \r                                           commit avalable and send a notificarion via mail if it\'s the case.

        \r{SB2}{bold}Output options{W}:
        \r===============

        \r  Options                                  Description
        \r  -------                                  -----------
        \r  -q,         --quiet                      Prevent header from displaying. {O}Warning{W}: bypass any "Are your sure?"
        \r                                           message!
        \r  -v [LEVEL], --verbose [LEVEL]            Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).

        \r{SB2}{bold}Additional options{W}:
        \r===================

        \r  Options                                  Description
        \r  -------                                  -----------
        \r  -y,         --no-confirm                 Bypass any and all "Are you sure?" messages.

        \r{SB2}{bold}Informations options{W}:
        \r=====================

        \r  Options                                  Description
        \r  -------                                  -----------
        \r              --info                       Show more informations about GitPy and exit.
        \r  -h,         --help                 [+]   Show this help message and exit or show more help for a option.
        \r  -V,         --version                    Show program's version and exit.

        \r{SB2}{bold}Miscellaneous options{W}:
        \r======================

        \r  Options                                  Description
        \r  -------                                  -----------
        \r  -u,         --update               [+]   Update the GitPy directly from GitHub.
        \r  -fu,        --force-update               Update AOVPNS even if the version on the machine is already the latest.
        \r              --show-config                Prompt the content of the config file.
        \r              --show-env-var         [+]   Prompt the value of the a environment variable.
        \r                                           (const: {G}install_path{W}).
        \r              --remove-cache         [+]   Delete python cache from the GitPy directory.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy <OPTIONS>

        \r  Others
        \r  ------
        \r  Report all bugs to <thomas.pellissier.pro@proton.me> or open an issue at <https://github.com/MyMeepSQL/gitpy/issues>.
        \r  The options with the [+] mean that it may require additional option(s).
        \r  If you want more details about a command, run: {G}gitpy --help <OPTION>{W}''' % Configuration.DEFAULT_INSTALL_PATH


    # -------------------- [ Main options ] -------------------- #
    
    
    def option_cli():
        '''
        The help message for the --cli option
        '''
        return '''
        \r{SB2}{bold}CLI option{W}:
        \r===========

        \r  Category
        \r  --------
        \r  Main options

        \r  Option's Description
        \r  --------------------
        \r  Start the CLI environment of GitPy. The CLI environment of GitPy
        \r  work like a shell, you can use the command like you do in a shell.
        \r  Inspired by the Metasploit Framework.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy --cli'''

    
    
    def option_console():
        '''
        The help message for the --console option
        '''
        return '''
        \r{SB2}{bold}Console option{W}:
        \r===============

        \r  Category
        \r  --------
        \r  Main options

        \r  Option's Description
        \r  --------------------
        \r  Start the main console of GitPy. This console work like a choice
        \r  menu console. Inspired by the Social Engineering Toolkit (SET).

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy --console'''


    # -------------------- [ Installation options ] -------------------- #
    
    
    def option_install():
        '''
        The help message for the --install option
        '''
        return '''
        \r{SB2}{bold}Install option{W}:
        \r===============

        \r  Category
        \r  --------
        \r  Installation options

        \r  Option's Description
        \r  --------------------
        \r  Install GitPy on your system with all of his depencies.

        \r  Options                         Description
        \r  -------                         -----------
        \r              --skip-update       Skip the system update phase during the installation of GitPy.
        \r  -y,         --noconfirm         Bypass any and all "Are you sure?" messages.
        \r  -q,         --quiet             Prevent header from displaying. {O}Warning{W}: bypass any "Are your sure?"
        \r                                  message!
        \r  -v [LEVEL], --verbose [LEVEL]   Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy --install [OPTIONS]'''

    
    
    def option_uninstall():
        '''
        The help message for the --uninstall option
        '''
        return '''
        \r{SB2}{bold}Uninstall option{W}:
        \r=================

        \r  Category
        \r  --------
        \r  Installation options

        \r  Option's Description
        \r  --------------------
        \r  Remove GitPy from your system (do not remove depencies)

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
        \r  gitpy --uninstall [OPTIONS]'''

    
    
    def option_skip_update():
        '''
        The help message for the --skip-update option
        '''
        return '''
        \r{SB2}{bold}Skip update option{W}:
        \r===================

        \r  Category
        \r  --------
        \r  Installation options

        \r  Option's Description
        \r  --------------------
        \r  Do no ask "Are your sure?" every time a choice appears.

        \r  Options     Description
        \r  -------     -----------
        \r  --install   Install GitPy with all depencies on your system.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy --install --skip-update'''

    
    
    def option_offline():
        '''
        The help message for the --offline option
        '''
        return '''
        \r{SB2}{bold}Offline option{W}:
        \r===============

        \r  Category
        \r  --------
        \r  Installation options

        \r  Option's Description
        \r  --------------------
        \r  Install GitPy from the local files (do not download anything).
        \r  By default, the installaiton process will download the latest 
        \r  version of GitPy from the GitHub repository.

        \r  Options     Description
        \r  -------     -----------
        \r  --install   Install GitPy with all depencies on your system.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy --install --offline'''

    
    
    def option_install_path():
        '''
        The help message for the --install-path option
        '''

        from src.config import Configuration

        return '''
        \r{SB2}{bold}Install Path option{W}:
        \r====================

        \r  Category
        \r  --------
        \r  Installation options

        \r  Option's Description
        \r  --------------------
        \r  You can specify the path where GitPy will be installed.
        \r  By default, GitPy will be installed in {C}%s{W}.

        \r  Options     Description
        \r  -------     -----------
        \r  --install   Install GitPy with all depencies on your system.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy --install -iP <PATH>
        \r    or
        \r  gitpy --install --install-path <PATH>''' % Configuration.DEFAULT_INSTALL_PATH


    # -------------------- [ Output options ] -------------------- #
    
    
    def option_quiet():
        '''
        The help message for the -q/--quiet option
        '''
        return '''
        \r{SB2}{bold}Quiet option{W}:
        \r===================

        \r  Category
        \r  --------
        \r  Output option

        \r  Option's Description
        \r  --------------------
        \r  No output given and bypass all "Are you sure?" style message.

        \r  Options           Description
        \r  -------           -----------
        \r      --install     Install GitPy with all depencies on your system.
        \r      --uninstall   Uninstall GitPy from your system.
        \r  -u, --update      Update the GitPy directly from GitHub.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy <OPTIONS> -q
        \r    or
        \r  gitpy <OPTIONS> --quiet'''

    
    
    def option_verbose():
        '''
        The help message for the -v/--verbose option
        '''
        return '''
        \r{SB2}{bold}Verbose option{W}:
        \r===============

        \r  Category
        \r  --------
        \r  Output option

        \r  Option's Description
        \r  --------------------
        \r  Prompt more informations during the execution of the script.
        \r  The default value of the verbose level is 0. If you use the -v 
        \r  without any value, the verbose level will be set to 1 (const).

        \r  LEVEL             Description
        \r  -----             -----------
        \r    0               No verbose
        \r    1               Display the command executed
        \r    2               Display the command executed and the output
        \r    3               Display the command executed and the output, and display more informations
        \r                    about the excecusion of python functions.

        \r  Options           Description
        \r  -------           -----------
        \r      --install     Install GitPy with all depencies on your system.
        \r      --uninstall   Uninstall GitPy from your system.
        \r  -u, --update      Update the GitPy directly from GitHub.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy <OPTIONS> -v [LEVEL]
        \r    or
        \r  gitpy <OPTIONS> --verbose [LEVEL]'''


    # -------------------- [ Additional options ] -------------------- #
    
    
    def option_no_confirm():
        '''
        The help message for the -y/--no-confirm option
        '''
        return '''
        \r{SB2}{bold}No confirmation option{W}:
        \r=======================

        \r  Category
        \r  --------
        \r  Additional options

        \r  Option's Description
        \r  --------------------
        \r  Do no ask "Are your sure?" every time a choice appears.

        \r  Options           Description
        \r  -------           -----------
        \r      --install     Install GitPy with all depencies on your system.
        \r      --uninstall   Uninstall GitPy from your system.
        \r  -u, --update      Update the GitPy directly from GitHub.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy <OPTIONS> -y
        \r    or
        \r  gitpy <OPTIONS> --no-confirm'''


    # -------------------- [ Informations options ] -------------------- #
    
    
    def option_info():
        '''
        The help message for the --info option
        '''
        return '''
        \r{SB2}{bold}Information option{W}:
        \r===================

        \r  Category
        \r  --------
        \r  Informations options

        \r  Option's Description
        \r  --------------------
        \r  Show all informations about GitPy. Version, owner, etc.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy --info'''

    
    
    def option_version():
        '''
        The help message for the -V/--version option
        '''
        return '''
        \r{SB2}{bold}Version option{W}:
        \r===============

        \r  Category
        \r  --------
        \r  Informations options

        \r  Option's Description
        \r  --------------------
        \r  Show the GitPy's version and exit.

        \r  Options                         Description
        \r  -------                         -----------
        \r  -v [LEVEL], --verbose [LEVEL]   Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).
        
        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy -V [OPTION]
        \r    or
        \r  gitpy --version [OPTION]'''


    # -------------------- [ Miscellaneous options ] -------------------- #
    
    
    def option_update():
        '''
        The help message for the -u/--update option
        '''
        return '''
        \r{SB2}{bold}Force Update option{W}:
        \r====================

        \r  Category
        \r  --------
        \r  Miscellaneous options

        \r  Option's Description
        \r  --------------------
        \r  Download and update the current instance of GitPy on the machine with
        \r  the latest stable version of GitPy from its repository.

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
        \r  gitpy -U [OPTIONS]
        \r    or
        \r  gitpy --update [OPTIONS]'''

    
    
    def option_force_update():
        '''
        The help message for the -fu/--force-update option
        '''
        return '''
        \r{SB2}{bold}Update option{W}:
        \r==============

        \r  Category
        \r  --------
        \r  Miscellaneous options

        \r  Option's Description
        \r  --------------------
        \r  Update AOVPN even if the GitPy' instance version on the machine is 
        \r  already the latest.

        \r  Options         Description
        \r  -------         -----------
        \r  -u,  --update   Update the GitPy directly from GitHub.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy -u -fu [OPTIONS]
        \r    or
        \r  gitpy -u --force-update [OPTIONS]
        \r    or
        \r  gitpy --update -fu [OPTIONS]
        \r    or
        \r  gitpy --update --force-update [OPTIONS]'''

    
    
    def option_show_env_var():
        '''
            The help message for the --show-env-var option
        '''

        from src.config import Configuration

        return '''
        \r{SB2}{bold}Show env var option{W}:
        \r====================

        \r  Category
        \r  --------
        \r  Miscellaneous options

        \r  Option's Description
        \r  --------------------
        \r  Show the value of the entered environment variable.

        \r  Arguments         Description
        \r  ---------         -----------
        \r  install_path      The value of the {G}%s{W} environment variable.
        \r  notif_conf_path   The value of the {G}%s{W} environment variable.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy --show-env-var [ARGUMENT]''' % (
            (
            Configuration.gitpy_install_path_env_var_name, Configuration.gitpy_notification_config_file_env_var_name
            )
        )

    
    
    def option_remove_cache():
        '''
            The help message for the --remove-cache option 
        '''
        return '''
        \r{SB2}{bold}Remove cache option{W}:
        \r====================

        \r  Category
        \r  --------
        \r  Miscellaneous options

        \r  Option's Description
        \r  --------------------
        \r  Delete all __pycache__ directories and .pyc files of GitPy.

        \r  Options                         Description
        \r  -------                         -----------
        \r  -v [LEVEL], --verbose [LEVEL]   Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Usage
        \r  -----
        \r  gitpy --remove-cache [OPTIONS]'''


    # -------------------- [ Consoles ] -------------------- #
    
    
    def console_help_message():
        '''
        The main help message of the main console (not the CLI one)
        '''

        from src.config import Configuration

        return '''
        \r{SB2}{bold}Core options{W}:
        \r=============
        
        \r  Options        Description
        \r  -------        -----------
        \r  88, back       Goes back one menu.

        \r{SB2}{bold}Global options{W}:
        \r===============

        \r  Options         Description
        \r  -------         -----------
        \r  help            Show this help message.
        \r  version         Show the version of GitPy.
        \r  info            Show more informations about GitPy.
        \r  verbose   [+]   Verbosity level: 1-3 (default: {G}0{W})
        \r  99, exit        Exit the console.

        \r{SB2}{bold}Others avalable informations{W}:
        \r=============================

        \r  Report all bugs to <%s> or open an issue at <%s>.''' % (
            (
            Configuration.OWNER_EMAIL_MYMEEPSQL,
            Configuration.REPO_ISSUES_URL
            )
        )

    # -------------------- [ CLI Consoles ] -------------------- #
    
    
    def CLI_env_main_help_msg():
        '''
        The main help message of the CLI environment
        '''
        return '''
        \r {SB2}{bold}Core commands{W}
        \r =============

        \r    Commands        Description
        \r    --------        -----------
        \r    search    [+]   Search a repository on GitHub.

        \r    clear           Clear the terminal prompt.
        \r    reset     [+]   Reset the current loaded module' variables
        \r    help      [+]   Show this help message.
        \r    whoami          Show the your current user.
        \r    version         Show version of GitPy.
        \r    exit            Exit the GitPy's CLI environment.

        \r {SB2}{bold}Miscellaneous commands{W}
        \r ======================

        \r    Command         Description
        \r    -------         -----------
        \r    update    [+]   Update the current instance of GitPy on the machine with the latest
        \r                    stable version of GitPy from its repository.
        \r    

        \r    The commands with the [+] mean that it may require additional arguments.
        \r    If you want more details about a command, run: {G}help <COMMAND>{W}'''
