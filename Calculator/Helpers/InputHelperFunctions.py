#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       InputHelperFunctions.py
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
***Function called by InputHandler***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
Instructors: Anatoly Peymer, Zehava Lavi
"""

import tkSimpleDialog
import tkFileDialog

class InputHelperFunctions():
	def __init__(self, root, entry, cnfg, parser):
		self.root = root
		self.entry = entry
		self.cnfg = cnfg
		self.parser = parser
		
	def toggle_prev_lbl(self):
		self.cnfg.toggle_prev_lbl()
		self.entry.prev_lbl.toggle_visible(self.cnfg.prev_lbl)

	def load_history(self):
		#load from file
		self.root.unset_bindings()
		file_ = tkFileDialog.askopenfile(title='Open history file', parent=self.root, initialfile='calc.history')
		if file_:
			try:
				self.entry.load_history(file_)
				self.revoke_redo()
			except:
				self.entry.error()
		self.root.set_bindings()

	def save_history(self):
		#save to file
		self.root.unset_bindings()
		filename = tkFileDialog.asksaveasfilename(title='Save history file', parent=self.root, initialfile='calc.history')
		#TODO - rewrite check needed
		if filename:
			try:
				file_ = open(filename, 'w')
				self.entry.save_history(file_)
			except:
				self.entry.error()
		self.root.set_bindings()

	def switch_to_manual(self):
		#let the user select the base (2-36)
		self.root.unset_bindings()
		base = tkSimpleDialog.askinteger('Base', 'Choose a base between 2-36:', initialvalue=10, minvalue=2, maxvalue=36)
		if base:
			self.convert_and_refresh(base)
		self.root.set_bindings()

	def revoke_undo(self):
		self.entry.undo(self.parser, self.cnfg.base)

	def revoke_redo(self):
		self.entry.redo(self.parser, self.cnfg.base)

	def convert_and_refresh(self, to):
		#converting the entry text to the given base, and saving the value to history
		try:
			to_display = self.parser.convert(self.entry.get(), self.cnfg.base, to)
			to_save = self.parser.convert(self.entry.get(), self.cnfg.base, 10)
			self.entry.new_value(to_display, [to_save], self.parser, to)
		except:
			self.entry.error()

		self.cnfg.refresh_numpad(to)

	def parse_and_replace(self, text=None):
		#parsing the value and saving to history
		try:
			to_display = self.parser.parse(text)
			to_save_old = self.parser.convert(text, self.cnfg.base, 10)
			to_save = self.parser.convert(to_display, self.cnfg.base, 10)
			self.entry.new_value(to_display, [to_save_old, to_save], self.parser, self.cnfg.base)
		except:
			self.entry.error()

	def help_screen(self, src, root=None):
		#opening the help screen. sigleton-like behavior.
		if src == 'Main':
			if self.root.help_widget:
				self.root.help_widget.deiconify()
			else:
				self.root.help_widget = self.root.Help(self.root)

	def refresh_entries(self):
		self.entry.update_len()
		self.root.fixes.update(self.entry.get())
