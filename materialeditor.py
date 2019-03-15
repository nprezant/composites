
import tkinter as tk


class MaterialEditor(tk.Frame):
    '''GUI to make the laminates'''
    def __init__(self, master=None):
        super().__init__(master)
        self.initialize_ui()


    def initialize_ui(self):
        '''Initialize the user interface'''
        self.master.title('Material Editor')

        # material title
        self.top_frame = tk.Frame(self.master)
        self.title = tk.Label(self.top_frame, text='Material Name')
        self.name_entry = tk.Entry(self.top_frame)
        self.title.grid(row=0, column=0, sticky='w')
        self.name_entry.grid(row=0, column=1, sticky='w')

        # parameter entry

        self.params = []
        params = ['E1', 'E2', 'G12', 'v12']
        operators = ['='] * 4
        values = [''] * 4
        self.lamina_props = BaseParametersFrame(
            self.master, zip(params, operators, values))
        # for varname in params:
        #     self.params.append(InputParameterFrame(self.master, varname, '=', ''))

        # bottom frame
        self.bottom_frame = tk.Frame(self.master)
        self.status_bar = tk.Label(self.bottom_frame, text='')
        self.status_bar.grid(row=0, column=1, sticky='w')

        # overall layout
        self.top_frame.grid(row=0, column=0, sticky='nwe')
        self.lamina_props.grid(row=1, column=0, sticky='we')
        # for i, param in enumerate(self.params):
        #     param.grid(row=i+1, column=0, sticky='nwe')
        self.bottom_frame.grid(row=None, column=0, sticky='we')

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.minsize(1, 1)

        # top-level menu
        menubar = tk.Menu(self.master)

        # file pulldown
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save', command=lambda: print('save'))
        filemenu.add_command(label='Open', command=lambda: print('open'))
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=self.close_event, accelerator='Ctrl+W')
        menubar.add_cascade(label='File', menu=filemenu)
        self.master.config(menu=menubar)

        # popup menu
        rclick = tk.Menu(self.master, tearoff=0)
        rclick.add_command(label='Print', command=lambda: print('hi'))

        def popup(event):
            rclick.post(event.x_root, event.y_root)

        # button bindings
        self.bind_all('<Button-3>', popup)

        # keypress bindings
        self.bind_all('<Control-KeyRelease-w>', self.close_event)


    def close_event(self, event=None):
        self.master.quit()


class BaseParametersFrame(tk.Frame):
    '''Base frame for the input parameters'''

    def __init__(self, parent, params):
        '''Initialize the parameters
        params is a tuple: (varname, operator, value)
        e.g. ('E1', '=', '100')'''
        super().__init__(parent)

        # make widgets
        self._widgets: InputParameterFrame = []
        for var, op, val in params:
            self._widgets.append(
                InputParameterFrame(self.master, var, op, val)
                )

        # grid widgets
        for param in self._widgets:
            param.grid(row=None, column=0, sticky='nwe')
        


class InputParameterFrame(tk.Frame):
    '''Frame for an input parameter'''

    def __init__(self, parent, varname, operator='=', value=''):
        '''Initialize the table'''
        super().__init__(parent)

        # variable name
        txt = tk.StringVar()
        txt.set(varname)
        self._varname = tk.Label(self, textvariable=txt, borderwidth=0, width=10)
        self._varname.text = txt

        # variable operator
        txt = tk.StringVar()
        txt.set(operator)
        self._operator = tk.Label(self, textvariable=txt, borderwidth=0, width=10)
        self._operator.text = txt

        # variable value
        txt = tk.StringVar()
        txt.set(value)
        self._value = tk.Entry(self, textvariable=txt, borderwidth=0, width=10)
        self._value.text = txt

        # grid positions
        self._varname.grid(row=0, column=0, sticky='w')
        self._operator.grid(row=0, column=1, sticky='w')
        self._value.grid(row=0, column=2, sticky='we', pady=2)


    @property
    def varname(self):
        '''Name of this variable'''
        return self._varname.text.get()


    @varname.setter
    def varname(self, value):
        '''Name of this variable'''
        return self._varname.text.set(value)


    @property
    def operator(self):
        '''Name of this variable's operator'''
        return self._operator.text.get()


    @operator.setter
    def operator(self, value):
        '''Name of this variable's operator'''
        return self._operator.text.set(value)


    @property
    def value(self):
        '''Name of this variable's value'''
        return self._value.text.get()


    @value.setter
    def value(self, value):
        '''Name of this variable's value'''
        return self._value.text.set(value)


    def widgets(self):
        '''List of widgets in this frame'''
        return [self._varname, self._operator, self._value]






if __name__ == '__main__':
    root = tk.Tk()
    app = MaterialEditor(master=root)
    app.mainloop()