"""
Example showing for tkinter and ttk:
  -- ttk.Checkbutton
  -- ttk.Radiobutton
  -- Using tkinter's StringVar, IntVar, DoubleVar to track changes
Authors: David Mutchler and his colleagues
         at Rose-Hulman Institute of Technology.
"""

try:
    # Python2
	import Tkinter as tk
	from Tkinter import *
	import ttk
	from ttk import Button, Style
	import tkFileDialog as fdlg
	import tkMessageBox as mbox
except ImportError:
    # Python3
	import tkinter as tk
	from tkinter import *
	import tkinter.ttk as ttk
	from tkinter.ttk import *
	from tkinter.filedialog import Open
	import tkinter.messagebox as mbox
import os
import sys
import ast
#import time
#import datetime
#from demopanels import MsgPanel, SeeDismissPanel
import xlsx2csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
#from matplotlib.cbook import get_sample_data
#import matplotlib.dates as mdates
#import matplotlib.cbook as cbook

LARGE_FONT = ('Verdana', 12) # font's family is Verdana, font's size is 12 
 
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title('SVI handing excel to plot') # set the title of the main window
		self.geometry('900x500') # set size of the main window to 300x300 pixels
		#tk.Tk.iconbitmap(self, default="'C:/Users/huyhoang.SVI/Desktop/test_excel/savarti.ico'")
		#img = PhotoImage(file='C:/Users/huyhoang.SVI/Desktop/test_excel/savarti.jfif')
		#self.tk.call('wm', 'iconphoto', root._w, img)
		#self.iconbitmap('C:/Users/huyhoang.SVI/Desktop/test_excel/savarti.ico')
		
        # this container contains all the pages
		container = tk.Frame(self)
		self.container = container
		container.pack(side='top', fill='both', expand=True)
		container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
		container.grid_columnconfigure(0,weight=1) # make the cell in grid cover the entire window
		self.frames = {} # these are pages we want to navigate to
		
		self.frames["StartPage"] = StartPage(parent=container, controller=self)
		self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
		self.show_frame("StartPage") # let the first page is StartPage
 
    def show_frame(self, name):
		if name == "PageOne": 
			self.frames["PageOne"] = PageOne(parent=self.container, controller=self)
			self.frames["PageOne"].grid(row=0, column=0, sticky="nsew")
		elif name == "PageTwo":
			if len(list_info) == 0:
				mbox.showerror("Error", "Choose at least one in field \'Info\'")
			elif len(list_filter) == 0:
				mbox.showerror("Error", "Choose at least one in field \'Filter\'")
			elif len(list_data) == 0:
				mbox.showerror("Error", "Choose at least one in field \'Data\'")
			elif not set(list_info).isdisjoint(set(list_filter)):
				mbox.showerror("Error", "Header in %s can not be appear together in two field 'Info' and 'Filter'"%(set(list_info) & set(list_filter)))
			elif not set(list_data).isdisjoint(set(list_filter)):
				mbox.showerror("Error", "Header in %s can not be appear together in two field 'Data' and 'Filter'"%(set(list_data) & set(list_filter)))
			elif not set(list_info).isdisjoint(set(list_filter)):
				mbox.showerror("Error", "Header in %s can not be appear together in two field 'Info' and 'Data'"%(set(list_info) & set(list_filter)))
			else:
				dict_config_tmp = {'list_info_order': list_info_order, 'list_filter_order': list_filter_order, 'list_data_order': list_data_order}
				with open(path_file_config, 'w') as file_config:
					file_config.write(str(dict_config_tmp))
				self.frames["PageTwo"] = PageTwo(parent=self.container, controller=self)
				self.frames["PageTwo"].grid(row=0, column=0, sticky="nsew")
		elif name == "PageThree_All":
			self.frames["PageThree_All"] = PageThree_All(parent=self.container, controller=self)
			self.frames["PageThree_All"].grid(row=0, column=0, sticky="nsew")
		elif name == "PageThree_Filter":
			self.frames["PageThree_Filter"] = PageThree_Filter(parent=self.container, controller=self)
			self.frames["PageThree_Filter"].grid(row=0, column=0, sticky="nsew")
		elif name == "PageThree_Compare":
			self.frames["PageThree_Compare"] = PageThree_Compare(parent=self.container, controller=self)
			self.frames["PageThree_Compare"].grid(row=0, column=0, sticky="nsew")
		
		frame = self.frames[name]
		frame.tkraise()
 
class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text='Start Page', font=LARGE_FONT)
		label.pack(pady=10, padx=10) # center alignment
 
		self.controller = controller
		
		frame1 = Frame(self)#, relief=RAISED)
		frame1.pack(fill=BOTH, expand=True)
		lbl = ttk.Label(frame1, width=20, text='Select a file to open ')
		ent = ttk.Entry(frame1, width=25)
		btn = ttk.Button(frame1, text='Browse...', command=lambda i='open', e=ent: self.file_dialog(i, e))
		lbl.pack(side=LEFT, padx=5, pady=5)
		ent.pack(side=LEFT, expand=Y, fill=X)
		btn.pack(side=LEFT, padx=5, pady=5)
		
		frame_button = Frame(self)
		frame_button.pack(fill=X)
		closeButton = Button(frame_button, text="Exit", command=self.quit)
		closeButton.pack(side=RIGHT, padx=5, pady=5)
		nextButton = Button(frame_button, text="Next", command=self.checkfile)
		nextButton.pack(side=RIGHT)
		
	def file_dialog(self, type, ent):
        # triggered when the user clicks a 'Browse' button 
		fn = None
		opts = {'initialfile': ent.get(), 'filetypes': (('Excel Workbook', '.xlsx'), ('Excel 97-2003 Workbook', '.xls'), ('All files', '.*'),)}
        
		opts['title'] = 'Select a file to open...'
		fn = fdlg.askopenfilename(**opts)

		if fn:
			ent.delete(0, END)
			ent.insert(END, fn)
		path_file.append(ent.get())
		return

	def checkfile(self):
		if len(path_file) == 0:
			mbox.showerror("Error", "Path file is empty")
		else:
			real_path_file = path_file[-1]
			if '.xls' in real_path_file and not '.xlsx' in real_path_file:
				path_file_csv = real_path_file.replace('.xls', '.csv')
			elif '.xlsx' in real_path_file:
				path_file_csv = real_path_file.replace('.xlsx', '.csv')
				
			xlsx2csv.Xlsx2csv(real_path_file).convert(path_file_csv, sheetid=1)
			'''	
			if os.path.exists(path_file_csv):
				os.system('rm %s'%(path_file_csv))
				xlsx2csv.Xlsx2csv(real_path_file).convert(path_file_csv, sheetid=1)
			else:
				xlsx2csv.Xlsx2csv(real_path_file).convert(path_file_csv, sheetid=1)
			'''
			
			#find path of config file
			name_file_excel = real_path_file.split('/')[-1]
			folder_path = real_path_file.split(name_file_excel)[0]
			global path_file_config
			global list_info_order
			global list_filter_order
			global list_data_order
			path_file_config = folder_path + name_file_excel.split('.')[0] + '.txt'
			if os.path.exists(path_file_config):
				answer = mbox.askyesno("Question","Do you want to load file config?")
				if answer:
					dict_config = self.reading(path_file_config)
					list_info_order = dict_config['list_info_order']
					list_filter_order = dict_config['list_filter_order']
					list_data_order = dict_config['list_data_order']	
			
			global my_dataframe
			my_dataframe = pd.read_csv(path_file_csv)
			for it in list(my_dataframe.columns.values):
				if 'Unnamed:' in it:
					my_dataframe = my_dataframe.drop(it, axis=1)
			global list_header
			list_header = list(my_dataframe.columns.values)
			self.controller.show_frame('PageOne')
		return	

	def reading(self, path_file):
		with open(path_file, 'r') as f:
			s = f.read()
			config = ast.literal_eval(s)
		return config
	
 
class PageOne(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text='Page One', font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		
		frame_info = Frame(self)
		frame_info.pack(fill=X, expand=True)
		V = Label(frame_info, text="Info", fg="red")#.grid(row=1, column=11, sticky=W)	
		V.pack(side=LEFT, padx=8, pady=5)
		
		self.i0 = IntVar()
		self.i1 = IntVar()
		self.i2 = IntVar()
		self.i3 = IntVar()
		self.i4 = IntVar()
		self.i5 = IntVar()
		self.i6 = IntVar()
		self.i7 = IntVar()
		self.i8 = IntVar()
		self.i9 = IntVar()
		self.i10 = IntVar()
		self.list_info_tmp = [self.i0, self.i1, self.i2, self.i3, self.i4, self.i5, self.i6, self.i7, self.i8, self.i9, self.i10]
		for it in self.list_info_tmp:
			it.set(0)
		if list_info_order:
			index = 0
			for it2 in list_info_order:
				self.list_info_tmp[index].set(it2)
				index += 1
			global list_info
			list_info = list()
			list_info_tmp_1 = list()
			list_info_tmp_2 = list()
			for x in range(0, len(list_header)):
				list_info_tmp_1.append(self.list_info_tmp[x].get())
			dict_info = OrderedDict(zip(list_header, list_info_tmp_1))
			for it in dict_info:
				if dict_info[it] == 1:
					list_info_tmp_2.append(it)
			list_info = list_info_tmp_2
			
		for x in range(0, len(list_header)):
			if list_header[x].upper() != 'STT':
				Checkbutton(frame_info, text=list_header[x], variable=self.list_info_tmp[x], command=lambda: self.chk_changed_info()).pack(side=LEFT)
		
		frame_filter = Frame(self)
		frame_filter.pack(fill=X, expand=True)
		T = Label(frame_filter, text="Filter", fg="red").pack(side=LEFT, padx=5, pady=5)
		
		self.f0 = IntVar()
		self.f1 = IntVar()
		self.f2 = IntVar()
		self.f3 = IntVar()
		self.f4 = IntVar()
		self.f5 = IntVar()
		self.f6 = IntVar()
		self.f7 = IntVar()
		self.f8 = IntVar()
		self.f9 = IntVar()
		self.f10 = IntVar()
		self.list_filter_tmp = [self.f0, self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9, self.f10]
		
		for it in self.list_filter_tmp:
			it.set(0)
		if list_filter_order:
			index = 0
			for it2 in list_filter_order:
				self.list_filter_tmp[index].set(it2)
				index += 1
			global list_filter
			list_filter = list()
			list_filter_tmp_1 = list()
			list_filter_tmp_2 = list()
			for x in range(0, len(list_header)):
				list_filter_tmp_1.append(self.list_filter_tmp[x].get())
			dict_filter = OrderedDict(zip(list_header, list_filter_tmp_1))
			for it in dict_filter:
				if dict_filter[it] == 1:
					list_filter_tmp_2.append(it)
			list_filter = list_filter_tmp_2
				
		for x in range(0, len(list_header)):
			if list_header[x].upper() != 'STT':
				Checkbutton(frame_filter, text=list_header[x], variable=self.list_filter_tmp[x], command=lambda: self.chk_changed_filter()).pack(side=LEFT)
		
		frame_data = Frame(self)
		frame_data.pack(fill=X, expand=True)
		P = Label(frame_data, text="Data", fg="red").pack(side=LEFT, padx=6, pady=5)
		
		self.d0 = IntVar()
		self.d1 = IntVar()
		self.d2 = IntVar()
		self.d3 = IntVar()
		self.d4 = IntVar()
		self.d5 = IntVar()
		self.d6 = IntVar()
		self.d7 = IntVar()
		self.d8 = IntVar()
		self.d9 = IntVar()
		self.d10 = IntVar()
		self.list_data_tmp = [self.d0, self.d1, self.d2, self.d3, self.d4, self.d5, self.d6, self.d7, self.d8, self.d9, self.d10]
		
		for it in self.list_data_tmp:
			it.set(0)
		if list_data_order:
			index = 0
			for it2 in list_data_order:
				self.list_data_tmp[index].set(it2)
				index += 1
			global list_data
			list_data = list()
			list_data_tmp_1 = list()
			list_data_tmp_2 = list()
			for x in range(0, len(list_header)):
				list_data_tmp_1.append(self.list_data_tmp[x].get())
			dict_data = OrderedDict(zip(list_header, list_data_tmp_1))
			for it in dict_data:
				if dict_data[it] == 1:
					list_data_tmp_2.append(it)
			list_data = list_data_tmp_2
		
		for x in range(0, len(list_header)):
			if list_header[x].upper() != 'STT':
				Checkbutton(frame_data, text=list_header[x], variable=self.list_data_tmp[x], command=lambda: self.chk_changed_data()).pack(side=LEFT)
			
		frame_button = Frame(self)
		frame_button.pack(fill=X)
		closeButton = Button(frame_button, text="Exit", command=self.quit)
		closeButton.pack(side=RIGHT, padx=5, pady=5)
		button1 = Button(frame_button, text='Next', # likewise PageTwo
                            command=lambda : controller.show_frame('PageTwo'))
		button1.pack(side=RIGHT)
		button2 = Button(frame_button, text='Back', # likewise StartPage
                            command=lambda : controller.show_frame('StartPage'))
		button2.pack(side=RIGHT, padx=5, pady=5)
		
		#root.mainloop()  
		return

	def chk_changed_info(self):
		global list_info
		global list_info_order
		list_info = list()
		list_info_tmp_1 = list()
		list_info_tmp_2 = list()
		list_info_tmp_order = list()
		for x in range(0, len(list_header)):
			list_info_tmp_1.append(self.list_info_tmp[x].get())
		dict_info = OrderedDict(zip(list_header, list_info_tmp_1))
		for it in dict_info:
			if dict_info[it] == 1:
				list_info_tmp_2.append(it)
		list_info = list_info_tmp_2
		for it2 in dict_info:
			list_info_tmp_order.append(dict_info[it2])
		list_info_order = list_info_tmp_order			
		#print "list_info:%s"%list_info
		return
	
	def chk_changed_filter(self):
		global list_filter
		global list_filter_order
		list_filter = list()
		list_filter_tmp_1 = list()
		list_filter_tmp_2 = list()
		list_filter_tmp_order = list()
		for x in range(0, len(list_header)):
			list_filter_tmp_1.append(self.list_filter_tmp[x].get())
		dict_filter = OrderedDict(zip(list_header, list_filter_tmp_1))
		for it in dict_filter:
			if dict_filter[it] == 1:
				list_filter_tmp_2.append(it)
		list_filter = list_filter_tmp_2
		for it2 in dict_filter:
			list_filter_tmp_order.append(dict_filter[it2])
		list_filter_order = list_filter_tmp_order
		#print "list_filter:%s"%list_filter
		return
	
	def chk_changed_data(self):
		global list_data
		global list_data_order
		list_data = list()
		list_data_tmp_1 = list()
		list_data_tmp_2 = list()
		list_data_tmp_order = list()
		for x in range(0, len(list_header)):
			list_data_tmp_1.append(self.list_data_tmp[x].get())
		dict_data = OrderedDict(zip(list_header, list_data_tmp_1))
		for it in dict_data:
			if dict_data[it] == 1:
				list_data_tmp_2.append(it)
		list_data = list_data_tmp_2
		for it2 in dict_data:
			list_data_tmp_order.append(dict_data[it2])
		list_data_order = list_data_tmp_order
		#print "list_data:%s"%list_data
		return

class PageTwo(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text='Page Two', font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		
		self.controller = controller
		
		frame = Frame(self)
		frame.pack(fill=BOTH, expand=True)
		self.tkvar = StringVar()
		
		global page_name
		try:
			if page_name == 'PageThree_All':
				self.tkvar.set('All')
			elif page_name == 'PageThree_Filter':
				self.tkvar.set('Filter')
			elif page_name == 'PageThree_Compare':
				self.tkvar.set('Compare')
		except NameError:
			self.tkvar.set('All')
			page_name = 'PageThree_All'
		
		ttk.Label(frame, text = 'Do you want plot', width=20).pack(side=LEFT, padx=5, pady=5)
		ttk.Combobox(frame, textvariable=self.tkvar, values = ['All', 'Filter', 'Compare'], state="readonly").pack(side=LEFT)
		self.tkvar.trace('w',self.callback)
		
		frame_button = Frame(self)
		frame_button.pack(fill=X)
		closeButton = Button(frame_button, text="Exit", command=self.quit)
		closeButton.pack(side=RIGHT, padx=5, pady=5)
		button1 = Button(frame_button, text='Next', command=lambda : self.controller.show_frame(page_name))
		button1.pack(side=RIGHT)
		button2 = Button(frame_button, text='Back', command=lambda : self.controller.show_frame('PageOne'))
		button2.pack(side=RIGHT, padx=5, pady=5)
		
	def callback(self, *args):
		global page_name
		if self.tkvar.get() == 'All':
			page_name = 'PageThree_All'
			self.tkvar.set('All')
		elif self.tkvar.get() == 'Filter':
			page_name = 'PageThree_Filter'
			self.tkvar.set('Filter')
		elif self.tkvar.get() == 'Compare':
			page_name = 'PageThree_Compare'
			self.tkvar.set('Compare')
		
		
		
class PageThree_All(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text='Page Three_All', font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		
		frame = Frame(self)
		frame.pack(fill=BOTH, expand=True)
		self.tkvar = StringVar()
		
		global type_graph_all
		try:
			self.tkvar.set(type_graph_all)
		except NameError:
			self.tkvar.set('Line')
			type_graph_all = 'Line'
			
		ttk.Label(frame, text = 'Type of graph', width=20).pack(side=LEFT, padx=5, pady=5)
		ttk.Combobox(frame, textvariable=self.tkvar, values = ['Line', 'Bar'], state="readonly").pack(side=LEFT)
		self.tkvar.trace('w',self.callback)
		
		frame2 = Frame(self)
		frame2.pack(fill=X, expand=True)
		ttk.Label(frame2, text = 'Title', width=10).pack(side=LEFT, padx=5, pady=5)
		self.entry_title = StringVar()
		Entry(frame2, textvariable=self.entry_title, width=70).pack(side=LEFT, padx=5, pady=5)
		
		frame3 = Frame(self)
		frame3.pack(fill=X, expand=True)
		ttk.Label(frame3, text = 'xLabel', width=10).pack(side=LEFT, padx=5, pady=5)
		self.entry_xlabel = StringVar()
		Entry(frame3, textvariable=self.entry_xlabel, width=70).pack(side=LEFT, padx=5, pady=5)
		
		frame4 = Frame(self)
		frame4.pack(fill=X, expand=True)
		ttk.Label(frame4, text = 'yLabel', width=10).pack(side=LEFT, padx=5, pady=5)
		self.entry_ylabel = StringVar()
		Entry(frame4, textvariable=self.entry_ylabel, width=70).pack(side=LEFT, padx=5, pady=5)
		
		frame_button = Frame(self)
		frame_button.pack(fill=X)
		closeButton = Button(frame_button, text="Exit", command=self.quit)
		closeButton.pack(side=RIGHT, padx=5, pady=5)
		button1 = Button(frame_button, text='Create graph', # likewise PageTwo
                            command=self.plot)
		button1.pack(side=RIGHT)
		button2 = Button(frame_button, text='Back', # likewise StartPage
                            command=lambda : controller.show_frame('PageTwo'))
		button2.pack(side=RIGHT, padx=5, pady=5)
		
	def callback(self, *args):
		global type_graph_all
		type_graph_all = self.tkvar.get()
		
	def plot(self):
		color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
						  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
						  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
						  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
		
		fig, ax = plt.subplots(1, 1, figsize=(12, 9))

		ax.spines['top'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.spines['left'].set_visible(False)

		ax.get_xaxis().tick_bottom()
		ax.get_yaxis().tick_left()
		
		if type_graph_all == 'Line':
			fig.subplots_adjust(left=0.085, right=0.95, bottom=0.1, top=0.85)
			ind = np.arange(len(list_data))
			plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
			plt.tick_params(axis='both', which='both', bottom=False, top=False,
							labelbottom=True, left=False, right=False, labelleft=True)

			majors = list(my_dataframe[list_info].values)
			list_tmp = list(my_dataframe[list_data].values)

			for rank, column in enumerate(majors):
				column_rec_name = column[0]
				if type_graph_all == 'Line':
					line = plt.plot(ind,
									list_tmp[rank],
									lw=2.5,
									color=color_sequence[rank],
									label=column_rec_name)
			
			ax.set_title(self.entry_title.get(), fontsize=18, ha='center')
			ax.set_ylabel(self.entry_ylabel.get())
			ax.set_xlabel(self.entry_xlabel.get())
			ax.set_xticks(ind)
			ax.set_xticklabels(list_data, rotation=45)
			ax.legend()
			
			plt.show()
		elif type_graph_all == 'Bar':
			fig.subplots_adjust(left=0.085, right=0.95, bottom=0.1, top=0.85)
			plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
			plt.tick_params(axis='both', which='both', bottom=False, top=False,
							labelbottom=True, left=False, right=False, labelleft=True)

			majors = list_data
			list_y_bar = list()
			for it in list_data:
				list_y_bar.append(list(my_dataframe[it].values))
			
			ind = np.arange(len(list_y_bar[0]))
			width = (1-0.1)/len(list_data)
			
			def autolabel(rects, xpos='center'):
				"""
				Attach a text label above each bar in *rects*, displaying its height.

				*xpos* indicates which side to place the text w.r.t. the center of
				the bar. It can be one of the following {'center', 'right', 'left'}.
				"""

				xpos = xpos.lower()  # normalize the case of the parameter
				ha = {'center': 'center', 'right': 'left', 'left': 'right'}
				offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

				for rect in rects:
					height = rect.get_height()
					ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
							'{}'.format(height), ha=ha[xpos], va='bottom')
			number_bar_tmp = len(list_data)
			if number_bar_tmp % 2 == 0:
				number_bar_tmp = -(number_bar_tmp - 1)
				for rank, column in enumerate(majors):
					column_rec_name = column
					rects = ax.bar(ind + ((width/2)*number_bar_tmp), list_y_bar[rank], width, color=color_sequence[rank], label=column_rec_name)
					autolabel(rects, 'center')
					number_bar_tmp += 2
			else:
				number_bar_tmp = -(number_bar_tmp - 3)
				for rank, column in enumerate(majors):
					column_rec_name = column
					rects = ax.bar(ind + (width*number_bar_tmp), list_y_bar[rank], width, color=color_sequence[rank], label=column_rec_name)
					autolabel(rects, 'center')
					number_bar_tmp += 1

			ax.set_title(self.entry_title.get(), fontsize=18, ha='center')
			ax.set_ylabel(self.entry_ylabel.get())
			ax.set_xlabel(self.entry_xlabel.get())
			ax.set_xticks(ind)
			ax.set_xticklabels(list(my_dataframe[list_info[0]].values), rotation=45)
			ax.legend()
			
			plt.show()
		
class PageThree_Filter(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text='Page Three_Filter', font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		
		self.tkvar_1 = StringVar()
		self.tkvar_2 = StringVar()
		self.tkvar_3 = StringVar()
		self.tkvar_4 = StringVar()
		self.tkvar_5 = StringVar()
		self.tkvar_6 = StringVar()
		self.tkvar_7 = StringVar()
		self.list_tkvar = [self.tkvar_1, self.tkvar_2, self.tkvar_3, self.tkvar_4, self.tkvar_5, self.tkvar_6, self.tkvar_7]
		self.frame_1 = Frame(self)
		self.frame_2 = Frame(self)
		self.frame_3 = Frame(self)
		self.frame_4 = Frame(self)
		self.frame_5 = Frame(self)
		self.frame_6 = Frame(self)
		self.frame_7 = Frame(self)
		self.list_frame = [self.frame_1, self.frame_2, self.frame_3, self.frame_4, self.frame_5, self.frame_6, self.frame_7]
		
		global dict_filter
		dict_filter = OrderedDict()
		
		count_filter_header = -1
		for it in list_filter:
			count_filter_header += 1
			dict_filter[it] = self.list_tkvar[count_filter_header].get()
		
		self.count_frame = -1
		for it in list_filter:
			self.count_frame += 1
			self.list_frame[self.count_frame].pack(fill=X)
			
			list_values = list(dict.fromkeys(list(my_dataframe[it])))
			list_values = ['All'] + list_values
			ttk.Label(self.list_frame[self.count_frame], text = it, width=20).pack(side=LEFT, padx=5, pady=5)
			self.list_tkvar[self.count_frame].set('All')
			ttk.Combobox(self.list_frame[self.count_frame], textvariable=self.list_tkvar[self.count_frame], values = list_values, state="readonly").pack(side=LEFT)
			self.list_tkvar[self.count_frame].trace('w',self.callback)
		
		frame_typegraph = Frame(self)
		frame_typegraph.pack(fill=X, expand=True)
		self.tkvar = StringVar()
		
		global type_graph_filter
		try:
			self.tkvar.set(type_graph_filter)
		except NameError:
			self.tkvar.set('Line')
			type_graph_filter = 'Line'
		
		ttk.Label(frame_typegraph, text = 'Type of graph', width=20).pack(side=LEFT, padx=5, pady=5)
		ttk.Combobox(frame_typegraph, textvariable=self.tkvar, values = ['Line', 'Bar'], state="readonly").pack(side=LEFT)	
		self.tkvar.trace('w',self.callback2)
		
		frame2 = Frame(self)
		frame2.pack(fill=X, expand=True)
		ttk.Label(frame2, text = 'Title', width=10).pack(side=LEFT, padx=5, pady=5)
		self.entry_title_filter = StringVar()
		Entry(frame2, textvariable=self.entry_title_filter, width=70).pack(side=LEFT, padx=5, pady=5)
		
		frame3 = Frame(self)
		frame3.pack(fill=X, expand=True)
		ttk.Label(frame3, text = 'xLabel', width=10).pack(side=LEFT, padx=5, pady=5)
		self.entry_xlabel_filter = StringVar()
		Entry(frame3, textvariable=self.entry_xlabel_filter, width=70).pack(side=LEFT, padx=5, pady=5)
		
		frame4 = Frame(self)
		frame4.pack(fill=X, expand=True)
		ttk.Label(frame4, text = 'yLabel', width=10).pack(side=LEFT, padx=5, pady=5)
		self.entry_ylabel_filter = StringVar()
		Entry(frame4, textvariable=self.entry_ylabel_filter, width=70).pack(side=LEFT, padx=5, pady=5)
		
		frame_button = Frame(self)
		frame_button.pack(fill=X)
		closeButton = Button(frame_button, text="Exit", command=self.quit)
		closeButton.pack(side=RIGHT, padx=5, pady=5)
		button1 = Button(frame_button, text='Create graph', # likewise PageTwo
                            command=self.plot)
		button1.pack(side=RIGHT)
		button2 = Button(frame_button, text='Back', # likewise StartPage
                            command=lambda : controller.show_frame('PageTwo'))
		button2.pack(side=RIGHT, padx=5, pady=5)
		
	def callback(self, *args):
		for it in dict_filter:
			dict_filter[it] = self.list_tkvar[dict_filter.keys().index(it)].get()
		#for it in dict_filter:
		#	print "%s: %s"%(it, dict_filter[it])
		
	def callback2(self, *args):
		global type_graph_filter
		type_graph_filter = self.tkvar.get()
	
		'''
		frame_place = Frame(self)
		frame_place.pack(fill=X)
		ttk.Label(frame_place, text = 'Place', width=20).pack(side=LEFT, padx=5, pady=5)
		ttk.Combobox(frame_place, textvariable=self.tkvar_place, values = ['All', 'HCM', 'DN'], state="readonly").pack(side=LEFT)
		#combo_place.current(0) #set the selected item
		#combo.grid(column=0, row=0)
		self.tkvar_place.trace('w',self.callback_place)
		#btn = ttk.Button(frame_place, text="Get Value",command=self.print_value(combo_place))
		#btn.pack(side=LEFT)
		
		frame_work = Frame(self)
		frame_work.pack(fill=X)
		label_work = ttk.Label(frame_work, text = 'Work', width=20)
		label_work.pack(side=LEFT, padx=5, pady=5)
		combo_work = ttk.Combobox(frame_work, textvariable=self.tkvar_work, values = ['All', 'CAD', 'Circuit', 'Layout'], state="readonly")
		#combo_work.current(0) #set the selected item
		#combo.grid(column=0, row=0)
		combo_work.pack(side=LEFT)
		self.tkvar_work.trace('w',self.callback_work)
		'''
		
	def plot(self):
		color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
						  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
						  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
						  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
		
		fig, ax = plt.subplots(1, 1, figsize=(12, 9))

		ax.spines['top'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.spines['left'].set_visible(False)

		ax.get_xaxis().tick_bottom()
		ax.get_yaxis().tick_left()
		
		if type_graph_filter == 'Line':
			fig.subplots_adjust(left=0.085, right=0.95, bottom=0.1, top=0.85)
			
			ind = np.arange(len(list_data))
			plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
			plt.tick_params(axis='both', which='both', bottom=False, top=False,
							labelbottom=True, left=False, right=False, labelleft=True)
			
			my_dataframe_copy = my_dataframe.copy(deep = True)
			for it in dict_filter:
				if dict_filter[it].upper() != 'ALL':
					my_dataframe_copy = my_dataframe_copy[my_dataframe_copy[it] == dict_filter[it]]
			
			majors = list(my_dataframe_copy[list_info].values)
			list_tmp = list(my_dataframe_copy[list_data].values)
			
			for rank, column in enumerate(majors):
				column_rec_name = column[0]
				if type_graph_filter == 'Line':
					line = plt.plot(ind,
									list_tmp[rank],
									lw=2.5,
									color=color_sequence[rank],
									label=column_rec_name)
			
			ax.set_title(self.entry_title_filter.get(), fontsize=18, ha='center')
			ax.set_ylabel(self.entry_ylabel_filter.get())
			ax.set_xlabel(self.entry_xlabel_filter.get())
			ax.set_xticks(ind)
			ax.set_xticklabels(list_data, rotation=45)
			ax.legend()
			
			plt.show()
		elif type_graph_filter == 'Bar':
			fig.subplots_adjust(left=0.085, right=0.95, bottom=0.1, top=0.85)
			plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
			plt.tick_params(axis='both', which='both', bottom=False, top=False,
							labelbottom=True, left=False, right=False, labelleft=True)
			
			my_dataframe_copy = my_dataframe.copy(deep = True)
			for it in dict_filter:
				if dict_filter[it].upper() != 'ALL':
					my_dataframe_copy = my_dataframe_copy[my_dataframe_copy[it] == dict_filter[it]]
			
			majors = list_data
			list_y_bar = list()
			for it in list_data:
				list_y_bar.append(list(my_dataframe_copy[it].values))
			
			ind = np.arange(len(list_y_bar[0]))
			width = (1-0.1)/len(list_data)
			
			def autolabel(rects, xpos='center'):
				"""
				Attach a text label above each bar in *rects*, displaying its height.

				*xpos* indicates which side to place the text w.r.t. the center of
				the bar. It can be one of the following {'center', 'right', 'left'}.
				"""

				xpos = xpos.lower()  # normalize the case of the parameter
				ha = {'center': 'center', 'right': 'left', 'left': 'right'}
				offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

				for rect in rects:
					height = rect.get_height()
					ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
							'{}'.format(height), ha=ha[xpos], va='bottom')
			number_bar_tmp = len(list_data)
			if number_bar_tmp % 2 == 0:
				number_bar_tmp = -(number_bar_tmp - 1)
				for rank, column in enumerate(majors):
					column_rec_name = column
					rects = ax.bar(ind + ((width/2)*number_bar_tmp), list_y_bar[rank], width, color=color_sequence[rank], label=column_rec_name)
					autolabel(rects, 'center')
					number_bar_tmp += 2
			else:
				number_bar_tmp = -(number_bar_tmp - 3)
				for rank, column in enumerate(majors):
					column_rec_name = column
					rects = ax.bar(ind + (width*number_bar_tmp), list_y_bar[rank], width, color=color_sequence[rank], label=column_rec_name)
					autolabel(rects, 'center')
					number_bar_tmp += 1
			
			ax.set_title(self.entry_title_filter.get(), fontsize=18, ha='center')
			ax.set_ylabel(self.entry_ylabel_filter.get())
			ax.set_xlabel(self.entry_xlabel_filter.get())
			ax.set_xticks(ind)
			ax.set_xticklabels(list(my_dataframe_copy[list_info[0]].values), rotation=45)
			ax.legend()
			
			plt.show()
		
class PageThree_Compare(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text='Page Three_Compare', font=LARGE_FONT)
		label.pack(pady=10, padx=10)
		
		self.tkvar_1 = StringVar()
		self.tkvar_2 = StringVar()
		self.tkvar_3 = StringVar()
		self.tkvar_4 = StringVar()
		self.tkvar_5 = StringVar()
		self.tkvar_6 = StringVar()
		self.tkvar_7 = StringVar()
		self.list_tkvar_mini1 = [self.tkvar_1, self.tkvar_2, self.tkvar_3, self.tkvar_4, self.tkvar_5, self.tkvar_6, self.tkvar_7]
		self.tkvar_11 = StringVar()
		self.tkvar_21 = StringVar()
		self.tkvar_31 = StringVar()
		self.tkvar_41 = StringVar()
		self.tkvar_51 = StringVar()
		self.tkvar_61 = StringVar()
		self.tkvar_71 = StringVar()
		self.list_tkvar_mini2 = [self.tkvar_11, self.tkvar_21, self.tkvar_31, self.tkvar_41, self.tkvar_51, self.tkvar_61, self.tkvar_71]
		self.tkvar_12 = StringVar()
		self.tkvar_22 = StringVar()
		self.tkvar_32= StringVar()
		self.tkvar_42 = StringVar()
		self.tkvar_52 = StringVar()
		self.tkvar_62 = StringVar()
		self.tkvar_72 = StringVar()
		self.list_tkvar_mini3 = [self.tkvar_12, self.tkvar_22, self.tkvar_32, self.tkvar_42, self.tkvar_52, self.tkvar_62, self.tkvar_72]
		self.tkvar_13 = StringVar()
		self.tkvar_23 = StringVar()
		self.tkvar_33 = StringVar()
		self.tkvar_43 = StringVar()
		self.tkvar_53 = StringVar()
		self.tkvar_63 = StringVar()
		self.tkvar_73 = StringVar()
		self.list_tkvar_mini4 = [self.tkvar_13, self.tkvar_23, self.tkvar_33, self.tkvar_43, self.tkvar_53, self.tkvar_63, self.tkvar_73]
		self.tkvar_14 = StringVar()
		self.tkvar_24 = StringVar()
		self.tkvar_34 = StringVar()
		self.tkvar_44 = StringVar()
		self.tkvar_54 = StringVar()
		self.tkvar_64 = StringVar()
		self.tkvar_74 = StringVar()
		self.list_tkvar_mini5 = [self.tkvar_14, self.tkvar_24, self.tkvar_34, self.tkvar_44, self.tkvar_54, self.tkvar_64, self.tkvar_74]
		self.tkvar_15 = StringVar()
		self.tkvar_25 = StringVar()
		self.tkvar_35 = StringVar()
		self.tkvar_45 = StringVar()
		self.tkvar_55 = StringVar()
		self.tkvar_65 = StringVar()
		self.tkvar_75 = StringVar()
		self.list_tkvar_mini6 = [self.tkvar_15, self.tkvar_25, self.tkvar_35, self.tkvar_45, self.tkvar_55, self.tkvar_65, self.tkvar_75]
		self.tkvar_16 = StringVar()
		self.tkvar_26 = StringVar()
		self.tkvar_36 = StringVar()
		self.tkvar_46 = StringVar()
		self.tkvar_56 = StringVar()
		self.tkvar_66 = StringVar()
		self.tkvar_76 = StringVar()
		self.list_tkvar_mini7 = [self.tkvar_16, self.tkvar_26, self.tkvar_36, self.tkvar_46, self.tkvar_56, self.tkvar_66, self.tkvar_76]
		
		self.list_tkvar = [self.list_tkvar_mini1, self.list_tkvar_mini2, self.list_tkvar_mini3, self.list_tkvar_mini4, self.list_tkvar_mini5, self.list_tkvar_mini6, self.list_tkvar_mini7]
		
		self.frame_1 = Frame(self)
		self.frame_2 = Frame(self)
		self.frame_3 = Frame(self)
		self.frame_4 = Frame(self)
		self.frame_5 = Frame(self)
		self.frame_6 = Frame(self)
		self.frame_7 = Frame(self)
		self.list_frame = [self.frame_1, self.frame_2, self.frame_3, self.frame_4, self.frame_5, self.frame_6, self.frame_7]
		
		global dict_filter_compare
		dict_filter_compare = OrderedDict()
		
		count_filter_header = -1
		for it in list_filter:
			count_filter_header += 1
			dict_filter_compare[it] = list()
		
		self.count_frame = -1
		for it in list_filter:
			self.count_frame += 1
			self.list_frame[self.count_frame].pack(fill=BOTH)
				
			list_values = list(dict.fromkeys(list(my_dataframe[it])))
			ttk.Label(self.list_frame[self.count_frame], text = it, width=20).pack(side=LEFT, padx=5, pady=5)
			for it2 in list_values:
				ttk.Checkbutton(self.list_frame[self.count_frame], text=it2, variable=self.list_tkvar[list_filter.index(it)][list_values.index(it2)], command=lambda: self.chk_changed()).pack(side=LEFT, padx=5, pady=5)
		
		frame_typegraph = Frame(self)
		frame_typegraph.pack(fill=X, expand=True)
		self.tkvar = StringVar()
		
		global type_graph_compare
		try:
			self.tkvar.set(type_graph_compare)
		except NameError:
			self.tkvar.set('Line')
			type_graph_compare = 'Line'
		
		ttk.Combobox(frame_typegraph, textvariable=self.tkvar, values = ['Line', 'Bar'], state="readonly").pack(side=RIGHT, padx=5, pady=5)
		ttk.Label(frame_typegraph, text = 'Type of graph', width=20).pack(side=RIGHT)
		self.tkvar.trace('w',self.callback2)
		
		frame3 = Frame(self)
		frame3.pack(fill=X, expand=True)
		ttk.Label(frame3, text = 'xLabel', width=10).pack(side=LEFT, padx=5, pady=5)
		self.entry_xlabel_compare = StringVar()
		Entry(frame3, textvariable=self.entry_xlabel_compare, width=70).pack(side=LEFT, padx=5, pady=5)
		
		frame4 = Frame(self)
		frame4.pack(fill=X, expand=True)
		ttk.Label(frame4, text = 'yLabel', width=10).pack(side=LEFT, padx=5, pady=5)
		self.entry_ylabel_compare = StringVar()
		Entry(frame4, textvariable=self.entry_ylabel_compare, width=70).pack(side=LEFT, padx=5, pady=5)		
		
		frame_button = Frame(self)
		frame_button.pack(fill=BOTH)
		closeButton = Button(frame_button, text="Exit", command=self.quit)
		closeButton.pack(side=RIGHT, padx=5, pady=5)
		button1 = Button(frame_button, text='Create graph', # likewise PageTwo
                            command=self.plot)
		button1.pack(side=RIGHT)
		button2 = Button(frame_button, text='Back', # likewise StartPage
                            command=lambda : controller.show_frame('PageTwo'))
		button2.pack(side=RIGHT, padx=5, pady=5)
	
	def callback2(self, *args):
		global type_graph_compare
		type_graph_compare = self.tkvar.get()
	
	def chk_changed(self):
	
		global list_compare
		list_compare = list()
		list_compare_tmp_1 = list()
		list_compare_tmp_2 = list()
		for it in list_filter:
			list_compare_tmp_1 = list()
			for it2 in range(0, len(list(dict.fromkeys(list(my_dataframe[it]))))):
				list_compare_tmp_1.append(self.list_tkvar[list_filter.index(it)][it2].get())
			dict_tmp = dict(zip(list(dict.fromkeys(list(my_dataframe[it]))), list_compare_tmp_1))
			list_tmp = list()
			for it_tmp in dict_tmp:
				if dict_tmp[it_tmp] == '1':
					list_tmp.append(it_tmp)
			dict_filter_compare[it] = list_tmp
		
		return
	
	def plot(self):
	
		my_dataframe_copy = my_dataframe.copy(deep = True)
		for it in dict_filter_compare:
			if len(dict_filter_compare[it]) == 1:
				my_dataframe_copy = my_dataframe_copy[my_dataframe_copy[it] == dict_filter_compare[it][0]]
	
		color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
						  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
						  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
						  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
		if type_graph_compare == 'Line':
			for it1 in dict_filter_compare:
				#fig, axs = plt.subplots(2, 3, figsize=(12, 9))
				if len(dict_filter_compare[it1]) > 1:
					fig, axs = plt.subplots(1, len(dict_filter_compare[it1]), figsize=(12, 9))
					
					for itt in range(0, len(dict_filter_compare[it1])):
						#axs[itt].spines['top'].set_visible(False)
						#axs[itt].spines['bottom'].set_visible(False)
						#axs[itt].spines['right'].set_visible(False)
						#axs[itt].spines['left'].set_visible(False)

						axs[itt].get_xaxis().tick_bottom()
						axs[itt].get_yaxis().tick_left()
						#Calculate lim of y_axis
						all_data = list(my_dataframe_copy[list_data].values)
						for it_all in all_data:
							for its in it_all:
								y_min = its
								y_max = its
								break
						for it_alls in all_data:
							for itss in it_alls:
								if itss < y_min:
									y_min = itss
								if itss > y_max:
									y_max = itss
						axs[itt].set_ylim(y_min - 1, y_max + 1)
						
					fig.subplots_adjust(left=0.085, right=0.95, bottom=0.1, top=0.85)
					
					ind = np.arange(len(list_data))
					plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
					plt.tick_params(axis='both', which='both', bottom=False, top=False,
									labelbottom=True, left=False, right=False, labelleft=True)
					def isListEmpty(inList):
						if isinstance(inList, list):    # Is a list
							return all( map(isListEmpty, inList) )
						return False # Not a list
					count_plot = -1
					for it2 in dict_filter_compare[it1]:
						count_plot += 1
						majors_tmp = my_dataframe_copy[my_dataframe_copy[it1] == it2]
						majors = list(majors_tmp[list_info].values)
						list_tmp = list(majors_tmp[list_data].values)
						if not isListEmpty(list_tmp):
							for rank, column in enumerate(majors):
								column_rec_name = column[0]
								axs[count_plot].plot(ind,
												list_tmp[rank],
												lw=2.5,
												color=color_sequence[rank],
												label=column_rec_name)
								axs[count_plot].set_xticks(ind)
								axs[count_plot].set_xticklabels(list_data, rotation=45)
								axs[count_plot].legend()
								axs[count_plot].set_title(it2)	
								axs[count_plot].set_ylabel(self.entry_ylabel_compare.get())
								axs[count_plot].set_xlabel(self.entry_xlabel_compare.get())
						else:
							axs[count_plot].set_xticks(ind)
							axs[count_plot].set_xticklabels(list_data, rotation=45)
							axs[count_plot].set_title(it2)
							axs[count_plot].set_ylabel(self.entry_ylabel_compare.get())
							axs[count_plot].set_xlabel(self.entry_xlabel_compare.get())
							
			plt.show()
			
		elif type_graph_compare == 'Bar':
			for it1 in dict_filter_compare:
				#fig, axs = plt.subplots(2, 3, figsize=(12, 9))
				if len(dict_filter_compare[it1]) > 1:
					fig, axs = plt.subplots(1, len(dict_filter_compare[it1]), figsize=(12, 9))
					
					for itt in range(0, len(dict_filter_compare[it1])):
						#axs[itt].spines['top'].set_visible(False)
						#axs[itt].spines['bottom'].set_visible(False)
						#axs[itt].spines['right'].set_visible(False)
						#axs[itt].spines['left'].set_visible(False)

						axs[itt].get_xaxis().tick_bottom()
						axs[itt].get_yaxis().tick_left()
						#Calculate lim of y_axis
						all_data = list(my_dataframe_copy[list_data].values)
						for it_all in all_data:
							for its in it_all:
								y_min = its
								y_max = its
								break
						for it_alls in all_data:
							for itss in it_alls:
								if itss < y_min:
									y_min = itss
								if itss > y_max:
									y_max = itss
						axs[itt].set_ylim(y_min - 1, y_max + 1)
						
					fig.subplots_adjust(left=0.085, right=0.95, bottom=0.1, top=0.85)
					plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
					plt.tick_params(axis='both', which='both', bottom=False, top=False,
									labelbottom=True, left=False, right=False, labelleft=True)
					
					count_plot = -1
					for it2 in dict_filter_compare[it1]:
						count_plot += 1
						majors_tmp = my_dataframe_copy[my_dataframe_copy[it1] == it2]
						majors = list_data
						list_y_bar = list()
						for it3 in list_data:
							list_y_bar.append(list(majors_tmp[it3].values))
						
						def autolabel(rects, xpos='center'):
							"""
							Attach a text label above each bar in *rects*, displaying its height.

							*xpos* indicates which side to place the text w.r.t. the center of
							the bar. It can be one of the following {'center', 'right', 'left'}.
							"""

							xpos = xpos.lower()  # normalize the case of the parameter
							ha = {'center': 'center', 'right': 'left', 'left': 'right'}
							offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

							for rect in rects:
								height = rect.get_height()
								axs[count_plot].text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
										'{}'.format(height), ha=ha[xpos], va='bottom')
						
						def isListEmpty(inList):
							if isinstance(inList, list):    # Is a list
								return all( map(isListEmpty, inList) )
							return False # Not a list
						
						if not isListEmpty(list_y_bar):
							ind = np.arange(len(list_y_bar[0]))
							width = (1-0.1)/len(list_data)
							number_bar_tmp = len(list_data)
							if number_bar_tmp % 2 == 0:
								number_bar_tmp = -(number_bar_tmp - 1)
								for rank, column in enumerate(majors):
									column_rec_name = column
									rects = axs[count_plot].bar(ind + ((width/2)*number_bar_tmp), list_y_bar[rank], width, color=color_sequence[rank], label=column_rec_name)
									autolabel(rects, 'center')
									number_bar_tmp += 2
									axs[count_plot].set_xticks(ind)
									axs[count_plot].set_xticklabels(list(majors_tmp[list_info[0]].values), rotation=45)
									axs[count_plot].legend()
									axs[count_plot].set_title(it2)
									axs[count_plot].set_ylabel(self.entry_ylabel_compare.get())
									axs[count_plot].set_xlabel(self.entry_xlabel_compare.get())

							else:
								number_bar_tmp = -(number_bar_tmp - 3)
								for rank, column in enumerate(majors):
									column_rec_name = column
									rects = axs[count_plot].bar(ind + (width*number_bar_tmp), list_y_bar[rank], width, color=color_sequence[rank], label=column_rec_name)
									autolabel(rects, 'center')
									number_bar_tmp += 1
									axs[count_plot].set_xticks(ind)
									axs[count_plot].set_xticklabels(list(majors_tmp[list_info[0]].values), rotation=45)
									axs[count_plot].legend()
									axs[count_plot].set_title(it2)
									axs[count_plot].set_ylabel(self.entry_ylabel_compare.get())
									axs[count_plot].set_xlabel(self.entry_xlabel_compare.get())
						else:
							axs[count_plot].set_title(it2)
							axs[count_plot].set_ylabel(self.entry_ylabel_compare.get())
							axs[count_plot].set_xlabel(self.entry_xlabel_compare.get())
							
			plt.show()
	
			
		


def shutdown_ttk_repeat():
    app.eval('::ttk::CancelRepeat')
    app.destroy()
		
if __name__ == '__main__':
	path_file = list()
	
	list_header = list()
	list_info = list()
	list_filter = list()
	list_data = list()
	list_info_order = list()
	list_filter_order = list()
	list_data_order = list()
	
	app = MainWindow()
	app.protocol("WM_DELETE_WINDOW", shutdown_ttk_repeat)
	app.mainloop()
