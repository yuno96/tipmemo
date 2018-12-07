#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *

class PanelSearch(Frame):
	def __init__(self, mainobj, root):
	#def __init__(self, mainobj):
		print('init :' + __name__)
		Frame.__init__(self, root)
		self.entry = Entry(root)
		self.entry.pack(side=LEFT, fill=X, expand=True)
		self.btn = Button(root, text="click", command=mainobj.btn_search)
		self.btn.pack(side=RIGHT, fill=X)
		#self.pack(side=TOP, fill=X)

	def hello():
		print("hello!")

