#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ internet_check.py         [Created: 2023-02-21 |  8:32 - PM]  #
#                                       [Updated: 2023-02-21 |  9:10 - PM]  #
#---[Info]------------------------------------------------------------------#
#  Check if the user are connected to the Internet or not                   #
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
from urllib import request

# Main
def internet_check(host='https://google.com'):
    '''
    Check if the user have an Internet connection by connecting to google.com over https
    '''
    try:
        request.urlopen(host, timeout=4)
        return True
    except:
        return False
