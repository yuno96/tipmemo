#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *

class PanelSearch(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		Frame.__init__(self, root)
		self.entry = Entry(root)
		self.entry.pack(side=LEFT, fill=X, expand=True)
		self.btn = Button(root, text="Search", command=mainobj.btn_search)
		self.btn.pack(side=RIGHT, fill=X)

	def hello(self):
		self.logging.debug('hello')

