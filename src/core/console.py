#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ console.py                [Created: 2023-03-28 | 10:26 - AM]  #
#                                       [Updated: 2023-03-28 | 12:02 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The main console of gitpy                                                #
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
import os
import re
import sys
import rich
import json
import shutil
import random
import getpass
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
from src.util.check_path import check_folder_path
from src.util.clear import clear
from src.util.colors import Color
from src.util.exit_tool import exit_tool
from src.util.help_messages import Help_Messages as HM
from src.util.informations import Informations
from src.util.email_utils import Email_Utils as EU
from src.util.based_distro import Based_Distro
from src.util.add_cron_job import add_cron_job
from src.util.internet_check import internet_check
from src.tools.colored.colored import fg, attr
import src.tools.requests as requests
# from src.tools.box import box
# from src.tools.box.table import Table
# from src.tools.box.console import Console

# -------------------- [ The Main Console ] -------------------- #
class Main_Console():
    '''
        The main console of GitPy.
        This console work like a "choices menu" console.
    '''

    # Variables
    VERSION = Configuration.VERSION # Current version of GitPy in the Configuration's Class.
    # REPO_VERSION=config.Configuration.REPO_VERSION # The latest version of GitPy from the GitHub Repository
    REPO_URL = Configuration.REPO_URL
    REPO_ISSUES_URL = Configuration.REPO_ISSUES_URL
    gitpy_install_path_env_var_name = Configuration.gitpy_install_path_env_var_name

    # Parameters
    remove_existing_folder = False
    promptname = 'GitPy'
    show_main_menu = True
    SPACE = '#>SPACE$<#'

    # Commands
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
        search_url = 'https://api.github.com/search/repositories?q=%s' % repo_name
        if username:
            search_url += f"+user:{username}"

        if Configuration.verbose >= 3:
            Color.pl('  {§}  Searching for similar repositories with the GitHub API...')
            Color.pl('   {SY1}╰──╼{W} URL: {C}%s{W}' % search_url)

        response = requests.get(search_url)

        search_results = json.loads(response.text)

        # if Configuration.verbose >= 3:
        #     Color.pl('  {§}  Response: {C}%s{W}' % search_results)


        # Affichage des dépôts similaires trouvés
        items = search_results['items']
        if len(items) == 0:
            if Configuration.verbose >= 3:
                Color.pl('  {§} No items found in the "items" key of the search results.')
            Color.pl('  {!} No repositories found with the name \'%s\'.' % repo_name)
            return

        # while True:
        # clear()
        # Affichage des dépôts trouvés
        Color.pl('  {*} Here are the similar repositories found for \'%s\':' % repo_name)
        for index, repo in enumerate(search_results['items']):
            Color.pl('  {D}[{W}{SB2}%s{W}{D}]{W} %s'% (index+1,repo['full_name']))

        # Demande de l'utilisateur pour choisir un dépôt
        Color.pl('  {*} Select the repository that you want to clone.')
        Color.pl('  {*} Enter {G}back{W} to come back to the main menu.')
        while True:
            try:
                selected_index = input(self.prompt(menu='choose_repo'))
                if selected_index == 'back':
                    self.show_main_menu = True
                    break
                if not selected_index:
                    continue
                if int(selected_index) > len(items) or int(selected_index) < 1:
                    Color.pl('  {!} Invalid choice. Please enter a number between 1 and %s.' % len(items))
                    continue
                break
            except ValueError:
                Color.pl('  {!} Invalid choice. Please enter a number between 1 and %s.' % len(items))
                continue

        selected_index = int(selected_index) -1

        # Récupération des informations sur le dépôt
        if Configuration.verbose >= 3:
            Color.pl('  {§}  Getting information about the selected repository...')
            Color.pl('   {SY1}╰──╼{W} Python: {SY1}selected_repo = search_results[\'items\'][selected_index]{W}')
        selected_repo = search_results['items'][selected_index]

        # Récupération des informations sur le dépôt
        if Configuration.verbose >= 3:
            Color.pl('  {§}  Getting information about the selected repository...')
            Color.pl('   {SY1}├──╼{W} Python: {SY1}repo_url = selected_repo[\'url\']{W}')

        repo_url = selected_repo['url']

        if Configuration.verbose >= 3:
            Color.pl('   {SY1}├──╼{W} Python: {SY1}response = requests.get(repo_url){W}')
        
        response = requests.get(repo_url)

        if Configuration.verbose >= 3:
            Color.pl('   {SY1}╰──╼{W} Python: {SY1}repo_info = json.loads(response.text){W}')

        repo_info = json.loads(response.text)

        # if Configuration.verbose >= 3:
        #     Color.pl('   {SY1}├──╼{W} value: {C}%s{W}' % repo_info['name'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['size'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['owner']['login'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['description'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['stargazers_count'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['forks_count'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['language'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['created_at'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['updated_at'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['html_url'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['url'])
        #     Color.pl('   {SY1}├──╼{W} URL: {C}%s{W}' % repo_info['license']['name'] if repo_info['license'] else 'None')
            # Color.pl('   {SY1}╰──╼{W} URL: {C}%s{W}' % repo_info['clone_url'])
        # clear()

        # Data channel setting
        information_line_length = 'Information about \'%s\':' % repo_info['name']
        information_line_length = len(information_line_length)

        seconde_line = '=' * information_line_length

        # Replace with your GitHub username and repository name
        username = repo_info['owner']['login']
        repo_name = repo_info['name']

        # Build the URL for the API call
        url = 'https://api.github.com/repos/%s/%s/commits' % (username, repo_name)

        # Send a GET request to the API with the appropriate headers
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code != 200:
            raise Exception(f' Request failed with status code {response.status_code}')

        # Parse the JSON response and get the SHA hash of the latest commit
        current_commit_sha = response.json()[0]['sha']

        data = [
            ('',''), 
            ('  Information about \'%s\':' % repo_info['name'], ''),
            ('  %s' % seconde_line,'#1898CC'), 
            ('',''),
            ('  Repository\'s name   ::  %s' % repo_info['name'], ''),
            ('  Repository\'s size   ::  %s' % repo_info['size'], ''),
            ('  Author              ::  %s' % repo_info['owner']['login'], ''),
            ('  Description         ::  %s' % repo_info['description'], ''),
            ('  Number of stars     ::  %s' % repo_info['stargazers_count'], ''),
            ('  Number of forks     ::  %s' % repo_info['forks_count'], ''),
            ('  Main language       ::  %s' % repo_info['language'], ''),
            ('  Creation date       ::  %s' % repo_info['created_at'], ''),
            ('  Last update date    ::  %s' % repo_info['updated_at'], ''),
            ('  Repository\'s URL    ::  %s' % repo_info['html_url'], ''),
            ('  API\'s URL           ::  %s' % repo_info['url'], ''),
            ('  License             ::  %s' % repo_info['license']['name'] if repo_info['license'] else 'None', ''),
            ('  Cloning URL         ::  %s' % repo_info['clone_url'], ''),
            ('  Latest commit SHA   ::  %s' % current_commit_sha, ''),
            ('','')
        ]

        # Affichage des informations sur le dépôt
        if Configuration.verbose >= 3:
            Color.pl('  {§}  Displaying the information about the selected repository...')
            Color.pl('   {SY1}╰──╼{W} Python: {SY1}self.display_array(data=data){W}')
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
        if Configuration.verbose >= 3:
            Color.pl('  {§}  Getting information about the branches of the selected repository...')
            Color.pl('   {SY1}╰──╼{W} Request: {SY1}GET %s/branches{W}' % repo_info['url'])
        branches_url = f"{repo_info['url']}/branches"
        response = requests.get(branches_url)
        branches_info = json.loads(response.text)
        Color.pl('\n  {*} All branches avalable for \'%s\':' % repo_info['name'])
        for index, branch in enumerate(branches_info):
            Color.pl('  {D}[{W}{SB2}%s{W}{D}]{W} %s' % (index+1,branch['name']))
        Color.pl('  {*} Select the branch that you want to download.')
        while True:
            try:
                selected_branch_index = int(input(self.prompt(menu='choose_branch')))
                if not selected_branch_index:
                    continue
                if selected_branch_index > len(branches_info) or selected_branch_index < 1:
                    Color.pl('  {!} Invalid choice. Please enter a number between 1 and %s.' % len(branches_info))
                    continue
                break
            except ValueError:
                Color.pl('  {!} Invalid choice. Please enter a number between 1 and %s.' % len(branches_info))
                continue

        selected_branch = branches_info[selected_branch_index -1 ]['name']

        # Demande de l'utilisateur pour télécharger le dépôt
        download_url = repo_info['clone_url']
        Color.pl('  {*} Enter the path where you want to download the repository.')
        download_dir = input(self.prompt(menu='choose_download_dir'))

        repo_install_path = ''.join(download_dir).strip()
        repo_install_path = check_folder_path(repo_install_path,repo_info['name'])

        if os.path.isdir(repo_install_path):
            Color.pl('  {!} The folder {C}%s{W} already exists.' % repo_install_path)
            replace_choice = input(Color.s('  {?} Do you want to replace it? [Y/n] '))

            if replace_choice == "y" or not replace_choice:
                self.remove_existing_folder = True
            else:
                Color.pl('  {!} You need to choose a new path where you want to download the repository.')
                Color.pl('  {*} Enter the path where you want to download the repository.')
                while os.path.isdir(repo_install_path) == True:
                    download_dir = input(self.prompt(menu='choose_download_dir'))
                    repo_install_path = ''.join(download_dir).strip()
                    repo_install_path = check_folder_path(repo_install_path,repo_info['name'])

                    if os.path.isdir(repo_install_path):
                        Color.pl('  {!} The folder {C}%s{W} already exists.' % repo_install_path)
                        continue

        # while os.path.isdir(repo_install_path) is True:
        #     Color.pl('  {!} The folder {C}%s{W} already exists.' % repo_install_path)
        #     Color.pl('  {*} Enter a new path where you want to download the repository.')
        #     download_dir = input(self.prompt(menu='choose_download_dir'))
        #     repo_install_path = ''.join(download_dir).strip()
        #     repo_install_path = check_folder_path(repo_install_path,repo_info['name'])

        Color.pl('  {*} The repository \'%s\' will be downloaded in the folder {C}%s{W}.' % (repo_info['name'],repo_install_path))

        download_choice = input(Color.s('  {?} Do you want to download this repository? [Y/n] '))

        if download_choice == "y" or not download_choice:
            # download_command = f"git clone -b {selected_branch} {download_url} {repo_install_path}"

            if self.remove_existing_folder == True:
                Color.pl('  {-} Removing the existing folder...')
                Process.call('rm -fr "%s" ' % repo_install_path, shell=True)

            Color.pl('  {-} Downloading the repository...')
            Process.call('git clone -b "%s" "%s" "%s"' % (selected_branch,download_url,repo_install_path), shell=True)

            Color.pl('  {-} Applying files permissions...')
            Process.call('chmod -R 777 "%s" ' % repo_install_path, shell=True)

            Color.pl('  {*} The repository has successfully been downloaded in the folder {C}%s{W}.' % repo_install_path)

            notification_by_email = input(Color.s('  {?} Do you want to receive a notification by email when a new version of the repository is available? [y/N] '))

            if notification_by_email.lower() == 'n' or not notification_by_email:
                pass
            else:

                Color.pl('  {*} Enter the email address where you want to receive the notification.')
                receiver_email_address = input(self.prompt(menu='choose_email_address'))

                Color.pl('  {*} Enter the SMTP server address.')
                smtp_server = input(self.prompt(menu='choose_smtp_server'))

                Color.pl('  {*} Enter the SMTP server port.')
                smtp_port = input(self.prompt(menu='choose_smtp_port'))

                # Color.pl('  {*} Enter the SMTP server security (none or ssl or tls).')
                # smtp_security = input(self.prompt(menu='choose_smtp_security'))

                # if smtp_security.lower() == 'none':
                #     smtp_security = ''

                # The client's email address and password
                Color.pl('  {*} Enter the SMTP server username (the email).')
                smtp_username =  input(self.prompt(menu='choose_smtp_username'))
                Color.pl('  {*} Enter the SMTP server password.')
                smtp_password = getpass.getpass(self.prompt(menu='choose_smtp_password'))
                print(smtp_password)

                Color.pl('  {-} Saving the notification settings...')

                EU.save_notification_settings(
                    github_repo_name=repo_info['name'],
                    github_repo_owner=repo_info['owner']['login'],
                    github_repo_branch=selected_branch,
                    github_repo_url=repo_info['html_url'],
                    github_repo_api_url=repo_info['url'],
                    current_commit_sha=current_commit_sha,
                    
                    receiver_email_address=receiver_email_address,
                    
                    smtp_server=smtp_server,
                    smtp_port=smtp_port,
                    
                    smtp_username=smtp_username,
                    smtp_password=smtp_password
                    
                    )

                Color.pl('  {-} Adding the notification cron job...')
                add_cron_job()

            Color.pl('  {*} All done!')
            Color.pl('  {*} You will receive a notification by email when a new version of the repository is available.')
            Color.pl('  {°} Press {C}Enter{W} to return to the main menu.')
            input()
            
            self.show_main_menu = True
            clear()
            self.main_menu()

        else:
            self.show_main_menu = True
            self.main_menu()

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

        if menu == 'choose_branch':
            return Color.s('{underscore}%s{W}:{underscore}choose-branch{W}> ' % ptnm)

        if menu == 'choose_download_dir':
            return Color.s('{underscore}%s{W}:{underscore}choose-download-dir{W}> ' % ptnm)


        # SMTP settings
        if menu == 'choose_email_address':
            return Color.s('{underscore}%s{W}:{underscore}choose-email-adress{W}> ' % ptnm)
        
        if menu == 'choose_sender_email_address':
            return Color.s('{underscore}%s{W}:{underscore}choose-sender-email-adress{W}> ' % ptnm)

        if menu == 'choose_smtp_server':
            return Color.s('{underscore}%s{W}:{underscore}choose-smtp-server{W}> ' % ptnm)

        if menu == 'choose_smtp_port':
            return Color.s('{underscore}%s{W}:{underscore}choose-smtp-port{W}> ' % ptnm)

        if menu == 'choose_smtp_username':
            return Color.s('{underscore}%s{W}:{underscore}choose-smtp-username{W}> ' % ptnm)

        if menu == 'choose_smtp_password':
            return Color.s('{underscore}%s{W}:{underscore}choose-smtp-password{W}> ' % ptnm)
        
        if menu == 'choose_smtp_security':
            return Color.s('{underscore}%s{W}:{underscore}choose-smtp-security{W}> ' % ptnm)

        # if menu == 'replace_folder':
        #     return Color.s('{underscore}%s{W}:{underscore}replace-folder{W}> ' % ptnm)

    def main_menu(self):
        try:
            while True:
                if self.show_main_menu == True:
                    clear()
                    Color.pl(GitPy.Banner())
                    Color.pl('''{D}╭──────────────────────────────────────────────────────────────╼
│
│{W}  GitPy - A tool to search and download a GitHub repository quickly.{D}
│
╰┬──╮
 │  │
 │  ├──────╼{W} Created by                    ::  {italic}Thomas Pellissier{W} ({R}{bold}MyMeepSQL{W}){D}
 │  │{W}                                      ::  {italic}Jonas Petitpierre{W} ({R}{bold}Bashy{W}){D}
 │  ├──────╼{W} Version                       ::  {G}%s{W}{D}
 │  │
 │  ├──────╼{W} Follow MyMeepSQL on Twitter   ::  {SB4}MyMeepSQL{W}{D}
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
            # Exit and removing the python cache
            exit_tool(1,pwd=self.pwd)

    def __init__(self, pwd):

        # Set the current working directory
        self.pwd = pwd

        # Check if the user's platform is a Linux machine or not
        if Configuration.verbose == 3:
            Color.pl('  {§} Checking if the user\'s platform is a Linux machine or not...')
            Color.pl('   {SY1}├──╼{W} Python: {SY1}platform.system() != Linux{W}')
            sleep(0.2)
        if platform.system() != 'Linux':
            if Configuration.verbose == 3:
                Color.pl('   {SY1}├──╼{W} The user\'s platform is {R}%s{W}' % platform.system())
                Color.pl('   {SY1}╰──╼{W} The user\'s platform is not a Linux machine.')
                sleep(0.2)

            Color.pl('  {!} You tried to run GitPy on a non-linux machine!')
            Color.pl('  {*} GitPy can be run only on a Linux kernel.')

            # Exit and removing the python cache
            exit_tool(1,pwd=self.pwd)

        else:
            if Configuration.verbose == 3:
                Color.pl('   {SY1}╰──╼{W} The user\'s platform is {C}%s{W}' % platform.system())
                sleep(0.2)

            # Check if the GITPY_INSTALL_PATH environment variable is set or not
            try:
                GITPY_PATH = os.environ[self.gitpy_install_path_env_var_name]
                INSTALL_PATH = GITPY_PATH

            except KeyError:
                Color.pl('  {!} GitPy is not installed on this machine.')
                Color.pl('  {*} Because the {C}{bold}%s{W} environment variable is not set.' % self.gitpy_install_path_env_var_name)
                Color.pl('  {*} If you just installed GitPy without restart you machine after, please reboot it and try again.')
                Color.pl('  {*} Otherwise, please install GitPy before using it.')
                reboot = input(Color.s('  {?} Do you want to reboot now? [y/n] '))

                if reboot.lower() == 'y':
                    Color.pl('  {-} Rebooting...')
                    Process.call('reboot')
                else:
                    Color.pl('  {*} Check if GitPy is correctly installed by reinstalling it and try again.')
                    Color.pl('  {*} If you still have the same problem, please report it on the GitPy\'s GitHub repository issues (%s).' % self.REPO_URL)

                    # remove_python_cache(pwd=pwd, line_enter=True)
                    exit_tool(1,pwd=self.pwd)

            # Check if the user is root or not
            if Configuration.verbose == 3:
                Color.pl('  {§} Checking if the user is root or not...')
                Color.pl('   {SY1}├──╼{W} Python: {SY1}os.getuid() != 0{W}')
            if os.getuid() != 0:
                if Configuration.verbose == 3:
                    Color.pl('   {SY1}╰──╼{W} The user is {C}not root{W}')
                Color.pl('  {!} The GitPy Console must be run as root.')
                Color.pl('  {*} Re-run with sudo or switch to root user.')
                # Exit and removing the python cache
                exit_tool(1,pwd=self.pwd)
            else:
                if Configuration.verbose == 3:
                    Color.pl('   {SY1}╰──╼{W} The user is {C}%s{W}' % ('root' if os.getuid() == 0 else 'not root'))
                    sleep(0.2)
                    Color.pl('  {§} Checking if the user\'s Linux distro is Debian or Arch based...')
                    Color.pl('   {SY1}├──╼{W} Python: {SY1}Based_Distro(){W}')
                    sleep(0.2)
                # Distro check
                if Based_Distro() == 'Arch':
                    if Configuration.verbose == 3:
                        Color.pl('   {SY1}╰──╼{W} The user\'s Linux distro is {C}Arch{W}')
                        sleep(0.2)
                    based_distro = 'Arch'
                    pass
                elif Based_Distro() == 'Debian':
                    if Configuration.verbose == 3:
                        Color.pl('   {SY1}╰──╼{W} The user\'s Linux distro is {C}Arch{W}')
                        sleep(0.2)
                    based_distro = 'Debian'
                    pass
                else:
                    if Configuration.verbose == 3:
                        Color.pl('   {SY1}╰──╼{W} The user\'s Linux distro is {C}not Arch or Debian{W}')
                    Color.pl('  {!} You\'re not running Debian or Arch variant.')
                    Color.pl('  {*} GitPy can only be run on Debian or Arch based Linux distros.')
                    # Exit and removing the python cache
                    exit_tool(1,pwd=self.pwd)

                # Check if the use are connected to the Internet network with the internet_check() function
                Color.pl('  {-} Checking for internet connexion...')
                if Configuration.verbose == 3:
                    Color.pl('  {§} Call the {P}internet_check(){W} function.')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}request.urlopen(host, timeout=10){W}')

                # Check if the user is connected to the Internet
                if internet_check() == True:
                    Color.pl('  {+} Internet status: {G}Connected{W}.')
                    pass
                else:
                    Color.pl('  {+} Internet status: {R}Not connected{W}.')
                    Color.pl('  {!} No Internet connexion found, please check if you are connected to the Internet and retry.')
                    exit_tool(1,pwd=self.pwd)

                # Load the main menu
                if Configuration.verbose == 3:
                    Color.pl('  {§} Loading the main menu...')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}self.main_menu(){W}')
                    sleep(0.2)
                self.main_menu()
        
