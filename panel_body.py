#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import time
from tkinter import *
from tkinter.messagebox import showinfo, showerror, askyesno

class PanelBody(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		Frame.__init__(self, root)
		self.mainobj = mainobj

		tmpframe = Frame(self)
		tmplabel = Label(tmpframe, text='Title:')
		tmplabel.pack(side=LEFT, fill=X)
		self.title = Entry(tmpframe)
		self.title.pack(side=LEFT, fill=BOTH, expand=True)
		tmpframe.pack(side=TOP, fill=BOTH)

		self.contents = Text(self)
		self.contents.pack(side=TOP, fill=BOTH, expand=True)

		#btmframe = Frame(self)
		self.btn_del = Button(self, text='Del')
		self.btn_del.pack(side=RIGHT, fill=BOTH)
		self.btn_save = Button(self, text='Save',command=self.save_body)
		self.btn_save.pack(side=RIGHT, fill=BOTH)
		self.btn_new = Button(self, text='New')
		self.btn_new.pack(side=RIGHT, fill=BOTH)
		#btmframe.pack(side=BOTTOM)
		'''
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
		'''

		self.logging.debug('init')

	def make_new_filename(self, t):
		for cnt in range(0, 64):
			fname = self.mainobj.DBPATH + '/%d-%d' % (t, cnt);
			if not os.path.isfile(fname):
				return fname
		return None

	def save_body(self):
		self.logging.debug('savebody')
		title = self.title.get().strip()
		if not title:
			showinfo('info', 'Please fill the title')
			return

		t = int(time.time())
		fname = make_new_filename(t)
		if not fname:
			showerror('erorr', 'Cannot create file')
			return

		with open(fname, 'w') as f:
			f.write(title+'\n')
			f.write(self.contents.get(1.0, END))

		self.mainobj.sig_db_append(fname, title)


	def redraw_body(self, entry0):
		self.logging.debug('param:' + entry0)
		self.logging.debug('here open file and insert values to widgets each ')
		self.title.insert(0, 'aaaa')
		self.contents.insert(0, 'bbbbbbbb\ncccccc\n')


