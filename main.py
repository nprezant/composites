
import tkinter as tk

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
        menubar.add_command(label='New Layer', command=self.table.add_row)
        menubar.add_command(label='Quit!', command=self.master.quit)
        self.master.config(menu=menubar)

        # popup menu
        rclick = tk.Menu(self.master, tearoff=0)
        rclick.add_command(label='Add layer', command=self.table.add_row)
        rclick.add_command(label='Delete layers', command=self.table.delete_selected_rows)
        rclick.add_command(label='Copy layer', command=self.table.copy_selected_rows)

        def popup(event):
            rclick.post(event.x_root, event.y_root)

        self.master.bind('<Button-3>', popup)


class EntryTable(tk.Frame):
    '''Writable table of entries using tk grid'''

    def __init__(self, parent, headers=None, rows=10, columns=2):
        '''Initialize the table'''
        super().__init__(parent)
        self._widgets = []
        self._columns = columns
        self.add_header_row(headers)
        self.add_row(count=rows)


    def insert_row(self, row, count=1):
        '''Inserts an empty row at the specified `row`'''
        for _ in range(count):
            new_row = self._make_row()
            self._widgets.insert(row, new_row)
        self._re_order_widgets()


    def add_row(self, count=1):
        '''Adds an empty row (or rows) to the bottom of the table'''
        self.insert_row(len(self._widgets), count)


    def copy(self, row):
        '''Copies the row index provided and inserts it below'''
        self.insert_row(row+1)
        for j, cell in enumerate(self._widgets[row][1:]):
            cell.text.set(self._widgets[row+1][j+1].text.get())


    def add_header_row(self, headers=None):
        '''Adds the header row to the top of the table'''
        if headers is None:
            headers = ['' for x in self._columns]
        new_row = self._make_header_row(headers)
        self._widgets.insert(0, new_row)
        self._re_order_widgets()


    def selected_rows(self):
        '''Generator for the selected rows'''
        for row, widget in enumerate(self._widgets[1:]):
            if widget[0].var.get() == 1:
                yield row, widget


    def delete_selected_rows(self):
        '''Deletes the selected rows'''
        for _, widget in self.selected_rows():
            [cell.grid_forget() for cell in widget]
            self._widgets.remove(widget)
        self._re_order_widgets()


    def copy_selected_rows(self):
        '''Copies the selected rows'''
        for i, _ in self.selected_rows():
            print(f'copy row {i}')
            if not i == 0:
                self.copy(i)
        self._re_order_widgets()


    def _make_row(self):
        '''Makes an empty row for the table.
        Doesn't put it anywhere'''
        current_row = []

        v = tk.IntVar()
        c = tk.Checkbutton(
            self, variable=v)
        c.var = v
        current_row.append(c)

        for _ in range(self._columns):
            txt = tk.StringVar()
            entry = tk.Entry(self, textvariable=txt, justify=tk.CENTER, borderwidth=0, width=10)
            entry.text = txt
            current_row.append(entry)
        return current_row


    def _make_header_row(self, headers):
        '''Makes the header row for the table.
        Doesn't put it anywhere'''
        current_row = []

        label = tk.Label(self, borderwidth=0, width=10)
        current_row.append(label)

        for header in headers:
            label = tk.Label(self, text=header, borderwidth=0, width=10)
            current_row.append(label)
        return current_row


    def _re_order_widgets(self):
        '''Re numbers the widget grid locations based on the list order'''
        for row, widget in enumerate(self._widgets):
            for column, cell in enumerate(widget):

                # update the layer count
                if column == 1:
                    if hasattr(cell, 'text'):
                        cell.text.set(str(row))

                cell.grid(row=row, column=column, sticky='nsew', padx=1, pady=1)
                self.grid_columnconfigure(column, weight=1)        


root = tk.Tk()
root.title('Laminate Maker')

for x in range(1):
    root.columnconfigure(x, weight=1)
for x in range(1):
    root.rowconfigure(x, weight=1)
root.minsize(1, 1)

app = LaminateMaker(master=root)
app.mainloop()