
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
        self.table = EntryTable(self.master, headers=headers, rows=10, columns=4)

        # bottom frame
        self.bottom_frame = tk.Frame(self.master)
        self.status_bar = tk.Label(self.bottom_frame, text='OK')
        self.status_bar.grid(row=0, column=1, sticky='w')

        # overall layout
        self.table.grid(row=0, column=0, sticky='nwe')
        self.bottom_frame.grid(row=2, column=0, sticky='we')

        # top-level menu
        menubar = tk.Menu(self.master)
        menubar.add_command(label='New', command=self.table.add_row)
        menubar.add_command(label='Delete', command=self.table.delete_selected_rows)
        menubar.add_command(label='Copy', command=self.table.copy_selected_rows)
        menubar.add_command(label='Mirror', command=self.table.mirror_selected_rows)
        menubar.add_command(label='Export', command=self.table.export_data)
        menubar.add_command(label='Import', command=self.table.import_data)
        menubar.add_command(label='Quit!', command=self.close_event)
        self.master.config(menu=menubar)

        # popup menu
        rclick = tk.Menu(self.master, tearoff=0)
        rclick.add_command(label='New layer', command=self.table.add_row)
        rclick.add_command(label='Delete layers', command=self.table.delete_selected_rows)
        rclick.add_command(label='Copy layers', command=self.table.copy_selected_rows)
        rclick.add_command(label='Select All', command=self.table.select_all)

        def popup(event):
            rclick.post(event.x_root, event.y_root)

        # button bindings
        self.master.bind('<Button-3>', popup)

        # keypress bindings
        self.master.bind('<Control-KeyRelease-a>', self.table.select_all)
        self.master.bind('<Control-KeyRelease-w>', self.close_event)


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