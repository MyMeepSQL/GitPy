#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ cli_console.py            [Created: 2023-01-14 |  5:49 - PM]  #
#                                       [Updated: 2023-01-14 |  5:49 - PM]  #
#---[Info]------------------------------------------------------------------#
#  The CLI console of gitpy                                             #
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
import re
import sys
import rich
import shutil
import os.path
import platform
import subprocess
import configparser
from time import sleep
from time import strftime
from tracemalloc import start
from rich import box
from rich.table import Table
from rich.console import Console
import gnureadline as global_readline # pip install gnureadline


## Third party libraries

import src.config as config
from src.__main__ import GitPy
from src.util.clear import clear
from src.util.colors import Color
from src.util.help_messages import Help_Messages as HM
from src.util.tab_completer import Completer
from src.config import Main_prompt



class Help_message:
    commands = {

        # ---------- [ Core commands ] ---------- #
        'search' : {
            'help' : Color.s('''
            \r{SB2}{bold}Search command{W}:
            \r===============
    
            \r  Category
            \r  --------
            \r  Core commands
    
            \r  Description
            \r  -----------
            \r  Search a repository on GitHub with the GitHub API.
            
            \r{SB2}{bold}Others avalable informations{W}:
            \r=============================
    
            \r  Usage
            \r  -----
            \r  search <REPONAME>
            '''),
			'least_args' : 1,
			'max_args' : 1
        },


		'clear' : {
			'help' : '''
            \r    Description
            \r    -----------
			\r    Clear the terminal screen.
			''',
			'least_args' : 0,
			'max_args' : 0
		},


		'reset' : {
			'help' : Color.s('''
            \r{SB2}{bold}Reset command{W}:
            \r==============
    
            \r  Category
            \r  --------
            \r  Core commands
    
            \r  Description
            \r  -----------
            \r  Reset the terminal like if you ran it for the first time.
            
            \r{SB2}{bold}Others avalable informations{W}:
            \r=============================
    
            \r  Usage
            \r  -----
            \r  reset
			'''),
            'least_args' : 0,
            'max_args' : 1
		},

		'help' : {
			'help' : '''
			\r  What?! You're kidding.
			''',
			'least_args' : 0,
			'max_args' : 1
		},


		'whoami' : {
			'help' : Color.s('''
            \r{SB2}{bold}Whoami command{W}:
            \r===============
    
            \r  Category
            \r  --------
            \r  Core commands
    
            \r  Description
            \r  -----------
            \r  Show the username of your current user that you have loaded GitPy.
            
            \r{SB2}{bold}Others avalable informations{W}:
            \r=============================
    
            \r  Usage
            \r  -----
            \r  whoami
			'''),
			'least_args' : 0,
			'max_args' : 0
		},


		'version' : {
			'help' : Color.s('''
            \r{SB2}{bold}Version command{W}:
            \r===============
    
            \r  Category
            \r  --------
            \r  Core commands
    
            \r  Description
            \r  -----------
            \r  Show the current instance version of GitPy on your system.

            \r  Options                         Description
            \r  -------                         -----------
            \r  -v [LEVEL], --verbose [LEVEL]   Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).

            \r{SB2}{bold}Others avalable informations{W}:
            \r=============================
    
            \r  Usage
            \r  -----
            \r  version [OPTION]
			'''),
            'options' :  {
                '-v',
                '--verbose'
            },
			'least_args' : 0,
			'max_args' : 2
		},


		'exit' : {
			'help' : Color.s('''
            \r{SB2}{bold}Exit command{W}:
            \r=============
    
            \r  Category
            \r  --------
            \r  Core commands
    
            \r  Description
            \r  -----------
            \r  Clear cache and exit the GitPy's CLI environment.

            \r{SB2}{bold}Others avalable informations{W}:
            \r=============================
    
            \r  Usage
            \r  -----
            \r  exit]
			'''),
			'least_args' : 0,
			'max_args' : 0
		},


        # ---------- [ Miscellaneous commands ] ---------- #
		'update' : {
			'help' : Color.s('''
            \r    Description
            \r    -----------
            \r    Download and update the current instance of GitPy on the machine with
            \r    the latest stable version of GitPy from its repository.

            \r    Options                         Description
            \r    -------                         -----------
            \r    -q,         --quiet             Prevent header from displaying. {O}Warning{W}: bypass any "Are your sure?"
            \r                                    message!
            \r                --noconfirm         Bypass any and all "Are you sure?" messages.
            \r    -v [LEVEL], --verbose [LEVEL]   Verbosity level: 1-3 (default: {G}0{W} | const: {G}1{W}).

            \r    Usage
            \r    -----
            \r    update [OPTIONS]
			'''),
			'least_args' : 0,
			'max_args' : 5
		}
    }


    @staticmethod
    def print_detailed(cmd):
        if cmd in Help_message.commands.keys():
            Color.pl(Help_message.commands[cmd]['help'])

        else:
            Color.pl('  {!} No help message for command "%s".' % cmd)


    @staticmethod
    def validate(cmd, num_of_args):
        valid = True
        if cmd not in Help_message.commands.keys():
            Color.pl('  {!} Unknown command: "%s"' % cmd)
            Color.pl('  {*} Run {G}help{W} command for see all commands.')
            valid = False

        elif num_of_args < Help_message.commands[cmd]['least_args']:
            Color.pl('  {!} Missing arguments.')
            valid = False

        elif num_of_args > Help_message.commands[cmd]['max_args']:
            Color.pl('  {!} Too many arguments.')
            valid = False

        return valid


class CLI_Console():

    VERSION = config.Configuration.VERSION # Current version of GitPy in the Configuration's Class.
    DEFAULT_INSTALL_PATH = config.Configuration.DEFAULT_INSTALL_PATH  # Where GitPy is installed
    # REPO_VERSION = config.Configuration.REPO_VERSION # The latest version of GitPy from the GitHub Repository
    REPO_URL = config.Configuration.REPO_URL

    def __init__(self, pwd):

        self.pwd = pwd

        GitPy.Banner()
        print()

        Color.pl('  {+} For see all commands, try {G}help{W} command.\n')

        comp = Completer()
        global_readline.set_completer(comp.complete)
        global_readline.parse_and_bind("tab: complete")

        cwd = os.path.dirname(os.path.abspath(__file__))
        while True:

            try:
                if Main_prompt.main_prompt_ready:
                    user_input = input(Main_prompt.prompt).strip()
                    options = user_input.split()

                    if user_input == '':
                        continue

                    # Handle single/double quoted arguments
                    quoted_args_single = re.findall("'{1}[\s\S]*'{1}" , user_input)
                    quoted_args_double = re.findall('"{1}[\s\S]*"{1}' , user_input)
                    quoted_args = quoted_args_single + quoted_args_double

                    if len(quoted_args):
                        for arg in quoted_args:
                            space_escaped = arg.replace(' ' , Main_prompt.SPACE)

                            if (space_escaped[0] == "'" and space_escaped[-1] == "'") or (space_escaped[0] == '"' and space_escaped[-1] == '"'):
                                space_escaped = space_escaped[1:-1]

                            user_input = user_input.replace(arg , space_escaped)


                    # Create cmd-line args list
                    user_input = user_input.split(' ')
                    cmd_list = [w.replace(Main_prompt.SPACE , ' ') for w in user_input if w]
                    cmd_list_len = len(cmd_list)
                    cmd = cmd_list[0].lower() if cmd_list else ''


                    # Validate number of args
                    valid = Help_message.validate(cmd , (cmd_list_len - 1))


                    if not valid:
                        continue

                    if cmd == 'exit':
                        sys.exit(0)

                    if cmd == 'help':
                        if cmd_list_len == 1:
                            HM.CLI_env_main_help_msg()

                        elif cmd_list_len == 2:
                            Help_message.print_detailed(cmd_list[1])

                    if cmd == 'clear':
                        clear()
                    if cmd == 'reset':
                        clear()
                        self.__init__(pwd=self.pwd)

                    if cmd == 'whoami':
                        subprocess.run('whoami' , shell = True)

            except KeyboardInterrupt:
                Color.p('  {*} Interrupt: For exit GitPy, run: {G}exit{W}\n')
                pass



