#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ set_env_var.py            [Created: 2023-02-21 |  9:32 - AM]  #
#                                       [Updated: 2023-02-28 |  9:13 - AM]  #
#---[Info]------------------------------------------------------------------#
#  A function to easly make or remove a environment variables               #
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

# Main functions
def set_env_var(var_name: str, var_value: str):
    '''
    Create a environment variable
    '''
    # ---------- [ For the /etc/bash.bashrc file ] ---------- #
    # Set the environment variable in the current process
    os.environ[var_name] = var_value
    # Open the /etc/bash.bashrc file
    with open("/etc/bash.bashrc", "r") as environment:
        # Read the file into a list of lines
        lines = environment.readlines()
    # Flag to check if the variable is found
    found = False
    # Iterate over the lines
    for i, line in enumerate(lines):
        # Check if the line starts with var_name
        if line.startswith('export %s' % var_name):
            # Replace the value of the environment variable
            lines[i] = 'export %s=\'%s\'\n' % (var_name, var_value)
            found = True
    if not found:
        lines.append('export %s=\'%s\'\n' % (var_name, var_value))
    # Open the /etc/environment file for writing
    with open("/etc/bash.bashrc", "w") as environment:
        # Write the modified lines to the file
        environment.writelines(lines)

    # ---------- [ For the /etc/environment file ] ---------- #
    # Open the /etc/environment file
    with open("/etc/environment", "r") as environment:
        # Read the file into a list of lines
        lines = environment.readlines()
    # Flag to check if the variable is found
    found = False
    # Iterate over the lines
    for i, line in enumerate(lines):
        # Check if the line starts with var_name
        if line.startswith(var_name):
            # Replace the value of the environment variable
            lines[i] = '%s=\'%s\'\n' % (var_name, var_value)
            found = True
    if not found:
        lines.append('%s=\'%s\'\n' % (var_name, var_value))
    # Open the /etc/environment file for writing
    with open("/etc/environment", "w") as environment:
        # Write the modified lines to the file
        environment.writelines(lines)

def remove_env_var(var_name: str):
    '''
    Remove a environment variable
    '''
    # ---------- [ For the /etc/bash.bashrc file ] ---------- #
    # Open the /etc/bash.bashrc file
    with open("/etc/bash.bashrc", "r") as environment:
        # Read the file into a list of lines
        lines = environment.readlines()
    # Flag to check if the variable is found
    found = False
    # Iterate over the lines
    for i, line in enumerate(lines):
        # Check if the line starts with 'export var_name'
        if line.startswith('export %s' % var_name):
            # Remove the line of the environment variable
            lines[i] = ''
            found = True
    if not found:
        pass
    # Open the /etc/environment file for writing
    with open("/etc/bash.bashrc", "w") as environment:
        # Write the modified lines to the file
        environment.writelines(lines)

    # ---------- [ For the /etc/environment file ] ---------- #
    # Open the /etc/environment file
    with open("/etc/environment", "r") as environment:
        # Read the file into a list of lines
        lines = environment.readlines()
    # Flag to check if the variable is found
    found = False
    # Iterate over the lines
    for i, line in enumerate(lines):
        # Check if the line starts with 'var_name'
        if line.startswith(var_name):
            # Remove the line of the environment variable
            lines[i] = ''
            found = True
    if not found:
        pass
    # Open the /etc/environment file for writing
    with open("/etc/environment", "w") as environment:
        # Write the modified lines to the file
        environment.writelines(lines)
