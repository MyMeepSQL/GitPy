#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ send_email.py             [Created: 2023-03-31 | 10:49 - AM]  #
#                                       [Updated: 2023-04-10 | 15:30 - PM]  #
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
    INSTALL_PATH = os.environ['GITPY_INSTALL_PATH']
    NOTIF_CONFIG_FILE_PATH = INSTALL_PATH + 'src/config/new_version_notification.conf'
    config_file = NOTIF_CONFIG_FILE_PATH

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
        # smtp_password_env_var_name = os.environ[config.get(section, 'smtp_password')]
        # print(smtp_password_env_var_name)
        smtp_password = os.environ[config.get(section, 'smtp_password')]
        # print(smtp_password) # for debugging
        receiver_email = config.get(section, 'receiver_email_address')
        github_repo_name = config.get(section, 'github_repo_name')
        github_repo_owner = config.get(section, 'github_repo_owner')
        github_repo_url = config.get(section, 'github_repo_url')
        current_commit_sha = config.get(section, 'current_commit_sha')

        # Check if the subsripted repo (in the section name) have a new version (if the repo got a new commit) using the GitHub API
        if check_for_new_commit(github_repo_owner, github_repo_name, current_commit_sha) is True:

            # Create the email message
            message = MIMEMultipart()
            message['From'] = 'GitPy Notification <%s>' % smtp_username
            message['To'] = receiver_email
            message['Subject'] = 'New version of %s' % github_repo_name


            # Body of the email
            body = 'A new version of %s is available on %s' % (github_repo_name, github_repo_url)
            message.attach(MIMEText(body, 'plain'))

            # Sending the emai via SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(smtp_username, smtp_password)
                smtp.send_message(message)

            Color.pl('  {*} A vew version of {G}%s{W} are avalable!' % github_repo_name)
            Color.pl('  {*} Email successfully sent to {G}%s{W}!' % receiver_email)
        
        else:
            Color.pl('  {!} No new version of {G}%s{W} available!' % github_repo_name)