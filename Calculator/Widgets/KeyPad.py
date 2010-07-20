#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       KeyPad.py
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
***Frame with action buttons inside***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
Instructors: Anatoly Peymer, Zehava Lavi
"""

from Tkinter import *
from Buttons import CalcButton
from math import *

class KeyPad(Frame):
	def __init__(self, root, btn_dict, width=None, **args):
		self.root=root
		self.btn_dict = btn_dict
		Frame.__init__(self, root, **args)
		self.create_draw_buttons(width)
		
	def create_draw_buttons(self, width):
		btns = self.buttons = []
		bd = self.btn_dict
		i, j = 0, 0
		if not width: sq = int(ceil(sqrt(len(bd))))
		else: sq = width
		for a in bd:
			cbtn = CalcButton(self, text=a)
			btns.append(cbtn)
			cbtn.bind("<Button-1>", self.root.in_hndl.btn_clicked)
			cbtn.grid(row=i, column=j, sticky=W+E)
			j=(j+1)%sq
			if j==0: i+=1
		try:
			mb = self.msg_box
		except:
			#msg box needs to be initialized
			mb = self.msg_box = Label(self)
			
		mb.grid(row=i+1, columnspan=sq)
			
	def refresh_buttons(self, btn_dict, width=None):
		#destroying buttons and making new ones according to new base
		self.btn_dict = btn_dict
		for i in self.buttons:
			i.destroy()
		self.create_draw_buttons(width)
