
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
        self.top_frame = tk.Frame(self.master, borderwidth=1, relief='solid', pady=5)
        self.title = tk.Label(self.top_frame, text='Material Name')
        self.name_entry = tk.Entry(self.top_frame)
        self.title.grid(row=0, column=0, sticky='w')
        self.name_entry.grid(row=0, column=1, sticky='we')
        self.top_frame.columnconfigure(1, weight=1)

        # lamina properties entry
        self.lamina_props = LaminaLevelParams(self.master)
        # varnames = ['E1', 'E2', 'G12', 'v12']
        # operators = ['='] * 4
        # values = [''] * 4
        # lamina_params = zip(varnames, operators, values)
        # self.lamina_props = BaseParametersFrame(
        #     self.master, lamina_params)

        # mixture properties entry
        varnames = ['Ef', 'Em', 'Nu_f', 'Nu_m', 'Vf']
        operators = ['='] * 5
        values = [''] * 5
        mixture_params = zip(varnames, operators, values)
        self.mixture_props = BaseParametersFrame(
            self.master, mixture_params)

        # bottom frame
        self.bottom_frame = tk.Frame(self.master)
        self.status_bar = tk.Label(self.bottom_frame, text='')
        self.status_bar.grid(row=0, column=1, sticky='w')

        # overall layout
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky='nwe')
        self.lamina_props.grid(row=1, column=1, sticky='nwe')
        self.mixture_props.grid(row=1, column=0, sticky='nwe')
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
        super().__init__(parent, borderwidth=2, relief='solid')

        # make widgets
        self._widgets: InputParameterFrame = []
        for var, op, val in params:
            self._widgets.append(
                InputParameterFrame(self, var, op, val)
                )

        # grid widgets
        for param in self._widgets:
            param.grid(row=None, column=0, sticky='nwe')


    def get_widget(self, key):
        '''Gets the widget of the KEY variable name'''
        for widget in self._widgets:
            if widget.varname == key:
                return widget

        # if the widget key is not found
        raise ValueError(f'Widget with varname "{key}" was not found')


    def get_value(self, key):
        '''Gets the value of the KEY variable name'''
        widget = self.get_widget(key)
        return widget.value


    @property
    def entries(self):
        return [frame._value for frame in self._widgets]
        
        


class LaminaLevelParams(BaseParametersFrame):
    '''Frame for the lamina level frame
    Includes: E1, E2, G12, v12
    Computes: v21'''

    def __init__(self, parent):
        '''Make a frame to input the lamina level parameters'''

        varnames = ['E1', 'E2', 'G12', 'v12', 'v21']
        operators = ['='] * 5
        values = [''] * 5
        lamina_params = zip(varnames, operators, values)

        super().__init__(parent, lamina_params)

        for entry in self.entries:
            entry.bind('<FocusOut>', self.on_focus_out)

        v21 = self.get_widget('v21')
        v21._value.config(state='readonly')


    def on_focus_out(self, event=None):
        '''When an entry is focused out on.
        Recalculates the v21 value'''
        try:
            self.v21 = float(self.E1) / float(self.E2) * float(self.v12)
        except:
            self.v21 = 'n/a'


    
    @property
    def E1(self):
        return self.get_value('E1')


    @E1.setter
    def E1(self, value):
        widget = self.get_widget('E1')
        widget.value = value


    @property
    def E2(self):
        return self.get_value('E2')


    @E2.setter
    def E2(self, value):
        widget = self.get_widget('E2')
        widget.value = value


    @property
    def G12(self):
        return self.get_value('G12')


    @G12.setter
    def G12(self, value):
        widget = self.get_widget('G12')
        widget.value = value


    @property
    def v12(self):
        return self.get_value('v12')


    @v12.setter
    def v12(self, value):
        widget = self.get_widget('v12')
        widget.value = value


    @property
    def v21(self):
        return self.get_value('v21')


    @v21.setter
    def v21(self, value):
        widget = self.get_widget('v21')
        widget.value = value
        # raise AttributeError('Cannot write to v21 parameter')
        


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
        self._varname.text.set(value)


    @property
    def operator(self):
        '''Name of this variable's operator'''
        return self._operator.text.get()


    @operator.setter
    def operator(self, value):
        '''Name of this variable's operator'''
        self._operator.text.set(value)


    @property
    def value(self):
        '''Name of this variable's value'''
        return self._value.text.get()


    @value.setter
    def value(self, value):
        '''Name of this variable's value'''
        self._operator_long_value = value
        try:
            disp_val = '{:.3f}'.format(value)
        except:
            disp_val = value
        self._value.text.set(disp_val)


    def widgets(self):
        '''List of widgets in this frame'''
        return [self._varname, self._operator, self._value]






if __name__ == '__main__':
    root = tk.Tk()
    app = MaterialEditor(master=root)
    app.mainloop()