#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ exit_tool.py              [Created: 2023-03-28 |  8:54 - PM]  #
#                                       [Updated: 2023-04-03 | 15:00 - PM]  #
#---[Info]------------------------------------------------------------------#
#  Just a small function to prompt a exit message if verbose was applied    #
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
import sys

## Third party libraries
from src.util.colors import Color

# Function section
def exit_tool(code,pwd):
    '''
        Exit and removing the python cache with a message if verbose was applied

        Args:
            code (int): The exit code
            pwd (str): The current working directory

    '''
    from src.config import Configuration
    from src.util.remove_python_cache import remove_python_cache

    if not pwd:
        pwd = Configuration.pwd
    remove_python_cache(pwd=pwd)
    if Configuration.verbose == 3:
        if code == 0:
            Color.pl('  {§} Exiting with the exit code: {G}0{W}')
            Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(0){W}')
        else:
            Color.pl('  {§} Exiting with the exit code: {R}1{W}')
            Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
    sys.exit(code)