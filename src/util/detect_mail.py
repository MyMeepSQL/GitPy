#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ detect_mail.py            [Created: 2023-03-29 |  9:31 - AM]  #
#                                       [Updated: 2023-03-29 |  9:31 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Check if the entered value are a correct email and detect the email      #
#  domain.                                                                  #
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

## Third party imports



class Email_Utils():
    '''
        Check if the entered value are a correct email and detect the email domain.
    '''

    # Email server
    mail_server = None
    mail_server_port = None
    mail_server_ssl = None
    mail_server_tls = None

        # Google mail server:

        # mail_server = 'smtp.gmail.com'
        # mail_port = 587
        # tls_port = 587
        # ssl_port = 465


        # Outlook mail server:

        # mail_server = 'smtp-mail.outlook.com'
        # mail_port = 587
        # tls_port = 587
        # ssl_port = 465

    @classmethod
    def detect_email_domain(cls,email):
        '''Detect the email domain.

        Args:
            email (str): The email to check.

        Returns:
            str: The email domain.
        '''
        if not cls.check_email(email):
            return 'Not a valid email!'

        return email.split("@")[1]

    @classmethod
    def check_email(cls,email):
        '''Check if the entered value are a correct email and detect the email domain.

        Args:
            email (str): The email to check.

        Returns:
            bool: True if the email is correct, False otherwise.
        '''
        if not isinstance(email, str):
            return False

        if not "@" in email:
            return False

        if not "." in email:
            return False

        return True
    
    @classmethod
    def __init__(cls, email):
        '''Init the class.
        
        Args:
            email (str): The email to check.
        '''

        domain = cls.detect_email_domain(email=email)
        print(domain)

        if domain == 'gmail.com':
            cls.mail_server = 'smtp.gmail.com'
            cls.mail_server_port = 587
            cls.mail_server_ssl = 465
            cls.mail_server_tls = 587

        elif domain == 'outlook.com' or domain == 'hotmail.com':
            cls.mail_server = 'smtp-mail.outlook.com'
            cls.mail_server_port = 587
            cls.mail_server_ssl = 465
            cls.mail_server_tls = 587

        print(cls.mail_server)
        print(cls.mail_server_port)
        print(cls.mail_server_ssl)
        print(cls.mail_server_tls)



# def test():
#     domain = Email_Utils.detect_email_domain(email='test@gmail.com')

#     if domain == 'gmail.com':
#         Email_Utils.mail_server = 'smtp.gmail.com'
#         Email_Utils.mail_server_port = 587
#         Email_Utils.mail_server_ssl = 465
#         Email_Utils.mail_server_tls = 587

#     elif domain == 'outlook.com' or domain == 'hotmail.com':
#         Email_Utils.mail_server = 'smtp-mail.outlook.com'
#         Email_Utils.mail_server_port = 587
#         Email_Utils.mail_server_ssl = 465
#         Email_Utils.mail_server_tls = 587



Email_Utils.__init__(email='bonjour@gmail.com')
