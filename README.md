<!--

#---[Metadata]--------------------------------------------------------------#
#  Filename ~ README.md                 [Created: 2022-11-23 |  1:23 - PM]  #
#                                       [Updated: 2023-04-11 |  9:57 - AM]  #
#---[Info]------------------------------------------------------------------#
#  A long description of the GitPy for the GitHub page                      #
#  Language ~ Markdown                                                      #
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

-->

---

<pre>
                              __________________________
                              __  ____/__(_)_  /___  __ \____  __
                              _  / __ __  /_  __/_  /_/ /_  / / /
                              / /_/ / _  / / /_ _  ____/_  /_/ / 
                              \____/  /_/  \__/ /_/     _\__, /  
                                                        /____/

  GitPy - A Python3 tool for search and download a GitHub's repository directly in the terminal

</pre>

---

<!--
Liens à modifier
-->

<!--  [ Authors ] -->
<p align="center">
    <a href="https://github.com/MyMeepSQL">
        <img src="https://img.shields.io/badge/Made%20by-Thomas%20Pellissier%20(MyMeepSQL)%20&%20Jonas%20Petitpierre%20(Bashy)-important?style=for-the-badge" alt="Made by">
    <a href="https://github.com/PentestSociety">
        <img src="https://img.shields.io/badge/Owner-©%20PSociety-important?style=for-the-badge" alt="Owner">
    </a>
</p>

<!--  [ Version ] -->
<p align="center">
    <img src="https://img.shields.io/badge/Version-0.0.1-success?style=for-the-badge" alt="gitpy's version">
</p>

<!--  [ Informations about this repository ] -->
<p align="center">
    <a href="https://github.com/MyMeepSQL/gitpy/stargazers">
        <img src="https://img.shields.io/github/stars/MyMeepSQL/gitpy?style=for-the-badge&color=success" alt="Stars">
    </a>
    <a href="https://github.com/MyMeepSQL/gitpy/network/members">
        <img src="https://img.shields.io/github/forks/MyMeepSQL/gitpy?color=cyan&style=for-the-badge&color=success" alt="Forks">
    </a>
    <a href="https://github.com/MyMeepSQL/gitpy/watchers">
        <img src="https://img.shields.io/github/watchers/MyMeepSQL/gitpy?color=cyan&style=for-the-badge&color=success" alt="Watchers">
    </a>
    <a href="https://github.com/MyMeepSQL/gitpy/issues">
        <img src="https://img.shields.io/github/issues/MyMeepSQL/gitpy?color=success&style=for-the-badge" alt="Issues">
    </a>
    <a href="https://github.com/MyMeepSQL/gitpy/issues">
        <img src="https://img.shields.io/github/last-commit/MyMeepSQL/gitpy/master?color=success&style=for-the-badge" alt="GitHub last commit (branch)">
    </a>

</p>

<!--  [ More informations ] -->
<p align="center">
    <img src="https://img.shields.io/badge/Release%20status-In%20Development-informational?style=for-the-badge" alt="Release status">
    <img src="https://img.shields.io/badge/Supported%20OS-Linux-informational?style=for-the-badge" alt="Supported OS">
    <img src="https://img.shields.io/badge/Supported%20distros-Arch%20&%20Debian%20based-informational?style=for-the-badge" alt="Supported ditros">
    <img src="https://img.shields.io/github/repo-size/MyMeepSQL/gitpy?color=informational&style=for-the-badge" alt="Repo size">
    <a href="https://github.com/MyMeepSQL/gitpy/blob/test_v1/LICENSE">
        <img src="https://img.shields.io/github/license/MyMeepSQL/gitpy?color=informational&style=for-the-badge" alt="Repo License" >
    </a>
</p>

<!--  [ Contribution ] -->
<p align="center">
    <img src="https://img.shields.io/badge/Contributions-Open!-green?style=for-the-badge" alt="Contrinutions">
</p>

---

# **Summary**

- [**About GitPy**](#about-GitPy)
- [**Credit & Copyrights**](#credit--copyrights)
- [**License**](#license)
- [**Installation**](#installation)
- [**Options of GitPy**](#options-of-GitPy)
- [**Update**](#update)
- [**Info**](#information-about-GitPy)

---

# **About GitPy**

**GitPy** is a program that can be use to search and download a repository on GitHub using the GitHub API REST. The program was written in Python3 and designed to be use on Arch and Debian based ditros. GitPy have a main console that can be used to search and download a repository. It could also be used in a CLI environment, inspired by the [Metasploit](https://github.com/rapid7/metasploit-framework) network testing tool (not yet implemented).

- **In development!**
- Can only be run on a **Linux machine**
- Can only be run on a  **Arch and Debian based Linux distros**

## **Credit & Copyrights**

```
            The GitPY is a product of PSociety™ by Thomas Pellissier (MyMeepSQL) 
                               and Jonas Petitpierre (Bashy).
                  Copyright (C) 2021-2023 © PSociety™. All rights reserved.

          This tool has been created and designed from scratch by Thomas Pellissier 
                                   and Jonas Petitpierre.
```

## **Changelogs**

All new changes compared to _**GitPy**_ can be found [here](src/docs/CHANGELOG.md).

## **License**

GitPy is licensed under the GNU General Public License v3.0 license. Refer to [LICENSE](LICENSE) for more informations.

## **Installation**

Instructions to install GitPy... (Linux commands)

```bash
# Install git tool for clone this repositories with (if you didn’t have it):
sudo pacman -S git
# or (if you use Debian based distros):
# sudo apt install git

# Clone the repositorie with:
git clone https://github.com/MyMeepSQL/GitPy.git

# And go in its directory
cd GitPy

# To install GitPy on your system, run:
sudo python3 gitpy.py --install

# Once installed, you can run the 'gitpy' command anywhere in the terminal

# Run the main console of GitPy with:
gitpy --console
```

## Options of _GitPy_

All avalable options for the **GitPy** command (the help message):

```
Main options:
============

  Options                                  Description
  -------                                  -----------
       --console                           Start the main console of GitPy.

Installation options:
=====================

  Options                                  Description
  -------                                  -----------
       --install                     [+]   Install GitPy with all depencies on your system.
       --uninstall                   [+]   Uninstall GitPy from your system.
 
       --skip-update                       Skip the system update phase during the installation of GitPy.
       --offline                           Install GitPy with the local file already downloaded
                                           (default: download new files from GitHub).
  -iP [PATH], --install-path [PATH]        Chose where GitPy will be install on the system
                                           (default: /opt/gitpy/).

Output options:
===============

  Options                                  Description
  -------                                  -----------
  -q,  --quiet                             Prevent header from displaying. Warning: bypass any "Are your sure?"
                                           message!
  -v [LEVEL], --verbose [LEVEL]            Verbosity level: 1-3 (default: 0 | const: 1).

Additional options:
===================

  Options                                  Description
  -------                                  -----------
  -y,  --no-confirm                        Bypass any and all "Are you sure?" messages.

Informations options:
=====================

  Options                                  Description
  -------                                  -----------
       --info                              Show more informations about GitPy and exit.
  -h,  --help                        [+]   Show this help message and exit or show more help for a option.
  -V,  --version                           Show program's version and exit.

Miscellaneous options:
======================

  Options                                  Description
  -------                                  -----------
  -u,  --update                      [+]   Update the GitPy directly from GitHub.
  -fu, --force-update                      Update GitPy even if the version on the machine is already the latest.
       --show-config                       Prompt the content of the config file.
       --show-env-var                      Prompt the value of the GITPY_INSTALL_PATH environment variable.
       --remove-cache                [+]   Delete python cache from the GitPy directory.

Others avalable informations:
=============================

  Usage 
  ----- 
  gitpy <OPTIONS>

  Others
  ------
  Report all bugs to <thomas.pellissier.pro@proton.me> or open an issue at <https://github.com/MyMeepSQL/GitPy/issues>.
  The options with the [+] mean that it may require additional option(s).
  If you want more details about a command, run: gitpy --help <OPTION>
```

## **Update**

To download and update the current GitPy instance on your system, run:

```bash
sudo gitpy --update
```

## **Information about GitPy**

If you want all informations about GitPy and authors' and with other informations, run:

```bash
gitpy --info
```

