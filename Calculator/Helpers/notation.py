#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       notation.py
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
***AST (abstract syntax tree) handling***

Calculator by Ariel Haviv (ariel.haviv@gmail.com)
Instructors: Anatoly Peymer, Zehava Lavi
"""

import re

def node(val, left=None, right=None):
  '''  make a node is the AST.
  val is either an operator (e.g. '+') or a repr(int) (e.g. '5')
  in case when val is operator, left and right must be nodes themselves.'''
  
  if re.match(r'[\w.]+$', val):
    #this is a number (of any base)
    return {'val': val}
  else:
    #this is an expression
    return {'val': val, 'left': left.copy(), 'right': right.copy()}

def visit(d):
  '''  calculate the AST's algebric result.
  d is a node.'''
  
  try:
    t = str(eval(d['val']))
    return t
  except:
    val = d['val'] == '^' and '**' or d['val']
    t = str(eval(visit(d['left']) + val + visit(d['right'])))
    return t

def nota(d, fix, prec=None):
  '''  represent an AST from a node and its decendants.
  d is the node. fix can be one of: ['in', 'pre', 'post']
  when fix is 'in', prec must be a number of precedence of the calling node.
  prec is used only used for recursive needs. always use prec=0 unless you have a good reason no to.'''

  if re.match(r'[\w.]+$', d['val']):
    #this is an expression
    return d['val']
  else:
    #this is an operand
    if fix == 'pre':
      #prefix
      t = '%s %s %s' % (d['val'], nota(d['left'], fix), nota(d['right'], fix))
      return ' '.join(t.split())
    elif fix == 'post':
      #postfix
      t = '%s %s %s' % (nota(d['left'], fix), nota(d['right'], fix), d['val'])
      return ' '.join(t.split())
    elif fix == 'in':
      #infix
      p = precedence(d['val'])
      b = prec >= p and ('(',')') or ('','') #if previous precedence is bigger, insert brackets
      left = nota(d['left'], fix, p)
      right = nota(d['right'], fix, p)
      val = d['val']
      e = eval(left + val + right)
      ev = []
      ev.append(left[1:-1] + val + right[1:-1])
      ev.append(left + val + right[1:-1])
      ev.append(left[1:-1] + val + right)
      ev.append(left + val + right)

      for i in ev:
        try:
          if eval(i) == e:
            #trying to give up some brackets
            t = i
            #removing explicit negative zero '0-4' ==> '-4' :
            t = re.sub(r'^0-', '-', t)
            t = re.sub(r'^--', '', t)  #removing double negation
            return b[0] + t + b[1]
        except:
          continue

def precedence(op):
  '''  return op's precedence number:
  ['+', '-'] => 1
  ['*', '/'] => 2
  ['^'] => 3'''

  if op == '(':
    return -1
  #elif op == ')':
    #return 0
  elif op in ['+', '-']:
    return 1
  elif op in ['*', '/', '%']:
    return 2
  elif op is '^':
    return 3

def make_list_from_str(s):
  '''  try to make AST from a string (s),
  and returns it.'''

  #inserting zeros where it's implicit (like '-4' or '(-4+7)')
  s = re.sub(r'^-', '0-', s)    #in the beginning
  s = re.sub(r'\(-', '(0-', s)  #after a '('

  #ss will contain the list of numbers and operators
  ss = []
  while s:
    if re.match('[\w.]+', s):
      ss.append(re.match('[\w.]+', s).group())
      s = re.sub('[\w.]+', '', s, 1)
    else:
      ss.append(re.match('\W', s).group())
      s = re.sub('\W', '', s, 1)

  while ss.count(' '): ss.remove(' ')
  return ss    


def make_ast_from_list(l):
  def pop_and_push_back():
    #print 'before:', n, o
    r, l = n.pop(), n.pop()
    n.append(node(o.pop(), l, r))
    #print 'after:', n, o
    
  o = [] #operator stack
  n = [] #number/node stack

  for i in l:
    if re.match('[\w.]+', i):
      #this is a number. push to node stack.
      n.append(node(i))
    else:
      #this is an operand
      if i == '(':
        o.append(i)
      elif i == ')':
        while o[-1] != '(':
          pop_and_push_back()
        o.pop() #popping the '('
      else:
        #there are operators in the stack.
        while o and precedence(i) <= precedence(o[-1]):
          #print o, i, precedence(i), precedence(o[-1])
          pop_and_push_back()
        o.append(i)

  while o:
    #there are operators left in the stack
    pop_and_push_back()

  return n[0]

if __name__ == '__main__':
  p = make_list_from_str('-((3^2-4)+2A)')
  p = make_list_from_str('3-3-4')
  print p
  d = make_ast_from_list(p)
  print d
  print visit(d)
  print nota(d, 'in', 0)
  print nota(d, 'pre')
  print nota(d, 'post')
