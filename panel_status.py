#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
from tkinter import *
import time
import datetime
import dbm

class PanelStatus(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		self.logging.debug('called')

		Frame.__init__(self, root, bd=4)

		self.statbar = Label(self, text='hello')#, relief=RAISED)
		self.statbar.pack(side=LEFT)




