#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ __main__.py               [Created: 2023-01-31 | 09:20 - AM]  #
#                                       [Updated: 2023-01-31 | 09:20 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The main file of GitPy, where all start                                  #
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
from gettext import gettext as _

## Third party libraries
from src.config import Configuration
from src.util.colors import Color
from src.util.exit_tool import exit_tool

# Main
class GitPy(object):
    '''
        The first GitPy class that will be called first when the user runs GitPy
    '''

    def __init__(self, pwd):
        if len(sys.argv) == 1:
            # If the user ran gitpy with any option(s) 

            # Print the banner before prompt the error message
            Color.pl(self.Banner())

            Color.pl('''
                \r  {*} {C}Usage{W}: gitpy <OPTIONS>
                \r  {!} Missing options
                \r  {*} Try {G}gitpy -h{W} or {G}gitpy --help{W} for more information.''')

            exit_tool(1, pwd=pwd)

        # elif '--help' in sys.argv or '-h' in sys.argv:

        #     ''' If the user ran gitpy with the '-h/--help' option '''

        #     Banner()
        #     print()

        #     # Get the avalable arguments of GitPy in Arguments class
        #     args = Arguments()

        #     # Load parsed argument into the Configuration class
        #     C.load_from_arguments(args.get_arguments, pwd = pwd)

        else:

            # Load parsed argument into the Configuration class
            Configuration.load_arguments(pwd=pwd)

        # if os.getuid() != 0:
        #     Color.pl('  {!} {O}You need to be root to run this script{W}')
        #     sys.exit(1)

    # Banner
    @staticmethod
    def Banner():
        '''
            The banner of the 'gitpy' command
        '''
        
        return '''{SB2}{bold}
            \r ┌─┐┬┌┬┐┌─┐┬ ┬ {W}{bold}{{W}{D}%s{W}{bold}}{W}{SB2}{bold}
            \r │ ┬│ │ ├─┘└┬┘ {W}{D}by MyMeepSQL & Bashy{W}{SB2}{bold}
            \r └─┘┴ ┴ ┴   ┴  {W}{GR}{underscore}%s{W}''' % (Configuration.VERSION, Configuration.REPO_URL)


# Main (entry point)
def entry_point(pwd):
    '''
        The entry point of the GitPy
    '''

    try:
        GitPy(pwd=pwd)
        # remove_python_cache(pwd=pwd)

    # ---- Catching some errors ---- #

    # except KeyError as ke:
    #     Color.pexception(ke)
    #     Color.pl('  {!} KeyError: Cannot get the field %s in the GitPy\'s config file ({C}%s{W}). Did you installed GitPy?   ' % (ke , CONFIG_FILE_PATH))
    #     Color.pl('  {*} Try to run {G}gitpy --install{W} to install GitPy properly on you system.')
    #     Color.pl('  {*} If the problem was not solved, please report the issue on {C}%s{W}' % Configuration.REPO_URL)

    except ModuleNotFoundError as mnfe:
        Color.pexception(mnfe)
        # Color.pl('  {!} ModuleNotFoundError: %s' % mnfe)
        Color.pl('  {*} Try to run {G}gitpy --install{W} to install GitPy properly on you system.')
        Color.pl('  {*} If the problem was not solved, please report the issue on {C}%s{W}' % Configuration.REPO_URL)

    except NameError as ne:
        Color.pexception(ne)
        # Color.pl('  {!} NameError: %s' % ne)
        Color.pl('  {*} Try to run {G}gitpy --install{W} to install GitPy properly on you system.')
        Color.pl('  {*} If the problem was not solved, please report the issue on {C}%s{W}' % Configuration.REPO_URL)

    except ImportError as ie:
        Color.pexception(ie)
        # Color.pl('  {!} ImportError: %s' % ie)
        Color.pl('  {*} Try to run {G}gitpy --install{W} to install GitPy properly on you system.')
        Color.pl('  {*} If the problem was not solved, please report the issue on {C}%s{W}' % Configuration.REPO_URL)

    except PermissionError as pe:
        Color.pexception(pe)
        Color.pl('  {*} Try to run the same command with sudo or as root.')

    except Exception as e:
        Color.pexception(e)
        # Color.pl('  {!} Exception error: %s' % e)
        Color.pl('  {*} Try to run {G}gitpy --install{W} to install GitPy properly on you system.')
        Color.pl('  {*} If the problem was not solved, please report the issue on {C}%s{W}' % Configuration.REPO_URL)

    except KeyboardInterrupt as ki:
        Color.pexception(ki)
        Color.pl('\n  {!} Interrupted, shutting down...')
