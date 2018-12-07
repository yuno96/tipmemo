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

class Tipmemo:
	def __init__(self, root):
		self.root = root
		self.logging = logging
		self.dbpath = './data'
		
		self.logging.basicConfig(level=logging.DEBUG, 
			format='%(levelname)s:%(filename)s:%(funcName)s:%(lineno)d:%(message)s')

		self.check_dbpath(self.dbpath)

		#psearch = PanelMenu(self, root)

		topframe = Frame(root)
		self.psearch = PanelSearch(self, topframe)
		topframe.pack(side=TOP, fill=X)

		btmframe = Frame(root)
		self.phead = PanelHead(self, btmframe)
		btmframe.pack(side=LEFT, fill=Y)

		btmframe2 = Frame(root)
		self.pbody = PanelBody(self, btmframe2)
		btmframe2.pack(side=LEFT, fill=BOTH, expand=True)

		self.logging.debug('init')


	def check_dbpath(self, directory):
		if not os.path.exists(directory):
			try:
				os.makedirs(directory) 
			except OSError as error:
				if error.errno != errno.EEXIST:
					raise

	def sig_phead_append(self, fname):
		self.logging.debug('-->' + fname)
		self.phead.append_to_head(fname)

	def btn_search(self):
		self.logging.debug('searh')

	def run(self):
		self.logging.debug('run')

if __name__ == '__main__':
	root = Tk()
	tipmemo = Tipmemo(root)
	root.mainloop()
