#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *
from tkinter.messagebox import showinfo, showerror, askyesno

class PanelBody(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		Frame.__init__(self, root)
		self.mainobj = mainobj

		tmpframe = Frame(root)
		tmplabel = Label(tmpframe, text='Title:')
		tmplabel.pack(side=LEFT, fill=X)
		self.title = Entry(tmpframe)
		self.title.pack(side=LEFT, fill=BOTH, expand=True)
		tmpframe.pack(side=TOP, fill=BOTH)

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
		title = self.title.get().strip()
		if not title:
			showinfo('info', 'Please fill the title')
			return

		fname = os.path.join(self.mainobj.dbpath, title+'.md')
		with open(fname, 'w') as f:
			f.write(self.contents.get(1.0, END))

		self.mainobj.sig_phead_append(fname)



