#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *
import re

class PanelSearch(Frame):
	def __init__(self, mainobj, root):
		self.mainobj = mainobj
		self.logging = mainobj.logging
		Frame.__init__(self, root)

		self.entry = Entry(self)
		self.entry.pack(side=LEFT, fill=X, expand=True)
		self.btn = Button(self, text="Search", command=self.btn_search)
		self.btn.pack(side=LEFT, fill=X)

		self.entry.bind('<Return>', self.entry_enter)

	def entry_enter(self, event):
		self.btn_search()

	def btn_search(self):
		val = self.entry.get().strip()
		if not val:
			self.logging.debug('no entry value')
			return

		self.logging.debug('val='+val)
		pattern = re.compile(val, re.IGNORECASE | re.UNICODE)
		if not pattern:
			self.logging.warning('failed to create pattern')
			return

		filelist = self.get_matched_filelist(pattern, val)
		if filelist:
			self.mainobj.sig_search_result(filelist)
		else:
			self.logging.debug('nothing to match')

	def get_matched_filelist(self, pattern, val):
		filelist = []
		exceptionlist = ['cache', 'cache.dat', 'cache.bak', 'cache.dir']
		for root, dirs, files in os.walk(self.mainobj.DBPATH):
			files = [x for x in files if x not in exceptionlist]
			for filename in files:
				apath = os.path.join(root, filename)
				lockfd = self.mainobj.file_read_lock()
				with open(apath, 'r', encoding='utf-8', errors='ignore') as f:
					if pattern.search(f.read()):
					#if val in f.read():
						self.logging.debug('MATCHED-%s' % filename)

						filelist.append(filename)
				self.mainobj.file_unlock(lockfd)

		return filelist
