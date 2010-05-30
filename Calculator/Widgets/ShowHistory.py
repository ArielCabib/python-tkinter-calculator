#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ShowHistory.py
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
***The History Management Window***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
instructor: Peymer Anatoly
"""

from Tkinter import *

class ShowHistory(Toplevel):
	def __init__(self, root, helper):
		#initializing:
		Toplevel.__init__(self, root)
		self.transient(root)
		self.grab_set()
		self.title('History')

		#setting instance vars:
		self.helper = helper
		self.history = helper.entry.history
		self.nav_int = IntVar()
		self.base_var = IntVar()
		self.base_modes = [("Current base (%d)" % self.helper.cnfg.base, self.helper.cnfg.base),
			("Decimal", 10)]
		self.selected_entry = self.history.index

		#calling init methods:		
		self.build_widgets(self)
		self.bind_widgets()
		self.draw_widgets()

	def build_widgets(self, root):
		#building main frames:
		self.labels_frame = Frame(root)
		self.scroll_frame = Frame(root)
		self.base_selection_frame = Frame(root)

		#building labels:
		self.labels = [Label(self.labels_frame, text=str(i)) for i in range(10)]
		self.default_font_color = self.labels[0]['fg']
		self.default_bg_color = self.labels[0]['bg']
		if len(self.history.history) < 10: to = 0
		else: to = len(self.history.history) - 10

		#building scroll:
		self.scroll = Scale(self.scroll_frame, variable=self.nav_int, from_=0, to=to,
			command=self.scroll_func, orient=VERTICAL, showvalue=False)

		#building base selection radio buttons:
		self.radio_btn = [Radiobutton(self.base_selection_frame, text=text, variable=self.base_var,
			value=val, command=self.change_base) for text, val in self.base_modes]

		#building buttons:
		self.select_btn = Button(root, text = 'Select')
		self.exit_btn = Button(root, text = 'Close', command = root.destroy)
		
	def bind_widgets(self):
		self.select_btn.bind("<Button-1>", self.label_double_clicked)
		for i in self.labels:
			i.bind("<Button-1>", self.label_clicked)
			i.bind("<Double-Button-1>", self.label_double_clicked)

	def label_clicked(self, e):
		#user clicked a label.
		e.widget['bg'] = 'yellow'
		self.selected_entry = e.widget.index
		for i in self.labels:
			if i != e.widget and i['bg'] == 'yellow':
				i['bg'] = self.default_bg_color

	def label_double_clicked(self, e):
		#user double clicked. this happens ALWAYS after a single click,
		#so 'label_clicked' method had been already revoked.
		self.history.index = self.selected_entry - 1
		self.helper.revoke_redo()
		self.destroy()
		
	def draw_widgets(self):
		self.scroll.pack(padx=10)
		for i in self.labels:
			i.pack(padx=20, anchor=W)
		for i in self.radio_btn:
			i.pack(padx=20, anchor=W)
		self.radio_btn[0].select()
		self.scroll_frame.grid(row=0, column=0)
		self.labels_frame.grid(row=0, column=1)
		self.base_selection_frame.grid(row=0, column=2)
		self.select_btn.grid(row=1, column=0, padx=10, pady=10)
		self.exit_btn.grid(row=1, column=1, padx=10, pady=10)
		self.update_idletasks()
		w, h, (max_w, max_h) = self.winfo_width(), self.winfo_height(), self.maxsize()
		self.geometry('+%d+%d' % ((max_w-w)/2, (max_h-h)/2))

	def scroll_func(self, nav_int):
		#revoked when user scrolls the 'Scale'.
		self.update_labels(int(nav_int))

	def change_base(self):
		#user changed the display base.
		self.update_labels(self.nav_int.get())

	def update_labels(self, nav_int):
		#updating labels to new values from history.
		for i in range(len(self.labels)):
			try:
				parse_success = True
				if self.base_var.get() == 10:
					self.labels[i]['text'] = self.history.history[nav_int+i]
				else:
					try:
						self.labels[i]['text'] = self.helper.parser.convert(self.history.history[nav_int+i], 10, self.base_var.get())
					except:
						self.labels[i]['text'] = self.history.history[nav_int+i]
						self.labels[i]['fg'] = 'red'
						parse_success = False
				self.labels[i].index = nav_int+i
				#setting current history entry to blue
				if self.history.index == nav_int+i:	self.labels[i].config(fg = 'blue')
				elif parse_success:					self.labels[i].config(fg = self.default_font_color)
				#setting current selected entry to yellow
				if self.selected_entry == nav_int+i:	self.labels[i].config(bg = 'yellow')
				else:								self.labels[i].config(bg = self.default_bg_color)
			except:
				self.labels[i]['text'] = ''
