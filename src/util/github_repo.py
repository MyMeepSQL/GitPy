#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ github_repo.py            [Created: 2023-02-21 | 11:12 - AM]  #
#                                       [Updated: 2023-02-21 | 12:03 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Compare the version between the GitPy instance on the system and         #
#  the GitHub's repositorie one.                                            #               
#  Also check if the GitPy' repositorie are reachable or not                #
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
import sys
from json import loads

## Third party libraries
from src.tools.packaging import version
import src.tools.requests as requests
from src.tools.requests import get
from src.util.colors import Color
from src.util.internet_check import internet_check
from src.util.exit_tool import exit_tool

# Class section
class GitHub_Repo():
    '''
        Classe to work with the GitPy's GitHub repository
    '''

    @staticmethod
    def compare_version(mode=None):
        '''
            Compare version between the GitPy instance on
            the system and the GitHub repositorie's version
            with the 'metadata.json' file.

            Arguments:
                mode (str): Where tis function have been called. 
                            It can be have 2 values:
                              - None: Display after using the -h/--help option
                              - 'update': Called by the '--update' option (so called by the 'updater.py' file)

        '''

        from src.config import Configuration

        # if os.path.isdir(Configuration.DEFAULT_INSTALL_PATH):
        if internet_check() == True:
            rqst = get(Configuration.REPO_METADATA_URL, timeout=3)
            fetch_sc = rqst.status_code

            if fetch_sc == 404:
                Color.pl('  {!} The GitPy\'s repositorie can\'t be reach for checking if a new version are avalable.')
                Color.pl('  {*} Maybe the repository has been switched to private mode.')
                Color.pl('  {*} Please contact MyMeepSQL by sending an email or add him on Discord (use the {G}--info{W} option for author\'s informations).')

            if fetch_sc == 200:
                metadata = rqst.text
                json_data = loads(metadata)
                # print(json_data)
                cp_online_ver = json_data['version']

                Configuration.REPO_VERSION = cp_online_ver
                # print(Configuration.VERSION)
                # print(cp_online_ver)
                # print(Configuration.REPO_VERSION)

                if version.parse(cp_online_ver) > version.parse(Configuration.VERSION):
                    Color.pl('  {*} A new update are avalable: %s (Current %s)' % (cp_online_ver, Configuration.VERSION))

                    if mode == None:
                        # Color.pl('  {*} A new update are avalable: %s (Current %s)' % (cp_online_ver, Configuration.VERSION))
                        Color.pl('  {*} You can update your GitPy instance with the {G}--update{W} option.')

                else:

                    if mode == 'update':
                        Color.pl('  {!} You already have the latest version of GitPy!')
                        exit_tool(1,pwd=Configuration.pwd)
                        
        else:
            Color.pl('  {!} You are not connected to the internet.')
            Color.pl('  {*} Cannot check if a new version of GitPy are avalable or not.')
            Configuration.REPO_VERSION = 'no-internet'

    @staticmethod
    def is_reachable(args):
        '''
            Checks if a GitHub repository is reachable.
            A repository is considered reachable if it is not in private mode.

            :return: True if the repository is reachable, False otherwise
        '''
        
        from src.config import Configuration

        try:
            repository_url = Configuration.REPO_URL
            rqst = requests.get(repository_url, timeout=7)

            # If the repository is in private mode, the page returns a 404 status (Not Found)
            if rqst.status_code == 404:
                if args.quiet:
                    Color.pl('The GitPy\'s repositorie can\'t be reach.')
                    Color.pl('Maybe the repository has been switched to private mode.')
                    exit_tool(1,pwd=Configuration.pwd)
                else:
                    Color.pl('  {!} The GitPy\'s repositorie can\'t be reach.')
                    Color.pl('  {*} Maybe the repository has been switched to private mode.')
                    Color.pl('  {*} Please contact MyMeepSQL by sending an email or add him on Discord (use the {G}--info{W} option for author\'s informations).')
                    exit_tool(1,pwd=Configuration.pwd)

        except KeyboardInterrupt:
            Color.pl('\n  {*} Aborted')
            exit_tool(1,pwd=Configuration.pwd)
