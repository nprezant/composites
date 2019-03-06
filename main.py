
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

        # bottom buttoms
        self.bottom_frame = tk.Frame(self.master)
        self.new_btn = tk.Button(self.bottom_frame, text='+New', command=self.table.add_row)
        self.new_btn.grid(row=0, column=1, sticky='w')

        # overall layout
        self.table.grid(row=0, column=0, sticky='we')
        self.bottom_frame.grid(row=2, column=0, sticky='we')

        # popup menu
        menu_commands = {
            'Add layer': self.table.add_row,
        }
        self.popup_menu = RightClick(self.table, **menu_commands)



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
        for _ in range(count):
            new_row = self._make_row()
            self._widgets.append(new_row)
        self._re_order_widgets()


    def add_header_row(self, headers=None):
        '''Adds the header row to the top of the table'''
        if headers is None:
            headers = ['' for x in self._columns]
        new_row = self._make_header_row(headers)
        self._widgets.insert(0, new_row)
        self._re_order_widgets()


    def _make_row(self):
        '''Makes an empty row for the table.
        Doesn't put it anywhere'''
        current_row = []

        check_box = tk.Checkbutton(self)
        current_row.append(check_box)

        for _ in range(self._columns):
            entry = tk.Entry(self, textvariable=tk.StringVar(), borderwidth=0, width=10)
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
                cell.grid(row=row, column=column, sticky='nsew', padx=1, pady=1)
                self.grid_columnconfigure(column, weight=1)        


class RightClick:
    '''A right click popup menu'''
    def __init__(self, master, **kwargs):

        # create a popup menu
        self.aMenu = tk.Menu(master, tearoff=0)
        self.aMenu.add_command(label='Say Hello', command=self.hello)

        for label, command in kwargs.items():
            self.aMenu.add_command(label=label, command=command)


    def hello(self):
        print('hello!')


    def popup(self, event):
        self.aMenu.post(event.x_root, event.y_root)


root = tk.Tk()
root.title('Laminate Maker')

for x in range(1):
    root.columnconfigure(x, weight=1)
for x in range(1):
    root.rowconfigure(x, weight=1)
root.minsize(1, 1)

app = LaminateMaker(master=root)
app.mainloop()