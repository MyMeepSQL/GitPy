#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ remove_python_cache.py    [Created: 2023-03-07 |  9:21 - AM]  #
#                                       [Updated: 2023-03-07 | 10:18 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Remove the __pycache__'s folder in the GitPy's folder                   #
#  Language ~ Python3                                                       #
#---[Author]----------------------------------------------------------------#
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
import shutil

## Third party libraries
from src.util.colors import Color
from src.config import Configuration

# Main
def remove_python_cache(pwd,line_enter=None):
    try:
        if Configuration.verbose == 0:
            # for dirpath, dirnames, filenames in os.walk(aovpns_dir):
            #     for dirname in dirnames:
            #         if search_pattern in dirname:
            #             full_path = os.path.join(dirpath, dirname)
            #             shutil.rmtree(full_path)

            if os.path.isdir('%s/src/__pycache__/' % pwd):
                shutil.rmtree('%s/src/__pycache__/' % pwd)

            if os.path.isdir('%s/src/core/__pycache__/' % pwd):
                shutil.rmtree('%s/src/core/__pycache__/' % pwd)

            if os.path.isdir('%s/src/modules/__pycache__/' % pwd):
                shutil.rmtree('%s/src/modules/__pycache__/' % pwd)

            if os.path.isdir('%s/src/util/__pycache__/' % pwd):
                shutil.rmtree('%s/src/util/__pycache__/' % pwd)

            if os.path.isdir('%s/src/tools/__pycache__/' % pwd):
                shutil.rmtree('%s/src/tools/__pycache__/' % pwd)

            if os.path.isdir('%s/src/tools/colored/__pycache__/' % pwd):
                shutil.rmtree('%s/src/tools/colored/__pycache__/' % pwd)

            if os.path.isdir('%s/src/tools/packaging/__pycache__/' % pwd):
                shutil.rmtree('%s/src/tools/packaging/__pycache__/' % pwd)

        else:
            # if args.v erbose:
            #     if Configuration.verbose >= 1:
            #         Color.pl('  {&} Removing python cache...')

            # for dirpath, dirnames, filenames in os.walk(aovpns_dir):
            #     for dirname in dirnames:
            #         if search_pattern in dirname:
            #             full_path = os.path.join(dirpath, dirname)

            #             if Configuration.verbose == 3:
            #                 Color.p('   {SY1}├──╼{W} Python: {SY1}shutil.rmtree(%s){W} ...' % full_path)

            #             if os.path.isdir(full_path):
            #                 shutil.rmtree(full_path)
            #                 if Configuration.verbose == 3:
            #                     Color.p(' {G}OK{W}\n')
            #             else:
            #                 if Configuration.verbose == 3:
            #                     Color.p(' {O}NOT FOUND{W}\n')


            if Configuration.verbose == 3:
                if line_enter is True:
                    Color.pl('\n  {§} Removing python cache...')
                else:
                    Color.pl('  {§} Removing python cache...')


            if Configuration.verbose == 3:
                Color.p('   {SY1}├──╼{W} Python: {SY1}shutil.rmtree(\'%s/src/__pycache__/\' % pwd){W} ...')

            if os.path.isdir('%s/src/__pycache__/' % pwd):
                shutil.rmtree('%s/src/__pycache__/' % pwd)

                if Configuration.verbose == 3:
                    Color.p(' {G}OK{W}\n')

            else:
                if Configuration.verbose == 3:
                    Color.p(' {O}NOT FOUND{W}\n')


            if Configuration.verbose == 3:
                Color.p('   {SY1}├──╼{W} Python: {SY1}shutil.rmtree(\'%s/src/core/__pycache__/\' % pwd){W} ...')

            if os.path.isdir('%s/src/core/__pycache__/' % pwd):
                shutil.rmtree('%s/src/core/__pycache__/' % pwd)

                if Configuration.verbose == 3:
                    Color.p(' {G}OK{W}\n')

            else:
                if Configuration.verbose == 3:
                    Color.p(' {O}NOT FOUND{W}\n')


            if Configuration.verbose == 3:
                Color.p('   {SY1}├──╼{W} Python: {SY1}shutil.rmtree(\'%s/src/modules/__pycache__/\' % pwd){W} ...')

            if os.path.isdir('%s/src/modules/__pycache__/' % pwd):
                shutil.rmtree('%s/src/modules/__pycache__/' % pwd)

                if Configuration.verbose == 3:
                    Color.p(' {G}OK{W}\n')

            else:
                if Configuration.verbose == 3:
                    Color.p(' {O}NOT FOUND{W}\n')


            if Configuration.verbose == 3:
                Color.p('   {SY1}├──╼{W} Python: {SY1}shutil.rmtree(\'%s/src/util/__pycache__/\' % pwd){W} ...')

            if os.path.isdir('%s/src/util/__pycache__/' % pwd):
                shutil.rmtree('%s/src/util/__pycache__/' % pwd)

                if Configuration.verbose == 3:
                    Color.p(' {G}OK{W}\n')

            else:
                if Configuration.verbose == 3:
                    Color.p(' {O}NOT FOUND{W}\n')


            if Configuration.verbose == 3:
                Color.p('   {SY1}├──╼{W} Python: {SY1}shutil.rmtree(\'%s/src/tools/__pycache__/\' % pwd){W} ...')

            if os.path.isdir('%s/src/tools/__pycache__/' % pwd):
                shutil.rmtree('%s/src/tools/__pycache__/' % pwd)

                if Configuration.verbose == 3:
                    Color.p(' {G}OK{W}\n')

            else:
                if Configuration.verbose == 3:
                    Color.p(' {O}NOT FOUND{W}\n')


            if Configuration.verbose == 3:
                Color.p('   {SY1}├──╼{W} Python: {SY1}shutil.rmtree(\'%s/src/tools/packaging/__pycache__/\' % pwd){W} ...')

            if os.path.isdir('%s/src/tools/packaging/__pycache__/' % pwd):
                shutil.rmtree('%s/src/tools/packaging/__pycache__/' % pwd)

                if Configuration.verbose == 3:
                    Color.p(' {G}OK{W}\n')

            else:
                if Configuration.verbose == 3:
                    Color.p(' {O}NOT FOUND{W}\n')


            if Configuration.verbose == 3:
                Color.p('   {SY1}╰──╼{W} Python: {SY1}shutil.rmtree(\'%s/src/tools/colored/__pycache__/\' % pwd){W} ...')

            if os.path.isdir('%s/src/tools/colored/__pycache__/' % pwd):
                shutil.rmtree('%s/src/tools/colored/__pycache__/' % pwd)

                if Configuration.verbose == 3:
                    Color.p(' {G}OK{W}\n')

            else:
                if Configuration.verbose == 3:
                    Color.p(' {O}NOT FOUND{W}\n')
    
    except PermissionError as pe:
        Color.pexception(pe)
        Color.pl('  {*} Try to run the same command with sudo or as root.')