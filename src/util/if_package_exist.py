#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ if_package_exists.py      [Created: 2023-02-28 |  8:46 - AM]  #
#                                       [Updated: 2023-02-28 |  9:22 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Check if a package are installed on the machine                          #
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
import subprocess

## Third party libraries
from src.util.based_distro import Based_Distro

# Main
def package_exists(package):
    '''
    Check if package are install on the machine
    '''
    if Based_Distro() == 'Debian':
        result = subprocess.run('dpkg -s %s' % package, shell = True, stdout = subprocess.PIPE)
    elif Based_Distro() == 'Arch':
        result = subprocess.run('pacman -Q %s' % package, shell = True, stdout = subprocess.PIPE)
    return result.stdout != b''
