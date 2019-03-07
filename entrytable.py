
import tkinter as tk
from tkinter import filedialog


class EntryTable(tk.Frame):
    '''Writable table of entries using tk grid'''

    def __init__(self, parent, headers=None, rows=10, columns=2):
        '''Initialize the table'''
        super().__init__(parent)
        self._table = []

        if headers is None:
            self._columns = columns
        else:
            self._columns = len(headers)

        self.add_header_row(headers)
        self.add_row(count=rows)


    @property
    def _table_body(self):
        '''Property for the body of the table'''
        return self._table[1:]
    
    
    @property
    def _table_header(self):
        '''Property for the header of the table.
        Does not return button header'''
        return self._table[0][1:]


    @property
    def _table_data(self):
        '''Property for the data in the table
        (excludes first row and column)'''
        return [row[1:] for row in self._table_body]


    def insert_row(self, row, count=1):
        '''Inserts an empty row at the specified `row`'''
        for _ in range(count):
            new_row = self._make_row()
            self._table.insert(row, new_row)
        self.draw()


    def add_row(self, event=None, count=1):
        '''Adds an empty row (or rows) to the bottom of the table'''
        self.insert_row(len(self._table), count)


    def _add_row_event(self, event):
        '''Adds a row underneath the row where the event was called'''
        try:
            row_num, _ = self._find_position(event.widget)
        except:
            pass
        else:
            self.insert_row(row_num + 2)
            self._move_focus_down(event)
            self.draw()


    def copy_row(self, row):
        '''Copies the row provided and returns it'''
        self.add_row()
        old_row = row
        new_row = self._table.pop()
        for x, cell in enumerate(new_row[1:]):
            cell.text.set(old_row[x+1].text.get())
        return new_row


    def copy_row_up(self, event):
        '''Copies the current row and inserts it above'''
        try:
            row_num, _ = self._find_position(event.widget)
        except:
            pass
        else:
            row = self._table[row_num]
            cp = self.copy_row(row)
            self._table.insert(row_num + 0, cp)
            self.draw()
        

    def copy_row_down(self, event):
        '''Copies the current row and inserts it below'''
        try:
            row_num, _ = self._find_position(event.widget)
        except:
            pass
        else:
            row = self._table[row_num]
            cp = self.copy_row(row)
            self._table.insert(row_num + 1, cp)
            self.draw()

    def add_header_row(self, headers=None):
        '''Adds the header row to the top of the table'''
        if headers is None:
            headers = ['' for x in self._columns]
        new_row = self._make_header_row(headers)
        self._table.insert(0, new_row)
        self.draw()


    def data_iter(self):
        '''Generator for the data table'''
        for row in self._table_data:
            for cell in row:
                yield cell


    def selected_rows(self):
        '''Generator for the selected rows'''
        for row, widget in enumerate(self._table_body):
            if widget[0].var.get() == 1:
                yield row+1, widget


    def delete_selected_rows(self, event=None):
        '''Deletes the selected rows'''
        for _, widget in self.selected_rows():
            [cell.grid_forget() for cell in widget]
            self._table.remove(widget)
        self.draw()


    def _delete_event(self, event):
        '''Deletes the row of the widget this was called from
        First, shifts the focus down'''
        try:
            row_num, _ = self._find_position(event.widget)
        except:
            pass # cell doesn't exist anymore, leave it be
        else:
            if row_num == len(self._table_body) - 1:
                self._move_focus_up(event)
            else:
                self._move_focus_down(event)
            row = self._table[row_num + 1]
            [cell.grid_forget() for cell in row]
            self._table.remove(row)
            self.draw()


    def copy_selected_rows(self, event=None):
        '''Copies the selected rows, inserts them below the originals'''
        for i, row in self.selected_rows():
            if not i == 0:
                new_row = self.copy_row(row)
                self._table.insert(i+1, new_row)
        self.draw()


    def mirror_selected_rows(self, event=None):
        '''Mirrors the selected rows about the bottom horizontal plane'''
        selected = [x for x, _ in self.selected_rows()]
        if len(selected) == 0:
            selected = list(range(1, len(self._table_body) + 1))
        first_row = min(selected)
        last_row = max(selected)

        # make a list of copied rows between the first and last
        selected_copies = []
        for x in range(first_row, last_row+1):
            new_row = self.copy_row(self._table[x])
            selected_copies.append(new_row)

        # insert list (reversed) after the last selected row
        for cp in selected_copies:
            self._table.insert(last_row+1, cp)
        self.draw()


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
            entry.bind('<FocusOut>', self._recolor_focusout_event)
            entry.bind('<Return>', self._move_focus_down)
            entry.bind('<Shift-Return>', self._move_focus_up)
            entry.bind('<Alt-Down>', self._move_row_down)
            entry.bind('<Alt-Up>', self._move_row_up)
            entry.bind('<Up>', self._move_focus_up)
            entry.bind('<Down>', self._move_focus_down)
            entry.bind('<Left>', self._move_focus_left)
            entry.bind('<Right>', self._move_focus_right)
            entry.bind('<Alt-d>', self._delete_event)
            entry.bind('<Alt-a>', self._add_row_event)
            entry.bind('<Alt-Shift-Up>', self.copy_row_up)
            entry.bind('<Alt-Shift-Down>', self.copy_row_down)
            current_row.append(entry)
        return current_row


    def _make_header_row(self, headers):
        '''Makes the header row for the table.
        Doesn't put it anywhere'''
        current_row = []

        label = tk.Label(self, borderwidth=0, width=10)
        current_row.append(label)

        for header in headers:
            txt = tk.StringVar()
            txt.set(header)
            label = tk.Label(self, textvariable=txt, borderwidth=0, width=10)
            label.text = txt
            current_row.append(label)
        return current_row


    def _recolor(self, row, color):
        '''Re colors a row of the table'''
        for cell in row:
            try:
                cell.config({'background': color})
            except:
                cell.config({'background': 'White'})


    def _recolor_focusout_event(self, event):
        '''Recolors the row when user focuses out of a widget'''
        orientation_col =  1 # self._table_header.index('Orientation')
        try:
            row_num, col_num = self._find_position(event.widget)
        except:
            # data was likely imported
            return
        else:
            if col_num == orientation_col:
                row = self._table_body[row_num]
                color = map_color(event.widget.text.get())
                self._recolor(row, color)


    def _find_position(self, cell):
        '''Find the position (row, column_num) of a CELL in the table'''
        for row_num, row in enumerate(self._table_data):
            try:
                column_num = row.index(cell)
            except:
                continue
            else:
                return row_num, column_num
        raise ValueError('cell not found')


    def _move_focus_down(self, event):
        '''Moves the focus down a cell in the table'''
        row_num, col_num = self._find_position(event.widget)
        try:
            new_cell = self._table_data[row_num + 1][col_num]
        except:
            pass
        else:
            new_cell.focus()


    def _move_focus_up(self, event):
        '''Moves the focus up a cell in the table'''
        row_num, col_num = self._find_position(event.widget)
        try:
            new_cell = self._table_data[row_num - 1][col_num]
        except:
            pass
        else:
            new_cell.focus()


    def _move_focus_left(self, event):
        '''Moves the focus down a cell in the table'''
        row_num, col_num = self._find_position(event.widget)
        try:
            new_cell = self._table_data[row_num][col_num - 1]
        except:
            pass
        else:
            new_cell.focus()


    def _move_focus_right(self, event):
        '''Moves the focus down a cell in the table'''
        row_num, col_num = self._find_position(event.widget)
        try:
            new_cell = self._table_data[row_num][col_num + 1]
        except:
            pass
        else:
            new_cell.focus()


    def _move_row_down(self, event):
        '''moves a row down one in the table'''
        row_num, _ = self._find_position(event.widget)
        moved_row = self._table.pop(row_num + 1)
        self._table.insert(row_num + 2, moved_row)
        self.draw()


    def _move_row_up(self, event):
        '''moves a row down one in the table'''
        row_num, _ = self._find_position(event.widget)
        moved_row = self._table.pop(row_num + 1)
        if row_num == 0:
            row_num = 1
        self._table.insert(row_num + 0, moved_row)
        self.draw()


    def draw(self):
        '''Re-draws the table'''
        self._re_order_rows()
        self._recolor_all()


    def _recolor_all(self):
        '''Re-colors all rows'''
        for row in self._table_body:
            color = map_color(row[2].text.get())
            self._recolor(row, color)


    def _re_order_rows(self):
        '''Re numbers the widget grid locations based on the list order'''
        for row, widget in enumerate(self._table):
            for column, cell in enumerate(widget):

                # update the layer number for that column
                if column == 1 and not row == 0:
                    cell.text.set(str(row))

                cell.lift()

                cell.grid(row=row, column=column, sticky='nsew', padx=1, pady=1)
                self.grid_columnconfigure(column, weight=1)
            self.grid_columnconfigure(0, weight=0)


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


    def export_data(self, event=None):
        '''Export the data for this laminate'''
        filename = filedialog.asksaveasfilename(
            title = 'Save file as',
            filetypes = (
                ('text files','*.txt'),
                ('csv files', '*.csv'),
                ('all files','*.*')))
        if filename == '': return
        with open(filename, 'w') as f:
            for cell in self._table_header:
                f.write('{:8},'.format(cell.text.get()))
            f.write('\n')

            for row in self._table_data:
                for cell in row:
                    f.write('{:8},'.format(cell.text.get()))
                f.write('\n')


    def import_data(self, event=None):
        '''Import the data for a laminate'''
        filename = filedialog.askopenfilename(
            title = 'Select file to open',
            filetypes = (
                ('text files','*.txt'),
                ('csv files', '*.csv'),
                ('all files','*.*')))
        if filename == '': return
        self.select_all()
        self.delete_selected_rows()
        with open(filename, 'r') as f:
            for _ in range(1):
                next(f)
            for row, line in enumerate(f):
                self.add_row()
                vals = line.split(',')
                for col, cell in enumerate(self._table_data[row]):
                    v = vals[col].strip()
                    cell.text.set(v)
        self.draw()


color_map = {
    '0':    '#99cfff', # Dark Blue
    '30':   '#99fbff', # Light Blue
    '45':   '#99ff9c', # Green
    '60':   '#ffe099', # Orange
    '90':   '#ffb099' # Red
}

def map_color(key):
    '''maps the KEY to a color'''
    try:
        color = color_map[key]
    except:
        color = 'White'
    finally:
        return color