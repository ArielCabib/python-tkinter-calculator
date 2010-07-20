#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Config.py
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
***Configuration class***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
Instructors: Anatoly Peymer, Zehava Lavi
"""

from Tkinter import *
import string

class Config():
	def __init__(self, root, base, prev_lbl = True):
		'''setting default configuration'''
		
		self.root = root
		self.prev_lbl = prev_lbl
		self.action_keys = ['Bksp', 'Clr', '+/-', '+', '-', 'X', '/', '^', '%', '(', ')']
		self.dot_key = ['.']
		self.base_keys = list(string.digits + string.letters[26:])
		self.legal_operators = ['-', '+', '/', '*', '^', '%', '(', ')']
		
		self.set_base(base)
		
	def set_base(self, base):
		#setting new base
		self.base = base
		self.numpad_keys = self.base_keys[:base]
		self.legal_input = self.base_keys[:base] + self.legal_operators
		if base == 10:
			self.numpad_keys += self.dot_key
			self.legal_input += self.dot_key
		self.numpad_keys += ['=']
		self.root.set_title(base)
		
	def refresh_numpad(self, base):
		self.set_base(base)
		if base>16:
			width=None #let it be auto-calulated width
		else:
			width=3
		self.root.num_pad.refresh_buttons(self.numpad_keys, width=width)

	def toggle_prev_lbl(self):
		self.prev_lbl = not self.prev_lbl
	
