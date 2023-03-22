#!/usr/bin/env python3

#---[Metadata]--------------------------------------------------------------#
#  Filename ~ informations.py           [Created: 2023-02-28 |  9:21 - AM]  #
#                                       [Updated: 2023-02-28 | 10:28 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The informations page about AOVPNS                                       #
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
## Third party libraries
from src.util.colors import Color
from src.config import Configuration

# Main
class Informations():
    '''
    The main class of the informations page of AOVPNS that will be called when the user runs aovpns --info. 
    This class will display all informations about AOVPNS.
    '''

    VERSION = Configuration.VERSION

    def __init__(self):
        Color.pl('''
        \r  {*} All informations about the AOVPNS.

        \r{SB2}{bold}Informations about AOVPNS{W}:
        \r==========================

        \r  Description
        \r  -----------
        \r  AOVPNS is a tool to automatate an OpenVPN server configuration 
        \r  and installation with users. It's a tool for Linux distros based
        \r  on Debian or Arch (for the moment).

        \r  Options                  Description
        \r  -------                  -----------
        \r  --install                Install AOVPNS with all depencies on your system.
        \r  --uninstall              Uninstall AOVPNS from your system.
        \r  --update                 Update the AOVPNS directly from GitHub.
        \r  --console                Start the main console of AOVPNS.
        \r  --cli                    Start the CLI environment of AOVPNS.

        \r  Program                  Version (on your system)
        \r  -------                  ------------------------
        \r  aovpns                   %s

        \r  Copyright & Licensing
        \r  ---------------------
        \r  Owner                    © PSociety™ by Thomas Pellissier (MyMeepSQL)
        \r  Copyright                Copyright (C) 2021-2023 PSociety™, {R}All rights reserved{W}. By Thomas Pellissier (MyMeepSQL)
        \r  License                  This program is under GNU General Public License v3.0 (GPL 3.0). You can modify the program and 
        \r                           share it as long as the original author appears in credits and the program is on the same license.

        \r  Other informations
        \r  ------------------
        \r  GitHub page              https://github.com/MyMeepSQL/aovpns
        \r  Changelogs               https://github.com/MyMeepSQL/aovpns/blob/main/CHANGLOG.md
        \r  Issues pages             https://github.com/MyMeepSQL/aovpns/issues

        \r{SB2}{bold}Informations about author{W}:
        \r==========================

        \r  General informations
        \r  --------------------
        \r  Author's fullname        Thomas Pellissier
        \r  Author's codename        MyMeepSQL
        \r  Author's email           thomas.pellissier.pro@proton.me ({bold}only for professional{W} or for {G}report bugs of AOVPNS{W})

        \r  Other informations
        \r  ------------------
        \r  GitHub profile           https://github.com/MyMeepSQL
        \r  Twitter profile          https://twitter.com/MyMeepSQL
        \r  Discord username         MyMeepSQL#0141''' % self.VERSION)
