
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

        # bottom frame
        self.bottom_frame = tk.Frame(self.master)
        self.status_bar = tk.Label(self.bottom_frame, text='OK')
        self.status_bar.grid(row=0, column=1, sticky='w')

        # overall layout
        self.top_frame.grid(row=0, column=0, sticky='nwe')
        self.bottom_frame.grid(row=1, column=0, sticky='we')

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


if __name__ == '__main__':
    root = tk.Tk()
    app = MaterialEditor(master=root)
    app.mainloop()