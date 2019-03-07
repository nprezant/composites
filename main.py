
import tkinter as tk

from entrytable import EntryTable


class LaminateMaker(tk.Frame):
    '''GUI to make the laminates'''
    def __init__(self, master=None):
        super().__init__(master)
        self.initialize_ui()


    def initialize_ui(self):
        '''Initialize the user interface'''
        # table
        headers = ['Layer', 'Orientation', 'Thickness', 'Material']
        self.table = EntryTable(self.master, headers=headers, rows=4)

        # bottom frame
        self.bottom_frame = tk.Frame(self.master)
        self.status_bar = tk.Label(self.bottom_frame, text='OK')
        self.status_bar.grid(row=0, column=1, sticky='w')

        # overall layout
        self.table.grid(row=0, column=0, sticky='nwe')
        self.bottom_frame.grid(row=2, column=0, sticky='we')

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
        layersmenu.add_command(label='Add', command=self.table.add_row, accelerator='Alt+A')
        layersmenu.add_command(label='Delete', command=self.table.delete_selected_rows, accelerator='Alt+D')
        layersmenu.add_command(label='Copy', command=self.table.copy_selected_rows, accelerator='Alt+C')
        layersmenu.add_command(label='Mirror', command=self.table.mirror_selected_rows, accelerator='Alt+M')
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
        self.bind_all('<Alt-KeyRelease-a>', self.table.add_row)
        self.bind_all('<Alt-KeyRelease-d>', self.table.delete_selected_rows)
        self.bind_all('<Alt-KeyRelease-c>', self.table.copy_selected_rows)
        self.bind_all('<Alt-KeyRelease-m>', self.table.mirror_selected_rows)


    def close_event(self, event):
        self.master.quit()


root = tk.Tk()
root.title('Laminate Maker')

for x in range(1):
    root.columnconfigure(x, weight=1)
for x in range(1):
    root.rowconfigure(x, weight=1)
root.minsize(1, 1)

app = LaminateMaker(master=root)
app.mainloop()