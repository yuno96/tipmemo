#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from panel_menu import *
from panel_search import *
from panel_head import *
from panel_body import *
#from panel_status import *
import os
import sys
import errno
import logging
from tkinter import *
import portalocker
from tempfile import gettempdir

class Tipmemo:
	def __init__(self, root):
		self.root = root
		self.logging = logging
		self.DBPATH = os.path.join(os.getcwd(), 'data')
		self.DBNAME = 'cache'
		self.ICONPATH = os.path.join(os.getcwd(), 'icons')
		self.LOCK_FILE = os.path.join(gettempdir(), 'tipmemo-flock')
		self.HEADLIST_MAX = 64
		self.root.title('Tipmemo')
		self.init_file_lock()
		
		self.logging.basicConfig(level=logging.WARNING,
			format='%(levelname)s:%(filename)s:%(funcName)s:%(lineno)d:%(message)s')

		self.img_win = PhotoImage(file=os.path.join(self.ICONPATH,
			'pen-32.png'))
		root.tk.call('wm', 'iconphoto', root._w, self.img_win)

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

		#self.pstatus = PanelStatus(self, root)
		#self.pstatus.pack(fill=BOTH)

	def run(self):
		self.redraw_all()
		self.logging.debug('pwd=%s lockfile=%s' % (self.DBPATH, 
			self.LOCK_FILE))

	def file_write_lock(self):
		fd = open(self.LOCK_FILE, 'r+')
		portalocker.lock(fd, portalocker.LOCK_EX)
		return fd

	def file_read_lock(self):
		fd = open(self.LOCK_FILE, 'r+')
		portalocker.lock(fd, portalocker.LOCK_SH)
		return fd 

	def file_unlock(self, fd):
		fd.close()

	def init_file_lock(self):
		open(self.LOCK_FILE, 'w+').close()

	def get_db_path(self):
		return os.path.join(self.DBPATH, self.DBNAME)

	def check_dbpath(self, directory):
		if not os.path.exists(directory):
			try:
				os.makedirs(directory) 
			except OSError as error:
				if error.errno != errno.EEXIST:
					raise

	def redraw_all(self, filelist=None):
		entry = self.phead.redraw_head(filelist)
		if entry:
			self.pbody.redraw_body(entry)

	def sig_refresh(self):
		self.logging.debug('-->called')
		self.redraw_all()

	def sig_redraw_body(self, entry):
		self.pbody.redraw_body(entry)

	def sig_db_append(self, fname, title):
		self.logging.debug('-->%s %s' % (fname, title))
		self.phead.db_append(fname, title)
		self.redraw_all()

	def sig_db_delete(self, fname):
		self.logging.debug('-->%s' % fname)
		self.phead.db_delete(fname)
		self.redraw_all()

	def sig_search_result(self, filelist=None):
		self.redraw_all(filelist)


if __name__ == '__main__':

	root = Tk()
	root.tk.call('encoding', 'system', 'utf-8')
	#f = font.nametofont('TkFixedFont')
	#f.configure(size=9)
	f = 'lucida 9'
	root.option_add( "*font", f)
	
	tipmemo = Tipmemo(root)
	tipmemo.run()

	root.mainloop()
