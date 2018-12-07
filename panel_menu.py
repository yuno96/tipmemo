#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *

class PanelMenu(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		Frame.__init__(self, root)

		# create a toplevel menu
		self.menubar = Menu(root)
		self.menubar.add_command(label="File", command=self.hello)
		self.menubar.add_command(label="Quit!", command=root.quit)

		# display the menu
		root.config(menu=self.menubar)
		self.logging.debug('init')

	def hello(self):
		self.logging.debug('hello!')

