#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       History.py
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
***Class to handle history records***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
instructor: Peymer Anatoly
"""

class History():
	def __init__(self):
		#all numbers will be saved allways at base 10
		self.history = ['0']
		self.index = 0

	def load_file(self, file_):
		if isinstance(file_, file):
			try:
				#integrity check:
				tmp = eval(file_.read())
				if not isinstance(tmp, list):
					raise Exception ("File read failed.")
				else:
					for i in tmp:
						if not isinstance(i, str):
							raise Exception ("File read failed.")
				#all good. replacing history
				self.history = tmp
				self.index = len(self.history)-2 #caller will revoke **redo** afterwards, so he will get the last member of history
			except:
				raise Exception ("File read failed.")
			file_.close()
		else:
			raise Exception ("Not a file chosen")
	
	def save_file(self, file_):
		if isinstance(file_, file):
			try:
				file_.write(str(self.history))
			except:
				raise Exception ("File write failed.")
			file_.close()
		else:
			raise Exception ("Not a file chosen")

	def append(self, text):
		#adding entry to history
		history = self.history

		if history[self.index] != text:
			self.index += 1
			history.insert(self.index, text)
			self.history = history[:self.index+1]

		#print 'append:', self.index, self.history

	def get_next(self):
		#returning next history entry
		history = self.history
		
		if self.index < len(history)-1:
			self.index += 1
			#print 'get_next:', self.index, self.history
			return history[self.index]
		else:
			raise Exception

	def get_prev(self, move_index = True):
		#returning last history entry
		history = self.history

		if self.index > 0:
			#print 'get_prev:', self.index, self.history
			if move_index:
				self.index -= 1
				return history[self.index]
			else:
				return history[self.index-1]
		else:
			if move_index:
				raise Exception
			else:
				return None

				
