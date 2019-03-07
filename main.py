
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
        menubar.add_command(label='New', command=self.table.add_row)
        menubar.add_command(label='Delete', command=self.table.delete_selected_rows)
        menubar.add_command(label='Copy', command=self.table.copy_selected_rows)
        menubar.add_command(label='Mirror', command=self.table.mirror_selected_rows)
        menubar.add_command(label='Quit!', command=self.master.quit)
        self.master.config(menu=menubar)

        # popup menu
        rclick = tk.Menu(self.master, tearoff=0)
        rclick.add_command(label='New layer', command=self.table.add_row)
        rclick.add_command(label='Delete layers', command=self.table.delete_selected_rows)
        rclick.add_command(label='Copy layers', command=self.table.copy_selected_rows)
        rclick.add_command(label='Select All', command=self.table.select_all)

        def popup(event):
            rclick.post(event.x_root, event.y_root)

        self.master.bind('<Button-3>', popup)


class EntryTable(tk.Frame):
    '''Writable table of entries using tk grid'''

    def __init__(self, parent, headers=None, rows=10, columns=2):
        '''Initialize the table'''
        super().__init__(parent)
        self._table = []
        self._columns = columns
        self.add_header_row(headers)
        self.add_row(count=rows)

        self.bind('<Control-KeyRelease-a>', self.select_all)
        self.bind('<Control-a>', self.select_all)
        self.bind('<Control_L>', self.select_all)


    @property
    def _table_body(self):
        '''Property for the body of the table'''
        return self._table[1:]
    
    
    @property
    def _table_header(self):
        '''Property for the header of the table'''
        return self._table[0]


    def insert_row(self, row, count=1):
        '''Inserts an empty row at the specified `row`'''
        for _ in range(count):
            new_row = self._make_row()
            self._table.insert(row, new_row)
        self._re_order_widgets()


    def add_row(self, count=1):
        '''Adds an empty row (or rows) to the bottom of the table'''
        self.insert_row(len(self._table), count)


    def copy_row(self, row):
        '''Copies the row index provided and returns it'''
        self.add_row()
        old_row = row
        new_row = self._table.pop()
        for x, cell in enumerate(new_row[1:]):
            cell.text.set(old_row[x+1].text.get())
        return new_row


    def add_header_row(self, headers=None):
        '''Adds the header row to the top of the table'''
        if headers is None:
            headers = ['' for x in self._columns]
        new_row = self._make_header_row(headers)
        self._table.insert(0, new_row)
        self._re_order_widgets()


    def selected_rows(self):
        '''Generator for the selected rows'''
        for row, widget in enumerate(self._table[1:]):
            if widget[0].var.get() == 1:
                yield row+1, widget


    def delete_selected_rows(self):
        '''Deletes the selected rows'''
        for _, widget in self.selected_rows():
            [cell.grid_forget() for cell in widget]
            self._table.remove(widget)
        self._re_order_widgets()


    def copy_selected_rows(self):
        '''Copies the selected rows, inserts them below the originals'''
        for i, row in self.selected_rows():
            if not i == 0:
                new_row = self.copy_row(row)
                self._table.insert(i+1, new_row)
        self._re_order_widgets()


    def mirror_selected_rows(self):
        '''Mirrors the selected rows about the bottom horizontal plane'''
        selected = [x for x, _ in self.selected_rows()]
        first_row = min(selected)
        last_row = max(selected)
        print(f'mirroring {first_row} to {last_row}')

        # make a list of copied rows between the first and last
        selected_copies = []
        for x in range(first_row, last_row+1):
            new_row = self.copy_row(self._table[x])
            selected_copies.append(new_row)

        # insert list (reversed) after the last selected row
        for cp in selected_copies:
            self._table.insert(last_row+1, cp)
        self._re_order_widgets()


    def _make_row(self):
        '''Makes an empty row for the table.
        Doesn't put it anywhere'''
        current_row = []

        v = tk.IntVar()
        cb = tk.Checkbutton(self, variable=v)
        cb.var = v
        cb.bind('<Button-1>', self._select_start)
        cb.bind('<Shift-Button-1>', self._select_range)
        current_row.append(cb)

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
        for row, widget in enumerate(self._table):
            for column, cell in enumerate(widget):

                # update the layer count
                if column == 1:
                    if hasattr(cell, 'text'):
                        cell.text.set(str(row))

                cell.lift()

                cell.grid(row=row, column=column, sticky='nsew', padx=1, pady=1)
                self.grid_columnconfigure(column, weight=1)


    def _select_start(self, event):
        '''mark this as the start of a range to select'''
        checkbuttons = [row[0] for row in self._table_body]
        self._start = checkbuttons.index(event.widget)
        checkbuttons.remove(event.widget)
        [cb.deselect() for cb in checkbuttons]

    
    def _select_range(self, event):
        '''select a whole range of check boxes'''
        checkbuttons = [row[0] for row in self._table_body]
        start = self._start
        end = checkbuttons.index(event.widget)
        sl = slice(min(start, end)+1, max(start, end))
        for cb in checkbuttons[sl]:
            cb.toggle()
        self._start = end


    def select_all(self, event=None):
        '''Select all check boxes
        if they are all already checked, uncheck them'''
        checkbuttons = [row[0] for row in self._table_body]
        checked = [cb for cb in checkbuttons if cb.var.get() == 1]
        if len(checked) == len(checkbuttons):
            [cb.deselect() for cb in checkbuttons]
        else:
            [cb.select() for cb in checkbuttons]


root = tk.Tk()
root.title('Laminate Maker')

for x in range(1):
    root.columnconfigure(x, weight=1)
for x in range(1):
    root.rowconfigure(x, weight=1)
root.minsize(1, 1)

app = LaminateMaker(master=root)
app.mainloop()