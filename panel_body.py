#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import time
from tkinter import *
from tkinter.messagebox import showinfo, showerror, askyesno

class PanelBody(Frame):
	def __init__(self, mainobj, root):
		self.logging = mainobj.logging
		Frame.__init__(self, root)
		self.mainobj = mainobj
		self.fname = None

		tmpframe = Frame(self)
		tmplabel = Label(tmpframe, text='Title:')
		tmplabel.pack(side=LEFT, fill=X)
		self.title = Entry(tmpframe)
		self.title.pack(side=LEFT, fill=BOTH, expand=True)
		tmpframe.pack(side=TOP, fill=BOTH)
		#self.title.bind('<Tab>', self.title_tab)

		contframe = Frame(self)
		scrollbar = Scrollbar(contframe)
		scrollbar.pack(side=RIGHT, fill=Y)
		self.textb = Text(contframe, yscrollcommand=scrollbar.set)
		#self.textb.bind('<KeyRelease>', self.begin_edit_textb)
		self.textb.bind('<<Modified>>', self.begin_edit_textb)
		self.textb.pack(fill=BOTH, expand=True)
		scrollbar.config(command=self.textb.yview)
		contframe.pack(side=TOP, fill=BOTH, expand=True)

		self.img_hl = PhotoImage(file=os.path.join(self.mainobj.ICONPATH, 'hl-16.png'))
		self.btn_hl = Button(self, text='highlighter', image=self.img_hl,
				compound='left', command=self.btn_hl)
		self.btn_hl.pack(side=LEFT, fill=BOTH)

		self.img_del = PhotoImage(file=os.path.join(self.mainobj.ICONPATH, 'delete-16.png'))
		self.btn_del = Button(self, text='Del', image=self.img_del,
				compound='left', command=self.btn_del)
		self.btn_del.pack(side=RIGHT, fill=BOTH)

		self.img_save = PhotoImage(file=os.path.join(self.mainobj.ICONPATH, 'save-16.png'))
		self.btn_save = Button(self, text='Save', image=self.img_save,
				compound='left', state='disabled',
				command=self.save_body)
		self.btn_save.pack(side=RIGHT, fill=BOTH)
		self.img_new = PhotoImage(file=os.path.join(self.mainobj.ICONPATH, 'newfile-16.png'))
		self.btn_new = Button(self, text='New', image=self.img_new,
				compound='left', command=self.btn_new_command)
		self.btn_new.pack(side=RIGHT, fill=BOTH)

		self.logging.debug('init')

		self.tag_hl = []
		self.TAG_PREFIX_HL = '#tag highlight:'
		self.textb.tag_config('notice', background='lemon chiffon')

	'''
	def title_tab(self, event):
		self.logging.debug('-->tab')
		self.textb.focus_set()
	'''

	def clear_tag_hl(self):
		self.tag_hl.clear()

	'''
	def merge_ranges(self, intervals):
		sorted_by_lower_bound = sorted(intervals, key=lambda l: l[0])
		merged = []
		for higher in sorted_by_lower_bound:
			if not merged:
				merged.append(higher)
			else:
				lower = merged[-1]
				#added this condition branch
				if higher[0] - lower[1] == 1:
					merged[-1] = (lower[0], higher[1])  # replace by merged interval
				#end addition. Also changed if below to elif
				# test for intersection between lower and higher:
				# we know via sorting that lower[0] <= higher[0]
				elif higher[0] <= lower[1]:
					upper_bound = max(lower[1], higher[1])
					merged[-1] = (lower[0], upper_bound)  # replace by merged interval
				else:
					merged.append(higher)
		return merged
	'''

	def ugly_convert(self, val):
		print (val)
		a, b = val.split('.')
		return int(a)*1000+int(b)

	def btn_hl(self):
		self.logging.debug('-->btn_hl')
		print (self.textb.index(INSERT))
		ranges = self.textb.tag_ranges(SEL)
		if ranges:
			x = str(ranges[0])
			y = str(ranges[1])
			self.tag_hl.append([x, y])
			#self.tag_hl = self.merge_ranges(self.tag_hl)
			print (self.tag_hl)
			self.textb.tag_add('notice', x, y)
			self.textb.edit_modified(True)
			self.begin_edit_textb()
		else:
			x = str(self.textb.index(INSERT))
			for idx, v in enumerate(self.tag_hl):
				self.logging.debug('%s %s %s' % (x, v[0], v[1]))
				if self.ugly_convert(v[0]) <= self.ugly_convert(x) <= self.ugly_convert(v[1]):
					self.textb.tag_remove('notice', v[0], v[1])
					self.logging.debug('%s <= %s <= %s' % (v[0], x, v[1]))
					del self.tag_hl[idx]
					return

	def btn_del(self):
		self.logging.debug('-->btn_del')
		fname = self.fname
		if fname:
			with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
				title = f.readline().strip()
			choice = askyesno('Warning', 'Delete ? '+title, icon='warning')
			if choice:
				self.mainobj.sig_db_delete(fname)
				os.remove(fname)

	def btn_new_command(self):
		self.set_title_state('normal')
		self.end_edit_textb()
		self.fname = None
		self.clear_all_widget()
		self.title.focus_set()

	def set_title_state(self, curstate):
		title_state = self.title['state']
		self.title.config(state=curstate)
		return title_state

	def begin_edit_textb(self, val=None):
		#self.logging.debug('-->%s'% self.textb.edit_modified())
		if self.textb.edit_modified():
			#self.logging.debug('changed')
			self.btn_save.config(state='normal')

	def end_edit_textb(self):
		#self.logging.debug("changed")
		self.btn_save.config(state='disabled')
		self.textb.edit_modified(False)

	def clear_all_widget(self):
		pre_title_state = self.set_title_state('normal')
		self.title.delete('0', END)
		self.textb.delete('1.0', END)
		self.set_title_state(pre_title_state)

	def make_new_filename(self, t):
		for cnt in range(0, 64):
			fname = os.path.join(self.mainobj.DBPATH, 
					'%d-%d'%(t, cnt))
			if not os.path.isfile(fname):
				return fname
		return None

	def save_body(self):
		self.logging.debug('savebody')
		title = self.title.get().strip()
		if not title:
			showinfo('info', 'Please fill the title')
			return

		if self.fname:
			fname = self.fname
		else:
			t = int(time.time())
			fname = self.make_new_filename(t)

		if not fname:
			self.logging.error('Cannot make filename')
			return

		lockfd = self.mainobj.file_write_lock()
		with open(fname, 'w', encoding='utf-8', errors='ignore') as f:
			if self.tag_hl:
				f.write(self.TAG_PREFIX_HL)
				for l in self.tag_hl:
					f.write('['+l[0]+','+l[1]+']')
				f.write('\n')
			f.write(title+u'\n')
			f.write(self.textb.get(1.0, END))
		self.mainobj.file_unlock(lockfd)

		self.end_edit_textb()
		self.set_title_state('readonly')
		if not self.fname:
			self.mainobj.sig_db_append(fname, title)
			self.fname = fname

	def handle_tag_hl(self, tagstr):
		if not tagstr:
			return
		tagstr = tagstr[len(self.TAG_PREFIX_HL):]
		for tag_range in tagstr.split('['):
			if not tag_range:
				continue
			tag_range_list = tag_range[:-1].split(',')
			if tag_range_list:
				tag_x = tag_range_list[0]
				tag_y = tag_range_list[1]
				self.tag_hl = append([tag_x, tag_y])
				self.textb.tag_add('notice', tag_x, tag_y)

	def redraw_body(self, entry):
		self.clear_all_widget()
		self.clear_tag_hl()

		self.fname = os.path.join(self.mainobj.DBPATH, entry[0])
		try:
			#import pdb;pdb.set_trace()
			pre_title_state = self.set_title_state('normal')
			with open(self.fname, 'r', encoding='utf-8', errors='ignore') as f:
				line = f.readline().strip()

				if line[0] == '#':
					tagstr = line
					line = f.readline().strip()
				self.title.insert(0, line)
				self.textb.insert(INSERT, f.read())
			self.set_title_state(pre_title_state)
			self.handle_tag_hl(tagstr)
		except:
			self.logging.error('Error open: '+self.fname)
			self.fname = None

		self.end_edit_textb()
		self.set_title_state('readonly')



