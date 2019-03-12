
import tkinter as tk

from entrytable import EntryTable


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

        # file pulldown
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Import', command=self.table.import_data)
        filemenu.add_command(label='Export', command=self.table.export_data)
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
        self.master.config(menu=menubar)

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
        self.bind_all('<Alt-KeyRelease-m>', self.table.mirror_selected_rows)


    def close_event(self, event):
        self.master.quit()


if __name__ == '__main__':
    root = tk.Tk()
    app = LaminateMaker(master=root)
    app.mainloop()