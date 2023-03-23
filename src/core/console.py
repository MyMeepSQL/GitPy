#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ console.py                [Created: 2023-03-28 | 10:26 - AM]  #
#                                       [Updated: 2023-03-28 | 12:02 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The main console of gitpy                                               #
#  Language ~ Python3                                                       #
#---[Author]----------------------------------------------------------------#
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
import os
import re
import sys
import rich
import json
import shutil
import random
import requests
import platform
import subprocess
import configparser
from time import sleep
from time import strftime
from tracemalloc import start
import gnureadline as global_readline # pip install gnureadline

## Third party libraries
from src.__main__ import GitPy
from src.config import Configuration
import src.util.ip_domain as IP_Domain
from src.util.process import Process
from src.util.clear import clear
from src.util.colors import Color
from src.util.help_messages import Help_Messages as HM
from src.util.informations import Informations
from src.util.based_distro import Based_Distro as BD
from src.util.internet_check import internet_check
from src.util.remove_python_cache import remove_python_cache
from src.util.if_package_exists import package_exists
from src.tools.colored.colored import fg, attr
# from src.tools.box import box
# from src.tools.box.table import Table
# from src.tools.box.console import Console

# -------------------- [ The Main Console ] -------------------- #
class Main_Console():
    '''
        The main console of GitPy.
        This console work like a "choices menu" console.
    '''

    VERSION = Configuration.VERSION # Current version of GitPy in the Configuration's Class.
    # REPO_VERSION=config.Configuration.REPO_VERSION # The latest version of GitPy from the GitHub Repository
    REPO_URL = Configuration.REPO_URL
    gitpy_path_env_var_name = Configuration.gitpy_path_env_var_name

    promptname = 'GitPy'

    show_main_menu = True

    SPACE = '#>SPACE$<#'
    
    global_commands = [

        '99',
        'exit',

        # 'clear',
        'verbose',
        'version',
        'info',
        'help'
    ]

    def get_github_repo_info(self,repo_name, username=None):
        # Recherche des dépôts ayant un nom similaire
        search_url = f"https://api.github.com/search/repositories?q={repo_name}"
        if username:
            search_url += f"+user:{username}"
        response = requests.get(search_url)
        search_results = json.loads(response.text)

        # Affichage des dépôts similaires trouvés
        items = search_results['items']
        if len(items) == 0:
            Color.pl('  {!} No repositories found with the name \'%s\'.' % repo_name)
            return

        while True:
            clear()
            # Affichage des dépôts trouvés
            Color.pl('\n  {*} Here are the similar repositories found for \'%s\':' % repo_name)
            for index, repo in enumerate(search_results["items"]):
                Color.pl('  {D}[{W}{SB2}%s{W}{D}]{W} %s'% (index+1,repo['full_name']))

            # Demande de l'utilisateur pour choisir un dépôt
            selected_index = int(input(self.prompt(menu='choose_repo'))) -1

            # if not selected_index:
            #     continue

            # if selected_index in search_results["items"]:
            #     print('test')
            #     continue

            selected_repo = search_results["items"][selected_index]

            # Récupération des informations sur le dépôt
            repo_url = selected_repo["url"]
            response = requests.get(repo_url)
            repo_info = json.loads(response.text)

            # Affichage des informations sur le dépôt
            clear()

            # Data channel setting
            data = [
                ('',''), 
                ('  Information about \'%s\':' % repo_info['name'], ''),
                ('',''), 
                ('  Repository\'s name   ::  %s' % repo_info['name'], ''),
                ('  Author              ::  %s' % repo_info['owner']['login'], ''),
                ('  Description         ::  %s' % repo_info['description'], ''),
                ('  Number of stars     ::  %s' % repo_info['stargazers_count'], ''),
                ('  Main language       ::  %s' % repo_info['language'], ''),
                ('  Creation date       ::  %s' % repo_info['created_at'], ''),
                ('  Last update date    ::  %s' % repo_info['updated_at'], ''),
                ('  Repository\'s URL    ::  %s' % repo_info['html_url'], ''),
                ('  License             ::  %s' % repo_info['license']['name'] if repo_info['license'] else 'None', ''),
                ('  Cloning URL         ::  %s' % repo_info['clone_url'], ''),
                ('',''),
            ]
            
            # Display the data
            self.display_array(data=data)

            # Color.pl('\nInformation about \'%s\':' % repo_info['name'])
            # Color.pl('Repository\'s name  ::  %s' % repo_info['name'])
            # Color.pl('Author             ::  %s' % repo_info['owner']['login'])
            # Color.pl('Description        ::  %s' % repo_info['description'])
            # Color.pl('Number of stars    ::  %s' % repo_info['stargazers_count'])
            # Color.pl('Main language      ::  %s' % repo_info['language'])
            # Color.pl('Creation date      ::  %s' % repo_info['created_at'])
            # Color.pl('Last update date   ::  %s' % repo_info['updated_at'])
            # Color.pl('Repository\'s URL   ::  %s' % repo_info['html_url'])
            # Color.pl('Cloning URL        ::  %s' % repo_info['clone_url'])
            # Color.pl('License            ::  %s' % repo_info['license']['name'] if repo_info['license'] else 'None')

            # Demande de l'utilisateur pour choisir la branche
            branches_url = f"{repo_info['url']}/branches"
            response = requests.get(branches_url)
            branches_info = json.loads(response.text)
            print(f"\nVoici les branches du dépôt {repo_info['name']}:")
            for index, branch in enumerate(branches_info):
                print(f"{index+1}. {branch['name']}")
            selected_branch_index = int(input("Entrez le numéro de la branche que vous souhaitez télécharger: ")) - 1
            selected_branch = branches_info[selected_branch_index]['name']

            # Demande de l'utilisateur pour télécharger le dépôt
            download_choice = input("Voulez-vous télécharger ce dépôt ? (y/n) ")
            if download_choice == "y":
                download_url = repo_info["clone_url"]
                download_dir = input("Entrez le répertoire de téléchargement: ")
                download_command = f"git clone -b {selected_branch} {download_url} {download_dir}"
                print(f"Téléchargement en cours avec la commande : {download_command}")
                os.system(download_command)

    def display_array(self, data):
        '''
        Display data in a table.

        Args:
            data (list): The list of data to display.
                Usage: [ ( 'data1', 'color1' ), ( 'data2', 'color2' ), ... ]
        '''
        
        max_len = max([len(s[0]) for s in data])
        border = f"{fg('#656565')}    ╭{'─' * (max_len + 4)}╮{attr('reset')}"
        print(border)
        for i, (s, color) in enumerate(data):
            padding = ' ' * (max_len - len(s))
            if color.startswith('#') and len(color) == 7:
                color_code = fg(color)
            else:
                color_code = attr('reset')
            print(f"{fg('#656565')}    │{attr('reset')} {color_code}{s}{attr('reset')}{padding}   {fg('#656565')}│{attr('reset')}")
        border = f"{fg('#656565')}    ╰{'─' * (max_len + 4)}╯{attr('reset')}"
        print(border)

    def prompt(self, menu):
        '''
        The prompt of the main console.
        '''

        ptnm = self.promptname

        if menu == 'main':
            return Color.s('{underscore}%s{W}:{underscore}search-repo{W}> ' % ptnm)
        
        if menu == 'choose_repo':
            return Color.s('{underscore}%s{W}:{underscore}choose-repo{W}> ' % ptnm)

    def main_menu(self):
        try:
            while True:
                if self.show_main_menu == True:
                    clear()
                    GitPy.Banner()
                    Color.pl('''{D}╭──────────────────────────────────────────────────────────────╼
│
│{W}  GitPy - A tool to automatate an OpenVPN server configuration{D}
│
╰┬──╮
 │  │
 │  ├──────╼{W} Created by             ::  {italic}Thomas Pellissier{W} ({R}{bold}MyMeepSQL{W}){D}
 │  │{W}                               ::  {italic}Jonas Petipierre{W} ({R}{bold}Bashy{W}){D}
 │  ├──────╼{W} Version                ::  {G}%s{W}{D}
 │  │
 │  ├──────╼{W} Follow me on Twitter   ::  {SB4}MyMeepSQL{W}{D}
 │  │
 │  │{W}                         {SG2}Welcome to the GitPy{W}{D}
 │  │
 │  │{W}           {italic}Developed for Debiant and Arch based Linux distros{W}{D}
 │  │
 │  │
 │  │
 │  │
 │  │{W}     {O}This tool is under development, so if you find any bug or have{W}{D}
 │  │{W}       {O}any suggestion please report it on the GitHub repo below.{W}{D}
 │  │
 │  │{W}   All news version will be added the official repository of GitPy.{D}
 │  │{W}               (%s){D}
 ╰──╯{W}''' % (self.VERSION, self.REPO_URL))


                self.show_main_menu = False

                # Get user input
                text_input = input(self.prompt(menu='main')).strip()

                # Create cmd-line args list
                user_input = text_input.split(' ')
                cmd_list = [w.replace(self.SPACE , ' ') for w in user_input if w]
                cmd_list_len = len(cmd_list)
                cmd = cmd_list[0].lower() if cmd_list else ''
                
                if not cmd:
                    continue

                self.get_github_repo_info(repo_name=text_input)

        except KeyboardInterrupt:
            Color.pl('  {!} Interrupted, shutting down...')
            remove_python_cache(pwd=self.pwd, line_enter=True)
            if Configuration.verbose == 3:
                Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
            sys.exit(1)

    def __init__(self, pwd):

        # Set the current working directory
        self.pwd = pwd

        # Check if the user's platform is a Linux machine or not
        if platform.system() != 'Linux':
            Color.pl('  {!} You tried to run GitPy on a non-linux machine. GitPy can be run only on a Linux kernel.')
            sys.exit(1)

        else:
            # Check if the GITPY_INSTALL_PATH environment variable is set or not
            # try:
            #     GITPY_PATH = os.environ[self.gitpy_path_env_var_name]
            #     INSTALL_PATH = GITPY_PATH
            # except KeyError:
            #     Color.pl('  {!} GitPy is not installed on this machine.')
            #     Color.pl('  {*} Because the {C}{bold}GITPY_INSTALL_PATH{W} environment variable is not set (in the {C}/etc/environment{W} file).')
            #     Color.pl('  {*} If you just installed GitPy without restart you machine after, please reboot it and try again.')
            #     Color.pl('  {*} Otherwise, please install GitPy before using it.')
            #     reboot = input(Color.s('  {?} Do you want to reboot now? [y/n] '))
            #     if reboot.lower() == 'y':
            #         Color.pl('  {-} Rebooting...')
            #         Process.call('reboot')
            #     else:
            #         Color.pl('  {-} Exiting...')
            #         # remove_python_cache(pwd=pwd, line_enter=True)
            #     if Configuration.verbose == 3:
            #         Color.pl('  {§} Exiting with the exit code: {R}1{W}')
            #         Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
            #     sys.exit(1)

            # Check if the user is root or not
            if os.getuid() != 0:
                Color.pl('  {!} The GitPy Console must be run as root.')
                Color.pl('  {*} Re-run with sudo or switch to root user.')
                if Configuration.verbose == 3:
                    Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                sys.exit(1)
            else:
                # Check if the tun module is available or not.
                if not os.path.exists('/dev/net/tun'):
                    Color.pl('  {!} The TUN/TAP module is not available.')
                    Color.pl('  {*} Please install it and try again.')
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                    sys.exit(1) 
                # Distro check
                if BD.__init__() == 'Arch':
                    based_distro = 'Arch'
                    pass
                elif BD.__init__() == 'Debian':
                    based_distro = 'Debian'
                    pass
                else:
                    Color.pl('  {!} You\'re not running Debian or Arch variant.')
                    Color.pl('  {*} GitPy can only be run on Debian or Arch based Linux distros.')
                    Color.pl('  {-} Exiting...')
                    if Configuration.verbose == 3:
                        Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                        Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                    sys.exit(1)
                
                self.main_menu()
