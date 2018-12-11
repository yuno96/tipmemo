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

		self.btn_del = Button(self, text='Del')
		self.btn_del.pack(side=RIGHT, fill=BOTH)
		self.btn_save = Button(self, text='Save', command=self.save_body)
		self.btn_save.pack(side=RIGHT, fill=BOTH)
		self.btn_new = Button(self, text='New', command=self.clear_all_widget)
		self.btn_new.pack(side=RIGHT, fill=BOTH)

		self.logging.debug('init')

	def clear_all_widget(self):
		self.title.delete('0', END)
		self.contents.delete('1.0', END)

	def make_new_filename(self, t):
		for cnt in range(0, 64):
			fname = os.path.join(self.mainobj.DBPATH, 
					'%d-%d'%(t, cnt))
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
		fname = self.make_new_filename(t)
		if not fname:
			showerror('erorr', 'Cannot create file')
			return

		with open(fname, 'w') as f:
			f.write(title+u'\n')
			f.write(self.contents.get(1.0, END))

		self.mainobj.sig_db_append(fname, title)


	def redraw_body(self, entry):
		self.clear_all_widget()

		fname = os.path.join(self.mainobj.DBPATH, entry[0])
		with open(fname, 'r') as f:
			title = f.readline().strip()
			contents = f.read()
		self.title.insert(0, title)
		self.contents.insert(INSERT, contents)


