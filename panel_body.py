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
		self.fname = None

		tmpframe = Frame(self)
		tmplabel = Label(tmpframe, text='Title:')
		tmplabel.pack(side=LEFT, fill=X)
		self.title = Entry(tmpframe)
		self.title.pack(side=LEFT, fill=BOTH, expand=True)
		tmpframe.pack(side=TOP, fill=BOTH)

		contframe = Frame(self)
		scrollbar = Scrollbar(contframe)
		scrollbar.pack(side=RIGHT, fill=Y)
		self.contents = Text(contframe, yscrollcommand=scrollbar.set)
		#self.contents.bind('<KeyRelease>', self.begin_edit_contents)
		self.contents.bind('<<Modified>>', self.begin_edit_contents)
		self.contents.pack(fill=BOTH, expand=True)
		scrollbar.config(command=self.contents.yview)
		contframe.pack(side=TOP, fill=BOTH, expand=True)

		self.btn_del = Button(self, text='Del',
				command=self.btn_del_command)
		self.btn_del.pack(side=RIGHT, fill=BOTH)
		self.btn_save = Button(self, text='Save', state='disabled',
				command=self.save_body)
		self.btn_save.pack(side=RIGHT, fill=BOTH)
		self.btn_new = Button(self, text='New',
				command=self.btn_new_command)
		self.btn_new.pack(side=RIGHT, fill=BOTH)

		self.logging.debug('init')

	def btn_del_command(self):
		self.logging.debug('-->btn_del_command')
		fname = self.fname
		if fname:
			self.mainobj.sig_db_delete(fname)
			os.remove(fname)
			#self.fname = None


	def btn_new_command(self):
		self.set_title_state('normal')
		self.end_edit_contents()
		self.fname = None
		self.clear_all_widget()


	def set_title_state(self, curstate):
		title_state = self.title['state']
		self.title.config(state=curstate)
		return title_state

	def begin_edit_contents(self, val=None):
		self.logging.debug('-->%s'% self.contents.edit_modified())
		if self.contents.edit_modified():
			self.logging.debug('changed')
			self.btn_save.config(state='normal')

	def end_edit_contents(self):
		self.logging.debug("changed")
		self.btn_save.config(state='disabled')
		self.contents.edit_modified(False)

	def clear_all_widget(self):
		pre_title_state = self.set_title_state('normal')
		self.title.delete('0', END)
		self.contents.delete('1.0', END)
		self.set_title_state(pre_title_state)

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

		if self.fname:
			fname = self.fname
		else:
			t = int(time.time())
			fname = self.make_new_filename(t)

		if not fname:
			self.logging.error('Cannot make filename')
			return

		with open(fname, 'w') as f:
			f.write(title+u'\n')
			f.write(self.contents.get(1.0, END))

		self.end_edit_contents()
		self.set_title_state('readonly')
		if not self.fname:
			self.mainobj.sig_db_append(fname, title)
			self.fname = fname


	def redraw_body(self, entry):
		self.clear_all_widget()

		self.fname = os.path.join(self.mainobj.DBPATH, entry[0])
		try:
			pre_title_state = self.set_title_state('normal')
			with open(self.fname, 'r') as f:
				self.title.insert(0, f.readline().strip())
				self.contents.insert(INSERT, f.read())
			self.set_title_state(pre_title_state)
		except:
			self.logging.error('Error open: '+self.fname)
			self.fname = None

		self.end_edit_contents()
		self.set_title_state('readonly')



