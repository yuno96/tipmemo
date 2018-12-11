#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import errno
import logging
from tkinter import *
from panel_menu import *
from panel_search import *
from panel_head import *
from panel_body import *
from panel_status import *

class Tipmemo:
	def __init__(self, root):
		self.root = root
		self.logging = logging
		self.DBPATH = './data'
		self.DBNAME = 'cache'
		self.HEADLIST_MAX = 64
		self.root.title('Tipmemo')
		
		self.logging.basicConfig(level=logging.DEBUG, 
			format='%(levelname)s:%(filename)s:%(funcName)s:%(lineno)d:%(message)s')

		self.check_dbpath(self.DBPATH)

		self.pmenu = PanelMenu(self, root)
		self.pmenu.pack(fill=X)

		self.psearch = PanelSearch(self, root)
		self.psearch.pack(side=TOP, fill=X)

		centerframe = Frame(root)
		self.phead = PanelHead(self, centerframe)
		self.phead.pack(side=LEFT, fill=Y)
		self.pbody = PanelBody(self, centerframe)
		self.pbody.pack(side=LEFT, fill=BOTH, expand=True)
		centerframe.pack(fill=BOTH, expand=True)

		self.pstatus = PanelStatus(self, root)
		self.pstatus.pack(fill=BOTH)

		entry = self.phead.redraw_head()
		if entry:
			self.pbody.redraw_body(entry)
		
		self.logging.debug('init')

	def get_db_path(self):
		return os.path.join(self.DBPATH, self.DBNAME)

	def check_dbpath(self, directory):
		if not os.path.exists(directory):
			try:
				os.makedirs(directory) 
			except OSError as error:
				if error.errno != errno.EEXIST:
					raise

	def sig_redraw_body(self, entry):
		self.pbody.redraw_body(entry)

	def sig_db_append(self, fname, title):
		self.logging.debug('-->%s %s' % (fname, title))
		self.phead.db_append(fname, title)

	def btn_search(self):
		self.logging.debug('searh')

	def run(self):
		self.logging.debug('run')

if __name__ == '__main__':

	root = Tk()
	root.tk.call('encoding', 'system', 'utf-8')
	root.option_add( "*font", "lucida 9" )
	tipmemo = Tipmemo(root)
	root.mainloop()
