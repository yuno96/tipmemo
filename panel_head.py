#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *
import time
import datetime
import dbm
from tkinter import font

class PanelHead(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		self.logging.debug('called')
		self.mainobj = mainobj

		Frame.__init__(self, root)

		tmpframe = Frame(self)

		listbframe = Frame(tmpframe)
		scrollbar = Scrollbar(listbframe)
		scrollbar.pack(side=RIGHT, fill=Y)
		self.listb = Listbox(listbframe, width=48,
				yscrollcommand=scrollbar.set)
		self.listb.bind('<Double-1>', self.double_click)
		self.listb.pack(fill=BOTH, expand=True)
		scrollbar.config(command=self.listb.yview)
		listbframe.pack(side=TOP, fill=BOTH, expand=True)

		self.btn_pfirst = Button(tmpframe, text='<<')
		self.btn_pfirst.pack(side=LEFT, fill=BOTH)
		self.btn_pprev = Button(tmpframe, text='<')
		self.btn_pprev.pack(side=LEFT, fill=BOTH)
		self.btn_pnext = Button(tmpframe, text='>')
		self.btn_pnext.pack(side=LEFT, fill=BOTH)
		self.btn_plast = Button(tmpframe, text='>>')
		self.btn_plast.pack(side=LEFT, fill=BOTH)

		tmpframe.pack(side=LEFT, fill=Y)

		# Get the listbox font
		listFont = font.Font(font=self.listb.cget("font"))

		# Define spacing between left and right strings in terms of single "space" length
		s0 = listFont.measure(' ')
		s1 = listFont.measure('a')
		s2 = listFont.measure('A')
		s3 = listFont.measure('가')
		s4 = listFont.measure('8')
		self.logging.debug('listb width=%d %d %d %d %d %d'%(self.listb['width'], s0, s1, s2, s3, s4))

	def load_db(self):
		kl = {}
		dbpath = self.mainobj.get_db_path()
		self.logging.debug(dbpath)
		try:
			db = dbm.open(self.mainobj.get_db_path(), 'r')
			for k in db.keys():
				kl[k.decode('utf-8')] = db[k].decode('utf-8')
				print ('--> %s' % db[k])
			db.close()
		except:
			return None
		self.logging.debug(kl)
		return kl

	def redraw_head(self):
		self.listb.delete(0, END)
		self.listb.focus_set()
		hdict = self.load_db()
		firstkey = None
		if hdict:
			for idx, key in enumerate(sorted(hdict, reverse=True)):
				if not firstkey:
					firstkey = key
				t = key.split('-')[0] 
				title = '%s '%time.ctime(int(t)) + hdict[key]
				self.listb.insert(idx, title)
			return (firstkey, hdict[firstkey])
		else:
			return None

	def db_append(self, fname, title):
		self.logging.debug('-->%s %s' % (fname, title))

		name = os.path.basename(fname)
		with dbm.open(self.mainobj.get_db_path(), 'c') as db:
			db[name] = title

		#self.redraw_head()

	def db_delete(self, fname):
		self.logging.debug('-->' + fname)

		name = os.path.basename(fname)
		with dbm.open(self.mainobj.get_db_path(), 'c') as db:
			del db[name]

		#self.redraw_head()

	def double_click(self, event):
		self.logging.debug('double clicked')
		print (self.listb.curselection()[0])
		print (self.listb.get(self.listb.curselection()[0]))
		val = self.listb.get(self.listb.curselection()[0])
		tmstruct = time.strptime(val[:24])
		t = time.mktime(tmstruct)
		self.mainobj.sig_redraw_body(('%d-0'%t, 'none'))
		




