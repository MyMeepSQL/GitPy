#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---[Name & Dates]----------------------------------------------------------#
#  Filename ~ tab_completer.py          [Created: 2022-12-10 | 3:38  - PM]  #
#                                       [Update:  2022-12-12 | 10:48 - AM]  #
#---[Info]------------------------------------------------------------------#
#  The tab autocomplete class			                                    #
#  Language ~ Python3                                                       #
#---[Author]----------------------------------------------------------------#
#  Thomas Pellissier ~ @MyMeepSQL                                           #
#---[Operating System]------------------------------------------------------#
#  Developed for Linux (Arch based)                                         #
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
import re
from time import sleep
from threading import Thread
import gnureadline as global_readline


## Third party libraries
import src.core.cli_console as Console
from src.config import *


# Main
class Completer(object):
	def __init__(self):
		self.tab_counter = 0
		self.main_prompt_commands = clone_dict_keys(Console.Help_message.commands)
		self.reset_arguments = ['set', 'status', 'variables']


	def reset_counter(self):
		sleep(0.4)
		self.tab_counter = 0


	def get_possible_cmds(self, cmd_frag):
		matches = []
		for cmd in self.main_prompt_commands:
			if re.match(f"^{cmd_frag}", cmd):
				matches.append(cmd)

		return matches

	def get_match_from_list(self, cmd_frag, wordlist):
		matches = []
		for w in wordlist:
			if re.match(f"^{cmd_frag}", w):
				matches.append(w)

		if len(matches) == 1:
			return matches[0]

		elif len(matches) > 1:
			char_count = 0
			while True:
				char_count += 1
				new_search_term_len = (len(cmd_frag) + char_count)
				new_word_frag = matches[0][0:new_search_term_len]
				unique = []
				for m in matches:
					if re.match(f"^{new_word_frag}", m):
						unique.append(m)

				if len(unique) < len(matches):
					if self.tab_counter <= 1:
						return new_word_frag[0:-1]

					else:
						print_shadow('\n' + '  '.join(matches))
						Main_prompt.rst_prompt()
						return False

				elif len(unique) == 1:
					return False
				else:
					continue

		else:
			return False


	def update_prompt(self, typed, new_content, lower = False):
		global_readline.insert_text(new_content[typed:])


	def complete(self, text, state):
		self.tab_counter += 1
		line_buffer_val = global_readline.get_line_buffer().strip()
		lb_list = re.sub(' +', ' ', line_buffer_val).split(' ')
		lb_list_len = len(lb_list) if lb_list != [''] else 0


		# Return all command if the user press tab
		if (lb_list_len == 0):
			options = [x for x in self.main_prompt_commands if x.startswith(text)]
			return options[state]


		# Get prompt command from word fragment
		elif lb_list_len == 1:
			match = self.get_match_from_list(lb_list[0].lower() , self.main_prompt_commands)
			self.update_prompt(len(lb_list[0]) , match) if match else chill()


		# Autocomplete reset
		elif (lb_list[0].lower() == 'reset') and (lb_list_len > 1):
			word_frag = lb_list[-1].lower()
			match = self.get_match_from_list(lb_list[-1] , self.reset_arguments)
			if match:
				self.update_prompt(len(lb_list[-1]) , match, lower = True)

			else:
				chill()


		# Autocomplete help
		elif (lb_list[0].lower() == 'help') and (lb_list_len > 1):
			word_frag = lb_list[-1].lower()
			match = self.get_match_from_list(lb_list[-1] , self.main_prompt_commands)
			self.update_prompt(len(lb_list[-1]) , match , lower = True) if match else chill()

			if not lb_list:
				options = [x for x in self.main_prompt_commands if x.startswith(text)]
				return options[state]


		# Autocomplete paths
		elif (lb_list[0].lower() in ['exec' , 'host']) and (lb_list_len > 1) and (lb_list[-1][0] == "/"):
			root = '/'
			search_term = lb_list[-1]

			# Check if root or subdir
			path_level = search_term.split('/')

			if re.search('/', search_term) and len(path_level) > 1:
				search_term	= path_level[-1]
				for i in range(0 , len(path_level) - 1):
					root += f'/{path_level[i]}'

			dirs = next(os.walk(root))[1]
			match = [d + '/' for d in dirs if re.match(f'^{search_term}' , d)]
			files = next(os.walk(root))[2]
			match += [f for f in files if re.match(f'^{search_term}' , f)]

			# Appending match substring
			if len(match) == 1:
				typed = len(search_term)
				global_readline.insert_text(match[0][typed:])
				self.tab_counter = 0


			# Print all matches
			elif len(match) > 1 and self.tab_counter > 1:
				print_shadow('\n' + '  '.join(match))
				self.tab_counter = 0
				Main_prompt.rst_prompt()


		# Reset tab counter after 0.5s of inactivity
		Thread(name = "reset_counter" , target = self.reset_counter).start()
		return
