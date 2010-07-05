#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       __init__.py
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
***Main initialization file***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
instructor: Peymer Anatoly
"""

from Tkinter import *
import os.path

import Widgets
import Helpers

def init(root):
	return Calculator(root)

class Calculator(Frame):
	def __init__(self, root):
		Frame.__init__(self, root)
		
		try:
			#maybe root is a Toplevel. if yes, try to set its title.
			root.title('Calculator')
		except:
			pass

		#calling init functions:
		self.config_init()
		self.build_widgets()
		self.draw_widgets()
		self.set_bindings()
		self.grid()
		
	def config_init(self):
		#building helper functions:
		self.cnfg = Helpers.Config(self, base=10)
		self.parser = Helpers.Parser(self.cnfg)
		self.history = Helpers.History()
		
		#saving classes as instance variables for later use:
		self.About = Widgets.About 
		self.ShowHistory = Widgets.ShowHistory
		self.Help = Widgets.Help
		
		#help_widget will contain Help(). never destroyed, just withdrawn & deiconified (to save xml load time).
		self.help_widget = None

		#setting global directories:
		self.global_dir_src = os.path.join(os.path.dirname(__file__))
		self.global_dir_xml = os.path.join(self.global_dir_src, 'XML')
		#and files:
		self.global_file_help_xml = os.path.join(self.global_dir_xml, 'help.xml')
		
	def set_bindings(self):
		ih = self.in_hndl
		self.bind_all("<Key>", ih.key_pressed)
		self.bind_all("<F1>", lambda x: ih.helper.help_screen("Main"))
		#CalcButton bindings are set in KeyPad class
		#menu bindings are set in MainMenu.
		
	def unset_bindings(self):
		self.unbind_all("<Key>")
		
	def build_widgets(self):
		self.prev_lbl = Widgets.PrevLabel(self)
		self.entry = Widgets.MainEntry(self, self.history, self.prev_lbl)
		self.fixes = Widgets.FixesWidget(self)
		self.in_hndl = Helpers.InputHandler(self, self.entry, self.cnfg, self.parser)
		self.menu = Widgets.MainMenu(self, self.in_hndl)
		self.num_pad = Widgets.KeyPad(self, btn_dict=self.cnfg.numpad_keys, width=3)
		self.action_pad = Widgets.KeyPad(self, btn_dict=self.cnfg.action_keys, width=3)
		
	def draw_widgets(self):
		self.menu.grid(row=0, sticky=W, columnspan=2)
		self.prev_lbl.grid(row=1, columnspan=2, sticky=W)
		self.entry.grid(row=2, columnspan=2, sticky=W+E)
		self.fixes.grid(row=3, columnspan=2, sticky=W+E)
		self.fixes.toggle_visible()
		self.num_pad.grid(row=4, column=0, padx=10)
		self.action_pad.grid(row=4, column=1, padx=10, sticky=N)
