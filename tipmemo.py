#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import errno
from tkinter import *
from panel_menu import *
from panel_search import *
from panel_head import *
from panel_body import *


class Tipmemo:
	def __init__(self, root):
		self.root = root
		self.dbpath = './data'
		
		self.check_dbpath(self.dbpath)

		psearch = PanelMenu(self, root)

		topframe = Frame(root)
		psearch = PanelSearch(self, topframe)
		topframe.pack(side=TOP, fill=X)

		btmframe = Frame(root)
		phead = PanelHead(self, btmframe)
		btmframe.pack(side=LEFT, fill=Y)

		btmframe2 = Frame(root)
		pbody = PanelBody(self, btmframe2)
		btmframe2.pack(side=LEFT, fill=Y)

	def check_dbpath(self, directory):
		if not os.path.exists(directory):
			try:
				os.makedirs(directory) 
			except OSError as error:
				if error.errno != errno.EEXIST:
					raise
	def btn_search(self):
		print('search')

	def run(self):
		print('tipmemo run')

if __name__ == '__main__':
	root = Tk()
	tipmemo = Tipmemo(root)
	root.mainloop()
