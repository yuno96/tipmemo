#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *
import time
import datetime

class PanelHead(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		Frame.__init__(self, root)
		self.listb = Listbox(root)
		self.listb.pack(side=TOP, fill=BOTH, expand=True)
		self.listb.config(width=40)	# set listbox size
		self.list_backup = []

		tmpframe = Frame(root)
		self.btn_pfirst = Button(root, text='<<')
		self.btn_pfirst.pack(side=LEFT, fill=BOTH)
		self.btn_pprev = Button(root, text='<')
		self.btn_pprev.pack(side=LEFT, fill=BOTH)
		self.btn_pnext = Button(root, text='>')
		self.btn_pnext.pack(side=LEFT, fill=BOTH)
		self.btn_plast = Button(root, text='>>')
		self.btn_plast.pack(side=LEFT, fill=BOTH)
		tmpframe.pack(side=BOTTOM)

		self.logging.debug('called')

	def append_to_head(self, fname):
		self.logging.debug('-->' + fname)
		self.list_backup.insert(0, fname)

		self.listb.delete(0, END)
		for idx, name in enumerate(self.list_backup):
			t = os.path.getctime(name)
			name = os.path.basename(name)
			name = os.path.splitext(name)[0]
			name = name + '(%s)' % time.ctime(t)
			self.listb.insert(idx, name)


