#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       MainEntry.py
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
***This entry is where the user enters calculations***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
instructor: Peymer Anatoly
"""

from Tkinter import *
import thread
import time

class MainEntry(Entry):
	def __init__(self, root, history, prev_lbl, **args):
		Entry.__init__(self, root, **args)
		self.prev_lbl = prev_lbl
		self.history = history
		self.error_semaphore = 0
		self.replace_with('0')
		#self.insert(0, '0')

	def load_history(self, file_):
		self.history.load_file(file_)

	def save_history(self, file_):
		self.history.save_file(file_)
		
	def undo(self, parser, to):
		func = self.history.get_prev
		self.undo_redo(func, parser, to)

	def redo(self, parser, to):
		func = self.history.get_next
		self.undo_redo(func, parser, to)

	def undo_redo(self, func, parser, to):
		#rapper for both undo & redo actions
		try:
			text = func()
			try:
				text = parser.convert(text, 10, to)
			except:
				self.error()
			self.update_prev_lbl(parser, to)
			self.replace_with(text)			
		except:
			self.error()
						
	def update_prev_lbl(self, parser, to):
		#update the label with previous entry
		try:
			self.prev_lbl.update(parser.convert(self.history.get_prev(move_index=False), 10, to))
		except:
			#conversion failed because of floating point. displaying decimal value.
			self.prev_lbl.update(self.history.get_prev(move_index=False) + "(Couldn't convert float)")
			
	def delete_last(self):
		#delete last character in entry
		self.delete(len(self.get())-1)
		self.check_empty()
		
	def check_empty(self):
		#don't let the entry be blank
		if self.get() is '':
			self.replace_with('0')
			#self.insert(0, '0')

	def new_value(self, to_display, to_save, parser, to):
		#saving values to history from list 'to_save' and displaying new value
		for i in to_save:
			self.history.append(i)
		self.update_prev_lbl(parser, to)
		self.replace_with(to_display)
	
	def replace_with(self, text):
		#replacing all text in entry
		self.delete(0, END)
		self.insert(0, text)

	def error(self):
		#turn on red background to 500ms.
		#using semaphore to avoid mutual exclusion
		self.config(bg='red')
		self.error_semaphore += 1
		self.after(500, self.color_off)

	def color_off(self):
		#turning off red background.
		#using semaphore from 'error' method.
		self.error_semaphore -= 1
		if self.error_semaphore is 0:
			self.config(bg='white')
