#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ console.py                [Created: 2023-03-28 | 10:26 - AM]  #
#                                       [Updated: 2023-03-28 | 12:02 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The main console of gitpy                                               #
#  Language ~ Python3                                                       #
#---[Author]----------------------------------------------------------------#
#  Thomas Pellissier (MyMeepSQL)                                            #
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
import re
import sys
import rich
import shutil
import random
import platform
import subprocess
import configparser
from time import sleep
from time import strftime
from tracemalloc import start
import gnureadline as global_readline # pip install gnureadline

## Third party libraries
from src.__main__ import GitPy
from src.config import Configuration
import src.util.ip_domain as IP_Domain
from src.util.process import Process
from src.util.clear import clear
from src.util.colors import Color
from src.util.help_messages import Help_Messages as HM
from src.util.informations import Informations
from src.util.based_distro import Based_Distro as BD
from src.util.internet_check import internet_check
from src.util.remove_python_cache import remove_python_cache
from src.util.if_package_exists import package_exists
from src.tools.colored.colored import fg, attr
# from src.tools.box import box
# from src.tools.box.table import Table
# from src.tools.box.console import Console

# -------------------- [ The Main Console ] -------------------- #
class Main_Console():
    '''
    The main console of GitPy.
    This console work like a "choices menu" console.
    '''

    VERSION = Configuration.VERSION # Current version of GitPy in the Configuration's Class.
    # REPO_VERSION=config.Configuration.REPO_VERSION # The latest version of GitPy from the GitHub Repository
    REPO_URL = Configuration.REPO_URL
    gitpy_path_env_var_name = Configuration.gitpy_path_env_var_name

    promptname = 'GitPy'

    show_main_menu = True
    show_server_config_settings_menu = True
    show_client_config_settings_menu = True
    show_openvpn_installation_menu = True

    SPACE = '#>SPACE$<#'
    
    global_commands = [

        '99',
        'exit',

        # 'clear',
        'verbose',
        'version',
        'info',
        'help'
    ]

    # OpenVPN server configuration settings
    server_ip = None
    public_ip = None
    server_port = None
    server_protocol = None
    server_dns = None
    
    ## Encryption settings
    data_channel_cipher = None
    type_of_certificate = None
    ### ECDSA
    ecdsa_key_curve = None
    ### RSA
    rsa_key_size = None

    control_chanel_cipher = None

    type_of_diffie_hellman = None
    ### ECDH
    ecdh_key_curve = None
    ### DH
    dh_key_size = None

    ### The digest algorithm authenticates tls-auth packets from the control channel.
    hmac_digest = None

    ## The control channel security
    control_channel_sec = None
    
    # First client configuration settings
    first_client_name = None
    passwordless = None


    # Check if the user's platform is a Linux machine or not
    if platform.system() != 'Linux':
        Color.pl('  {!} You tried to run GitPy on a non-linux machine. GitPy can be run only on a Linux kernel.')
        sys.exit(1)

    else:
        # Check if the GITPY_INSTALL_PATH environment variable is set or not
        try:
            GITPY_PATH = os.environ[gitpy_path_env_var_name]
            INSTALL_PATH = GITPY_PATH
        except KeyError:
            Color.pl('  {!} GitPy is not installed on this machine.')
            Color.pl('  {*} Because the {C}{bold}GITPY_INSTALL_PATH{W} environment variable is not set (in the {C}/etc/environment{W} file).')
            Color.pl('  {*} If you just installed GitPy without restart you machine after, please reboot it and try again.')
            Color.pl('  {*} Otherwise, please install GitPy before using it.')
            reboot = input(Color.s('  {?} Do you want to reboot now? [y/n] '))
            if reboot.lower() == 'y':
                Color.pl('  {+} Rebooting...')
                Process.call('reboot')
            else:
                Color.pl('  {-} Exiting...')
            if Configuration.verbose == 3:
                Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
            sys.exit(1)

        # Check if the user is root or not
        if os.getuid() != 0:
            Color.pl('  {!} The GitPy Console must be run as root.')
            Color.pl('  {*} Re-run with sudo or switch to root user.')
            if Configuration.verbose == 3:
                Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
            sys.exit(1)
        else:
            # Check if the tun module is available or not.
            if not os.path.exists('/dev/net/tun'):
                Color.pl('  {!} The TUN/TAP module is not available.')
                Color.pl('  {*} Please install it and try again.')
                if Configuration.verbose == 3:
                    Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                sys.exit(1) 
            # Distro check
            if BD.__init__() == 'Arch':
                based_distro = 'Arch'
                pass
            elif BD.__init__() == 'Debian':
                based_distro = 'Debian'
                pass
            else:
                Color.pl('  {!} You\'re not running Debian or Arch variant.')
                Color.pl('  {*} GitPy can only be run on Debian or Arch based Linux distros.')
                Color.pl('  {-} Exiting...')
                if Configuration.verbose == 3:
                    Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                    Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
                sys.exit(1)

    def is_valid_username(self, username):
        # Check if the username only contains alphanumeric characters, underscore, or dash
        return bool(re.match('^[a-zA-Z0-9_-]+$', username))
    
    def installUnbound(self):
        '''
        Install Unbound if it's not installed.
        '''
        if not os.path.exists('/etc/unbound/unbound.conf'):
            Color.pl('  {!} Unbound is not installed on this machine.')
            Color.pl('  {-} Installing Unbound...')
            Process.call('apt-get install -y unbound')
            Color.pl('  {+} Unbound has been installed successfully.')

            Color.pl('  {-} Configuring Unbound...')
            with open('/etc/unbound/unbound.conf', 'a') as f:
                f.write('''interface: 10.8.0.1
                            \raccess-control: 10.8.0.1/24 allow
                            \rhide-identity: yes
                            \rhide-version: yes
                            \ruse-caps-for-id: yes
                            \rprefetch: yes''')
        else:
            Color.pl('  {-} Configuring Unbound...')
            with open('/etc/unbound/unbound.conf', 'a') as f:
                f.write('include: /etc/unbound/openvpn.conf\n')
            with open('/etc/unbound/openvpn.conf', 'w') as f:
                f.write('''server:
                         \rinterface: 10.8.0.1
                         \raccess-control: 10.8.0.1/24 allow
                         \rhide-identity: yes
                         \rhide-version: yes
                         \ruse-caps-for-id: yes
                         \rprefetch: yes
                         \rprivate-address: 10.0.0.0/8
                         \rprivate-address: fd42:42:42:42::/112
                         \rprivate-address: 172.16.0.0/12
                         \rprivate-address: 192.168.0.0/16
                         \rprivate-address: 169.254.0.0/16
                         \rprivate-address: fd00::/8
                         \rprivate-address: fe80::/10
                         \rprivate-address: 127.0.0.0/8
                         \rprivate-address: ::ffff:0:0/96''')
        
        Color.pl('  {+} Unbound has been configured successfully.')

        Color.pl('  {-} Enabling Unbound...')
        Process.call('systemctl enable unbound')

        Color.pl('  {-} Restarting Unbound...')
        Process.call('systemctl restart unbound')

    def display_array(self, data):
        '''
        Display data in a table.

        Args:
            data (list): The list of data to display.
                Usage: [ ( 'data1', 'color1' ), ( 'data2', 'color2' ), ... ]
        '''
        
        max_len = max([len(s[0]) for s in data])
        border = f"{fg('#656565')}    ╭{'─' * (max_len + 4)}╮{attr('reset')}"
        print(border)
        for i, (s, color) in enumerate(data):
            padding = ' ' * (max_len - len(s))
            if color.startswith('#') and len(color) == 7:
                color_code = fg(color)
            else:
                color_code = attr('reset')
            print(f"{fg('#656565')}    │{attr('reset')} {color_code}{s}{attr('reset')}{padding}   {fg('#656565')}│{attr('reset')}")
        border = f"{fg('#656565')}    ╰{'─' * (max_len + 4)}╯{attr('reset')}"
        print(border)

    # def display_arrays(self, arr1, arr2):
    #     max_len1 = max([len(s[0]) for s in arr1])
    #     max_len2 = max([len(s[0]) for s in arr2])
    #     max_len = max(max_len1, max_len2)
    #     border = f"{fg('#555555')}╭{'─' * (max_len + 2)}╮{attr('reset')}"
    #     border2 = f"{fg('#555555')}╭{'─' * (max_len + 2)}╮"
    #     print(f"{border}{border2}")
    #     for i, (s1, color1) in enumerate(arr1):
    #         padding1 = ' ' * (max_len - len(s1))
    #         if color1.startswith('#') and len(color1) == 7:
    #             color_code1 = fg(color1)
    #             reset_code1 = attr('reset')
    #         else:
    #             color_code1 = fg(15)
    #             reset_code1 = attr('reset')
    #         s2, color2 = arr2[i]
    #         padding2 = ' ' * (max_len - len(s2))
    #         if color2.startswith('#') and len(color2) == 7:
    #             color_code2 = fg(color2)
    #             reset_code2 = attr('reset')
    #         else:
    #             color_code2 = fg(15)
    #             reset_code2 = attr('reset')
    #         print(f"{fg('#555555')}│ {color_code1}{s1}{reset_code1}{padding1} │ {color_code2}{s2}{reset_code2}{padding2} │{attr('reset')}")
    #     border = f"{fg('#555555')}╰{'─' * (max_len + 2)}╯{attr('reset')}"
    #     border2 = f"{fg('#555555')}╰{'─' * (max_len + 2)}╯"
    #     print(f"{border}{border2}")

    def prompt(self, menu):
        '''
        The prompt of the main console.
        '''

        ptnm = self.promptname

        if menu == 'main':
            return Color.s('{underscore}%s{W}> ' % ptnm)

        if menu == 'config_server':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}> ' % ptnm)
        
        if menu == 'config_server_ip':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}ip{W}> ' % ptnm)
        
        if menu == 'config_server_port':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}port{W}> ' % ptnm)
        if menu == 'config_server_port_custom':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}portcustom{W}> ' % ptnm)
        
        if menu == 'config_server_protocol':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}protocol{W}> ' % ptnm)
        
        if menu == 'config_server_dns':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}dns{W}> ' % ptnm)
        if menu == 'config_server_dns_custom':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}dnscustom{W}> ' % ptnm)
        
        if menu == 'config_data_channel_cipher':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}datachanelcipher{W}> ' % ptnm)
        
        if menu == 'config_server_type_of_certificate':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}typeofcertificate{W}> ' % ptnm)
        
        if menu == 'config_server_ecdsa_curve':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}ecdsacurve{W}> ' % ptnm)
        
        if menu == 'config_server_rsa_key_size':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}rsakeysize{W}> ' % ptnm)
        
        if menu == 'config_server_control_chanel_cipher':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}controlchanelcipher{W}> ' % ptnm)
        
        if menu == 'config_server_type_of_diffie_hellman':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}typeofdiffiehellman{W}> ' % ptnm)

        if menu == 'config_server_ecdh_curve':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}ecdhcurve{W}> ' % ptnm)
        
        if menu == 'config_server_dh_key_size':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}dhkeysize{W}> ' % ptnm)

        if menu == 'config_server_hmac_digest':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}hmacdigest{W}> ' % ptnm)

        if menu == 'config_server_control_chanel_security':
            return Color.s('{underscore}%s{W}:{underscore}configserver{W}:{underscore}controlchanelsecurity{W}> ' % ptnm)
        
        if menu == 'config_client_settings':
            return Color.s('{underscore}%s{W}:{underscore}configclient{W}> ' % ptnm)
        if menu == 'config_client_username':
            return Color.s('{underscore}%s{W}:{underscore}configclient{W}:{underscore}username{W}> ' % ptnm)
        if menu == 'config_client_passwordless':
            return Color.s('{underscore}%s{W}:{underscore}configclient{W}:{underscore}passwordless{W}> ' % ptnm)
        
        if menu == 'openvpn_installation':
            return Color.s('{underscore}%s{W}:{underscore}openvpninstallation{W}> ' % ptnm)
        if menu == 'openvpn_installation_confirmation':
            return Color.s('{underscore}%s{W}:{underscore}openvpninstallation{W}:{underscore}confirmation{W}> ' % ptnm)

    def execute_global_command(self, cmd):
        '''
        Execute the global commands with arguments of the "global_commands" variable.
        '''

        user_input = cmd.split(' ')
        cmd_list = [w.replace(self.SPACE , ' ') for w in user_input if w]
        cmd_list_len = len(cmd_list)
        cmd = cmd_list[0].lower() if cmd_list else ''

        if cmd == 'help':
            HM.console_help_message()

        if cmd == 'info':
            Informations()

        if cmd == 'version':
            if Configuration.verbose >= 1:
                Color.pl(Configuration.version_message_verbose)
            else:
                Color.pl(Configuration.version_message)

        if cmd == 'verbose':
            if cmd_list_len == 1:
                Color.pl('  {!} You must specify a level of verbosity.')
                Color.pl('  {*} Usage: verbose <level>')
                Color.pl('  {*} Verbose levels: 0, 1, 2, 3')
            elif cmd_list_len > 1:
                # if type(cmd_list[1]) != int:
                #     Color.pl('  {!} You must specify number instead a string to apply the verbosity level.')
                #     Color.pl('  {*} Usage: verbose <level>')
                #     Color.pl('  {*} Verbose levels: 0, 1, 2, 3')
                #     continue 
                if cmd_list[1] not in ['0', '1', '2', '3']:
                    Color.pl('  {!} You must specify number between 0 and 3.')
                    Color.pl('  {*} Usage: verbose <level>')
                    Color.pl('  {*} Verbose levels: 0, 1, 2, 3') 
                else:
                    if cmd_list[1] == '0':
                        Configuration.verbose = 0
                        Color.pl('  {+} Verbose level set to: {G}0{W}')
                    elif cmd_list[1] == '1':
                        Configuration.verbose = 1
                        Color.pl('  {+} Verbose level set to: {G}1{W}')
                    elif cmd_list[1] == '2':
                        Configuration.verbose = 2
                        Color.pl('  {+} Verbose level set to: {G}2{W}')
                    elif cmd_list[1] == '3':
                        Configuration.verbose = 3
                        Color.pl('  {+} Verbose level set to: {G}3{W}')

        if cmd == 'exit' or cmd == '99':
            remove_python_cache(pwd=self.pwd, line_enter=False)
            if Configuration.verbose == 3:
                Color.pl('  {§} Exiting with the exit code: {G}0{W}')
                Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(0){W}')
            sys.exit(0)

    # -------------------- [ The Main Console ] -------------------- #
    def config_server_settings(self):
        '''
        The OpenVPN configuration menu.
        '''

        while True:
            if self.show_server_config_settings_menu == True:
                clear()
                # A little box showing the current openvpn configuration settings (the variable under the __init__() function), the box should be adapted with the size of the variable.

                # The box should be updated when the user change the settings.
                if self.server_ip == None:
                    self.server_ip = '-'

                if self.server_port == None:
                    self.server_port = '-'

                if self.server_protocol == None:
                    self.server_protocol = '-'

                if self.server_dns == None:
                    self.server_dns = '-'

                if self.data_channel_cipher == None:
                    self.data_channel_cipher = '-'

                if self.type_of_certificate == None:
                    self.type_of_certificate = '-'

                if self.ecdsa_key_curve == None:
                    self.ecdsa_key_curve = '-'
                
                # If the user has chosen the ECDSA certificate, the RSA key 
                # size should not be applied. Because it is another certificate.
                if self.type_of_certificate == 'ECDSA':

                    if self.ecdsa_key_curve == None or self.ecdsa_key_curve == 'Not applicable':
                        self.ecdsa_key_curve = '-'

                    self.rsa_key_size = 'Not applicable'

                # If the user has chosen the RSA certificate, the ECDSA key 
                # curve should not be applied. Because it is another certificate.
                if self.type_of_certificate == 'RSA':

                    if self.rsa_key_size == None or self.rsa_key_size == 'Not applicable':
                        self.rsa_key_size = '-'

                    self.ecdsa_key_curve = 'Not applicable'

                if self.rsa_key_size == None:
                    self.rsa_key_size = '-'

                if self.control_chanel_cipher == None:
                    self.control_chanel_cipher = '-'

                if self.type_of_diffie_hellman == None:
                    self.type_of_diffie_hellman = '-'

                # If the user has chosen the ECDH Diffie-Hellman's key, the DH key size
                # should not be applied. Because it is another type of Diffie-Hellman's key
                if self.type_of_diffie_hellman == 'ECDH':

                    if self.ecdh_key_curve == None or self.ecdh_key_curve == 'Not applicable':
                        self.ecdh_key_curve = '-'

                    self.dh_key_size = 'Not applicable'

                # If the user has chosen the DH Diffie-Hellman's key, the ECDH key curve
                # should not be applied. Because it is another type of Diffie-Hellman's key
                if self.type_of_diffie_hellman == 'DH':
                        
                        if self.dh_key_size == None or self.dh_key_size == 'Not applicable':
                            self.dh_key_size = '-'
    
                        self.ecdh_key_curve = 'Not applicable'

                if self.ecdh_key_curve == None:
                    self.ecdh_key_curve = '-'

                if self.dh_key_size == None:
                    self.dh_key_size = '-'

                if self.hmac_digest == None:
                    self.hmac_digest = '-'

                if self.control_channel_sec == None:
                    self.control_channel_sec = '-'

                # Data channel settings
                data = [
                    ('',''), 
                    ('  Current OpenVPN configuration settings:  ', ''),
                    ('  =======================================', '#1898CC'),
                    ('',''), 
                    ('  IP                          ::  %s' % self.server_ip, ''),
                    ('  Port                        ::  %s' % self.server_port, ''),
                    ('  Protocol                    ::  %s' % self.server_protocol, ''),
                    ('  DNS server                  ::  %s' % self.server_dns, ''),
                    ('  Data channel cipher         ::  %s' % self.data_channel_cipher, ''),
                    ('  Type of certificate         ::  %s' % self.type_of_certificate, ''),
                    ('    - ECDSA\'s key curve       ::  %s' % self.ecdsa_key_curve, ''),
                    ('    - RSA\'s key size          ::  %s' % self.rsa_key_size, ''),
                    ('  Control chanel\'s cipher     ::  %s' % self.control_chanel_cipher, ''),
                    ('  Type of Diffie-Hellman      ::  %s' % self.type_of_diffie_hellman, ''),
                    ('    - ECDH\'s key curve        ::  %s' % self.ecdh_key_curve, ''),
                    ('    - DH\'s key size           ::  %s' % self.dh_key_size, ''),
                    ('  HMAC\'s digest               ::  %s' % self.hmac_digest, ''),
                    ('  Control chanel\'s security   ::  %s' % self.control_channel_sec, ''),
                    ('',''),
                    ]

                # Display the data
                self.display_array(data=data)

                # Display the menu
                Color.pl('''{D}    ╭────────────────────────────────────────────╮
                             \r    │                                            │
                             \r    │   {W}Select from the menu:{D}                    │
                             \r    │   {SB2}====================={W}{D}                    │
                             \r    │                                            │
                             \r    │   {W}[{SB2}{bold}01{W}] Set IP                              {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] Set Port                            {D}│
                             \r    │   {W}[{SB2}{bold}03{W}] Set Protocol                        {D}│
                             \r    │   {W}[{SB2}{bold}04{W}] Set DNS Server                      {D}│
                             \r    │   {W}[{SB2}{bold}05{W}] Set Data channel cipher             {D}│
                             \r    │   {W}[{SB2}{bold}06{W}] Set Type of certificate             {D}│
                             \r    │   {W}[{SB2}{bold}07{W}] Set ECDSA\'s key curve               {D}│
                             \r    │   {W}[{SB2}{bold}08{W}] Set RSA\'s key size                  {D}│
                             \r    │   {W}[{SB2}{bold}09{W}] Set Control chanel\'s cipher         {D}│
                             \r    │   {W}[{SB2}{bold}10{W}] Set Type of Diffie-Hellman\'s key    {D}│
                             \r    │   {W}[{SB2}{bold}11{W}] Set ECDH\'s key curve                {D}│
                             \r    │   {W}[{SB2}{bold}12{W}] Set DH\'s key size                   {D}│
                             \r    │   {W}[{SB2}{bold}13{W}] Set HMAC\'s digest                   {D}│
                             \r    │   {W}[{SB2}{bold}14{W}] Control chanel\'s security           {D}│
                             \r    │                                            │
                             \r    │   {SB2}======================================{W}{D}   │
                             \r    │                                            │
                             \r    │{W}   After applying these settings, go back   {D}│
                             \r    │{W}   to the first page and select {W}[{SB2}{bold}02{W}] to     {D}│
                             \r    │{W}   config the client's settings.            {D}│
                             \r    │                                            │
                             \r    ╰────────────────────────────────────────────╯{W}''')

            self.show_server_config_settings_menu = False

            # Get user input
            text_input = input(self.prompt(menu='config_server')).strip()

            # Create cmd-line args list
            user_input = text_input.split(' ')
            cmd_list = [w.replace(self.SPACE , ' ') for w in user_input if w]
            cmd_list_len = len(cmd_list)
            cmd = cmd_list[0].lower() if cmd_list else ''

            if not cmd:
                self.show_server_config_settings_menu = True
                continue

            if cmd == '1' or cmd == '01':
                # Set the IP address
                Color.pl('  {*} Type {G}88{W} or {G}back{W} to leave this input.')
                Color.pl('  {*} Enter the IPv4 address of the network interface you want OpenVPN listening to.')

                private_ip = IP_Domain.get_private_ip()
                Color.pl('  {*} Private IP: {G}%s{W} (Type Enter key to attribute without write it)' % private_ip)

                while True:
                    text_input = input(self.prompt(menu='config_server_ip')).strip()

                    ip = text_input

                    if text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    if text_input == '':
                        ip = private_ip

                    if ip == None:
                        Color.pl('  {!} Can get the current private IP of your machine.')
                        Color.pl('  {*} Please check your network configuration and try again.')
                        break

                    if IP_Domain.validate_ips_and_domains(values=ip) == False:
                        Color.pl('  {!} Invalid IP address!')
                        continue

                    if IP_Domain.is_private_ip(ip=ip) == True:
                        Color.pl('  {*} It seems this server is behind NAT. What is its public IPv4 address or hostname?')
                        public_ip = IP_Domain.get_public_ip()
                        Color.pl('  {*} Public IP: {G}%s{W} (Type Enter key to attribute without write it)' % public_ip)
                        text_input = input(self.prompt(menu='config_server_ip')).strip()

                        if text_input == '88' or text_input == 'back':
                            self.show_server_config_settings_menu = True
                            self.config_server_settings()

                        if text_input == '':
                            self.server_ip = public_ip
                            self.show_server_config_settings_menu = True
                            self.config_server_settings()

                    else:
                        self.server_ip = text_input
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

            elif cmd == '2' or cmd == '02':
                # Set the port
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] Default: 1194                 {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] Custom                        {D}│
                             \r    │   {W}[{SB2}{bold}03{W}] Random [49152-65535]          {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')

                while True:
                    text_input = input(self.prompt(menu='config_server_port')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.server_port = '1194'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        Color.pl('  {*} Type {G}88{W} or {G}back{W} to leave this input.')
                        Color.pl('  {*} Enter the port number you want OpenVPN listening to.')

                        while True:
                            text_input = input(self.prompt(menu='config_server_port_custom')).strip()

                            if not text_input:
                                continue

                            if text_input == '88' or text_input == 'back':
                                self.show_server_config_settings_menu = True
                                self.config_server_settings()

                            if int(text_input) < 1 or int(text_input) > 65535:
                                Color.pl('  {!} Invalid port number!')
                                continue

                            self.server_port = text_input
                            self.show_server_config_settings_menu = True
                            self.config_server_settings()

                    elif text_input == '3' or text_input == '03':
                        self.server_port = str(random.randint(49152, 65535))
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            
            elif cmd == '3' or cmd == '03':
                # Set the protocol
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] UDP (recommended)             {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] TCP                           {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')
                
                while True:
                    text_input = input(self.prompt(menu='config_server_protocol')).strip()
                    
                    if not text_input:
                        continue

                    elif text_input == '1' or text_input == '01':
                        self.server_protocol = 'UDP'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.server_protocol = 'TCP'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()
                    
                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            elif cmd == '4' or cmd == '04':
                # Set the DNS servers 
                Color.pl('''{D}    ╭──────────────────────────────────────────────────────────╮
                             \r    │                                                          │
                             \r    │   {W}Select from the menu:{D}                                  │
                             \r    │   {SB2}====================={W}{D}                                  │
                             \r    │                                                          │
                             \r    │   {W}[{SB2}{bold}01{W}] Current system resolvers (from /etc/resolv.conf)  {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] Self-hosted DNS Resolver (Unbound)                {D}│
                             \r    │   {W}[{SB2}{bold}03{W}] Cloudflare (Anycast: worldwide)                   {D}│
                             \r    │   {W}[{SB2}{bold}04{W}] Quad9 (Anycast: worldwide)                        {D}│
                             \r    │   {W}[{SB2}{bold}05{W}] Quad9 uncensored (Anycast: worldwide)             {D}│
                             \r    │   {W}[{SB2}{bold}06{W}] FDN (France)                                      {D}│
                             \r    │   {W}[{SB2}{bold}07{W}] DNS.WATCH (Germany)                               {D}│
                             \r    │   {W}[{SB2}{bold}08{W}] OpenDNS (Anycast: worldwide)                      {D}│
                             \r    │   {W}[{SB2}{bold}09{W}] Google (Anycast: worldwide)                       {D}│
                             \r    │   {W}[{SB2}{bold}10{W}] Yandex Basic (Russia)                             {D}│
                             \r    │   {W}[{SB2}{bold}11{W}] AdGuard DNS (Anycast: worldwide)                  {D}│
                             \r    │   {W}[{SB2}{bold}12{W}] NextDNS (Anycast: worldwide)                      {D}│
                             \r    │   {W}[{SB2}{bold}13{W}] Custom                                            {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu                       {D}│
                             \r    │                                                          │
                             \r    ╰──────────────────────────────────────────────────────────╯{W}''')
                
                while True:
                    text_input = input(self.prompt(menu='config_server_dns')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.server_dns = IP_Domain.get_default_dns_resolver()
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.server_dns = '10.8.0.1'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '3' or text_input == '03':
                        self.server_dns = '1.1.1.1,1.0.0.1'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '4' or text_input == '04':
                        self.server_dns = '9.9.9.9,149.112.112.112'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '5' or text_input == '05':
                        self.server_dns = '9.9.9.10,149.112.112.10'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '6' or text_input == '06':
                        self.server_dns = '80.67.169.40,80.67.169.12'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '7' or text_input == '07':
                        self.server_dns = '84.200.69.80,84.200.70.40'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '8' or text_input == '08':
                        self.server_dns = '208.67.222.222,208.67.220.220'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '9' or text_input == '09':
                        self.server_dns = '8.8.8.8,8.8.4.4'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '10':
                        self.server_dns = '77.88.8.8,77.88.8.1'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '11':
                        self.server_dns = '94.140.14.14,94.140.15.15'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '12':
                        self.server_dns = '45.90.28.167,45.90.30.167'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()
                    
                    elif text_input == '13':
                        Color.pl('  {*} Type {G}88{W} or {G}back{W} to leave this input.')
                        Color.pl('  {*} Enter a custom DNS server IP address or domain name')
                        Color.pl('  {*} You can enter multiple DNS servers separated by commas')

                        while True:
                            text_input = input(self.prompt(menu='config_server_dns_custom')).strip()

                            if not text_input:
                                continue

                            if text_input == '88' or text_input == 'back':
                                self.show_server_config_settings_menu = True
                                self.config_server_settings()

                            if IP_Domain.validate_ips(ips=text_input) == False:
                                Color.pl('  {!} Invalid IP address. Please try again.')
                                continue

                            self.server_dns = text_input
                            self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        break

                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            elif cmd == '5' or cmd == '05':
                # Set the Data channel cipher
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] AES-128-GCM (recommended)     {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] AES-192-GCM                   {D}│
                             \r    │   {W}[{SB2}{bold}03{W}] AES-256-GCM                   {D}│
                             \r    │   {W}[{SB2}{bold}04{W}] AES-128-CBC                   {D}│
                             \r    │   {W}[{SB2}{bold}05{W}] AES-192-CBC                   {D}│
                             \r    │   {W}[{SB2}{bold}06{W}] AES-256-CBC                   {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')
                while True:
                    text_input = input(self.prompt(menu='config_data_channel_cipher')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.data_channel_cipher = 'AES-128-GCM'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.data_channel_cipher = 'AES-192-GCM'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '3' or text_input == '03':
                        self.data_channel_cipher = 'AES-256-GCM'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '4' or text_input == '04':
                        self.data_channel_cipher = 'AES-128-CBC'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '5' or text_input == '05':
                        self.data_channel_cipher = 'AES-192-CBC'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '6' or text_input == '06':
                        self.data_channel_cipher = 'AES-256-CBC'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()
                    
                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            elif cmd == '6' or cmd == '06':
                # Set the type of certificate
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] ECDSA (recommended)           {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] RSA                           {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')
                
                while True:
                    text_input = input(self.prompt(menu='config_server_type_of_certificate')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.type_of_certificate = 'ECDSA'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.type_of_certificate = 'RSA'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()
                    
                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            # elif cmd == '7' or cmd == '07' and self.type_of_certificate == 'RSA':
            #     if self.type_of_certificate == None:
            #         Color.pl('  {!} Chose a type of certificate first and try again.')
                    
            #     else:
            #         Color.pl('  {!} You cannot change the key curve for ECDSA certificate.')
            #         Color.pl('  {*} Because you have selected RSA as the type of certificate and not ECDSA.')

            elif cmd == '7' or cmd == '07':
                # Set the ECDSA's key curve
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] prime256v1 (recommended)      {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] secp384r1                     {D}│
                             \r    │   {W}[{SB2}{bold}03{W}] secp521r1                     {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')
                while True:
                    text_input = input(self.prompt(menu='config_server_ecdsa_curve')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.ecdsa_key_curve = 'prime256v1'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.ecdsa_key_curve = 'secp384r1'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '3' or text_input == '03':
                        self.ecdsa_key_curve = 'secp521r1'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()
                    
                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            # elif cmd == '8' or cmd == '08' and self.type_of_certificate == 'ECDSA':
            #     print(self.type_of_certificate)
            #     Color.pl('  {!} You cannot change the key size for RSA certificate.')
            #     Color.pl('  {*} Because you have selected ECDSA as the type of certificate and not RSA.')

            elif cmd == '8' or cmd == '08':
                # Set the RSA's key size
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] 2048 bits (recommended)       {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] 3072 bits                     {D}│
                             \r    │   {W}[{SB2}{bold}03{W}] 4096 bits                     {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')
                
                while True:
                    text_input = input(self.prompt(menu='config_server_rsa_key_size')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.rsa_key_size = '2048'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.rsa_key_size = '3072'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '3' or text_input == '03':
                        self.rsa_key_size = '4096'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()
                    
                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            elif cmd == '9' or cmd == '09':
                # Set the Control chanel's cipher

                ## For ECDSA
                if self.type_of_certificate == 'ECDSA':

                    Color.pl('''{D}    ╭───────────────────────────────────────────────────────╮
                                 \r    │                                                       │
                                 \r    │   {W}Select from the menu:{D}                               │
                                 \r    │   {SB2}====================={W}{D}                               │
                                 \r    │                                                       │
                                 \r    │   {W}[{SB2}{bold}01{W}] ECDHE-ECDSA-AES-128-GCM-SHA256 (recommended)   {D}│
                                 \r    │   {W}[{SB2}{bold}02{W}] ECDHE-ECDSA-AES-256-GCM-SHA384                 {D}│
                                 \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu                    {D}│
                                 \r    │                                                       │
                                 \r    ╰───────────────────────────────────────────────────────╯{W}''')
                    
                    while True:
                        text_input = input(self.prompt(menu='config_server_control_chanel_cipher')).strip()

                        if not text_input:
                            continue

                        if text_input == '1' or text_input == '01':
                            self.control_chanel_cipher = 'TLS-ECDHE-ECDSA-AES-128-GCM-SHA256'
                            self.show_server_config_settings_menu = True
                            self.config_server_settings()

                        elif text_input == '2' or text_input == '02':
                            self.control_chanel_cipher = 'TLS-ECDHE-ECDSA-AES-256-GCM-SHA384'
                            self.show_server_config_settings_menu = True
                            self.config_server_settings()

                        elif text_input == '88' or text_input == 'back':
                            self.show_server_config_settings_menu = True
                            self.config_server_settings()
                        
                        else:
                            Color.pl('  {!} Invalid option. Please try again.')
                            continue

                ## For RSA
                elif self.type_of_certificate == 'RSA':

                    Color.pl('''{D}    ╭─────────────────────────────────────────────────────╮
                                 \r    │                                                     │
                                 \r    │   {W}Select from the menu:{D}                             │
                                 \r    │   {SB2}====================={W}{D}                             │
                                 \r    │                                                     │
                                 \r    │   {W}[{SB2}{bold}01{W}] ECDHE-RSA-AES-128-GCM-SHA256 (recommended)   {D}│
                                 \r    │   {W}[{SB2}{bold}02{W}] ECDHE-RSA-AES-256-GCM-SHA384                 {D}│
                                 \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu                  {D}│
                                 \r    │                                                     │
                                 \r    ╰─────────────────────────────────────────────────────╯{W}''')
                    
                    while True:
                        text_input = input(self.prompt(menu='config_server_control_chanel_cipher')).strip()

                        if not text_input:
                            continue

                        if text_input == '1' or text_input == '01':
                            self.control_chanel_cipher = 'TLS-ECDHE-ECDSA-AES-128-GCM-SHA256'
                            self.show_server_config_settings_menu = True
                            self.config_server_settings()

                        elif text_input == '2' or text_input == '02':
                            self.control_chanel_cipher = 'TLS-ECDHE-ECDSA-AES-256-GCM-SHA384'
                            self.show_server_config_settings_menu = True
                            self.config_server_settings()

                        elif text_input == '88' or text_input == 'back':
                            self.show_server_config_settings_menu = True
                            self.config_server_settings()
                        
                        else:
                            Color.pl('  {!} Invalid option. Please try again.')
                            continue
                        
                else:
                    Color.pl('  {!} Chose a type of certificate first and try again.')

            elif cmd == '10':
                # Set the type of Diffie-Hellman's key
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] ECDH (recommended)            {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] DH                            {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')

                while True:
                    text_input = input(self.prompt(menu='config_server_type_of_diffie_hellman')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.type_of_diffie_hellman = 'ECDH'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.type_of_diffie_hellman = 'DH'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()
                    
                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            elif cmd == '11':
                # Set the ECDH key's curve
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] prime256v1 (recommended)      {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] secp384r1                     {D}│
                             \r    │   {W}[{SB2}{bold}03{W}] secp521r1                     {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')

                while True:
                    text_input = input(self.prompt(menu='config_server_ecdh_curve')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.ecdh_key_curve = 'prime256v1'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.ecdh_key_curve = 'secp384r1'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '3' or text_input == '03':
                        self.ecdh_key_curve = 'secp521r1'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            elif cmd == '12':
                # Set the DH key's size
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] 2048 bits (recommended)       {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] 3072 bits                     {D}│
                             \r    │   {W}[{SB2}{bold}03{W}] 4096 bits                     {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')

                while True:
                    text_input = input(self.prompt(menu='config_server_dh_key_size')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.dh_key_size = '2048'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.dh_key_size = '3072'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '3' or text_input == '03':
                        self.dh_key_size = '4096'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            elif cmd == '13':
                # Set the HMAC digest algorithm
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] SHA-256 (recommended)        {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] SHA-384                      {D}│
                             \r    │   {W}[{SB2}{bold}03{W}] SHA-512                      {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')

                while True:
                    text_input = input(self.prompt(menu='config_server_hmac_digest')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.hmac_digest = 'SHA-256'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.hmac_digest = 'SHA-384'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '3' or text_input == '03':
                        self.hmac_digest = 'SHA-512'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            elif cmd == '14':
                # Set Control chanel's security
                Color.pl('''{D}    ╭──────────────────────────────────────╮
                             \r    │                                      │
                             \r    │   {W}Select from the menu:{D}              │
                             \r    │   {SB2}====================={W}{D}              │
                             \r    │                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] tls-crypt (recommended)       {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] tls-auth                      {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu   {D}│
                             \r    │                                      │
                             \r    ╰──────────────────────────────────────╯{W}''')

                while True:
                    text_input = input(self.prompt(menu='config_server_control_chanel_security')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.control_channel_sec = 'tls-crypt'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '2' or text_input == '02':
                        self.control_channel_sec = 'tls-auth'
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_server_config_settings_menu = True
                        self.config_server_settings()

                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            elif cmd == '88' or cmd == 'back':
                self.show_main_menu = True
                self.__init__(pwd=self.pwd)

            elif cmd in self.global_commands:
                self.execute_global_command(cmd=text_input)

            else:
                Color.pl('  {!} Invalid option. Please try again.')
                continue

    def config_clients_settings(self):
        '''
        The OpenVPN client's configuration menu.
        '''
        
        while True:
            if self.show_client_config_settings_menu == True:
                clear()

                if self.first_client_name == None:
                    self.first_client_name = '-'

                if self.passwordless == None:
                    self.passwordless = '-'
                    
                # Data channel settings
                data = [
                    ('',''), 
                    ('  Current client\'s configuration settings:  ', ''),
                    ('  ========================================', '#1898CC'),
                    ('',''), 
                    ('  Username                    ::  %s' % self.first_client_name, ''),
                    ('  Passwordless                ::  %s' % self.passwordless, ''),
                    ('',''),
                    ]

                # Display the data
                self.display_array(data=data)

                # Display the menu
                Color.pl('''{D}    ╭────────────────────────────────────────────╮
                             \r    │                                            │
                             \r    │   {W}Select from the menu:{D}                    │
                             \r    │   {SB2}====================={W}{D}                    │
                             \r    │                                            │
                             \r    │   {W}[{SB2}{bold}01{W}] Set Username                        {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] Set Passwordless                    {D}│
                             \r    │                                            │
                             \r    │   {SB2}======================================{W}{D}   │
                             \r    │                                            │
                             \r    │{W}   After applying these settings, go back   {D}│
                             \r    │{W}   to the first page and select {W}[{SB2}{bold}03{W}] to     {D}│
                             \r    │{W}   run the OpenVPN's installation.          {D}│
                             \r    │                                            │
                             \r    ╰────────────────────────────────────────────╯{W}''')

            self.show_client_config_settings_menu = False

            # Get user input
            text_input = input(self.prompt(menu='config_client_settings')).strip()

            # Create cmd-line args list
            user_input = text_input.split(' ')
            cmd_list = [w.replace(self.SPACE , ' ') for w in user_input if w]
            cmd_list_len = len(cmd_list)
            cmd = cmd_list[0].lower() if cmd_list else ''

            if not cmd:
                self.show_client_config_settings_menu = True
                continue

            if cmd == '1' or cmd == '01':
                Color.pl('  {*} Type {G}88{W} or {G}back{W} to leave this input.')
                Color.pl('  {*} The name must consist of alphanumeric character. It may also include an underscore or a dash.')
                while True:
                    text_input = input(self.prompt(menu='config_client_username')).strip()

                    if not text_input:
                        continue

                    if text_input == '88' or text_input == 'back':
                        self.show_client_config_settings_menu = True
                        self.config_clients_settings()

                    if self.is_valid_username(username=text_input):
                        self.first_client_name = text_input
                        self.show_client_config_settings_menu = True
                        self.config_clients_settings()
                    else:
                        Color.pl('  {!} Invalid username. Please try again.')
                        continue
            
            elif cmd == '2' or cmd == '02':
                # Set passwordless for the first client or not
                Color.pl('''{D}    ╭──────────────────────────────────────────────────────╮
                             \r    │                                                      │
                             \r    │   {W}Select from the menu:{D}                              │
                             \r    │   {SB2}====================={W}{D}                              │
                             \r    │                                                      │
                             \r    │   {W}[{SB2}{bold}01{W}] Add a passwordless client                     {D}│
                             \r    │   {W}[{SB2}{bold}02{W}] Use a password for the client (recommended)   {D}│
                             \r    │   {W}[{SB2}{bold}88{W}] Return to the previous menu                   {D}│
                             \r    │                                                      │
                             \r    ╰──────────────────────────────────────────────────────╯{W}''')

                while True:
                    text_input = input(self.prompt(menu='config_client_passwordless')).strip()

                    if not text_input:
                        continue

                    if text_input == '1' or text_input == '01':
                        self.passwordless = 'Yes'
                        self.show_client_config_settings_menu = True
                        self.config_clients_settings()

                    elif text_input == '2' or text_input == '02':
                        self.passwordless = 'No'
                        self.show_client_config_settings_menu = True
                        self.config_clients_settings()

                    elif text_input == '88' or text_input == 'back':
                        self.show_client_config_settings_menu = True
                        self.config_clients_settings()

                    else:
                        Color.pl('  {!} Invalid option. Please try again.')
                        continue

            elif cmd == '88' or cmd == 'back':
                self.show_main_menu = True
                self.__init__(pwd=self.pwd)

            elif cmd in self.global_commands:
                self.execute_global_command(cmd=text_input)

            else:
                Color.pl('  {!} Invalid option. Please try again.')
                continue
            
    def openvpn_instllation(self):
        '''
        OpenVPN installaiton process.
        '''
        while True:
            if self.show_openvpn_installation_menu == True:
                clear()
                if self.server_ip == None:
                    self.server_ip = '-'

                if self.server_port == None:
                    self.server_port = '-'

                if self.server_protocol == None:
                    self.server_protocol = '-'

                if self.server_dns == None:
                    self.server_dns = '-'

                if self.data_channel_cipher == None:
                    self.data_channel_cipher = '-'

                if self.type_of_certificate == None:
                    self.type_of_certificate = '-'

                if self.ecdsa_key_curve == None:
                    self.ecdsa_key_curve = '-'
                
                # If the user has chosen the ECDSA certificate, the RSA key 
                # size should not be applied. Because it is another certificate.
                if self.type_of_certificate == 'ECDSA':

                    if self.ecdsa_key_curve == None or self.ecdsa_key_curve == 'Not applicable':
                        self.ecdsa_key_curve = '-'

                    self.rsa_key_size = 'Not applicable'

                # If the user has chosen the RSA certificate, the ECDSA key 
                # curve should not be applied. Because it is another certificate.
                if self.type_of_certificate == 'RSA':

                    if self.rsa_key_size == None or self.rsa_key_size == 'Not applicable':
                        self.rsa_key_size = '-'

                    self.ecdsa_key_curve = 'Not applicable'

                if self.rsa_key_size == None:
                    self.rsa_key_size = '-'

                if self.control_chanel_cipher == None:
                    self.control_chanel_cipher = '-'

                if self.type_of_diffie_hellman == None:
                    self.type_of_diffie_hellman = '-'

                # If the user has chosen the ECDH Diffie-Hellman's key, the DH key size
                # should not be applied. Because it is another type of Diffie-Hellman's key
                if self.type_of_diffie_hellman == 'ECDH':

                    if self.ecdh_key_curve == None or self.ecdh_key_curve == 'Not applicable':
                        self.ecdh_key_curve = '-'

                    self.dh_key_size = 'Not applicable'

                # If the user has chosen the DH Diffie-Hellman's key, the ECDH key curve
                # should not be applied. Because it is another type of Diffie-Hellman's key
                if self.type_of_diffie_hellman == 'DH':
                        
                        if self.dh_key_size == None or self.dh_key_size == 'Not applicable':
                            self.dh_key_size = '-'

                        self.ecdh_key_curve = 'Not applicable'

                if self.ecdh_key_curve == None:
                    self.ecdh_key_curve = '-'

                if self.dh_key_size == None:
                    self.dh_key_size = '-'

                if self.hmac_digest == None:
                    self.hmac_digest = '-'

                if self.control_channel_sec == None:
                    self.control_channel_sec = '-'


                # Data channel settings
                data = [
                    ('',''), 
                    ('  Current OpenVPN configuration settings:  ', ''),
                    ('  =======================================', '#1898CC'),
                    ('',''), 
                    ('  IP                          ::  %s' % self.server_ip, ''),
                    ('  Port                        ::  %s' % self.server_port, ''),
                    ('  Protocol                    ::  %s' % self.server_protocol, ''),
                    ('  DNS server                  ::  %s' % self.server_dns, ''),
                    ('  Data channel cipher         ::  %s' % self.data_channel_cipher, ''),
                    ('  Type of certificate         ::  %s' % self.type_of_certificate, ''),
                    ('    - ECDSA\'s key curve       ::  %s' % self.ecdsa_key_curve, ''),
                    ('    - RSA\'s key size          ::  %s' % self.rsa_key_size, ''),
                    ('  Control chanel\'s cipher     ::  %s' % self.control_chanel_cipher, ''),
                    ('  Type of Diffie-Hellman      ::  %s' % self.type_of_diffie_hellman, ''),
                    ('    - ECDH\'s key curve        ::  %s' % self.ecdh_key_curve, ''),
                    ('    - DH\'s key size           ::  %s' % self.dh_key_size, ''),
                    ('  HMAC\'s digest               ::  %s' % self.hmac_digest, ''),
                    ('  Control chanel\'s security   ::  %s' % self.control_channel_sec, ''),
                    ('',''),
                    ]


                # Display the OpenVPN server settings
                self.display_array(data=data)


                if self.first_client_name == None:
                    self.first_client_name = '-'

                if self.passwordless == None:
                    self.passwordless = '-'

                # Data channel settings
                data = [
                    ('',''), 
                    ('  Current client\'s configuration settings:  ', ''),
                    ('  ========================================', '#1898CC'),
                    ('',''), 
                    ('  Username                    ::  %s' % self.first_client_name, ''),
                    ('  Passwordless                ::  %s' % self.passwordless, ''),
                    ('',''),
                    ]

                # Display the OpenVPN first client's settings
                self.display_array(data=data)

                Color.pl('\n  {$} Are these settings correct?')
                Color.pl('  {$} Please check them carefully before the installation.')
                Color.pl('  {*} If you want to change any of them, enter {G}88{W} or {G}back{W} to go back to the main menu.')
                Color.pl('  {*} If you want to continue with the installation, enter {G}y{W}.\n')

            self.show_openvpn_installation_menu = False

            # Get user input
            text_input = input(self.prompt(menu='openvpn_installation_confirmation')).strip()

            # Create cmd-line args list
            user_input = text_input.split(' ')
            cmd_list = [w.replace(self.SPACE , ' ') for w in user_input if w]
            cmd_list_len = len(cmd_list)
            cmd = cmd_list[0].lower() if cmd_list else ''

            if not cmd:
                self.show_openvpn_installation_menu = True
                continue

            elif cmd.lower() == 'n' or cmd == '88' or cmd == 'back':
                self.show_main_menu = True
                self.__init__(pwd=self.pwd)

            elif cmd in self.global_commands:
                self.execute_global_command(cmd=cmd)

            elif cmd.lower() == 'y' or cmd.lower() == 'yes':
                if self.server_ip  and self.server_port and \
                    self.server_protocol and self.server_dns and \
                    self.data_channel_cipher and self.type_of_certificate and \
                    self.ecdsa_key_curve and self.rsa_key_size and self.control_chanel_cipher and \
                    self.type_of_diffie_hellman and self.ecdh_key_curve and \
                    self.dh_key_size and self.hmac_digest and self.control_channel_sec \
                    and self.first_client_name and self.passwordless \
                    \
                    == '-':

                    Color.pl('\n  {!} You must enter all the required settings.\n')

                    # text_input = input(Color.s('  {?} Do you want to use the default settings? [y/N]: ')).strip()
                    



                # An old version of easy-rsa was available by default in some openvpn packages
                # if os.path.isdir('/etc/openvpn/easy-rsa/'):
                #     shutil.rmtree('/etc/openvpn/easy-rsa/')

    def new_client(self, client):
        # Generates the custom client.ovpn
        with open('/etc/openvpn/server/client-common.txt') as f:
            client_common = f.read()
        with open('/etc/openvpn/server/easy-rsa/pki/ca.crt') as f:
            ca_crt = f.read()
        with open(f'/etc/openvpn/server/easy-rsa/pki/issued/{client}.crt') as f:
            issued_crt = f.read()
        with open(f'/etc/openvpn/server/easy-rsa/pki/private/{client}.key') as f:
            private_key = f.read()
        with open('/etc/openvpn/server/tc.key') as f:
            tc_key = f.read()
        with open(os.path.expanduser(f'~/{client}.ovpn'), 'w') as f:
            f.write(f"{client_common}\n<ca>\n{ca_crt}\n</ca>\n<cert>\n{issued_crt}\n</cert>\n<key>\n{private_key}\n</key>\n<tls-crypt>\n{tc_key}\n</tls-crypt>\n")

    def __init__(self, pwd):

        # Set the current working directory
        self.pwd = pwd

        try:
            while True:
                if self.show_main_menu == True:
                    clear()
                    GitPy.Banner()
                    Color.pl('''{D}╭──────────────────────────────────────────────────────────────►
│
│{W}  Automatate OpenVPN Server (GitPy) - A tool to automatate an OpenVPN server configuration{D}
│{W}                                       and installation with users.{D}
╰┬──╮
 │  │
 │  ├──────╼ {W}Created by             ::  {italic}Thomas Pellissier{W} ({R}{bold}MyMeepSQL{W}){D}
 │  ├──────╼ {W}Version                ::  {G}%s{W}{D}
 │  │
 │  ├──────╼ {W}Follow me on Twitter   ::  {SB4}MyMeepSQL{W}{D}
 │  │
 │  │{W}                         {SG2}Welcome to the GitPy{W}{D}
 │  │
 │  │{W}           {italic}Developed for Debiant and Arch based Linux distros{W}{D}
 │  │
 │  │{W}       This tools will help you to automatate the installation and{D}
 │  │{W}                   configuration of a OpenVPN server.{D}
 │  │
 │  │{W}     {O}This tool is under development, so if you find any bug or have{W}{D}
 │  │{W}       {O}any suggestion please report it on the GitHub repo below.{W}{D}
 │  │
 │  │{W}   All news version will be added the official repository of GitPy.{D}
 │  │{W}               (%s){D}
 ╰──╯

    ╭───────────────────────────────────────╮
    │                                       │
    │   {W}Select from the menu:{D}               │
    │   {SB2}====================={W}{D}               │
    │                                       │
    │   {W}[{SB2}{bold}01{W}] Config server settings         {D}│
    │   {W}[{SB2}{bold}02{W}] Config clients settings        {D}│
    │   {W}[{SB2}{bold}03{W}] Run the installation process   {D}│
    │                                       │
    ╰───────────────────────────────────────╯{W}''' % (self.VERSION, self.REPO_URL))


                self.show_main_menu = False

                # Get user input
                text_input = input(self.prompt(menu='main')).strip()

                # Create cmd-line args list
                user_input = text_input.split(' ')
                cmd_list = [w.replace(self.SPACE , ' ') for w in user_input if w]
                cmd_list_len = len(cmd_list)
                cmd = cmd_list[0].lower() if cmd_list else ''

                if not cmd:
                    self.show_main_menu = True
                    continue

                elif cmd == '1' or cmd == '01':
                    self.show_server_config_settings_menu = True
                    self.config_server_settings()

                elif cmd == '2' or cmd == '02':
                    self.show_client_config_settings_menu = True
                    self.config_clients_settings()

                elif cmd == '3' or cmd == '03':
                    self.show_openvpn_installation_menu = True
                    self.openvpn_instllation()

                elif cmd in self.global_commands:
                    self.execute_global_command(cmd=text_input)

                else:
                    Color.pl('  {!} Invalid option. Please try again.')
                    continue

        except KeyboardInterrupt:
            Color.pl('  {!} Interrupted, shutting down...')
            remove_python_cache(pwd=pwd, line_enter=True)
            if Configuration.verbose == 3:
                Color.pl('  {§} Exiting with the exit code: {R}1{W}')
                Color.pl('   {SY1}╰──╼{W} Python: {SY1}sys.exit(1){W}')
            sys.exit(1)
