#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Parser.py
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
***A class to parse input and change bases***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
instructor: Peymer Anatoly
"""

from Tkinter import *
import radix
import notation
import re

class Parser():
	def __init__(self, cnfg):
		self.cnfg = cnfg
		self.nota = notation

	def convert(self, text, from_, to):
		#convert from base to base
		if from_ == to:
			return text
			
		if '.' in text:
			raise Exception

		cnfg = self.cnfg
		legal_sep = cnfg.legal_operators
		
		text = self.separate_ops_from_nums(text, legal_sep)
		text = self.convert_to_10(text, legal_sep, from_)
		text = self.convert_to_radix(text, legal_sep, to)

		return ''.join(text)
		
	def parse(self, text):
		#parsing the text and returning calculated value
		cnfg = self.cnfg
		legal_sep = cnfg.legal_operators
		base = cnfg.base

		text = re.sub(r'\^', '**', text)  #converting all powers from ^ to **
		#print text
		if base != 10:
			if '.' in text:
				raise Exception
			text = self.separate_ops_from_nums(text, legal_sep)
			text = self.convert_to_10(text, legal_sep, base)
			num = eval(''.join(text))
			return radix.str(num , base)
		else:
			text = self.separate_ops_from_nums(text, legal_sep)
			text = self.insert_float(text, legal_sep)
			num = eval(''.join(text))
			if int(num) == num:
				num=int(num)
			return str(num)
			
	def insert_float(self, text, legal_sep):
		#forcing floating point to ALL values (decimal base only).
		#this is in order to avoid int divisions. values who have dot won't get a '.0' obviously.
		while '.' in text:
			i = text.index('.')
			if 0 < i < len(text)-1:
				text[i-1] = ''.join(text[i-1:i+2])
				del(text[i:i+2])

		for i in range(len(text)):
			if text[i] not in legal_sep and '.' not in text[i]:
				text[i] += '.0'

		#print text
		return text
	
	def separate_ops_from_nums(self, text, legal_sep):
		#separating operator from numbers:
		tmp = []
		for i in text:
			if i in legal_sep:
				tmp.append(i)
				tmp.append('')
			else:
				try:
					if tmp[-1] in legal_sep:
						tmp.append(i)
					else:
						tmp[-1] += i
				except:
					tmp.append(i)
					
		#clearing the list of: ''
		while '' in tmp:
			tmp.remove('')

		#print tmp
		return tmp

	def convert_to_10(self, text, legal_sep, base):
		#converting to base 10
		#print 'base:', base
		for i in range(len(text)):
			if text[i] not in legal_sep:
				text[i] = str(int(text[i], base))

		#print text
		return text

	def convert_to_radix(self, text, legal_sep, base):
		#converting base 10 to radix
		#print 'to:', base
		for i in range(len(text)):
			if text[i] not in legal_sep:
				text[i] = radix.str(int(text[i]), base)

		#print text
		return text
