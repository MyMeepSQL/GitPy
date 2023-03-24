#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Metadata]--------------------------------------------------------------#
#  Filename ~ based_distro.py           [Created: 2023-02-07 |  8:38 - AM]  #
#                                       [Updated: 2023-02-07 |  9:24 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The function for check if the user's machine ran on a Debian distro      #
#  based or an Arch based.                                                  #
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

## Third party libraries
from src.util.process import Process

# Main
class Based_Distro():
    '''
    Check if the user machine distro is based on Debian or Arch
    '''
    def __init__(self=None):
        # if we trigger on sources.list then we know its Debian based distro
        if os.path.isfile("/etc/apt/sources.list"):
            return 'Debian'
        # If pacman.conf exists, we have a Arch based distro
        elif os.path.isfile("/etc/pacman.conf"):
            return 'Arch'
        else:
            return 'Any based'
    