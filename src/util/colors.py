#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---[Name & Dates]----------------------------------------------------------#
#  Filename ~ colors.py                  [Created: 2023-02-21 |  8:37 - AM]  #
#                                        [Updated: 2023-02-21 | 10:25 - AM]  #
# ---[Info]------------------------------------------------------------------#
#  All colors directly from the system                                       #
#  Language ~ Python3                                                        #
# ---[Author]----------------------------------------------------------------#
#  Thomas Pellissier (MyMeepSQL)                                             #
#  Jonas Petitpierre (Bashy)                                                 #
# ---[Operating System]------------------------------------------------------#
#  Developed for Linux                                                       #
# ---[License]---------------------------------------------------------------#
#  GNU General Public License v3.0                                           #
#  -------------------------------                                           #
#                                                                            #
#  This program is free software; you can redistribute it and/or modify      #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation; either version 2 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  This program is distributed in the hope that it will be useful,           #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License along   #
#  with this program; if not, write to the Free Software Foundation, Inc.,   #
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.               #
# ---------------------------------------------------------------------------#

# Import section
import os
import sys

# Third party libraries
from src. tools.colored.colored import fg, attr

# Main
class Color():
    '''
    The colors directly available on the system
    '''

    last_sameline_length = 0

    # Basic colors
    colors = {
        'W'             : '\033[0m',       # white (like 'reset')
        'D'             : '\033[2m',       # dims current color
        'R'             : '\033[31m',      # red
        'O'             : '\033[33m',      # orange
        'G'             : '\033[32m',      # green
        'GR'            : '\033[37m',      # gray
        'B'             : '\033[34m',      # blue
        'P'             : '\033[35m',      # purple
        'C'             : '\033[36m',      # cyan
 
        # Light colors 
        'LG'            : '\033[90m',      # light gray
        'LR'            : '\033[91m',      # light red
        'LL'            : '\033[92m',      # light green
        'LY'            : '\033[93m',      # light yellow
        'LB'            : '\033[94m',      # light blue
        'LP'            : '\033[95m',      # light purple

        # Dark colors
        'darkblack'     : '\033[030m',
        'darkR'         : '\033[031m',
        'darkgreen'     : '\033[032m',
        'darkyellow'    : '\033[033m',
        'darkB'         : '\033[034m',
        'darkmagenta'   : '\033[035m',
        'darkcyan'      : '\033[036m',
        'darkwhite'     : '\033[037m',

        # Text formating
        'bold'          : '\033[1m',
        'dark'          : '\033[2m',
        'italic'        : '\033[3m',
        'underscore'    : '\033[4m',

        # Colored's PIP package color
        # The 'S' is for 'Special'
        'SG1'           : fg('#00FF80'),   # Green n°1
        'SG2'           : fg('#00FF37'),   # Green n°2
        'SY1'           : fg('#FFEB3B'),   # Yellow n°1
        'SB1'           : fg('#2190B5'),   # Blue n°1
        'SB2'           : fg('#1898CC'),   # Blue n°2
        'SB3'           : fg('#00658E'),   # Darker Blue n°3
        'SB4'           : fg('#1d9bf0'),   # Twitter's Blue n°4
        'SGR1'          : fg('#777777'),   # Grey n°1
        'SW1'           : fg('#FFFFFF'),   # White n°1 (real white)
        'SW0'           : attr('reset')    # Reset
    }

    # Helper string replacements
    replacements = {
        '{+}'           : '{W}{D}[{W}{G}+{W}{D}]{W}',   # Finished process
        '{-}'           : '{W}{D}[{W}{G}-{W}{D}]{W}',   # Process in execution
        '{>}'           : '{W}{D}[{W}{C}>{W}{D}]{W}',   # Input
        '{*}'           : '{W}{D}[{W}{G}*{W}{D}]{W}',   # Information(s)
        '{&}'           : '{W}{D}[{W}{C}&{W}{D}]{W}',   # Command executed (verbose level: 1)
        '{#}'           : '{W}{D}[{W}{P}&{W}{D}]{W}',   # Command output (verbose level: 2)
        '{§}'           : '{W}{D}[{W}{SY1}&{W}{D}]{W}', # More information (verbose level: 3)
        '{!}'           : '{W}{D}[{W}{R}!{W}{D}]{W}',   # Error
        '{$}'           : '{W}{D}[{W}{O}${W}{D}]{W}',   # Warning
        '{?}'           : '{W}{D}[{W}{C}?{W}{D}]{W}'    # Question
    }

    @staticmethod
    def p(text):
        '''
        Prints text using colored format on same line.
        '''
        sys.stdout.write(Color.s(text))
        sys.stdout.flush()
        if '\r' in text:
            text = text[text.rfind('\r')+1:]
            Color.last_sameline_length = len(text)
        else:
            Color.last_sameline_length += len(text)

    @staticmethod
    def pl(text):
        '''
        Prints text using colored format with trailing new line.
        '''
        Color.p('%s\n' % text)
        Color.last_sameline_length = 0

    @staticmethod
    def pe(text):
        '''
        Prints text using colored format with leading and trailing new line to STDERR.
        '''
        sys.stderr.write(Color.s('%s\n' % text))
        Color.last_sameline_length = 0

    @staticmethod
    def s(text):
        '''
        Returns colored string
        '''
        output = text
        for (key, value) in Color.replacements.items():
            output = output.replace(key, value)
        for (key, value) in Color.colors.items():
            output = output.replace('{%s}' % key, value)
        return output

    @staticmethod
    def clear_line():
        spaces = ' ' * Color.last_sameline_length
        sys.stdout.write('\r%s\r' % spaces)
        sys.stdout.flush()
        Color.last_sameline_length = 0

    @staticmethod
    def clear_entire_line():
        (rows, columns) = os.popen('stty size', 'r').read().split()
        Color.p('\r' + (' ' * int(columns)) + '\r')

    @staticmethod
    def pexception(exception):
        '''
        Prints an exception. Includes stack trace if necessary.
        '''
        # from src.__main__ import GitPy
        from src.config import Configuration
        # Color.pl(GitPy.Banner())
        # print()
        Color.pl('\n  {!} {R}Error: %s' % str(exception))
        if Configuration.verbose == 0:
            Color.pl('  {*} Use {G}-v{W}/{G}--verbose{W} to show the full stack trace')
        
        # Don't dump trace for the "no targets found" case.
        if 'No targets found' in str(exception):
            return

        # if Configuration.verbose == 0:
        #     Color.pl('  {!} Full stack trace below')
        #     from traceback import format_exc
        #     Color.p('  {!}    ')
        #     err = format_exc().strip()
        #     err = err.replace('\n', '\n  {!} {C}   ')
        #     err = err.replace('  File', '{W}File')
        #     err = err.replace('  Exception: ', '{R}Exception:{W}')
        #     Color.pl(err)

        if Configuration.verbose > 0:
            Color.pl('  {!} Full stack trace below')
            from traceback import format_exc
            Color.p('  {!}    ')
            err = format_exc().strip()
            err = err.replace('\n', '\n  {!} {C}   ')
            err = err.replace('  File', '{W}File')
            err = err.replace('  Exception: ', '{R}Exception:{W}')
            Color.pl(err)


# For testing replacements
if __name__ == '__main__':
    Color.pl('{-} Testing...')
    Color.p('{+} Test complete')
    Color.pe('{-} Updating...')
    Color.pl('{!} No update package found')
