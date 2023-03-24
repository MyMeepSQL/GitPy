#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ gitpy.py                 [Created: 2023-01-26 | 10:37 - AM]  #
#                                       [Updated: 2023-02-13 |  4:12 - PM]  #
#---[Info]------------------------------------------------------------------#
#  The call methode of gitpy                                               #
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
import sys
from src import __main__

## Third party libraries
from src.util.colors import Color
from src.config import Configuration

# Main
try:
    # Where this file is executed
    cwd = os.path.dirname(os.path.abspath(__file__))

    # Call the entry point of the main file of GitPy
    __main__.entry_point(pwd = cwd)

except ModuleNotFoundError as mnfe:
    Color.pexception(mnfe)
    Color.pl('  {!} ModuleNotFoundError: %s' % mnfe)
    Color.pl('  {*} Try to run {G}gitpy --install{W} to install GitPy properly on you system.')
    Color.pl('  {*} If the problem was not solved, please report the issue on {C}%s{W}' % Configuration.REPO_URL)

except NameError as ne:
    Color.pexception(ne)
    Color.pl('  {!} NameError: %s' % ne)
    Color.pl('  {*} Try to run {G}gitpy --install{W} to install GitPy properly on you system.')
    Color.pl('  {*} If the problem was not solved, please report the issue on {C}%s{W}' % Configuration.REPO_URL)

except ImportError as ie:
    Color.pexception(ie)
    Color.pl('  {!} ImportError: %s' % ie)
    Color.pl('  {*} Try to run {G}gitpy --install{W} to install GitPy properly on you system.')
    Color.pl('  {*} If the problem was not solved, please report the issue on {C}%s{W}' % Configuration.REPO_URL)

except Exception as e:
    Color.pexception(e)
    Color.pl('  {!} Exception error: %s' % e)
    Color.pl('  {*} Try to run {G}gitpy --install{W} to install GitPy properly on you system.')
    Color.pl('  {*} If the problem was not solved, please report the issue on {C}%s{W}' % Configuration.REPO_URL)

except KeyboardInterrupt:
    Color.pl('\n  {!} Interrupted, shutting down...')
    sys.exit(1)
