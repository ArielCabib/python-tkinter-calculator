#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       InputHandler.py
#       
#       Copyright 2010 Ariel Haviv <ariel.haviv@gmail.com>
#       
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
***This class handles all kinds of input (key/mouse/menu),
and calls helper functions to do actions***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
instructor: Peymer Anatoly
"""

from InputHelperFunctions import InputHelperFunctions
from Tkinter import *

class InputHandler():
	def __init__(self, root, entry, cnfg, parser):
		self.helper = InputHelperFunctions(root, entry, cnfg, parser)
		self.root = root
		self.entry = entry
		self.cnfg = cnfg
		self.parser = parser

		self.shortcuts = {
			chr(26): {'func': self.helper.revoke_undo, 'args': None},  #Ctrl+Z - Undo
			chr(25): {'func': self.helper.revoke_redo, 'args': None},  #Ctrl+Y - Redo
			chr(2): {'func': self.helper.convert_and_refresh, 'args': 2},  #Ctrl+B - Binary
			chr(4): {'func': self.helper.convert_and_refresh, 'args': 10},  #Ctrl+D - Decimal
			chr(15): {'func': self.helper.convert_and_refresh, 'args': 8},  #Ctrl+O - Octal
			chr(24): {'func': self.helper.convert_and_refresh, 'args': 16},  #Ctrl+X - Manual
			chr(1): {'func': self.helper.switch_to_manual, 'args': None},  #Ctrl+A - Manual
			chr(12): {'func': self.helper.load_history, 'args': None}, #Ctrl+L - Load history
			chr(19): {'func': self.helper.save_history, 'args': None}, #Ctrl+S - Save history
			chr(16): {'func': self.helper.toggle_prev_lbl, 'args': None}, #Ctrl+P - Toggle previous label
			}
		
	def key_pressed(self, event):
		self.handle_input(event.char, 'key')
		
	def btn_clicked(self, event):
		key = event.widget['text']
		if key == 'X': key = '*'
		self.handle_input(key, 'btn')

	def mnu_clicked(self, cmd):
		#menu entry clicked
		if cmd[0] == 'File':
			if cmd[1] == 'Load_History':
				self.helper.load_history()
			elif cmd[1] == 'Save_History':
				self.helper.save_history()
			elif cmd[1] == 'Quit':
				self.root.destroy()
		elif cmd[0] == 'Edit':
			if cmd[1] == 'Undo':
				self.helper.revoke_undo()
			elif cmd[1] == 'Redo':
				self.helper.revoke_redo()
		elif cmd[0] == 'View':
			if cmd[1] == 'Toggle_Prev_Lbl':
				self.helper.toggle_prev_lbl()
			elif cmd[1] == 'Show_History':
				self.root.ShowHistory(self.root, self.helper)
		elif cmd[0] == 'NumPad':
			if cmd[1] == 'Binary':
				self.helper.convert_and_refresh(2)
			elif cmd[1] == 'Octal':
				self.helper.convert_and_refresh(8)
			elif cmd[1] == 'Decimal':
				self.helper.convert_and_refresh(10)
			elif cmd[1] == 'Hexa':
				self.helper.convert_and_refresh(16)
			elif cmd[1] == 'Manual':
				self.helper.switch_to_manual()
		elif cmd[0] == 'Help':
			if cmd[1] == 'Contents':
				self.helper.help_screen("Main")
			if cmd[1] == 'About':
				self.root.About(self.root)
		#print cmd
		
	def handle_input(self, key, src):
		if self.check_legal_chars(key, src):
			return
		else:
			self.check_functions(key)
		
	def check_legal_chars(self, key, src):
		key_orig = str(key)  #will contain original key for in-entry focus check
		key = key_orig.upper()  #contain uppercase to other checks
		#checking legal chars to insert to entry
		legal = self.cnfg.legal_input
		if key in legal and (src is 'btn' or self.root.focus_get() is not self.entry):
			#key is legal and comes from btn or keyboard out of entry focus
			self.entry.insert(END, key)
			if self.entry.get()[0] is '0': self.entry.delete(0)
			return True
		else:
			#user is typing directly to entry. need to check input.
			if key_orig and key_orig not in legal:
				try:
					self.entry.delete(self.entry.get().index(key_orig))
				except:
					#irrelevant key
					pass
			elif key_orig and self.entry.get()[0] is '0':
				#key is legal, and must replace the zero currently in the entry
				self.entry.delete(0)
				return True
		return False
	
	def check_functions(self, key):
		'''#un-comment to debug
		if len(key) == 1:
			print ord(key)
		else:
			print key'''
		#checking functions
		if key in ['=', chr(10), chr(13)]:  #Enter key is good too
			self.helper.parse_and_replace(self.entry.get())
		
		elif key in ['Clr', chr(27)]:  #Esc is good too
			self.entry.replace_with('0')
		
		elif key == 'Bksp':
			self.entry.delete_last()
		
		elif key == chr(8):
			if self.root.focus_get() is not self.entry:
				self.entry.delete_last()
			else:
				self.entry.check_empty()
		
		elif key in ['+/-', '`']:  # ` is good also
			self.helper.parse_and_replace('-(' + self.entry.get() + ')')

		elif key in self.shortcuts.keys():  #checking shortcut (Ctrl+?)
			if self.shortcuts[key]['args']:
				self.shortcuts[key]['func'](self.shortcuts[key]['args'])
			else:
				self.shortcuts[key]['func']()
