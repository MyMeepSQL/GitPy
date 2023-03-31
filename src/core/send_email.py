#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ send_email.py             [Created: 2023-03-31 | 10:49 - AM]  #
#                                       [Updated: 2023-03-28 | 10:49 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Send a email via SMTP server                                             #
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
import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
## Third party imports
from src.config import Configuration

# Main

def send_email():

    # Créer un objet ConfigParser
    config_file = 'test.conf'
    config = configparser.ConfigParser()
    config.read('new_version_notification.conf')

    # Récupérer toutes les sections
    sections = config.sections()

    # Afficher les sections
    for section in sections:
        print(section)


    # Write the updated configuration back to the file
    with open(config_file, 'w') as configfile:
        config.write(configfile)

    # Value variables (of the 'convpro.conf' file)
    rootperm = config.get('general', 'rootperm')
    reset = config.get('console', 'reset')

    # Get the console section
    console_info = config['console']
    # Write the loaded module into 'convpro.conf' file
    console_info['module_selected'] = 'VALUE

    # SMTP connection settings
    smtp_server = smtp_server
    smtp_port = smtp_port
    smtp_username = smtp_username

    PASSWORD = smtp_password_env_var_name
    smtp_password = 'votre_mot_de_passe_gmail'

    # Creation of the SMTP connection object
    smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
    ## Enable TLS encryption
    smtp_conn.starttls()  
    ## Connection to the SMTP server
    smtp_conn.login(smtp_username, smtp_password)  

    # Construction of the email
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = receiver_email
    msg['Subject'] = 'New version of %s' % github_repo_name

    # Body of the email
    body = 'A new version of %s is available on %s' % (github_repo_name, github_repo_url)
    msg.attach(MIMEText(body, 'plain'))

    # Sending the email
    smtp_conn.sendmail(smtp_username, receiver_email , msg.as_string())

    # Disconnection of the SMTP server
    smtp_conn.quit()