#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *
from tkinter.messagebox import showinfo

class PanelMenu(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		Frame.__init__(self, root)

		self.menubar = Menu(root)

		# File
		help_menu = Menu(self.menubar)
		help_menu.add_command(label='Open DB', command=self.open_db)
		help_menu.add_command(label='Exit', command=root.quit)
		self.menubar.add_cascade(label='File', menu=help_menu)

		# Help
		about_menu = Menu(self.menubar, tearoff=0)
		about_menu.add_command(label='About', command=self.show_about)
		about_menu.add_command(label='Info', command=self.show_help)
		self.menubar.add_cascade(label='Help',  menu=about_menu)

		# Display the menu
		root.config(menu=self.menubar)
		self.logging.debug('init')

	def open_db(self):
		self.logging.debug('called')

	def show_about(self):
		about_msg = '''
		\rYou can get the latest version here:
		\rhttps://github.com/yuno96/tipmemo.git
		'''
		showinfo('About', about_msg)

	def show_help(self):
		self.logging.debug('help!')

