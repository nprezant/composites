
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

import numpy as np

import mixtures as mix
from stiffness import (
    Q2props,
    make_Q,
    rotate_Q
)

# GUI spacing
HSPACE = 20
VSPACE = 10

class MaterialEditor(tk.Frame):
    '''GUI to make the laminates'''
    def __init__(self, master=None):
        super().__init__(master)
        self.initialize_ui()


    def initialize_ui(self):
        '''Initialize the user interface'''
        self.master.title('Material Editor')

        # material title
        self.top_frame = tk.Frame(self, borderwidth=1, relief='raised', pady=5)
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
        self.lamina_frame = tk.Frame(self, borderwidth=1, relief='raised')
        self.lamina_radio = tk.Radiobutton(
            self.lamina_frame, 
            text='Lamina Level Properties', 
            variable=self.radio, 
            value='lamina')
        self.lamina_radio.value = 'lamina'
        self.lamina_input = LaminaInputFrame(self.lamina_frame)
        self.lamina_radio.grid(sticky='w')
        self.lamina_input.grid()

        # mixture properties entry
        self.mixture_frame = tk.Frame(self, borderwidth=1, relief='raised')
        self.mixture_radio = tk.Radiobutton(
            self.mixture_frame,
            text='Fiber/Matrix Properties', 
            variable=self.radio, 
            value='mixture')
        self.mixture_radio.value = 'mixture'
        self.mixture_input = FiberInputFrame(self.mixture_frame)
        self.mixture_radio.grid(sticky='w')
        self.mixture_input.grid()

        # Q matrix properties entry
        self.q_frame = tk.Frame(self, borderwidth=1, relief='raised')
        self.q_radio = tk.Radiobutton(
            self.q_frame,
            text='Q Matrix Properties', 
            variable=self.radio, 
            value='q')
        self.q_radio.value = 'q'
        self.q_input = QInputFrame(self.q_frame)
        self.q_radio.grid(sticky='w')
        self.q_input.grid()

        # bottom frame
        self.bottom_frame = tk.Frame(self)
        self.status_bar = tk.Label(self.bottom_frame, text='')
        self.status_bar.grid(row=0, column=1, sticky='w')

        # overall layout
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky='nwe')
        self.lamina_frame.grid(row=2, column=0, sticky='nwe')
        self.mixture_frame.grid(row=4, column=0, sticky='nwe')
        self.q_frame.grid(row=6, column=0, sticky='nwe')
        self.bottom_frame.grid(row=None, column=0, sticky='we')

        ttk.Separator(self, orient='horizontal').grid(row=1, column=0)
        ttk.Separator(self, orient='horizontal').grid(row=3, column=0)
        ttk.Separator(self, orient='horizontal').grid(row=5, column=0)

        self.master.minsize(3, 2)

        # top-level menu
        menubar = tk.Menu(self.master)
        menubar.add_command(label='Q Rotations', command=self.open_q_rotater)

        # file pulldown
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save', command=self.save, accelerator='Ctrl+S')
        filemenu.add_command(label='Save', command=self.save_as)
        filemenu.add_command(label='Open', command=self.open_dialog, accelerator='Ctrl+O')
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
        self.bind_all('<Control-KeyRelease-o>', self.open_dialog)


    def open_q_rotater(self, event=None):
        '''Opens the q rotater form
        This is just a test area to put this'''
        t = tk.Toplevel(self)
        qrot = QRotateUi(t)
        qrot.grid()


    def close_event(self, event=None):
        self.quit()


    def save(self, event=None):
        '''Save the file to the already saved path'''
        try:
            path = self._save_path
            if path is None:
                raise ValueError
        except:
            self.save_as()
        else:
            self._write_to_file(path)


    def save_as(self, event=None):
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
        else:
            self._save_path = filename
            self.save(filename)


    def _write_to_file(self, filename):
        '''Writes the data in this form out to a file'''

        # main material dict
        mat = {'name': self.name_entry.text.get()}

        # modulus dict
        # TODO take off the "lamina" and let it access both lamina and qmat attributes
        if self.radio.get() == 'lamina':
            enabled_mod = self.lamina_input
        elif self.radio.get() == 'mixture':
            enabled_mod = self.mixture_input
        elif self.radio.get() == 'q':
            enabled_mod = self.q_input
        else:
            raise ValueError(f'Radio value not valid: {self.radio.get}')
        
        mod = {
            'E1': enabled_mod.lamina.E1,
            'E2': enabled_mod.lamina.E2,
            'G12': enabled_mod.lamina.G12,
            'v12': enabled_mod.lamina.v12,
            'v21': enabled_mod.lamina.v21,
            'Q': enabled_mod.qmat.Q.tolist()
        }

        # save lamina level input options
        lam = {
            'enabled': self.radio.get() == self.lamina_radio.value,
            'E1': self.lamina_input.lamina.E1,
            'E2': self.lamina_input.lamina.E2,
            'G12': self.lamina_input.lamina.G12,
            'v12': self.lamina_input.lamina.v12,
            'v21': self.lamina_input.lamina.v21,
            'Q': self.lamina_input.qmat.Q.tolist()
        }

        # save fiber mixture input options
        mix = {
            'enabled': self.radio.get() == self.mixture_radio.value,
            'Ef': self.mixture_input.fiber.Ef,
            'Em': self.mixture_input.fiber.Em,
            'vf': self.mixture_input.fiber.vf,
            'vm': self.mixture_input.fiber.vm,
            'Vf': self.mixture_input.fiber.Vf,
            'Vm': self.mixture_input.fiber.Vm,
            'E1': self.mixture_input.lamina.E1,
            'E2': self.mixture_input.lamina.E2,
            'G12': self.mixture_input.lamina.G12,
            'v12': self.mixture_input.lamina.v12,
            'v21': self.mixture_input.lamina.v21,
            'Q': self.mixture_input.qmat.Q.tolist()
        }

        # save q input options
        qmat = {
            'enabled': self.radio.get() == self.q_radio.value,
            'E1': self.q_input.lamina.E1,
            'E2': self.q_input.lamina.E2,
            'G12': self.q_input.lamina.G12,
            'v12': self.q_input.lamina.v12,
            'v21': self.q_input.lamina.v21,
            'Q': self.q_input.qmat.Q.tolist()
        }

        # add radio option to output
        mod['radio'] = self.radio.get()

        # put modulus together
        mod['lamina'] = lam
        mod['mixture'] = mix
        mod['qmatrix'] = qmat

        # add modulus to main material
        mat['modulus'] = mod

        # write
        with open(filename, 'w') as f:
            json.dump(mat, f, indent=4)


    def open_dialog(self, event=None):
        '''Opens material data with user dialog'''
        filename = filedialog.askopenfilename(
            title = 'Select file to open',
            filetypes = (
                ('json files', '*.json'),
                ('all files','*.*')))
        if filename == '':
            return
        else:
            self.open(filename)



    def open(self, filename):
        '''Loads material data from a file'''

        self._save_path = filename

        with open(filename, 'r') as f:
            mat = json.load(f)

        # set material name
        self.name_entry.text.set(mat['name'])

        # set radio button
        self.radio.set(mat['modulus']['radio'])

        # set lamina properties
        lam = mat['modulus']['lamina']
        self.lamina_input.lamina.E1 = lam['E1']
        self.lamina_input.lamina.E2 = lam['E2']
        self.lamina_input.lamina.G12 = lam['G12']
        self.lamina_input.lamina.v12 = lam['v12']

        # set mixture properties
        mix = mat['modulus']['mixture']
        self.mixture_input.fiber.Ef = mix['Ef']
        self.mixture_input.fiber.Em = mix['Em']
        self.mixture_input.fiber.vf = mix['vf']
        self.mixture_input.fiber.vm = mix['vm']
        self.mixture_input.fiber.Vf = mix['Vf']

        # set q matrix properties
        q = mat['modulus']['qmatrix']['Q']
        q_np = np.array(q)
        self.q_input.qmat.Q = q_np

        # recalculate the fields
        self.lamina_input.recalculate()
        self.mixture_input.recalculate()
        self.q_input.recalculate()


class BaseParametersFrame(tk.Frame):
    '''Base frame for the input parameters'''

    def __init__(self, master, params):
        '''Initialize the parameters
        params is a tuple: (varname, operator, value)
        e.g. ('E1', '=', '100')'''
        super().__init__(master, borderwidth=1, relief='raised')

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

    
    @property
    def widgets(self):
        return self._widgets
        

class LaminaParamsFrame(BaseParametersFrame):
    '''Frame for the lamina level frame
    Includes: E1, E2, G12, v12
    Computes: v21'''

    def __init__(self, master):
        '''Make a frame to input the lamina level parameters'''

        varnames = ['E1', 'E2', 'G12', 'v12', 'v21']
        operators = ['='] * len(varnames)
        values = [''] * len(varnames)
        lamina_params = zip(varnames, operators, values)

        super().__init__(master, lamina_params)

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


class FiberParamsFrame(BaseParametersFrame):
    '''Frame for the fiber level frame
    Includes: Ef, Em, vf, vm, Vf
    Computes: E1, E2, G12, v12, v21'''

    def __init__(self, master):
        '''Make a frame to input the fiber level parameters'''

        varnames = ['Ef', 'Em', 'vf', 'vm', 'Vf', 'Vm']
        operators = ['='] * len(varnames)
        values = [''] * len(varnames)
        lamina_params = zip(varnames, operators, values)

        super().__init__(master, lamina_params)

        # matrix fraction is readonly
        self.get_widget('Vm')._value.config(state='readonly')

        # when user leaves a mixture field, update stuff
        for entry in self.entries:
            entry.bind('<FocusOut>', self.recalculate)


    def recalculate(self, event=None):
        '''When an entry is focused out on.
        Recalculates the matrix fraction'''

        # compute the matrix volume fraction
        try:
            self.Vm = 1 - float(self.Vf)
        except:
            self.Vm = 'n/a'

    
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


class QInputFrame(tk.Frame):
    '''Frame for the inputting Q parameters
    Includes: Q matrix input
    Computes: E1, E2, G12, v12, v21'''

    def __init__(self, master):
        '''Make a frame to input the Q matrix parameters'''
        super().__init__(master)

        self.qmat = QParamsFrame(self)
        self.lamina = LaminaParamsFrame(self)

        self.qmat.grid(row=0, column=0, sticky='nw')
        self.lamina.grid(row=0, column=2, sticky='nw')

        self.columnconfigure(1, minsize=HSPACE)
        self.columnconfigure(3, minsize=HSPACE)

        # when user leaves a mixture field, update stuff
        for entry in self.qmat.entries:
            entry.bind('<FocusOut>', self.recalculate, '+')

        # lamina properties are read only here
        for entry in self.lamina.entries:
            entry.config(state='readonly')


    def recalculate(self, event=None):
        '''When an entry is focused out on.
        Recalculates the lamina level values'''

        # back out lamina parameters from Q matrix if possible
        try:
            q = self.qmat.Q.astype(float)
        except:
            pass
        else:
            E1, E2, v12, _, G12 = Q2props(q)
            self.lamina.E1 = E1
            self.lamina.E2 = E2
            self.lamina.G12 = G12
            self.lamina.v12 = v12
            self.lamina.recalculate()


class LaminaInputFrame(tk.Frame):
    '''Frame for the inputting lamina level parameters
    Includes: E1, E2, v12, G12 input
    Computes: v12, Q'''

    def __init__(self, master):
        '''Make a frame to input the Q matrix parameters'''
        super().__init__(master)

        self.lamina = LaminaParamsFrame(self)
        self.qmat = QParamsFrame(self)

        self.lamina.grid(row=0, column=0, sticky='nw')
        self.qmat.grid(row=0, column=2, sticky='nw')

        self.columnconfigure(1, minsize=HSPACE)
        self.columnconfigure(3, minsize=HSPACE)

        # when user leaves a lamina field, update stuff
        for entry in self.lamina.entries:
            entry.bind('<FocusOut>', self.recalculate, '+')

        # q matrix properties are read only here
        for entry in self.qmat.entries:
            entry.config(state='readonly')


    def recalculate(self, event=None):
        '''When an entry is focused out on.
        Recalculates the q matrix values'''

        # update lower level widgets
        self.lamina.recalculate()

        try:
            E1 = float(self.lamina.E1)
            E2 = float(self.lamina.E2)
            G12 = float(self.lamina.G12)
            v12 = float(self.lamina.v12)
        except:
            pass
        else:
            q = make_Q(E1, E2, G12, v12)
            self.qmat.Q = q


class FiberInputFrame(tk.Frame):
    '''Frame for the inputting fiber level parameters
    Includes: Ef, Em, vf, vm, Vf
    Computes: E1, E2, G12, v12, v21, Q'''

    def __init__(self, master):
        '''Make a frame to input the Q matrix parameters'''
        super().__init__(master)

        self.fiber = FiberParamsFrame(self)
        self.lamina = LaminaParamsFrame(self)
        self.qmat = QParamsFrame(self)

        self.fiber.grid(row=0, column=0, sticky='nw')
        self.lamina.grid(row=0, column=2, sticky='nw')
        self.qmat.grid(row=0, column=4, sticky='nw')

        self.columnconfigure(1, minsize=HSPACE)
        self.columnconfigure(3, minsize=HSPACE)
        self.columnconfigure(5, minsize=HSPACE)

        # when user leaves a fiber field, update stuff
        for entry in self.fiber.entries:
            entry.bind('<FocusOut>', self.recalculate, '+')

        # lamina properties are read only here
        for entry in self.lamina.entries:
            entry.config(state='readonly')

        # q matrix properties are read only here
        for entry in self.qmat.entries:
            entry.config(state='readonly')


    def recalculate(self, event=None):
        '''When an entry is focused out on.
        Recalculates the lamina level values'''

        # update lower level widgets
        self.fiber.recalculate()
        self.lamina.recalculate()

        # mix the parameters into a lamina if possible
        try:
            Ef = float(self.fiber.Ef)
            Em = float(self.fiber.Em)
            Vf = float(self.fiber.Vf)
            Vm = float(self.fiber.Vm)
            vf = float(self.fiber.vf)
            vm = float(self.fiber.vm)
        except:
            pass
        else:
            mixed = mix.EffectiveLamina(Ef, Em, Vf, Vm, vf, vm)
            self.lamina.E1 = mixed.E1
            self.lamina.E2 = mixed.E2
            self.lamina.G12 = mixed.G12
            self.lamina.v12 = mixed.v12
            self.lamina.recalculate()

            q = make_Q(
                mixed.E1,
                mixed.E2,
                mixed.G12,
                mixed.v12
            )
            self.qmat.Q = q


class QParamsFrame(BaseParametersFrame):
    '''Frame for the Q Matrix.
    Includes: Q11, Q12, Q16,
              Q21, Q22, Q26,
              Q61, Q62, Q66.
    Computes Nothing.'''

    def __init__(self, master):
        '''Make a frame to input the fiber level parameters'''

        varnames = [
            'Q11', 'Q12', 'Q16', 
            'Q21', 'Q22', 'Q26',
            'Q61', 'Q62', 'Q66']
        operators = ['='] * len(varnames)
        values = [''] * len(varnames)
        params = zip(varnames, operators, values)

        super().__init__(master, params)

        widgets = iter(self.widgets)
        for i in range(3):
            for j in range(3):
                widget = next(widgets)
                # widget._varname.width = 50
                widget.grid(row=i, column=j)


    
    @property
    def Q(self):
        Q11 = self.get_value('Q11')
        Q12 = self.get_value('Q12')
        Q16 = self.get_value('Q16')
        Q22 = self.get_value('Q22')
        Q21 = self.get_value('Q21')
        Q26 = self.get_value('Q26')
        Q61 = self.get_value('Q61')
        Q62 = self.get_value('Q62')
        Q66 = self.get_value('Q66')
        return np.array([
            [Q11, Q12, Q16],
            [Q21, Q22, Q26],
            [Q61, Q62, Q66]
        ])


    @Q.setter
    def Q(self, matrix):
        self.get_widget('Q11').value = matrix[0,0]
        self.get_widget('Q12').value = matrix[0,1]
        self.get_widget('Q16').value = matrix[0,2]
        self.get_widget('Q22').value = matrix[1,1]
        self.get_widget('Q21').value = matrix[1,0]
        self.get_widget('Q26').value = matrix[1,2]
        self.get_widget('Q61').value = matrix[2,0]
        self.get_widget('Q62').value = matrix[2,1]
        self.get_widget('Q66').value = matrix[2,2]


class InputParameterFrame(tk.Frame):
    '''Frame for an input parameter'''

    def __init__(self, master, varname, operator='=', value=''):
        '''Initialize the table'''
        super().__init__(master)

        # variable name
        txt = tk.StringVar()
        txt.set(varname)
        self._varname = tk.Label(self, textvariable=txt, borderwidth=0, width=3)
        self._varname.text = txt

        # variable operator
        txt = tk.StringVar()
        txt.set(operator)
        self._operator = tk.Label(self, textvariable=txt, borderwidth=0, width=2)
        self._operator.text = txt

        # variable value
        txt = tk.StringVar()
        txt.set(value)
        self._value = tk.Entry(self, textvariable=txt, borderwidth=1, width=10, relief='sunken', validate='focusout', validatecommand=self._validate)
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
            disp_val = '{:.3g}'.format(value)
        except:
            disp_val = value
        self._value.text.set(disp_val)


    def _validate(self):
        '''validates the value entry
        Really, just updates the long value
        and the display value'''
        self._long_value = self._value.text.get()
        return True


    def widgets(self):
        '''List of widgets in this frame'''
        return [self._varname, self._operator, self._value]


class QRotateUi(tk.Frame):
    '''User interface for rotating Q matrices
    Inputs: Q, theta
    Computes: Q_rotated'''

    def __init__(self, master):
        '''Make a frame to input Q matrix params
        Also display the rotations'''
        super().__init__(master)

        self.theta_frame = InputParameterFrame(self, chr(952))
        self.qmat1 = QParamsFrame(self)
        self.qmat2 = QParamsFrame(self)

        self.theta_frame.grid()
        self.qmat1.grid()
        self.qmat2.grid()

        # when user leaves an input Q field, update stuff
        for entry in self.qmat1.entries:
            entry.bind('<FocusOut>', self.recalculate, '+')

        # when theta entry is left, update stuff
        self.theta_frame._value.bind('<FocusOut>', self.recalculate, '+')

        # output Q fields are read only
        for entry in self.qmat2.entries:
            entry.config(state='readonly')

        
    def recalculate(self, event=None):
        '''When an entry is focused out on.
        Recalculates the rotated Q values'''

        # rotate Q if possible
        try:
            q = self.qmat1.Q.astype(float)
            theta = float(self.theta_frame.value) * np.pi / 180
        except:
            pass
        else:
            q_rot = rotate_Q(q, theta)
            self.qmat2.Q = q_rot


class AParamsFrame(BaseParametersFrame):
    '''Frame for the A Matrix.
    Includes: A11, A12, A16,
              A21, A22, A26,
              A61, A62, A66.
    Computes Nothing.'''

    def __init__(self, master):
        '''Make a frame to display A matrix parameters'''

        varnames = [
            'A11', 'A12', 'A16', 
            'A21', 'A22', 'A26',
            'A61', 'A62', 'A66']
        operators = ['='] * len(varnames)
        values = [''] * len(varnames)
        params = zip(varnames, operators, values)

        super().__init__(master, params)

        widgets = iter(self.widgets)
        for i in range(3):
            for j in range(3):
                widget = next(widgets)
                widget.grid(row=i, column=j)


    
    @property
    def A(self):
        A11 = self.get_value('A11')
        A12 = self.get_value('A12')
        A16 = self.get_value('A16')
        A22 = self.get_value('A22')
        A21 = self.get_value('A21')
        A26 = self.get_value('A26')
        A61 = self.get_value('A61')
        A62 = self.get_value('A62')
        A66 = self.get_value('A66')
        return np.array([
            [A11, A12, A16],
            [A21, A22, A26],
            [A61, A62, A66]
        ])


    @A.setter
    def A(self, matrix):
        self.get_widget('A11').value = matrix[0,0]
        self.get_widget('A12').value = matrix[0,1]
        self.get_widget('A16').value = matrix[0,2]
        self.get_widget('A22').value = matrix[1,1]
        self.get_widget('A21').value = matrix[1,0]
        self.get_widget('A26').value = matrix[1,2]
        self.get_widget('A61').value = matrix[2,0]
        self.get_widget('A62').value = matrix[2,1]
        self.get_widget('A66').value = matrix[2,2]


class BParamsFrame(BaseParametersFrame):
    '''Frame for the A Matrix.
    Includes: A11, A12, A16,
              A21, A22, A26,
              A61, A62, A66.
    Computes Nothing.'''

    def __init__(self, master):
        '''Make a frame to display A matrix parameters'''

        varnames = [
            'B11', 'B12', 'B16', 
            'B21', 'B22', 'B26',
            'B61', 'B62', 'B66']
        operators = ['='] * len(varnames)
        values = [''] * len(varnames)
        params = zip(varnames, operators, values)

        super().__init__(master, params)

        widgets = iter(self.widgets)
        for i in range(3):
            for j in range(3):
                widget = next(widgets)
                widget.grid(row=i, column=j)


    
    @property
    def B(self):
        B11 = self.get_value('B11')
        B12 = self.get_value('B12')
        B16 = self.get_value('B16')
        B22 = self.get_value('B22')
        B21 = self.get_value('B21')
        B26 = self.get_value('B26')
        B61 = self.get_value('B61')
        B62 = self.get_value('B62')
        B66 = self.get_value('B66')
        return np.array([
            [B11, B12, B16],
            [B21, B22, B26],
            [B61, B62, B66]
        ])


    @B.setter
    def B(self, matrix):
        self.get_widget('B11').value = matrix[0,0]
        self.get_widget('B12').value = matrix[0,1]
        self.get_widget('B16').value = matrix[0,2]
        self.get_widget('B22').value = matrix[1,1]
        self.get_widget('B21').value = matrix[1,0]
        self.get_widget('B26').value = matrix[1,2]
        self.get_widget('B61').value = matrix[2,0]
        self.get_widget('B62').value = matrix[2,1]
        self.get_widget('B66').value = matrix[2,2]


class DParamsFrame(BaseParametersFrame):
    '''Frame for the A Matrix.
    Includes: D11, D12, D16,
              D21, D22, D26,
              D61, D62, D66
    Computes Nothing.'''

    def __init__(self, master):
        '''Make a frame to display A matrix parameters'''

        varnames = [
            'D11', 'D12', 'D16', 
            'D21', 'D22', 'D26',
            'D61', 'D62', 'D66']
        operators = ['='] * len(varnames)
        values = [''] * len(varnames)
        params = zip(varnames, operators, values)

        super().__init__(master, params)

        widgets = iter(self.widgets)
        for i in range(3):
            for j in range(3):
                widget = next(widgets)
                widget.grid(row=i, column=j)


    
    @property
    def D(self):
        D11 = self.get_value('D11')
        D12 = self.get_value('D12')
        D16 = self.get_value('D16')
        D22 = self.get_value('D22')
        D21 = self.get_value('D21')
        D26 = self.get_value('D26')
        D61 = self.get_value('D61')
        D62 = self.get_value('D62')
        D66 = self.get_value('D66')
        return np.array([
            [D11, D12, D16],
            [D21, D22, D26],
            [D61, D62, D66]
        ])


    @D.setter
    def D(self, matrix):
        self.get_widget('D11').value = matrix[0,0]
        self.get_widget('D12').value = matrix[0,1]
        self.get_widget('D16').value = matrix[0,2]
        self.get_widget('D22').value = matrix[1,1]
        self.get_widget('D21').value = matrix[1,0]
        self.get_widget('D26').value = matrix[1,2]
        self.get_widget('D61').value = matrix[2,0]
        self.get_widget('D62').value = matrix[2,1]
        self.get_widget('D66').value = matrix[2,2]


class ABDInputFrame(tk.Frame):
    '''Frame for the inputting ABD parameters
    Includes: ABD matrix input
    Computes: nothing'''

    def __init__(self, master):
        '''Make a frame to input the ABD matrix parameters'''
        super().__init__(master)

        self.a_frame = AParamsFrame(self)
        self.b_frame = BParamsFrame(self)
        self.d_frame = DParamsFrame(self)

        self.a_frame.grid(row=0, column=0, sticky='nsew')
        self.b_frame.grid(row=0, column=1, sticky='nsew')
        self.d_frame.grid(row=1, column=1, sticky='nsew')

        self._display_mode = False


    @property
    def display_mode(self):
        '''When it is in display mode, entries are read-only'''
        return self._display_mode


    @display_mode.setter
    def display_mode(self, value:bool):
        '''Sets the display mode.
        TRUE means entries are read only
        FALSE means entries can be inserted'''

        entries = []
        entries.extend(self.a_frame.entries)
        entries.extend(self.b_frame.entries)
        entries.extend(self.d_frame.entries)

        if value == True:
            for entry in entries:
                entry.config(state='readonly')
        else:
            for entry in entries:
                entry.config(state='normal')



if __name__ == '__main__':
    root = tk.Tk()
    app = MaterialEditor(master=root)
    app.grid()
    app.mainloop()