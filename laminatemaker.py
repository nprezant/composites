
from pathlib import Path

import tkinter as tk
from tkinter import filedialog

from entrytable import EntryTable
from materialeditor import ABDInputFrame
from abd import calculate_ABD


class LaminateMaker(tk.Frame):
    '''GUI to make the laminates'''
    def __init__(self, master=None):
        super().__init__(master)
        self.initialize_ui()


    def initialize_ui(self):
        '''Initialize the user interface'''
        self.master.title('Laminate Maker')

        # table
        headers = ['Layer', 'Orientation', 'Thickness', 'Material']
        self.table = EntryTable(self.master, headers=headers, rows=4)

        # bottom frame
        self.bottom_frame = tk.Frame(self.master)
        self.status_bar = tk.Label(self.bottom_frame, text='OK')
        self.status_bar.grid(row=0, column=1, sticky='w')

        # overall layout
        self.table.grid(row=0, column=0, sticky='nwe')
        self.bottom_frame.grid(row=1, column=0, sticky='we')

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.minsize(1, 1)

        # top-level menu
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # file pulldown
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Open', command=self.open_dialog)
        filemenu.add_command(label='Save', command=self.save)
        filemenu.add_command(label='Save As', command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=self.close_event, accelerator='Ctrl+W')
        menubar.add_cascade(label='File', menu=filemenu)

        # layers pulldown
        layersmenu = tk.Menu(menubar, tearoff=0)
        layersmenu.add_command(label='Add layer', command=self.table.add_row)
        layersmenu.add_command(label='Delete Selected', command=self.table.delete_selected_rows)
        layersmenu.add_command(label='Copy Selected', command=self.table.copy_selected_rows)
        layersmenu.add_command(label='Mirror Selected', command=self.table.mirror_selected_rows, accelerator='Alt+M')
        menubar.add_cascade(label='Layers', menu=layersmenu)

        # view ABD button
        menubar.add_command(label='View ABD', command=self.view_abd)

        # popup menu
        rclick = tk.Menu(self.master, tearoff=0)
        rclick.add_command(label='Add layer', command=self.table.add_row)
        rclick.add_command(label='Delete layers', command=self.table.delete_selected_rows)
        rclick.add_command(label='Copy layers', command=self.table.copy_selected_rows)
        rclick.add_command(label='Mirror layers', command=self.table.mirror_selected_rows)
        rclick.add_command(label='Select All', command=self.table.select_all)

        def popup(event):
            rclick.post(event.x_root, event.y_root)

        # button bindings
        self.bind_all('<Button-3>', popup)

        # keypress bindings
        self.bind_all('<Control-KeyRelease-a>', self.table.select_all)
        self.bind_all('<Control-KeyRelease-w>', self.close_event)
        self.bind_all('<Control-KeyRelease-s>', self.save)
        self.bind_all('<Control-KeyRelease-o>', self.open_dialog)
        self.bind_all('<Alt-KeyRelease-m>', self.table.mirror_selected_rows)


    def view_abd(self, event=None):
        '''Computes ABD matrix and shows it'''
        try:
            path = self._save_path
            if path is None:
                raise ValueError
        except:
            self.save_as()

        path = Path(path)

        A, B, D = calculate_ABD(
            lam_file=path.parts[-1], 
            lam_dir=str(path.parent) + '\\', 
            mat_dir=str(path.parent) + '\\'
        )
        t = tk.Toplevel(self)
        abd = ABDInputFrame(t)
        abd.display_mode = True
        abd.a_frame.A = A
        abd.b_frame.B = B
        abd.d_frame.D = D
        abd.grid()


    def close_event(self, event=None):
        self.quit()


    def open_dialog(self, event=None):
        '''Opens a file from user dialog'''
        filename = filedialog.askopenfilename(
            title = 'Select file to open',
            filetypes = (
                ('csv files', '*.csv'),
                ('text files','*.txt'),
                ('all files','*.*')))
        if filename == '':
            return
        else:
            self.open(filename)


    def open(self, filename):
        '''Opens `filename` file'''
        try:
            self.table.import_data(filename)
        except:
            print(f'error opening file: {filename}')
        else:
            self._save_path = filename


    def save(self, event=None):
        '''Save the file to the already saved path'''
        try:
            path = self._save_path
            if path is None:
                raise ValueError
        except:
            self.save_as()
        else:
            self.table.export_data(path)


    def save_as(self):
        '''Saves self with user dialog'''
        filename = filedialog.asksaveasfilename(
            title = 'Save file as',
            filetypes = (
                ('csv files', '*.csv'),
                ('text files','*.txt'),
                ('all files','*.*')))
        if filename == '':
            return
        else:
            self.table.export_data(filename)
            self._save_path = filename


if __name__ == '__main__':
    root = tk.Tk()
    app = LaminateMaker(master=root)
    app.mainloop()