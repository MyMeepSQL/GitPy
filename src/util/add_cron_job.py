#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Metadata]--------------------------------------------------------------#
#  Filename ~ add_cron_job.py           [Created: 2023-04-05 | 11:12 - AM]  #
#                                       [Updated: 2023-04-05 | 11:43 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Check if the folder_path finish with 'gitpy/'.                           # 
#  Exemple: if the user enter '/home' for the install path, it will add     #
#  '/gitpy/' to the folder_path. So it give '/home/gitpy/'                  #
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
from crontab import CronTab

# Functions section
def add_cron_job():
    # Create an instance of CronTab for the current user
    cron = CronTab(user=True)

    # Create a new CronTab task that runs at 7pm every day
    job = cron.new(command='gitpy --check-repo')
    job.setall('0 19 * * *')

    # Activate the CronTab task
    job.enable()

    # Writes the modifications of CronTab
    cron.write()
    