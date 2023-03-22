#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Metadata]--------------------------------------------------------------#
#  Filename ~ check_path.py             [Created: 2023-02-21 | 11:12 - AM]  #
#                                       [Updated: 2023-02-21 | 11:54 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Check if the folder_path finish with 'aovpns/'.                          # 
#  Exemple: if the user enter '/home' for the install path, it will add     #
#  '/aovpns/' to the folder_path. So it give '/home/aovpns/'                #
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
import sys

## Third party modules
from src.util.colors import Color
from src.__main__ import AOVPNS
from src.config import Configuration

# Main
def check_folder_path(folder_path):
    if '//' in folder_path:
        AOVPNS.Banner()
        print()
        Color.pl('  {!} The path must not contain double slash (//)!')
        if Configuration.verbose == 3:
            Color.pl('  {§} Exiting with the exit code: {R}1{W}')
            Color.pl('    {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
        sys.exit(1)
    elif folder_path.endswith('aovpns/'):
        pass
    elif folder_path.endswith('aovpns'):
        folder_path += '/'
    elif not folder_path.endswith('aovpns'):
        if folder_path.endswith('/'):
            folder_path += 'aovpns/'
        else:
            folder_path += '/aovpns/'
        
    return folder_path