#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ ip_domain.py              [Created: 2023-03-07 |  8:33 - AM]  #
#                                       [Updated: 2023-03-07 |  9:15 - AM]  #
#---[Info]------------------------------------------------------------------#
#  Check if the string is a valid IP/Domain or not                          #
#  Check if the string is a private IP or not                               #
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

# Imports section
import re
import ipaddress
import requests
import socket

## Third party libraries
from src.util.colors import Color

# Functions section
def validate_ips(ips):
    ip_list = ips.split(',')
    invalid_ips = []
    for ip in ip_list:
        try:
            socket.inet_aton(ip.strip())
        except socket.error:
            invalid_ips.append(ip.strip())
    if len(invalid_ips) == 0:
        return True
    else:
        return False

def validate_ips_and_domains(values):
    ip_list = []
    domain_list = []
    invalid_ips = []
    invalid_domains = []
    values_list = values.split(',')
    for value in values_list:
        value = value.strip()
        try:
            socket.inet_aton(value)
            ip_list.append(value)
        except socket.error:
            try:
                socket.gethostbyname(value)
                domain_list.append(value)
            except socket.gaierror:
                if "." in value:
                    invalid_domains.append(value)
                else:
                    invalid_ips.append(value)
    if len(invalid_ips) == 0 and len(invalid_domains) == 0:
        return True
    else:
        if len(invalid_ips) > 0:
            Color.pl('Invalid IPs: %s' .join(invalid_ips))
        if len(invalid_domains) > 0:
            Color.pl('Invalid domains: %s' .join(invalid_ips))

    return (ip_list, domain_list)

def is_private_ip(ip):
    '''
    Returns True if the given IP address is a private IP address, False otherwise.
    '''
    octets = ip.split('.')
    if len(octets) != 4:
        return False

    first_octet = int(octets[0])
    second_octet = int(octets[1])

    if first_octet == 10:
        return True
    elif first_octet == 172 and 16 <= second_octet <= 31:
        return True
    elif first_octet == 192 and second_octet == 168:
        return True
    else:
        return False

def get_public_ip() -> str:
    '''
    Get the public IP of the machine
    '''
    r = requests.get('http://ifconfig.io/ip')
    return r.text.strip()

def get_private_ip() -> str:
    ''''
    Get the private IP of the machine
    '''
    # Create a temporary socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Attempt to connect to a remote server (CloudFlare DNS) using the socket
        s.connect(('1.1.1.1', 80))
        
        # Get the IP address of the socket (i.e. the IP address of the current interface)
        private_ip = s.getsockname()[0]
    except socket.error:
        # If the connection fails, return None
        private_ip = None
    finally:
        # Close the socket
        s.close()

    return private_ip

def get_default_dns_resolver():
    '''
    Returns the default DNS resolver of the system on Linux
    '''
    # Open the resolv.conf file for reading
    with open("/etc/resolv.conf", "r") as f:
        lines = f.readlines()
        
    # Loop through the lines and find the nameserver line
    for line in lines:
        if line.startswith("nameserver"):
            dns_server = line.split()[1]
            return dns_server
        
    # If no nameserver line is found, raise an exception
    raise Exception("Could not find default DNS resolver")