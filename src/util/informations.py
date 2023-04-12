#!/usr/bin/env python3

#---[Metadata]--------------------------------------------------------------#
#  Filename ~ informations.py           [Created: 2023-02-28 |  9:21 - AM]  #
#                                       [Updated: 2023-02-28 | 10:28 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The informations page about GitPy                                        #
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
 
# Third party libraries
from src.util.colors import Color
from src.config import Configuration

# Main
class Informations():
    '''
        The main class of the informations page of GitPy that will be called when the user runs gitpy --info. 
        This class will display all informations about GitPy.
    '''

    PROGRAM_NAME = Configuration.PROGRAM_NAME
    VERSION = Configuration.VERSION

    REPO_URL = Configuration.REPO_URL
    REPO_CLONE_URL = Configuration.REPO_CLONE_URL
    REPO_CHANGELOG_URL = Configuration.REPO_CHANGELOG_URL
    REPO_ISSUES_URL = Configuration.REPO_ISSUES_URL

    OWNER_EMAIL_MYMEEPSQL = Configuration.OWNER_EMAIL_MYMEEPSQL
    OWNER_DISCORDTAG_MYMEEPSQL = Configuration.OWNER_DISCORDTAG_MYMEEPSQL

    OWNER_EMAIL_BASHY = Configuration.OWNER_EMAIL_BASHY
    OWNER_DISCORDTAG_BASHY = Configuration.OWNER_DISCORDTAG_BASHY

    @classmethod
    def print_info(self):

        return '''
        \r  {*} All informations about the GitPy.

        \r{SB2}{bold}Informations about GitPy{W}:
        \r=========================

        \r  Description
        \r  -----------
        \r  GitPy is a tool to search and download GitHub repositories. 
        \r  It's a Python3 program that uses the GitHub API to search and download repositories.

        \r  Main Options                   Description
        \r  ------------                   -----------
        \r       --install                 Install GitPy with all depencies on your system.
        \r       --uninstall               Uninstall GitPy from your system.
        \r       --update                  Update the GitPy directly from GitHub.
        \r       --console                 Start the main console of GitPy.
        \r       --cli                     Start the CLI environment of GitPy.
        \r  -h,  --help                    Display the help page of GitPy.

        \r  Program                        Version (on your system)
        \r  -------                        ------------------------
        \r  %s                          %s

        \r  Copyright & Licensing          Description
        \r  ---------------------          ----------- 
        \r  Owner                          © PSociety
        \r  Copyright                      Copyright (C) 2021-2023 PSociety, {R}All rights reserved{W}.
        \r  License                        This program is under GNU General Public License v3.0 (GPL 3.0). 
        \r                                 You can modify the program and share it as long as the original 
        \r                                 author appears in credits and the program is on the same license.

        \r  Other informations             Description
        \r  ------------------             -----------
        \r  GitHub page URL                %s
        \r  Clone URL                      %s
        \r  Changelogs                     %s
        \r  Issues pages                   %s

        \r{SB2}{bold}Informations about authors{W}:
        \r===========================

        \r  Main informations              Description
        \r  -----------------              -----------
        \r  MyMeepSQL's fullname           Thomas Pellissier
        \r  MyMeepSQL's email              %s ({bold}only for professional{W} or for {G}report bugs of GitPy{W})

        \r  Bashy's fullname               Jonas Petitpierre
        \r  Bashy's email                  %s ({bold}only for personal{W} or for {G}report bugs of GitPy{W})

        \r  Other informations             Description
        \r  ------------------             -----------
        \r  MyMeepSQL's GitHub profile     https://github.com/MyMeepSQL
        \r  MyMeepSQL's Twitter profile    https://twitter.com/MyMeepSQL
        \r  MyMeepSQL's Discord username   %s

        \r  Bashy's GitHub profile         https://github.com/jonas52
        \r  Bashy's Discord username       %s''' % (

            self.PROGRAM_NAME,
            self.VERSION,

            self.REPO_URL,
            self.REPO_CLONE_URL,
            self.REPO_CHANGELOG_URL,
            self.REPO_ISSUES_URL,

            self.OWNER_EMAIL_MYMEEPSQL,
            self.OWNER_EMAIL_BASHY,
            self.OWNER_DISCORDTAG_MYMEEPSQL,
            self.OWNER_DISCORDTAG_BASHY
        )
