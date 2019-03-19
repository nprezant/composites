# explores the  composites and does stuff with them

import os
from pathlib import Path

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from materialeditor import MaterialEditor
from laminatemaker import LaminateMaker

class Explorer(tk.Frame):
    '''GUI to make the laminates'''
    def __init__(self, master=None):
        super().__init__(master)
        self.initialize_ui()


    def initialize_ui(self):
        '''Initialize the user interface'''
        self.master.title('Composites Explorer')

        # material title
        working_dir_frame = tk.Frame(self, borderwidth=1, relief='raised', pady=5)
        working_dir_label = tk.Label(working_dir_frame, text='Directory')
        txt = tk.StringVar()
        self.working_dir_entry = tk.Entry(working_dir_frame, textvariable=txt)
        self.working_dir_entry.text = txt
        self.working_dir_entry.text.set(r'C:\Users\Noah\Documents\Dev\composites')
        self.working_dir_entry.bind('<FocusOut>', self.re_draw)
        self.working_dir_entry.bind('<Return>', self.re_draw)

        working_dir_label.grid(row=0, column=0, sticky='w')
        self.working_dir_entry.grid(row=0, column=1, sticky='we')
        working_dir_frame.columnconfigure(1, weight=1)

        # make treeview
        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ('size', 'type')
        self.tree.column('#1', anchor='center')
        self.tree.column('#2', anchor='center')

        # make treeview headings
        self.tree.heading('#0', text='Name')
        self.tree.heading('size', text='Size')
        self.tree.heading('type', text='Type')

        # populate treeview files
        self.expand_selected_dir()

        # add events
        self.bind_all('<Control-KeyRelease-w>', self.close_event)
        self.tree.tag_bind('dir', '<Double-Button-1>', self.item_clicked)  
        self.tree.tag_bind('file', '<Double-Button-1>', self.item_clicked)  

        # configure tags
        self.tree.tag_configure('dir', background='#fff9a5')
        self.tree.tag_configure('file', background='#e0ecff')

        working_dir_frame.grid(sticky='nswe')
        self.tree.grid(sticky='nswe')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # top level menu
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # new pulldown
        newmenu = tk.Menu(menubar, tearoff=0)
        newmenu.add_command(label='New Material', command=self.new_material)
        newmenu.add_command(label='New Laminate', command=self.new_laminate)
        menubar.add_cascade(label='New', menu=newmenu)


    def close_event(self, event=None):
        self.quit()


    def new_material(self, event=None):
        '''Make a new material with a new form'''
        t = tk.Toplevel(self)
        mat = MaterialEditor(t)
        mat.grid()


    def new_laminate(self, event=None):
        '''Make a new laminate with a form'''
        t = tk.Toplevel(self)
        lam = LaminateMaker(t)
        lam.grid()


    def re_draw(self, event=None):
        '''Re draws the files based on the address bar'''
        self.tree.delete(*self.tree.get_children())
        self.expand_selected_dir()


    def make_path(self, node):
        '''Returns a path made from the selected node'''
        root = Path(self.working_dir_entry.text.get())

        tip = Path()
        while not node == '':
            txt = self.tree.item(node)['text']
            tip = txt / tip
            node = self.tree.parent(node)

        path = root / Path(tip)
        return path


    def item_clicked(self, event=None):
        '''Event for when item is clicked'''
        selected = self.tree.focus()
        path = self.make_path(selected)

        if path.is_dir():
            self.expand_selected_dir()
        elif path.is_file():
            print(f'opening file: {path}')
            self.open_file(path)


    def open_file(self, path):
        '''Opens the file provided at `path`
        Chooses editor based on extension.'''
        if path.suffix == '.json':
            self.open_material(path)
        elif path.suffix == '.csv':
            self.open_laminate(path)


    def open_material(self, path):
        '''Opens the material file provided at `path`
        Opens with the material editor.'''
        t = tk.Toplevel(self)
        mat = MaterialEditor(t)
        try:
            mat.open(path)
        except:
            print('error opening file')
        else:
            mat.grid()


    def open_laminate(self, path):
        '''Opens the laminate file provided at `path`
        Opens with the laminate editor.'''
        t = tk.Toplevel(self)
        lam = LaminateMaker(t)
        try:
            lam.open(path)
        except:
            print('error opening file')
        else:
            lam.grid()


    def expand_selected_dir(self):
        '''Expands the parent node directory'''
        selected = self.tree.focus()
        path = self.make_path(selected)

        for _, dirs, files in os.walk(path):
            for d in dirs:
                self.add_dir_node(d, selected)
            for f in files:
                self.add_file_node(f, selected)
            break

    
    def add_dir_node(self, dirname, parent):
        '''Adds a directory node to the tree'''
        self.tree.insert(parent, 'end', text=dirname, tags=('dir'))


    def add_file_node(self, filename, parent):
        '''Adds a file node to the tree'''
        id_ = self.tree.insert(parent, 'end', text=filename, tags=('file'))
        path = self.make_path(id_)
        size = path.stat().st_size / 1000
        suffix = path.suffix
        self.tree.set(id_, 'size', '{:.0f} Kb'.format(size))
        self.tree.set(id_, 'type', suffix)
        

if __name__ == '__main__':
    root = tk.Tk()
    app = Explorer(master=root)
    app.grid(sticky='nsew')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app.mainloop()