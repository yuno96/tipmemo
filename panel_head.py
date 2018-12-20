#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *
import time
import datetime
import dbm
from tkinter import font
import re

class PanelHead(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		self.logging.debug('called')
		self.mainobj = mainobj

		Frame.__init__(self, root)

		tmpframe = Frame(self)

		listbframe = Frame(tmpframe)
		self.status_bar = StringVar()
		self.status = Label(tmpframe, textvariable=self.status_bar, anchor='w')
		self.status.pack(side=TOP, fill=X)
		scrollbar = Scrollbar(listbframe)
		scrollbar.pack(side=RIGHT, fill=Y)
		self.listb = Listbox(listbframe, width=60,
				yscrollcommand=scrollbar.set)
		self.listb.bind('<Double-1>', self.double_click)
		self.listb.pack(fill=BOTH, expand=True)
		scrollbar.config(command=self.listb.yview)
		listbframe.pack(side=TOP, fill=BOTH, expand=True)

		self.img_refresh = PhotoImage(file=os.path.join(self.mainobj.ICONPATH, 'refresh-16.png'))
		self.btn_refresh = Button(tmpframe, text='Refresh',
				image=self.img_refresh, compound='left',
				command=self.mainobj.sig_refresh)
		self.btn_refresh.pack(side=LEFT, fill=BOTH)

		'''
		self.btn_pprev = Button(tmpframe, text='1')
		self.btn_pprev.pack(side=LEFT, fill=BOTH)
		self.btn_pnext = Button(tmpframe, text='2')
		self.btn_pnext.pack(side=LEFT, fill=BOTH)
		self.btn_plast = Button(tmpframe, text='3')
		self.btn_plast.pack(side=LEFT, fill=BOTH)
		'''
		tmpframe.pack(side=LEFT, fill=Y)

		# Get the listbox font
		self.listFont = font.Font(font=self.listb.cget("font"))
		s4 = self.listFont.measure('0')
		# width of listb is the number of '0' fitted in listb
		# Note: '0', 'A', 'a', and '가' are all different
		self.unit_strsz = s4*self.listb['width']
		self.logging.debug('list width=%d %d'%(self.listb['width'], 
			self.unit_strsz))

	def load_db(self, filelist=None):
		kl = {}
		dbpath = self.mainobj.get_db_path()
		self.logging.debug(dbpath)

		try:
			lockfd = self.mainobj.file_read_lock()
			db = dbm.open(self.mainobj.get_db_path(), 'r')
			keylist = db.keys()
			if filelist:
				for k in filelist:
					kl[k] = db[k].decode('utf-8')
			else:
				for k in db.keys():
					kl[k.decode('utf-8')] = db[k].decode('utf-8')
			db.close()
			self.mainobj.file_unlock(lockfd)
		except Exception as e:
			self.logging.warning(e)
			return None
		return kl

	def truncate_str(self, val):
		for i in range(24, len(val)): #datestr size in front is 24
			if self.listFont.measure(val[:i]) > self.unit_strsz:
				return val[:i-3] + '...'
		else:
			return val


	def redraw_head(self, filelist=None):
		self.listb.delete(0, END)
		self.listb.focus_set()
		hdict = self.load_db(filelist)
		tmp = ' Items: %d' % len(hdict)
		if (filelist):
			tmp = tmp + ' (Searched)'
		self.status_bar.set(tmp)
		firstkey = None
		if hdict:
			for idx, key in enumerate(sorted(hdict, reverse=True)):
				if not firstkey:
					firstkey = key
				t = key.split('-')[0]
				title = '%s '%time.ctime(int(t)) + hdict[key]
				title = self.truncate_str(title)
				#self.logging.debug('-->len=%d' % self.listFont.measure(title))
				self.listb.insert(idx, title)
			return (firstkey, hdict[firstkey])
		else:
			return None

	def db_append(self, fname, title):
		self.logging.debug('-->%s %s' % (fname, title))

		name = os.path.basename(fname)
		lockfd = self.mainobj.file_write_lock()
		with dbm.open(self.mainobj.get_db_path(), 'c') as db:
			db[name] = title
		self.mainobj.file_unlock(lockfd)

		#self.redraw_head()

	def db_delete(self, fname):
		self.logging.debug('-->' + fname)

		name = os.path.basename(fname)
		lockfd = self.mainobj.file_write_lock()
		with dbm.open(self.mainobj.get_db_path(), 'c') as db:
			del db[name]
		self.mainobj.file_unlock(lockfd)

		#self.redraw_head()

	def double_click(self, event):
		self.logging.debug('double clicked')
		val = self.listb.get(self.listb.curselection()[0])
		tmstruct = time.strptime(val[:24])
		t = time.mktime(tmstruct)
		self.mainobj.sig_redraw_body(('%d-0'%t, 'none'))
		




