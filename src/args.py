#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ args.py                   [Created: 2023-03-21 | 10:26 - AM]  #
#                                       [Updated: 2023-04-10 | 13:18 - PM]  #
#---[Info]------------------------------------------------------------------#
#  All arguments of the 'gitpy' command                                     #
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

# Import section
import sys
from gettext import gettext as _

## Third party libraries
import src.tools.argparse as argparse
import src.config as config
import src.__main__ as _MAIN
from src.util.colors import Color

# Custom help formatter (not in use because to the custom help message in the 'help_messages.py' file)
class BetterHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = Color.s('{SB2}{bold}Usage{W}: ')
        return super(BetterHelpFormatter , self).add_usage(usage, actions, groups, prefix)
    def _fill_text(self, text, width, indent):
        return ''.join(indent + line for line in text.splitlines(keepends=True))

# Main
class Arguments(argparse.ArgumentParser):
    '''
    All arguments of the 'gitpy' command
    '''
    @classmethod
    def get_arguments(cls):
        '''
        Returns parser.args() containing all program arguments
        '''

        """
            Keyword Arguments:

            - option_strings -- A list of command-line option strings which
                should be associated with this action.

            - dest -- The name of the attribute to hold the created object(s)

            - nargs -- The number of command-line arguments that should be
                consumed. By default, one argument will be consumed and a single
                value will be produced.  Other values include:
                    - N (an integer) consumes N arguments (and produces a list)
                    - '?' consumes zero or one arguments
                    - '*' consumes zero or more arguments (and produces a list)
                    - '+' consumes one or more arguments (and produces a list)
                Note that the difference between the default and nargs=1 is that
                with the default, a single value will be produced, while with
                nargs=1, a list containing a single value will be produced.

            - const -- The value to be produced if the option is specified and the
                option uses an action that takes no values.

            - default -- The value to be produced if the option is not specified.

            - type -- A callable that accepts a single string argument, and
                returns the converted value.  The standard Python types str, int,
                float, and complex are useful examples of such callables.  If None,
                str is used.

            - choices -- A container of values that should be allowed. If not None,
                after a command-line argument has been converted to the appropriate
                type, an exception will be raised if it is not a member of this
                collection.

            - required -- True if the action must always be specified at the
                command line. This is only meaningful for optional command-line
                arguments.

            - help -- The help string describing the argument.

            - metavar -- The name to be used for the option's argument with the
                help string. If None, the 'dest' value will be used as the name.
        """

        gitpy = Arguments(
            prog='gitpy',
            description='GitPy - A Python3 tool for search and download a GitHub\'s repository directly in the terminal',
            usage='gitpy [options]',
            add_help=False,
            allow_abbrev=False,
            prefix_chars='-',
            formatter_class=lambda prog: BetterHelpFormatter(prog, max_help_position=80, width=100,indent_increment=2),
        )

        cls._add_main_args(gitpy.add_argument_group(Color.s('{SB2}{bold}Main options{W}')))
        cls._add_installation_args(gitpy.add_argument_group(Color.s('{SB2}{bold}Installation options{W}')))
        cls._add_repo_args(gitpy.add_argument_group(Color.s('{SB2}{bold}Repository options{W}')))
        cls._add_output_args(gitpy.add_argument_group(Color.s('{SB2}{bold}Output options{W}')))
        cls._add_additional_args(gitpy.add_argument_group(Color.s('{SB2}{bold}Additional options{W}')))
        cls._add_informations_args(gitpy.add_argument_group(Color.s('{SB2}{bold}Informations options{W}')))
        cls._add_miscellaneous_args(gitpy.add_argument_group(Color.s('{SB2}{bold}Miscellaneous options{W}')))
        # cls._add_test_args(gitpy.add_argument_group(Color.s('{SB2}{bold}Test options{W}')))

        # argcomplete.autocomplete(parser)
        return gitpy.parse_args()


    # -------------------- [ Main Arguments ] -------------------- #
    @classmethod
    def _add_main_args(cls,main):
        main.add_argument(
            '--console',
            action='store_true',
            dest='console',
            help='start tthe main console of GitPy'
        )
        main.add_argument(
            '--cli',
            action='store_true',
            dest='cli',
            help='start the CLI environment of GitPy'
        )


    # -------------------- [ Installation Arguments ] -------------------- #
    @classmethod
    def _add_installation_args(cls,install):
        install.add_argument(
            '-i','--install',
            action='store_true',
            dest='install',
            help='install GitPy with all depencies on your system'
        )
        install.add_argument(
            '--uninstall',
            action='store_true',
            help='uninstall GitPy from your system'
        )
        install.add_argument(
            '--skip-update',
            action='store_true',
            dest='skip_update',
            help='skip the system update phase during the installation of GitPy'
        )
        install.add_argument(
            '--offline',
            action='store_true',
            dest='offline',
            help='install GitPy with the local file already downloaded. By default, the Installer download the latest version from GitHub and install it on the machine'
        )
        install.add_argument(
            '-iP','--install-path',
            type=str,
            nargs='?',
            const='0',
            metavar='PATH',
            dest='install_path',
            help=Color.s('the path where GitPy will be installed (default: {G}%s{W})' % config.Configuration.DEFAULT_INSTALL_PATH),
        )


    # -------------------- [ Repository Arguments ] -------------------- #
    @classmethod
    def _add_repo_args(cls,repo):
        repo.add_argument(
            '-cr','--check-repo',
            action='store_true',
            dest='check_repo',
            help=Color.s('check if the repository in the notification config file have a new commit avalable and send a notificarion via mail if it\'s the case')
        )


    # -------------------- [ Output Arguments ] -------------------- #
    @classmethod
    def _add_output_args(cls,output):
        output.add_argument(
            '-q','--quiet',
            action='store_true',
            help=Color.s('prevent header from displaying. {O}Warning{W}: bypass any "Are your sure?" message!')
        )
        output.add_argument(
            '-v','--verbose',
            type=int,
            nargs='?',
            const=1,
            choices=[1,2,3],
            metavar='LEVEL',
            dest='verbose',
            help=Color.s('verbosity level: 1-2 (default: {G}0{W} | const: {G}%(const)s{W})')
        )


    # -------------------- [ Additional Arguments ] -------------------- #
    @classmethod
    def _add_additional_args(cls,add):
        add.add_argument(
            '-y','--no-confirm',
            action='store_true',
            dest='no_confirm',
            help='bypass any and all "Are you sure?" messages.'
        )


    # -------------------- [ Informations Arguments ] -------------------- #
    @classmethod
    def _add_informations_args(cls,info):
        info.add_argument(
            '--info',
            action='store_true',
            help='show more informations about GitPy and exit'
        )
        info.add_argument(
            '-h','--help',
            action='store_true',
            # action='help',
            help='show this help message and exit'
        )
        info.add_argument(
            '-V','--version',
            action='store_true',
            help=f"show program's version and exit"
        )


    # -------------------- [ Miscellaneous Arguments ] -------------------- #
    @classmethod
    def _add_miscellaneous_args(cls,misc):
        misc.add_argument(
            '-u','--update',
            action='store_true',
            dest='update',
            help='update GitPy directly from GitHub'
        )
        misc.add_argument(
            '-fu','--force-update',
            action='store_true',
            dest='force_update',
            help='update AOVPN even if the version on the machine is already the latest'
        )
        misc.add_argument(
            '--show-config',
            action='store_true',
            dest='show_config',
            help='show the value of the config file'
        )
        misc.add_argument(
            '--show-env-var',
            type=str,
            nargs='?',
            const='install_path',
            choices=['install_path','notif_conf_path'],
            dest='show_env_var',
            help='prompt the value of the a environment variable'
        )
        misc.add_argument(
            '--remove-cache',
            action='store_true',
            dest='remove_cache',
            help='delete any \'__pycache__\' folder in the GitPy\' directory'
        )


    # -------------------- [ Tests Arguments ] -------------------- #
    # @classmethod
    # def _add_test_args(cls,test):
    #     test.add_argument(
    #         '--process',
    #         action='store_true',
    #         dest='process',
    #     )
