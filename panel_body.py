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

		self.TAG_HL_PREFIX = '#tag highlight:'
		self.TAG_HL_COLOR = 'gold'
		self.textb.tag_config('notice', background=self.TAG_HL_COLOR)

	def clear_textb_tag_hl(self):
		self.textb.tag_delete('notice')
		self.textb.tag_config('notice', background=self.TAG_HL_COLOR)

	def remove_tag(self, begin, end):
		self.logging.debug(self.textb.tag_ranges('notice'))
		self.textb.tag_remove('notice', begin, end)

	def btn_hl(self):
		textb_edited = False
		ranges = self.textb.tag_ranges(SEL)
		#self.logging.debug(ranges)
		if ranges:
			tag_indices =  self.textb.tag_ranges('notice')
			for begin, end in zip(tag_indices[0::2], tag_indices[1::2]):
				if begin == ranges[0] and end == ranges[1]:
					self.logging.debug('%s %s %s %s' % (begin, end, ranges[0], ranges[1]))
					self.remove_tag(begin, end)
			else:
				self.textb.tag_add('notice', ranges[0], ranges[1])
			textb_edited = True
		else:
			x = self.textb.index(INSERT)

			self.logging.debug(self.textb.tag_ranges('notice'))
			tag_indices =  self.textb.tag_ranges('notice')
			for begin, end in zip(tag_indices[0::2], tag_indices[1::2]):
				v0 = str(begin)
				v1 = str(end)
				if self.textb.compare(v0, '<=', x) and self.textb.compare(x, '<=', v1):
					self.remove_tag(begin, end)
					textb_edited = True

		if textb_edited:
			self.textb.edit_modified(True)
			self.begin_edit_textb()

	def btn_del(self):
		fname = self.fname
		if fname:
			lockfd = self.mainobj.file_read_lock()
			with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
				title = f.readline().strip()
			self.mainobj.file_unlock(lockfd)
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
		if self.textb.edit_modified():
			#self.logging.debug('changed')
			self.btn_save.config(state='normal')

	def end_edit_textb(self):
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

			tag_str = ''
			tag_indices =  self.textb.tag_ranges('notice')
			for begin, end in zip(tag_indices[0::2], tag_indices[1::2]):
				tag_str += '['+str(begin)+','+str(end)+']'

			if tag_str:
				f.write(self.TAG_HL_PREFIX+tag_str+'\n')

			f.write(title+u'\n')
			f.write(self.textb.get(1.0, END))
		self.mainobj.file_unlock(lockfd)

		self.end_edit_textb()
		self.set_title_state('readonly')
		if not self.fname:
			self.mainobj.sig_db_append(fname, title)
			self.fname = fname

	def handle_textb_tag_hl(self, tagstr):
		if not tagstr:
			return
		tagstr = tagstr[len(self.TAG_HL_PREFIX):]
		for tag_range in tagstr.split('['):
			if not tag_range:
				continue
			tag_xy = tag_range[:-1].split(',')
			if tag_xy:
				tag_x = tag_xy[0]
				tag_y = tag_xy[1]
				#self.logging.debug('tag: %s' % tag_xy)
				self.textb.tag_add('notice', tag_x, tag_y)

	def redraw_body(self, entry):
		self.clear_all_widget()
		self.clear_textb_tag_hl()

		self.fname = os.path.join(self.mainobj.DBPATH, entry[0])
		try:
			tagstr = ''
			pre_title_state = self.set_title_state('normal')
			lockfd = self.mainobj.file_read_lock()
			with open(self.fname, 'r', encoding='utf-8', errors='ignore') as f:
				line = f.readline().strip()

				if line[0] == '#':
					tagstr = line
					line = f.readline().strip()
				self.title.insert(0, line)
				self.textb.insert(INSERT, f.read())
			self.mainobj.file_unlock(lockfd)
			self.set_title_state(pre_title_state)
			if tagstr:
				self.handle_textb_tag_hl(tagstr)
		except Exception as e:
			self.logging.error(e)
			self.fname = None

		self.end_edit_textb()
		self.set_title_state('readonly')



