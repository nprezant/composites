
import tkinter as tk
from tkinter import filedialog
import json

import mixtures as mix

class MaterialEditor(tk.Frame):
    '''GUI to make the laminates'''
    def __init__(self, master=None):
        super().__init__(master)
        self.initialize_ui()


    def initialize_ui(self):
        '''Initialize the user interface'''
        self.master.title('Material Editor')

        # material title
        self.top_frame = tk.Frame(self.master, borderwidth=1, relief='raised', pady=5)
        self.title = tk.Label(self.top_frame, text='Material Name')
        txt = tk.StringVar()
        self.name_entry = tk.Entry(self.top_frame, textvariable=txt)
        self.name_entry.text = txt
        self.title.grid(row=0, column=0, sticky='w')
        self.name_entry.grid(row=0, column=1, sticky='we')
        self.top_frame.columnconfigure(1, weight=1)

        # make a radio button value to track
        self.radio = tk.StringVar()
        self.radio.set('lamina')

        # lamina properties entry
        self.lamina_frame = tk.Frame(self.master, borderwidth=1, relief='raised')
        self.lamina_radio = tk.Radiobutton(
            self.lamina_frame, 
            text='Lamina Level Properties', 
            variable=self.radio, 
            value='lamina')
        self.lamina_radio.value = 'lamina'
        self.lamina_props = LaminaLevelParams(self.lamina_frame)
        self.lamina_radio.grid()
        self.lamina_props.grid()

        # mixture properties entry
        self.mixture_frame = tk.Frame(self.master, borderwidth=1, relief='raised')
        self.mixture_radio = tk.Radiobutton(
            self.mixture_frame,
            text='Fiber/Matrix Properties', 
            variable=self.radio, 
            value='mixture')
        self.mixture_radio.value = 'mixture'
        self.mixture_props = FiberLevelParams(self.mixture_frame)
        self.mixture_radio.grid()
        self.mixture_props.grid()

        # bottom frame
        self.bottom_frame = tk.Frame(self.master)
        self.status_bar = tk.Label(self.bottom_frame, text='')
        self.status_bar.grid(row=0, column=1, sticky='w')

        # overall layout
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky='nwe')
        self.lamina_frame.grid(row=1, column=1, sticky='nwe')
        self.mixture_frame.grid(row=1, column=0, sticky='nwe')
        self.bottom_frame.grid(row=None, column=0, sticky='we')

        # self.master.rowconfigure(0, weight=1)
        # self.master.columnconfigure(0, weight=1)
        self.master.minsize(3, 2)

        # top-level menu
        menubar = tk.Menu(self.master)

        # file pulldown
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save', command=self.save, accelerator='Ctrl+S')
        filemenu.add_command(label='Open', command=self.open, accelerator='Ctrl+O')
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
        self.bind_all('<Control-KeyRelease-s>', self.save)
        self.bind_all('<Control-KeyRelease-o>', self.open)


    def close_event(self, event=None):
        self.master.quit()


    def save(self, event=None):
        '''Writes the data in this form out to a file'''

        # file path
        filename = filedialog.asksaveasfilename(
            title = 'Save file as',
            initialfile = self.name_entry.text.get(),
            filetypes = (
                ('json files','*.json'),
                ('all files','*.*')))

        if filename == '':
            return

        if not filename[-5:] == '.json':
            filename = filename + '.json'

        # main material dict
        mat = {'name': self.name_entry.text.get()}

        # modulus dict
        if self.radio == 'lamina':
            enabled_mod = self.lamina_props
        else:
            enabled_mod = self.mixture_props.lamina
        
        mod = {
            'E1': enabled_mod.E1,
            'E2': enabled_mod.E2,
            'G12': enabled_mod.G12,
            'v12': enabled_mod.v12,
            'v21': enabled_mod.v21
        }

        # save lamina options
        lam = {
            'enabled': self.radio.get() == self.lamina_radio.value,
            'E1': self.lamina_props.E1,
            'E2': self.lamina_props.E2,
            'G12': self.lamina_props.G12,
            'v12': self.lamina_props.v12,
            'v21': self.lamina_props.v21
        }

        mix = {
            'enabled': self.radio.get() == self.mixture_radio.value,
            'Ef': self.mixture_props.Ef,
            'Em': self.mixture_props.Em,
            'vf': self.mixture_props.vf,
            'vm': self.mixture_props.vm,
            'Vf': self.mixture_props.Vf,
            'Vm': self.mixture_props.Vm,
            'E1': self.mixture_props.lamina.E1,
            'E2': self.mixture_props.lamina.E2,
            'G12': self.mixture_props.lamina.G12,
            'v12': self.mixture_props.lamina.v12,
            'v21': self.mixture_props.lamina.v21
        }

        # add radio option to output
        mod['radio'] = self.radio.get()

        # put it all together
        mod['lamina'] = lam
        mod['mixture'] = mix
        mat['modulus'] = mod

        # write
        with open(filename, 'w') as f:
            json.dump(mat, f, indent=4)


    def open(self, event=None):
        '''Loads material data from a file'''
        filename = filedialog.askopenfilename(
            title = 'Select file to open',
            filetypes = (
                ('json files', '*.json'),
                ('all files','*.*')))
        if filename == '': return

        with open(filename, 'r') as f:
            mat = json.load(f)

        # set material name
        self.name_entry.text.set(mat['name'])

        # set radio button
        self.radio = mat['modulus']['radio']

        # set lamina properties
        lam = mat['modulus']['lamina']
        self.lamina_props.E1 = lam['E1']
        self.lamina_props.E2 = lam['E2']
        self.lamina_props.G12 = lam['G12']
        self.lamina_props.v12 = lam['v12']

        # set mixture properties
        mix = mat['modulus']['mixture']
        self.mixture_props.Ef = mix['Ef']
        self.mixture_props.Em = mix['Em']
        self.mixture_props.vf = mix['vf']
        self.mixture_props.vm = mix['vm']
        self.mixture_props.Vf = mix['Vf']

        # recalculate the fields
        self.lamina_props.recalculate()
        self.mixture_props.recalculate()


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
        operators = ['='] * len(varnames)
        values = [''] * len(varnames)
        lamina_params = zip(varnames, operators, values)

        super().__init__(parent, lamina_params)

        for entry in self.entries:
            entry.bind('<FocusOut>', self.recalculate)

        v21 = self.get_widget('v21')
        v21._value.config(state='readonly')


    def recalculate(self, event=None):
        '''When an entry is focused out on.
        Recalculates the v21 value'''
        try:
            self.v21 = float(self.E2) / float(self.E1) * float(self.v12)
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


class FiberLevelParams(BaseParametersFrame):
    '''Frame for the fiber level frame
    Includes: Ef, Em, vf, vm, Vf
    Computes: E1, E2, G12, v12, v21'''

    def __init__(self, parent):
        '''Make a frame to input the fiber level parameters'''

        varnames = ['Ef', 'Em', 'vf', 'vm', 'Vf', 'Vm']
        operators = ['='] * len(varnames)
        values = [''] * len(varnames)
        lamina_params = zip(varnames, operators, values)

        super().__init__(parent, lamina_params)

        self.lamina = LaminaLevelParams(self)
        self.lamina.grid()

        # matrix fraction is readonly
        self.get_widget('Vm')._value.config(state='readonly')

        # when user leaves a mixture field, update stuff
        for entry in self.entries:
            entry.bind('<FocusOut>', self.recalculate)

        # lamina properties are read only here
        for entry in self.lamina.entries:
            entry.config(state='readonly')


    def recalculate(self, event=None):
        '''When an entry is focused out on.
        Recalculates the lamina level values'''

        # compute the matrix volume fraction
        try:
            self.Vm = 1 - float(self.Vf)
        except:
            self.Vm = 'n/a'

        # mix the parameters into a lamina if possible
        try:
            Ef = float(self.Ef)
            Em = float(self.Em)
            Vf = float(self.Vf)
            Vm = float(self.Vm)
            vf = float(self.vf)
            vm = float(self.vm)
        except Exception as e:
            pass
        else:
            mixed = mix.EffectiveLamina(Ef, Em, Vf, Vm, vf, vm)
            self.lamina.E1 = mixed.E1
            self.lamina.E2 = mixed.E2
            self.lamina.G12 = mixed.G12
            self.lamina.v12 = mixed.G12
            self.lamina.recalculate()

    
    @property
    def Ef(self):
        return self.get_value('Ef')


    @Ef.setter
    def Ef(self, value):
        widget = self.get_widget('Ef')
        widget.value = value


    @property
    def Em(self):
        return self.get_value('Em')


    @Em.setter
    def Em(self, value):
        widget = self.get_widget('Em')
        widget.value = value


    @property
    def vf(self):
        return self.get_value('vf')


    @vf.setter
    def vf(self, value):
        widget = self.get_widget('vf')
        widget.value = value


    @property
    def vm(self):
        return self.get_value('vm')


    @vm.setter
    def vm(self, value):
        widget = self.get_widget('vm')
        widget.value = value


    @property
    def Vf(self):
        return self.get_value('Vf')


    @Vf.setter
    def Vf(self, value):
        widget = self.get_widget('Vf')
        widget.value = value


    @property
    def Vm(self):
        return self.get_value('Vm')


    @Vm.setter
    def Vm(self, value):
        widget = self.get_widget('Vm')
        widget.value = value
        


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
        self._value = tk.Entry(self, textvariable=txt, borderwidth=1, width=10, relief='sunken')
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
        try:
            return self._long_value
        except:
            return self._value.text.get()


    @value.setter
    def value(self, value):
        '''Name of this variable's value'''
        self._long_value = value
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