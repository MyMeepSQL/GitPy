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

# Imports section
import os
import sys
import requests
from json import loads
from requests import get

## Third party libraries
import src.config as C
from src.tools.packaging import version
from src.util.colors import Color
from src.util.internet_check import internet_check


# Main
def compare_version(mode=None):
    '''
    Compare version between the GitPy instance on
    the system and the GitHub repositorie's version
    with the 'metadata.json' file.
    '''

    # if os.path.isdir(C.Configuration.DEFAULT_INSTALL_PATH):
    if internet_check() == True:
        rqst = get('https://raw.githubusercontent.com/MyMeepSQL/gitpy/master/metadata.json', timeout=3)
        fetch_sc = rqst.status_code

        if fetch_sc == 404:
            Color.pl('  {!} The GitPy\'s repositorie can\'t be reach for checking if a new version are avalable.')
            Color.pl('  {*} Maybe the repository has been switched to private mode.')
            Color.pl('  {*} Please contact MyMeepSQL by sending an email or add him on Discord (use the {G}--info{W} option for author\'s informations).')

        if fetch_sc == 200:
            metadata = rqst.text
            json_data = loads(metadata)
            cp_online_ver = json_data['version']

            REPO_VERSION = cp_online_ver
            # print(REPO_VERSION)

            if version.parse(cp_online_ver) > version.parse(C.Configuration.VERSION):
                Color.pl('  {*} A new update are avalable : %s' % cp_online_ver)

                if mode == None:
                    Color.pl('  {*} You can update your GitPy instance with the {G}--update{W} option.')

            else:

                if mode == 'update':
                    Color.pl('  {!} You already have the latest version of GitPy!')
                    sys.exit(1)
                    
    else:
        Color.pl('  {!} You are not connected to the internet.')
        Color.pl('  {*} I can\'t check if a new version of GitPy are avalable. or not')
        REPO_VERSION = 'no-internet'


def is_reachable(args):
    '''
    Checks if a GitHub repository is reachable.
    A repository is considered reachable if it is not in private mode.

    :return: True if the repository is reachable, False otherwise
    '''
    
    try:
        repository_url = C.Configuration.REPO_URL
        rqst = requests.get(repository_url, timeout=7)

        # If the repository is in private mode, the page returns a 404 status (Not Found)
        if rqst.status_code == 404:
            if args.quiet:
                Color.pl('The GitPy\'s repositorie can\'t be reach.')
                Color.pl('Maybe the repository has been switched to private mode.')
                sys.exit(1)
            else:
                Color.pl('  {!} The GitPy\'s repositorie can\'t be reach.')
                Color.pl('  {*} Maybe the repository has been switched to private mode.')
                Color.pl('  {*} Please contact MyMeepSQL by sending an email or add him on Discord (use the {G}--info{W} option for author\'s informations).')
                if args.verbose == 3:
                    Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                    Color.pl('    {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                sys.exit(1)

    except KeyboardInterrupt:
        Color.pl('\n  {*} Aborted')
        if args.verbose == 3:
            Color.pl('  {§} Exiting with the exit code: {R}1{W}')
            Color.pl('    {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
        sys.exit(1)
