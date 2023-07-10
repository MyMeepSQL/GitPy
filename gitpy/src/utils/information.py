#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---[Name & Creation/Update Dates]------------------------------------------ #
#  Filename ~ information.py                 [ Created: 2023-02-28 |  9:21 ]  #
#                                            [ Updated: 2023-07-10 | 13:51 ]  #
# ---[Description & File Language]------------------------------------------- #
#  The information page about GitPy                                           #
#  Language ~ Python3                                                         #
# ---[Author & Maintainer(s)]------------------------------------------------ #
#  Author:                                                                    #
#    Thomas Pellissier (MyMeepSQL)                                            #
#  Maintainer(s):                                                             #
#    Thomas Pellissier (MyMeepSQL)                                            #
# ---[Operating System]------------------------------------------------------ #
#  Developed for Linux distros (for Debian and Arch, for the moment)          #
# --------------------------------------------------------------------------- #


"""
This module contain the information message of GitPy.
"""


class Information:
    """
    The main class of the Information page of GitPy that will be called when the user runs 'gitpy info'.
    This class will display all Information about GitPy.
    """

    @classmethod
    def print_info(
        cls,
        PROGRAM_NAME,
        VERSION,
        REPO_URL,
        REPO_CLONE_URL,
        REPO_CHANGELOG_URL,
        REPO_ISSUES_URL,
        OWNERS_DISCORD_TUPLE,
        OWNERS_EMAILS_TUPLE,
        OWNERS_GITHUB_TUPLE,
        OWNERS_TWITTER_TUPLE,
    ):
        """
        Initialize all arguments of the class.

        Arguments:
            PROGRAM_NAME (string): The name of the program.
            VERSION (string): The version of the program.

            REPO_URL (string): The URL of the GitHub repository.
            REPO_CLONE_URL (string): The clone URL of the GitHub repository.
            REPO_CHANGELOG_URL (string): The URL of the changelog of the GitHub repository.
            REPO_ISSUES_URL (string): The URL of the issues page of the GitHub repository.

            OWNERS_DISCORD_TUPLE (tuple): The tuple of the owners Discord tags.
            OWNERS_EMAILS_TUPLE (tuple): The tuple of the owners emails.
            OWNERS_GITHUB_TUPLE (tuple): The tuple of the owners GitHub usernames.
            OWNERS_TWITTER_TUPLE (tuple): The tuple of the owners Twitter usernames.

        Returns:
            message (string): The information message about GitPy.
        """

        cls.PROGRAM_NAME = PROGRAM_NAME
        cls.VERSION = VERSION

        cls.REPO_URL = REPO_URL
        cls.REPO_CLONE_URL = REPO_CLONE_URL
        cls.REPO_CHANGELOG_URL = REPO_CHANGELOG_URL
        cls.REPO_ISSUES_URL = REPO_ISSUES_URL

        cls.OWNERS_DISCORD_TUPLE = OWNERS_DISCORD_TUPLE
        cls.OWNERS_EMAILS_TUPLE = OWNERS_EMAILS_TUPLE
        cls.OWNERS_GITHUB_TUPLE = OWNERS_GITHUB_TUPLE
        cls.OWNERS_TWITTER_TUPLE = OWNERS_TWITTER_TUPLE

        return """
        \r   Information about GitPy:
        \r   {SB4}{bold}========================{W}

        \r      Description
        \r      {SB3}-----------{W}
        \r      GitPy is a program that can be use to search and download a repository on GitHub using the GitHub API REST. 

        \r      Program                        Version (on your system)
        \r      {SB3}-------{W}                        {SB3}------------------------{W}
        \r      %s                           %s

        \r      Copyright & Licensing          Description
        \r      {SB3}---------------------{W}          {SB3}----------- {W}
        \r      Copyright                      Copyright (C) 2023 Thomas Pellissier. All rights reserved.
        \r      License                        This program is under GNU General Public License v3.0 (GPL 3.0).
        \r                                     This is free software: you are free to change and redistribute it.
        \r                                     There is NO WARRANTY, to the extent permitted by law.

        \r      Other information              Description
        \r      {SB3}-----------------{W}              {SB3}-----------{W}
        \r      GitHub page URL                <%s>
        \r      Clone URL                      <%s>
        \r      Changelogs                     <%s>
        \r      Issues pages                   <%s>

        \r   Information about author:
        \r   {SB4}{bold}========================={W}

        \r      Main information               Description
        \r      {SB3}----------------{W}               {SB3}-----------{W}
        \r      MyMeepSQL's fullname           Thomas Pellissier
        \r      MyMeepSQL's email              <%s> ({bold}only for professional{W} or for {G}report bugs of GitPy{W})

        \r      Other information              Description
        \r      {SB3}-----------------{W}              {SB3}-----------{W}
        \r      MyMeepSQL's GitHub profile     <%s>
        \r      MyMeepSQL's Twitter profile    <%s>
        \r      MyMeepSQL's Discord username   %s

        \r   Information about contributors:
        \r   {SB4}{bold}==============================={W}

        \r      No contributors for the moment :(""" % (
            cls.PROGRAM_NAME,
            cls.VERSION,
            cls.REPO_URL,
            cls.REPO_CLONE_URL,
            cls.REPO_CHANGELOG_URL,
            cls.REPO_ISSUES_URL,
            cls.OWNERS_EMAILS_TUPLE[0],
            cls.OWNERS_GITHUB_TUPLE[0],
            cls.OWNERS_TWITTER_TUPLE[0],
            cls.OWNERS_DISCORD_TUPLE[0],
        )
