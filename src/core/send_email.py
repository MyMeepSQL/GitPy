#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ send_email.py             [Created: 2023-03-31 | 10:49 - AM]  #
#                                       [Updated: 2023-04-05 |  9:59 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Send a email of the new Repo's version  via SMTP server                  #
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
import requests
import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

## Third party libraries
from src.util.colors import Color

# Functions section
def check_for_new_commit(repo_owner, repo_name, current_sha):
    '''
    Check whether a GitHub repository has a new commit using the GitHub API.

    Parameters:
        repo_owner (str): The username or organization that owns the repository.
        repo_name (str): The name of the repository.
        current_sha (str): The SHA hash of the current commit to compare against.

    Returns:
        bool: True if there is a new commit, False otherwise.
    '''

    # Build the URL for the API call
    url = 'https://api.github.com/repos/%s/%s/commits' % (repo_owner, repo_name)

    # Send a GET request to the API with the appropriate headers
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(url, headers=headers)

    # Check the response status code
    if response.status_code != 200:
        raise Exception(f'Request failed with status code {response.status_code}')

    # Parse the JSON response and get the SHA hash of the latest commit
    latest_sha = response.json()[0]['sha']

    # Compare the latest SHA hash to the current one
    if latest_sha != current_sha:
        return True
    else:
        return False

def send_email():
    '''
        Send a email via SMTP server
    '''

    # Variables
    notification_config_file_path = os.environ['GITPY_NOTIFICATION_CONFIG_FILE_PATH']

    config_file = notification_config_file_path

    # Create the configparser object
    config = configparser.ConfigParser()
    config.read(config_file)

    # Get the sections
    sections = config.sections()

    # Get all sections
    for section in sections:

        # Initialise a SMTP connection
        smtp_server = config.get(section, 'smtp_server')
        smtp_port = config.get(section, 'smtp_port')
        smtp_username = config.get(section, 'smtp_username')
        smtp_password_env_var_name = os.environ[config.get(section, 'smtp_password')]
        smtp_password = os.environ[smtp_password_env_var_name]
        receiver_email = config.get(section, 'receiver_email')
        github_repo_name = config.get(section, 'github_repo_name')
        github_repo_owner = config.get(section, 'github_repo_owner')
        github_repo_url = config.get(section, 'github_repo_url')
        current_commit_sha = config.get(section, 'current_commit_sha')

        # Check if the subsripted repo (in the section name) have a new version (if the repo got a new commit) using the GitHub API
        if check_for_new_commit(github_repo_owner, github_repo_name, current_commit_sha) is True:

            # SMTP connection
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

            Color.pl('  {*} Email successfully sent to {G}%s{W}!' % receiver_email)



    # # Write the updated configuration back to the file
    # with open(config_file, 'w') as configfile:
    #     config.write(configfile)

    # # Value variables (of the 'convpro.conf' file)
    # rootperm = config.get('general', 'rootperm')
    # reset = config.get('console', 'reset')

    # # Get the console section
    # console_info = config['console']
    # # Write the loaded module into 'convpro.conf' file
    # console_info['module_selected'] = 'VALUE'

    # # SMTP connection settings
    # smtp_server = smtp_server
    # smtp_port = smtp_port
    # smtp_username = smtp_username

    # PASSWORD = smtp_password_env_var_name
    # smtp_password = 'votre_mot_de_passe_gmail'

    # # Creation of the SMTP connection object
    # smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
    # ## Enable TLS encryption
    # smtp_conn.starttls()  
    # ## Connection to the SMTP server
    # smtp_conn.login(smtp_username, smtp_password)  

    # # Construction of the email
    # msg = MIMEMultipart()
    # msg['From'] = smtp_username
    # msg['To'] = receiver_email
    # msg['Subject'] = 'New version of %s' % github_repo_name

    # # Body of the email
    # body = 'A new version of %s is available on %s' % (github_repo_name, github_repo_url)
    # msg.attach(MIMEText(body, 'plain'))

    # # Sending the email
    # smtp_conn.sendmail(smtp_username, receiver_email , msg.as_string())

    # # Disconnection of the SMTP server
    # smtp_conn.quit()