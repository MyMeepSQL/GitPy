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
 
# Imports section
## Third party libraries
from src.util.colors import Color
from src.config import Configuration

# Main
class Informations():
    '''
    The main class of the informations page of GitPy that will be called when the user runs gitpy --info. 
    This class will display all informations about GitPy.
    '''

    VERSION = Configuration.VERSION

    def __init__(self):
        Color.pl('''
        \r  {*} All informations about the GitPy.

        \r{SB2}{bold}Informations about GitPy{W}:
        \r=========================

        \r  Description
        \r  -----------
        \r  GitPy is a tool to automatate an OpenVPN server configuration 
        \r  and installation with users. It's a tool for Linux distros based
        \r  on Debian or Arch (for the moment).

        \r  Options                         Description
        \r  -------                         -----------
        \r  --install                       Install GitPy with all depencies on your system.
        \r  --uninstall                     Uninstall GitPy from your system.
        \r  --update                        Update the GitPy directly from GitHub.
        \r  --console                       Start the main console of GitPy.
        \r  --cli                           Start the CLI environment of GitPy.

        \r  Program                         Version (on your system)
        \r  -------                         ------------------------
        \r  gitpy                           %s

        \r  Copyright & Licensing
        \r  ---------------------
        \r  Owner                           © PSociety
        \r  Copyright                       Copyright (C) 2021-2023 PSociety, {R}All rights reserved{W}.
        \r  License                         This program is under GNU General Public License v3.0 (GPL 3.0). You can modify the program and 
        \r                                  share it as long as the original author appears in credits and the program is on the same license.

        \r  Other informations
        \r  ------------------
        \r  GitHub page                     https://github.com/MyMeepSQL/gitpy
        \r  Changelogs                      https://github.com/MyMeepSQL/GitPy/blob/master/src/docs/CHANGELOG.md
        \r  Issues pages                    https://github.com/MyMeepSQL/gitpy/issues

        \r{SB2}{bold}Informations about authors{W}:
        \r===========================

        \r  Main informations
        \r  -----------------
        \r  MyMeepSQL's fullname            Thomas Pellissier
        \r  MyMeepSQL's email               thomas.pellissier.pro@proton.me ({bold}only for professional{W} or for {G}report bugs of GitPy{W})

        \r  Bashy's fullname                Jonas Petitpierre
        \r  Bashy's email                   petitpierre@duck.com ({bold}only for personal{W} or for {G}report bugs of GitPy{W})

        \r  Other informations
        \r  ------------------
        \r  MyMeepSQL's GitHub profile      https://github.com/MyMeepSQL
        \r  MyMeepSQL's Twitter profile     https://twitter.com/MyMeepSQL
        \r  MyMeepSQL's Discord username    MyMeepSQL#0141

        \r  Bashy's GitHub profile          https://github.com/jonas52
        \r  Bashy's Discord username        Bashy#2643''' % self.VERSION)
