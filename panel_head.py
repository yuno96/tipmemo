#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *

class PanelHead(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		Frame.__init__(self, root)
		self.listb = Listbox(root)
		self.listb.pack(side=TOP, fill=BOTH, expand=True)

		tmpframe = Frame(root)
		self.listb = Button(root, text='<')
		self.listb.pack(side=LEFT, fill=BOTH)
		self.listc = Button(root, text='o')
		self.listc.pack(side=LEFT, fill=BOTH)
		self.listd = Button(root, text='>')
		self.listd.pack(side=LEFT, fill=BOTH)
		tmpframe.pack(side=BOTTOM)

		self.logging.debug('init')

	def hello(self):
		print("hello!")


