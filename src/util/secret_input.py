#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ secret_input.py           [Created: 2023-03-31 |  9:45 - AM]  #
#                                       [Updated: 2023-03-31 |  9:45 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Get a ghost input                                                        #
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
import shutil

## Third party libraries
# from src.util.colors import Color
# from src.config import Configuration


# Main
class SecretInput:
    '''

    '''
    def __init__(self, prompt, show='*'):
        import os
        import sys
        import pynput
        import getpass

        self.on_char = 0
        self.show = show
        self.value = str()

        def get_active_window():
            active_window_name = None
            if sys.platform in ['linux', 'linux2']:
                try:
                    import wnck
                except ImportError:
                    os.system('sudo pip install wnck')
                    wnck = None
                if wnck is not None:
                    screen = wnck.screen_get_default()
                    screen.force_update()
                    window = screen.get_active_window()
                    if window is not None:
                        pid = window.get_pid()
                        with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
                            return f.read()
                else:
                    try:
                        from gi.repository import Gtk, Wnck
                        gi = "Installed"
                    except ImportError:
                        os.system('sudo pip install gi')
                        gi = None
                    if gi is not None:
                        Gtk.init([])
                        screen = Wnck.Screen.get_default()
                        screen.force_update()
                        active_window = screen.get_active_window()
                        pid = active_window.get_pid()
                        with open("/proc/{pid}/cmdline".format(pid=pid)) as f:
                            return f.read()
            elif sys.platform in ['Windows', 'win32', 'cygwin']:
                import win32gui
                window = win32gui.GetForegroundWindow()
                return win32gui.GetWindowText(window)
            elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
                from AppKit import NSWorkspace
                return (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])
            else:
                sys.exit(0)

        def GetPrint(prompt):
            sys.stdout.write(prompt)
            sys.stdout.flush()

            def on_press(key):
                if 'py' not in str(get_active_window()).lower():
                    return
                if(key == pynput.keyboard.Key.enter):
                    getpass.getpass('')
                    quit()
                if(key != pynput.keyboard.Key.backspace):
                    try:
                        char = key.char
                        if(key.char == None and str(format(key)).startswith('<')):
                            char = str(int(str(format(key)).replace('<', '').replace('>', ''))-96)
                        self.value += char if key != pynput.keyboard.Key.space else ' '
                        self.on_char += 1
                        sys.stdout.write(self.show)
                    except:
                        pass
                else:
                    if(self.on_char <= 0):
                        return
                    sys.stdout.write('\b \b'*len(self.show))
                    self.on_char -= 1
                    self.value = self.value[0:len(self.value)-1]

                sys.stdout.flush()

            with pynput.keyboard.Listener(on_press = on_press) as listener:
                listener.join()

        GetPrint(prompt)
        del self.on_char, self.show

    def __str__(self):
        return self.value
    

test = SecretInput('Password: ')
print(test)