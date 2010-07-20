#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       MainMenu.py
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
***Main menu container (a Frame)***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
Instructors: Anatoly Peymer, Zehava Lavi
"""

from Tkinter import *

#auto-generated methods will use this list:
m = [['File',
		['Load history (Ctrl+L)', 'Load_History'],
		['Save history (Ctrl+S)', 'Save_History'],
		['Quit (Alt+F4)', 'Quit']],
	['Edit',
		['Undo (Ctrl+Z)', 'Undo'],
		['Redo (Ctrl+Y)', 'Redo']],
	['View',
		['Toggle previous action bar (Ctrl+P)', 'Toggle_Prev_Lbl'],
		['Show history', 'Show_History'],
		['Toggle Prefix & Postfix', 'Toggle_Fixes']],
	['Base',
		['Binary (Ctrl+B)', 'Binary'],
		['Octal (Ctrl+O)', 'Octal'],
		['Decimal (Ctrl+D)', 'Decimal'],
		['Hexa (Ctrl+X)', 'Hexa'],
		['Manual (Ctrl+A)', 'Manual']],
	['Help',
		['Contents (F1)', 'Contents'],
		['About...', 'About']]]

class MainMenu(Frame):
	def __init__(self, root, in_hndl, **args):
		Frame.__init__(self, root, **args)
		self.root = root
		self.in_hndl = in_hndl
		mb = self.menuBtns = []
		mn = self.menus = []

		#drawing menus
		for i in range(len(m)):
			mb.append(Menubutton(self, text=m[i][0]))
			mb[i].grid(row=0, column=i)
			mn.append(Menu(mb[i], tearoff=False))
			mb[i]['menu'] = mn[i]
			
			for j in m[i][1:]:
				#pointing to auto-generated class methods
				method = ("%s_%s" % (m[i][0], j[1]))
				eval('mn[i].add_command(label=j[0], command=self.%s)' % method)

	#auto-generating methods
	for i in range(len(m)):
		for j in m[i][1:]:
			#generating auto class methods for menu commands
			method = ("%s_%s" % (m[i][0], j[1]))
			exec("""def %s(self):
		self.in_hndl.mnu_clicked(["%s", "%s"])""" % (method, m[i][0], j[1]))
	
