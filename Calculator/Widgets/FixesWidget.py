#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       FixesWidget.py
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
***The widget that contains prefix & postfix Text widgets***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
instructor: Peymer Anatoly
"""

from Tkinter import *

class FixesWidget(Frame):
	def __init__(self, root, visible = True):
		Frame.__init__(self, root)
		self.root = root
		self.nota = root.parser.nota
		self.visible = visible  #initiating with true, because first call to 'toggle_visible' will make if false.
		self.create_widgets()
		self.draw_widgets()
		self.bind_widgets()
		self.update('0')

	def create_widgets(self):
		self.pre = Text(self, height=1, width=10, state=DISABLED, font=('arial',10))
		self.post = Text(self, height=1, width=10, state=DISABLED, font=('arial',10))

	def draw_widgets(self):
		Label(self, text='prefix: ').grid(row=0, column=0, sticky=W)
		Label(self, text='postfix: ').grid(row=1, column=0, sticky=W)
		self.pre.grid(row=0, column=1, sticky=E)
		self.post.grid(row=1, column=1, sticky=E)

	def bind_widgets(self):
		self.pre.bind('<Enter>', lambda x: x.widget.tag_add(SEL, 1.0, END))
		self.post.bind('<Enter>', lambda x: x.widget.tag_add(SEL, 1.0, END))

	def update(self, content):
		#updating texts with new value
		nota = self.nota
		try:
		  d = nota.make_ast_from_list(nota.make_list_from_str(content))
		  pre = self.nota.nota(d, 'pre')
		  post = self.nota.nota(d, 'post')
		except:
			pre = post = 'Expression incomplete.'
		finally:
		  self.update_text(self.pre, pre)
		  self.update_text(self.post, post)

	def update_text(self, widget, text):
		ln = len(text) > 10 and len(text) or 10  #minimum length of 10
		widget.config(state=NORMAL, width=ln)
		widget.delete(0.0, END)
		widget.insert(0.0, text)
		widget.config(state=DISABLED)

	def toggle_visible(self):
		#toggle visibility on<=>off
		self.visible = not self.visible
		if self.visible:
			self.grid()
		else:
			self.grid_remove()

if __name__ == '__main__':
	pass
