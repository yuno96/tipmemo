#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *
import time
import datetime
import dbm

class PanelHead(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		self.logging.debug('called')

		Frame.__init__(self, root)

		tmpframe = Frame(self)
		self.listb = Listbox(tmpframe)
		self.listb.pack(side=TOP, fill=BOTH, expand=True)
		self.listb.config(width=40)	# set listbox size

		self.btn_pfirst = Button(tmpframe, text='<<')
		self.btn_pfirst.pack(side=LEFT, fill=BOTH)
		self.btn_pprev = Button(tmpframe, text='<')
		self.btn_pprev.pack(side=LEFT, fill=BOTH)
		self.btn_pnext = Button(tmpframe, text='>')
		self.btn_pnext.pack(side=LEFT, fill=BOTH)
		self.btn_plast = Button(tmpframe, text='>>')
		self.btn_plast.pack(side=LEFT, fill=BOTH)
		tmpframe.pack(side=LEFT, fill=Y)

	def load_db(self, num):
		kl = {}
		db = dbm.open(self.mainobj.DBNAME, 'r')
		keylist = db.keys().sort(reverse=True)
		for x in range(0, num):
			k = keylist[x]
			kl[k] = db[k]
		db.close()
		return kl

	def redraw_head(self):
		self.listb.delete(0, END)
		headlist = load_db(self.mainobj.HEADLIST_MAX)
		if headlist:
			for idx, key in enumerate(headlist):
				t = key.split('-')[0] 
				title = headlist[key] + '(%s)' % time.ctime(t)
				self.listb.insert(idx, title)
			return headlist[0]
		else:
			return None

	def db_append(self, fname, title):
		self.logging.debug('-->' + fname)

		name = os.path.basename(fname)
		with dbm.open(self.mainobj.DBNAME, 'c') as db:
			db[name] = title

		redraw_listb()


