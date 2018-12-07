#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *

class PanelBody(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		Frame.__init__(self, root)
		self.mainobj = mainobj
		self.title = Entry(root)
		self.title.pack(side=TOP, fill=BOTH)
		self.contents = Text(root)
		self.contents.pack(side=TOP, fill=BOTH, expand=True)

		tmpframe = Frame(root)
		self.btn_del = Button(root, text='Del')
		self.btn_del.pack(side=RIGHT, fill=BOTH)
		self.btn_save = Button(root, text='Save',command=self.save_body)
		self.btn_save.pack(side=RIGHT, fill=BOTH)
		self.btn_new = Button(root, text='New')
		self.btn_new.pack(side=RIGHT, fill=BOTH)
		tmpframe.pack(side=BOTTOM)

		self.logging.debug('init')

	def hello(self):
		self.logging.debug('hello')

	def save_body(self):
		self.logging.debug('savebody')
		with open('./data/aa.md', 'w') as f:
			f.write(self.contents.get(1.0, END))

