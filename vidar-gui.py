'''
Vidar - A rewrite of the Thor Flash Utility in Python with a GUI 
Copyright (C) 2023  ethical_haquer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import webbrowser
import os
from functools import partial
import sv_ttk
from tkinter import ttk
import pickle
import sys
from tktooltip import ToolTip
from tkinterdnd2 import DND_FILES, TkinterDnD
import platform
import vidar
from threading import Timer
import typing as typ

version = 'Pre-Alpha'

path_to_vidar_gui = os.path.dirname(os.path.abspath(sys.argv[0]))
odin_running = False
Thor = None
connection = False
tag = 'green'
graphical_flash = False
prompt_available = False
sudo_prompt_available = False
operating_system = platform.system()
architecture = platform.machine()

successful_commands = []

odin_archives = []

tooltip_list = [
        ('Connect_Button', 'Connect a device in download mode'),
        ('Begin_Button', 'Start an Odin session'),
        ('Command_Entry', 'You can enter a Thor command here,\nand press enter to send it'),
        ('Enter_Button', "Send Thor an 'Enter'"),
        ('Space_Button', "Send Thor a 'Space'"),
        ('Page_Up_Button', "Send Thor a 'Page Up'"),
        ('Page_Down_Button', "Send Thor a 'Page Down'"),
        ('BL_Checkbutton', 'The Odin archives selected with these check-boxes will be flashed'),
        ('AP_Checkbutton', 'The Odin archives selected with these check-boxes will be flashed'),
        ('CP_Checkbutton', 'The Odin archives selected with these check-boxes will be flashed'),
        ('CSC_Checkbutton', 'The Odin archives selected with these check-boxes will be flashed'),
        ('USERDATA_Checkbutton', 'The Odin archives selected with these check-boxes will be flashed'),
        ('BL_Button', 'Select a BL file'),
        ('AP_Button', 'Select an AP file'),
        ('CP_Button', 'Select a CP file'),
        ('CSC_Button', 'Select a CSC file'),
        ('USERDATA_Button', 'Select a USERDATA file'),
        ('BL_Entry', "Drag and drop a BL file here, or paste it's path"),
        ('AP_Entry', "Drag and drop an AP file here, or paste it's path"),
        ('CP_Entry', "Drag and drop a CP file here, or paste it's path"),
        ('CSC_Entry', "Drag and drop a CSC file here, or paste it's path"),
        ('USERDATA_Entry', "Drag and drop a USERDATA file here, or paste it's path"),
        ('Log_Button', 'Log Tab'),
        ('Options_Button', 'Options Tab'),
        ('Pit_Button', 'Pit Tab'),
        ('Settings_Button', 'Settings Tab'),
        ('Help_Button', 'Help Tab'),
        ('About_Button', 'About Tab'),
        ('Apply_Options_Button', 'Apply the above options'),
        ('Theme_Toggle', 'Toggle Theme'),
        ('Tooltip_Toggle', 'Toggle Tooltips'),
        ('Thor_Toggle', 'Toggle using an internal/external Thor build'),
        ('Thor_Entry', 'Vidar GUI will look for the external Thor build in this directory'),
        ('Sudo_Toggle', 'Toggle running Thor with/without sudo'),
        ('Default_Directory_Entry', 'The file picker will open to this directory'),
        ('Start_Flash_Button', 'Start a flash'),
        ('Reset_Button', 'Reset the options in the Options Tab to defaults, and clear the Odin archive check-boxes and archive entries')
    ]

print(f'''
__     ___     _            
\ \   / (_) __| | __ _ _ __ 
 \ \ / /| |/ _` |/ _` | '__|
  \ V / | | (_| | (_| | |   
   \_/  |_|\__,_|\__,_|_|  

        {version}
''')

# This loads the 'vidar-gui_settings.pkl' file, which contains variables
if os.path.isfile(f'{path_to_vidar_gui}/vidar-gui_settings.pkl'):
    f2 = open(f'{path_to_vidar_gui}/vidar-gui_settings.pkl', 'rb')
    filed_version = pickle.load(f2)
    f2.close()
    if filed_version != version:
        print("The found 'vidar-gui_settings.pkl' file was not created by this version of Vidar_GUI, so Vidar GUI is updating it.")
        if filed_version == 'Alpha v0.4.0':
            filed_version = version
            initial_directory = '~'
            thor = "internal"
            thor_directory = "~"

            f2 = open(f'{path_to_vidar_gui}/vidar-gui_settings.pkl', 'rb')
            # Has to be filed_version_2, otherwise it will overwrite the 'filed_version = version' line above
            filed_version_2 = pickle.load(f2)
            theme = pickle.load(f2)
            tooltips = pickle.load(f2)
            sudo = pickle.load(f2)
            first_run = pickle.load(f2)
            f2.close()

            f1 = open(f'{path_to_vidar_gui}/vidar-gui_settings.pkl', 'wb')
            pickle.dump(filed_version, f1)
            pickle.dump(theme, f1)
            pickle.dump(tooltips, f1)
            pickle.dump(sudo, f1)
            pickle.dump(initial_directory, f1)
            pickle.dump(first_run, f1)
            pickle.dump(thor, f1)
            pickle.dump(thor_directory, f1)
            f1.close()
        elif filed_version == "Alpha v0.4.1":
            filed_version = version
            thor = "internal"
            thor_directory = "~"

            f2 = open(f'{path_to_vidar_gui}/vidar-gui_settings.pkl', 'rb')
            # Has to be filed_version_2, otherwise it will overwrite the 'filed_version = version' line above
            filed_version_2 = pickle.load(f2)
            theme = pickle.load(f2)
            tooltips = pickle.load(f2)
            sudo = pickle.load(f2)
            initial_directory = pickle.load(f2)
            first_run = pickle.load(f2)
            f2.close()

            f1 = open(f'{path_to_vidar_gui}/vidar-gui_settings.pkl', 'wb')
            pickle.dump(filed_version, f1)
            pickle.dump(theme, f1)
            pickle.dump(tooltips, f1)
            pickle.dump(sudo, f1)
            pickle.dump(initial_directory, f1)
            pickle.dump(first_run, f1)
            pickle.dump(thor, f1)
            pickle.dump(thor_directory, f1)
            f1.close()
else:
    print(f"The 'vidar-gui_settings.pkl' file was not found in the directory that this program is being run from ({path_to_vidar_gui}), so Vidar GUI is creating it.")
    filed_version = version
    theme = 'light'
    tooltips = True
    sudo = False
    initial_directory = '~'
    first_run = True
    thor = "internal"
    thor_directory = "~"
    f1 = open(f'{path_to_vidar_gui}/vidar-gui_settings.pkl', 'wb')
    pickle.dump(filed_version, f1)
    pickle.dump(theme, f1)
    pickle.dump(tooltips, f1)
    pickle.dump(sudo, f1)
    pickle.dump(initial_directory, f1)
    pickle.dump(first_run, f1)
    pickle.dump(thor, f1)
    pickle.dump(thor_directory, f1)
    f1.close()

f2 = open(f'{path_to_vidar_gui}/vidar-gui_settings.pkl', 'rb')
filed_version = pickle.load(f2)
theme = pickle.load(f2)
tooltips = pickle.load(f2)
sudo = pickle.load(f2)
initial_directory = pickle.load(f2)
first_run = pickle.load(f2)
thor = pickle.load(f2)
thor_directory = pickle.load(f2)
f2.close()

def toggle_connection():
    vidar.connect

def start_flash():
    return True

def toggle_odin():
    Connect_Button.configure(text='test')

def apply_options():
    return True

def testing():
    line = vidar.gui_test()
    Output_Text.configure(state='normal')
    Output_Text.insert(tk.END, line + '\n', 'green')

# Deals with enabling/disabling buttons - Mainly used by set_connect(), and set_odin()
def set_widget_state(*args, state='normal', text=None):
    for widget in args:
        widget.configure(state=state, text=text)
        if text is not None:
            widget.configure(text=text)

# Changes a tooltip
def change_tooltip(widget, message):
    delay = 0.25
    ToolTip(widget, msg=message, delay=delay)

# Tells the program when the user is running Thor with sudo and needs to enter their password
def set_sudo():
    Command_Entry.configure(show='*')
    Command_Entry.focus_set()
    set_widget_state(Command_Entry)

# Sets the 'Options' back to default and resets the Odin archive Check-buttons/Entries
def reset():
    try:
#        TFlash_Option_var.set(False)
        EFSClear_Option_var.set(False)
        BootloaderUpdate_Option_var.set(False)
        ResetFlashCount_Option_var.set(True)
        BL_Checkbutton_var.set(False)
        AP_Checkbutton_var.set(False)
        CP_Checkbutton_var.set(False)
        CSC_Checkbutton_var.set(False)
        USERDATA_Checkbutton_var.set(False)
        BL_Entry.delete(0, 'end')
        AP_Entry.delete(0, 'end')
        CP_Entry.delete(0, 'end')
        CSC_Entry.delete(0, 'end')
        USERDATA_Entry.delete(0, 'end')
    except Exception as e:
        print(f'An exception occurred in reset: {e}')

# Moves the correct frame to the top
def toggle_frame(name):
    frame_name = name + '_Frame'
    button_name = name + '_Button'
    frame = globals()[frame_name]
    button = globals()[button_name]
    frame.lift()
    buttons = [Log_Button, Options_Button, Pit_Button, Settings_Button, Help_Button, About_Button]
    for btn in buttons:
        if btn == button:
            btn.grid_configure(pady=0)
        else:
            btn.grid_configure(pady=5)

def log(text):
    Output_Text.configure(state='normal')
    for line, color in text:
        Output_Text.insert(tk.END, line + '\n', color)
    Output_Text.configure(state='disabled')

# Opens message-boxes - Used by nothing :) - Will be replaced by a class
def show_message(title, message, buttons, window_size=(300, 100)):
    global Message_Window

    Message_Window = tk.Toplevel(window)
    Message_Window.title(title)
    Message_Window.wm_transient(window)
    Message_Window.grab_set()
    Message_Window.update_idletasks()

    width, height = window_size
    x = window.winfo_rootx() + (window.winfo_width() - width) // 2
    y = window.winfo_rooty() + (window.winfo_height() - height) // 2
    Message_Window.geometry(f'{width}x{height}+{x}+{y}')
    Message_Window.grid_columnconfigure(0, weight=1)
#    Message_Window.grid_rowconfigure(0, weight=1)

    message_label = ttk.Label(Message_Window, text=message, anchor='center')
    message_label.grid(sticky='we', pady=20)

    row = 1
    for button in buttons:
        button_text = button.get('text', 'OK')
        button_fg = button.get('fg', 'black')
        button_command = button.get('command', Message_Window.destroy)
        Button_Widget = ttk.Button(Message_Window, text=button_text, command=button_command, fg=button_fg)
        Button_Widget.grid(row=row, pady=5)
        row = row + 1

# Opens the file picker when an Odin archive button is clicked
def open_file(type):
    global initial_directory
    try:
        def change_theme():
            sv_ttk.set_theme('dark')
        sv_ttk.set_theme('light')
        initialdir = Default_Directory_Entry.get()
        t = Timer(0, change_theme)
        t.start()
        if initialdir == '~' or os.path.isdir(initialdir) == True:
            initial_directory = initialdir
            if type == 'AP':
                file_path = filedialog.askopenfilename(title=f'Select an {type} file', initialdir=initialdir, filetypes=[(f'{type} file', '.tar .zip .md5')])
            else:
                file_path = filedialog.askopenfilename(title=f'Select a {type} file', initialdir=initialdir, filetypes=[(f'{type} file', '.tar .zip .md5')])
            if file_path:
                if type == 'BL':
                    BL_Entry.delete(0, 'end')
                    BL_Entry.insert(0, file_path)
                elif type == 'AP':
                    AP_Entry.delete(0, 'end')
                    AP_Entry.insert(0, file_path)
                elif type == 'CP':
                    CP_Entry.delete(0, 'end')
                    CP_Entry.insert(0, file_path)
                elif type == 'CSC':
                    CSC_Entry.delete(0, 'end')
                    CSC_Entry.insert(0, file_path)
                elif type == 'USERDATA':
                    USERDATA_Entry.delete(0, 'end')
                    USERDATA_Entry.insert(0, file_path)
                print(f"Selected {type}: '{file_path}' with file picker")
        else:
            print(f"Invalid directory - The directory: '{initialdir}' does not exist. You can change your initial file picker directory by going to: Settings - Flashing - Initial file picker directory")
#            show_message('Invalid directory', f"The directory: '{initialdir}' does not exist\nYou can change your initial file picker directory by going to:\nSettings - Flashing - Initial file picker directory", window_size=(480, 140))
#    except ttk.TclError:
#        print('Vidar GUI was closed with the file picker still open - Don't do that. :)')
    except Exception as e:
        print(f'An exception occurred in open_file: {e}')

# Opens websites
def open_link(link):
    webbrowser.open(link)

# Deals with showing links - From https://github.com/GregDMeyer/PWman/blob/master/tkHyperlinkManager.py, which itself is from http://effbot.org/zone/tkinter-text-hyperlink.htm, but that site no longer exists
class HyperlinkManager:

    def __init__(self, text):
        self.text = text
        self.text.tag_config('hyper', foreground='blue')
        self.text.tag_bind('hyper', '<Enter>', self._enter)
        self.text.tag_bind('hyper', '<Leave>', self._leave)
        self.text.tag_bind('hyper', '<ButtonRelease-1>', self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        tag = 'hyper-%d' % len(self.links)
        self.links[tag] = action
        return 'hyper', tag

    def _enter(self, event):
        self.text.config(cursor='hand2')

    def _leave(self, event):
        self.text.config(cursor='')

    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:6] == 'hyper-':
                self.links[tag]()
                return

def bind_file_drop(widget):
    widget.drop_target_register(DND_FILES)
    widget.dnd_bind('<<Drop>>', lambda e: [widget.delete(0, 'end'), widget.insert(tk.END, e.data)])

def change_variable(variable):
    global theme, tooltips, sudo, thor
    if variable == 'theme':
        if sv_ttk.get_theme() == 'dark':
            theme = 'light'
        elif sv_ttk.get_theme() == 'light':
            theme = 'dark'
        sv_ttk.set_theme(theme)
    elif variable == 'tooltips':
        tooltips = not tooltips
#        if tooltips == True:
#            create_tooltips()
    elif variable == 'sudo':
        sudo = not sudo
    elif variable == 'thor':
        if thor == 'internal':
            thor = 'external'
            Thor_Entry.configure(state='normal')
        elif thor == 'external':
            thor = 'internal'
            Thor_Entry.configure(state='disabled')

# Creates the start-up window
def create_startup_window():
    try:
        if operating_system == 'Linux':
            compatibility_message = "It looks like you're using Linux, so you're good to go!"
        elif operating_system == 'Windows':
            compatibility_message = "It looks like you're using Windows, so sadly Vidar GUI won't work for you."
        elif operating_system == 'Darwin':
            compatibility_message = "It looks like you're using macOS, so sadly Vidar GUI won't work for you."
        Startup_Window = tk.Toplevel(window)
        Startup_Window.title('Vidar GUI - A GUI for the Thor Flash Utility')
        Startup_Window.wm_transient(window)
        Startup_Window.grab_set()
        Startup_Window.update_idletasks()
        Startup_Window.columnconfigure(0, weight=1)
        Startup_Window.columnconfigure(1, weight=1)

        Label = ttk.Label(Startup_Window, text='Welcome to Vidar GUI!', font=('Monospace', 11), anchor='center')
        Label.grid(row=0, column=0, columnspan=2, pady=9)

        Label2 = ttk.Label(Startup_Window, text="If you're not sure how to use Vidar GUI, click the 'Help' tab.", font=('Monospace', 11), anchor='center')
        Label2.grid(row=2, column=0, columnspan=2, pady=9)

        Label3 = ttk.Label(Startup_Window, text="For info about Vidar GUI, click the 'About' tab.", font=('Monospace', 11), anchor='center')
        Label3.grid(row=1, column=0, columnspan=2, pady=9)

        Label4 = ttk.Label(Startup_Window, text='Vidar GUI currently only supports Linux.', font=('Monospace', 11), anchor='center')
        Label4.grid(row=3, column=0, columnspan=2, pady=9)

        Label5 = ttk.Label(Startup_Window, text=compatibility_message, font=('Monospace', 11), anchor='center')
        Label5.grid(row=4, column=0, columnspan=2, pady=9)

        Label6 = ttk.Label(Startup_Window, text="Click 'Close' to close this window, or 'Cancel' to close Vidar GUI.", font=('Monospace', 11), anchor='center')
        Label6.grid(row=6, column=0, columnspan=2, pady=9)

        def send_cancel():
            Startup_Window.destroy()
            on_window_close()

        def send_close():
            global first_run
            first_run = False
            Startup_Window.destroy()

        Cancel_Button = ttk.Button(Startup_Window, text='Cancel', command=send_cancel)
        Cancel_Button.grid(row=7, column=0, sticky='we', pady=5, padx=(5,2.5))

        Close_Button = ttk.Button(Startup_Window, text='Close', command=send_close)
        Close_Button.grid(row=7, column=1, sticky='we', pady=5, padx=(2.5,5))

        width = 640
        height = 257
        x = window.winfo_rootx() + (window.winfo_width() - width) // 2
        y = window.winfo_rooty() + (window.winfo_height() - height) // 2
        Startup_Window.geometry(f'{width}x{height}+{x}+{y}')

        Startup_Window.mainloop()
    except Exception as e:
        print(f'An exception occurred in create_startup_window: {e}')

# Handles stopping everything when the window is closed, or the 'Stop Thor' button is clicked
def on_window_close():
    global Thor, prompt_available, Message_Window
    try:
        print('Stopping Vidar GUI...')
        f1 = open(f'{path_to_vidar_gui}/vidar-gui_settings.pkl', 'wb')
        pickle.dump(filed_version, f1)
        pickle.dump(theme, f1)
        pickle.dump(tooltips, f1)
        pickle.dump(sudo, f1)
        pickle.dump(initial_directory, f1)
        pickle.dump(first_run, f1)
        pickle.dump(thor, f1)
        pickle.dump(thor_directory, f1)
        f1.close()
        window.destroy()
    except Exception as e:
        print(f'An exception occurred in on_window_close: {e}')

class TooltipManager:
    def __init__(self, tooltip_list):
        self.tooltip_list = tooltip_list
        self.tooltip_delay = 0.25

    def create_tooltips(self, widget, widget_name):
        for tooltip_widget, msg in self.tooltip_list:
            if tooltip_widget == widget_name:
                ToolTip(widget, msg=msg, delay=self.tooltip_delay, width=len(msg) * 10)
            
# My first-ever class :)
class Button():
    def __init__(self, name: str, master: ttk.Frame, text: str, command: typ.Callable,
        state: str = 'normal', 
        column: int = 0,
        row: int = 0,
        sticky: str = 'we',
        padx: int = 5,
        pady: int = 5, 
        columnspan: int = 1):
            
        self.name = name + '_Button'
        self.master = master
        self.text = text
        self.command = command
        self.state = state
        self.column = column
        self.row = row
        self.sticky = sticky
        self.padx = padx
        self.pady = pady
        self.columnspan = columnspan
        self.tooltip_delay = 0.25
        self.button = ttk.Button(self.master, text=self.text, command=self.command, state=self.state)
        self.button.grid(column=self.column, row=self.row, columnspan=self.columnspan, sticky=self.sticky, padx=self.padx, pady=self.pady)
        self.tooltip_manager = TooltipManager(tooltip_list)
        self.tooltip_manager.create_tooltips(self.button, self.name)

    def __getattr__(self, attr):
        return getattr(self.button, attr)

class Entry():
    def __init__(self, name: str, master: ttk.Frame,
        state: str = 'normal', 
        column: int = 0,
        row: int = 0,
        sticky: str = 'we',
        padx: int = 5,
        pady: int = 5, 
        columnspan: int = 1):
            
        self.name = name + '_Entry'
        self.master = master
        self.state = state
        self.column = column
        self.row = row
        self.sticky = sticky
        self.padx = padx
        self.pady = pady
        self.columnspan = columnspan
        self.tooltip_delay = 0.25
        self.entry = ttk.Entry(self.master, state=self.state)
        self.entry.grid(column=self.column, row=self.row, columnspan=self.columnspan, sticky=self.sticky, padx=self.padx, pady=self.pady)
        self.tooltip_manager = TooltipManager(tooltip_list)
        self.tooltip_manager.create_tooltips(self.entry, self.name)

    def __getattr__(self, attr):
        return getattr(self.entry, attr)

class Checkbutton():
    def __init__(self, name: str, master: ttk.Frame, variable,
        text: str = None,
        style: str = None,
        state: str = 'normal', 
        column: int = 0,
        row: int = 0,
        sticky: str = 'we',
        padx: int = 5,
        pady: int = 5, 
        columnspan: int = 1):

        self.name = name + '_Checkbutton'
        self.master = master
        self.variable = variable
        self.text = text,
        self.style = style
        self.state = state
        self.column = column
        self.row = row
        self.sticky = sticky
        self.padx = padx
        self.pady = pady
        self.columnspan = columnspan
        self.tooltip_delay = 0.25
        self.checkbutton = ttk.Checkbutton(self.master, variable=self.variable, state=self.state)
        if self.text is not None and self.text[0] is not None:
            self.checkbutton.config(text=self.text)
        if self.style is not None and self.style[0] is not None:
            self.checkbutton.config(style=self.style)
        self.checkbutton.grid(column=self.column, row=self.row, columnspan=self.columnspan, sticky=self.sticky, padx=self.padx, pady=self.pady)
        self.tooltip_manager = TooltipManager(tooltip_list)
        self.tooltip_manager.create_tooltips(self.checkbutton, self.name)

    def __getattr__(self, attr):
        return getattr(self.checkbutton, attr)

def create_label(name, master, text, font=('Monospace', 11), sticky='we', padx=0, pady=0, anchor='center'):
    label = name + '_Label'
    label = ttk.Label(master, text=text, font=font, anchor=anchor)
    label.grid(sticky=sticky, padx=padx, pady=pady)

def create_text(name, master, lines, font=('Monospace', 11)):
    text = name + '_Text'
    text = tk.Text(master, font=font, height=1, bd=0, highlightthickness=0, wrap='word')
    text.grid(sticky='ew')
    hyperlink = HyperlinkManager(text)
    text.tag_configure('center', justify='center')
    for line, link in lines:
        if link != None:
            text.insert(tk.END, line, hyperlink.add(partial(open_link, link)))
        else:
            text.insert(tk.END, line)
    text.tag_add('center', '1.0', 'end')
    text.config(state=tk.DISABLED)

# Creates the main window
window = TkinterDnD.Tk(className='Vidar GUI')
window.title(f'Vidar GUI - {version}')
window.geometry('985x600')

# Hide the window, and then show it as soon as possible - Without this, the window is grey while being initialised, something caused by tkinterdnd2
window.withdraw()
window.after(0,window.deiconify)

# Sets the row and column widths
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_rowconfigure(5, weight=1)
window.grid_rowconfigure(6, weight=1)
window.grid_rowconfigure(7, weight=1)
window.grid_columnconfigure(6, weight=1)

# Creates the main window widgets
Title_Label = ttk.Label(window, text='Vidar Pre-Alpha', font=('Monospace', 20), anchor='center')
Title_Label.grid(row=0, column=0, columnspan=7, rowspan=2, sticky='nesw')

Connect_Button = Button('Connect', window, 'Connect', toggle_connection, 'normal', 8, 0, 'we', (5, 2.5), 5)
Begin_Button = Button('Begin', window, 'Start Odin Protocol', toggle_odin, 'normal', 10, 0, 'we', (2.5, 5), 5)

Command_Entry = Entry('Command', window, 'disabled', 8, 1, 'nesw', 5, 0, 4)
Command_Entry.bind('<Return>', lambda event: vidar.run_command(Command_Entry.get(), 'entry'))

Enter_Button = Button('Enter', window, 'Enter', lambda: Thor.send('\n'), 'disabled', 8, 2, 'ew', 5)
Space_Button = Button('Space', window, 'Space', lambda: Thor.send('\x20'), 'disabled', 9, 2, 'ew', (0, 5))
Page_Up_Button = Button('Page_Up', window, 'PgUp', lambda: Thor.send('\x1b[A'), 'disabled', 10, 2, 'ew')
Page_Down_Button = Button('Page_Down', window, 'PgDn', lambda: Thor.send('\x1b[B'), 'disabled', 11, 2, 'ew')
Start_Flash_Button = Button('Start_Flash', window, 'Start', start_flash, 'disabled', 8, 8, 'ew', 0, 5, 2)
Reset_Button =Button('Reset', window, 'Reset', reset, 'normal', 10, 8, 'we', 5, 5, 2)

# Creates the Odin Archive Check-boxes
BL_Checkbutton_var = tk.IntVar()
AP_Checkbutton_var = tk.IntVar()
CP_Checkbutton_var = tk.IntVar()
CSC_Checkbutton_var = tk.IntVar()
USERDATA_Checkbutton_var = tk.IntVar()

BL_Checkbutton = Checkbutton('BL', window, BL_Checkbutton_var, state='normal', column=7, row=3)
AP_Checkbutton = Checkbutton('AP', window, AP_Checkbutton_var, state='normal', column=7, row=4)
CP_Checkbutton = Checkbutton('CP', window, CP_Checkbutton_var, state='normal', column=7, row=5)
CSC_Checkbutton = Checkbutton('CSC', window, CSC_Checkbutton_var, state='normal', column=7, row=6)
USERDATA_Checkbutton = Checkbutton('USERDATA', window, USERDATA_Checkbutton_var, state='normal', column=7, row=7)

# Creates the Odin archive Buttons
BL_Button = Button('BL', window, 'BL', lambda: open_file('BL'), 'normal', 8 , 3, 'we', 4)
AP_Button = Button('AP', window, 'AP', lambda: open_file('AP'), 'normal', 8, 4, 'we', 4)
CP_Button = Button('CP', window, 'CP', lambda: open_file('CP'), 'normal', 8, 5, 'we', 4)
CSC_Button = Button('CSC', window, 'CSC', lambda: open_file('CSC'), 'normal', 8 , 6, 'we', 4)
USERDATA_Button = Button('USERDATA', window, 'USERDATA', lambda: open_file('USERDATA'), 'normal', 8 , 7, 'we', 4)

# Creates the Odin archive Entries
BL_Entry = Entry('BL', window, 'normal', 9, 3, 'we', 5, 0, 3)
AP_Entry = Entry('AP', window, 'normal', 9, 4, 'we', 5, 0, 3)
CP_Entry = Entry('CP', window, 'normal', 9, 5, 'we', 5, 0, 3)
CSC_Entry = Entry('CSC', window, 'normal', 9, 6, 'we', 5, 0, 3)
USERDATA_Entry = Entry('USERDATA', window, 'normal', 9, 7, 'we', 5, 0, 3)

bind_file_drop(BL_Entry)
bind_file_drop(AP_Entry)
bind_file_drop(CP_Entry)
bind_file_drop(CSC_Entry)
bind_file_drop(USERDATA_Entry)

# Creates the five Frame Buttons
Log_Button = Button('Log', window, 'Log', lambda:toggle_frame('Log'), 'normal', 0, 2, 'wes', (5, 0), 0)
Options_Button = Button('Options', window, 'Options', lambda:toggle_frame('Options'), 'normal', 1, 2, 'wes', 0, (0, 5))
Pit_Button = Button('Pit', window, 'Pit', lambda:toggle_frame('Pit'), 'normal', 2, 2, 'wes', 0, 5)
Help_Button = Button('Help', window, 'Help', lambda:toggle_frame('Help'), 'normal', 4, 2, 'wes', 0, 5)
About_Button = Button('About', window, 'About', lambda:toggle_frame('About'), 'normal', 5, 2, 'wes', 0, 5)
Settings_Button = Button('Settings', window, 'Settings', lambda:toggle_frame('Settings'), 'normal', 3, 2, 'wes', 0, 5)

# Creates the 'Log' frame
Log_Frame = ttk.Frame(window)
Log_Frame.grid(row=3, rowspan=6, column=0, columnspan=7, sticky='nesw', padx=5)
Log_Frame.grid_columnconfigure(0, weight=1)
Log_Frame.grid_rowconfigure(0, weight=1)

Output_Text = scrolledtext.ScrolledText(Log_Frame, state='disabled', highlightthickness=0, font=('Monospace', 9), borderwidth=0)
Output_Text.grid(row=0, column=0, rowspan=6, sticky='nesw')

# Creates the 'Options' frame and check-boxes
Options_Frame = ttk.Frame(window)
Options_Frame.grid(row=3, rowspan=6, column=0, columnspan=7, sticky='nesw', padx=5)

NOTE_Label = ttk.Label(Options_Frame, text="NOTE: The 'T Flash' option is temporarily not supported by Vidar GUI.")
NOTE_Label.grid(row=0, column=0, pady=10, padx=10, sticky='w')

TFlash_Option_var = tk.IntVar()
TFlash_Option = ttk.Checkbutton(Options_Frame, variable=TFlash_Option_var, text='T Flash', state='disabled')
TFlash_Option.grid(row=1, column=0, pady=10, padx=10, sticky='w')

TFlash_Label = ttk.Label(Options_Frame, text='Writes the bootloader of a working device onto the SD card', cursor='hand2')
TFlash_Label.grid(row=2, column=0, pady=10, padx=10, sticky='w')

TFlash_Label.bind('<ButtonRelease-1>', lambda e: open_link('https://android.stackexchange.com/questions/196304/what-does-odins-t-flash-option-do'))

EFSClear_Option_var = tk.IntVar()
EFSClear_Option = ttk.Checkbutton(Options_Frame, variable=EFSClear_Option_var, text='EFS Clear')
EFSClear_Option.grid(row=3, column=0, pady=10, padx=10, sticky='w')

EFSClear_Label = ttk.Label(Options_Frame, text="Wipes the EFS partition (WARNING: You better know what you're doing!)", cursor='hand2')
EFSClear_Label.grid(row=4, column=0, pady=10, padx=10, sticky='w')

EFSClear_Label.bind('<ButtonRelease-1>', lambda e: open_link('https://android.stackexchange.com/questions/185679/what-is-efs-and-msl-in-android'))

BootloaderUpdate_Option_var = tk.IntVar()
BootloaderUpdate_Option = ttk.Checkbutton(Options_Frame, variable=BootloaderUpdate_Option_var, text='Bootloader Update')
BootloaderUpdate_Option.grid(row=5, column=0, pady=10, padx=10, sticky='w')

BootloaderUpdate_Label = ttk.Label(Options_Frame, text='')
BootloaderUpdate_Label.grid(row=6, column=0, pady=10, padx=10, sticky='w')

ResetFlashCount_Option_var = tk.IntVar(value=True)
ResetFlashCount_Option = ttk.Checkbutton(Options_Frame, variable=ResetFlashCount_Option_var, text='Reset Flash Count')
ResetFlashCount_Option.grid(row=7, column=0, pady=10, padx=10, sticky='w')

ResetFlashCount_Label = ttk.Label(Options_Frame, text='')
ResetFlashCount_Label.grid(row=8, column=0, pady=10, padx=10, sticky='w')

Apply_Options_Button = Button('Apply_Options', Options_Frame, 'Apply', apply_options, 'disabled', 0, 9, 'w', 10, 10)

# Creates the 'Pit' frame
Pit_Frame = ttk.Frame(window)
Pit_Frame.grid(row=3, rowspan=6, column=0, columnspan=7, sticky='nesw', padx=5)

Test_Label = ttk.Label(Pit_Frame, text='Just a test :)')
Test_Label.grid(row=0, column=0, pady=10, padx=10, sticky='w')
create_label('Test', Pit_Frame, 'Just a test :)', sticky='w', padx=10, pady=10)

Although_Label = ttk.Label(Pit_Frame, text='Pull requests are always welcome though!')
Although_Label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

# Creates the 'Settings' frame
Settings_Frame = ttk.Frame(window)
Settings_Frame.grid(row=3, rowspan=6, column=0, columnspan=7, sticky='nesw', padx=5)
Settings_Frame.grid_columnconfigure(0, weight=1)

create_label('Theme', Settings_Frame, 'Appearance', ('Monospace', 12), 'w')

if theme == 'light':
    other_theme = 'Dark'
elif theme == 'dark':
    other_theme = 'Light'

if tooltips == True:
    other_tooltip = 'off'
elif tooltips == False:
    other_tooltip = 'on'

if sudo == True:
    other_sudo = 'without'
elif sudo == False:
    other_sudo = 'with'
    
if thor == "internal":
    other_thor = "an external"
elif thor == "external":
    other_thor = "the internal"

Theme_Toggle = Checkbutton('Theme', Settings_Frame, lambda: change_variable('theme'), other_theme + 'theme', 'Switch.TCheckbutton', 'normal', 0, 1, 'we', 10)

Tooltip_Toggle = ttk.Checkbutton(Settings_Frame, text=f'Tooltips {other_tooltip}', style='Switch.TCheckbutton', command=lambda: change_variable('tooltips'))
Tooltip_Toggle.grid(row=2, column=0, padx=10, sticky='w')

create_label('Tooltip', Settings_Frame, 'A restart is required to turn off tooltips\n', ('Monospace', 8), 'w', 15)

create_label('Thor', Settings_Frame, 'Thor', ('Monospace', 12), 'w')

Thor_Toggle = ttk.Checkbutton(Settings_Frame, text=f'Use {other_thor} Thor build', style='Switch.TCheckbutton', command=lambda: change_variable('thor'))
Thor_Toggle.grid(row=5, column=0, padx=10, sticky='w')

create_label('Thor_Directory', Settings_Frame, 'Path to external Thor build:', ('Monospace', 9), 'w', 15, 5)

Thor_Entry = Entry('Thor', Settings_Frame, 'normal', 0, 7, 'we', (15, 120))
Thor_Entry.insert(tk.END, thor_directory)
if thor == "internal":
    Thor_Entry.configure(state="disabled")

Sudo_Toggle = ttk.Checkbutton(Settings_Frame, text=f'Run Thor {other_sudo} sudo', style='Switch.TCheckbutton', command=lambda: change_variable('sudo'))
Sudo_Toggle.grid(row=8, column=0, padx=10, sticky='w')

create_label('Sudo', Settings_Frame, 'A restart is required if Thor is already running\n', ('Monospace', 8), 'w', 15)

create_label('Flashing', Settings_Frame, 'Flashing', ('Monospace', 12), 'w')

create_label('Default_Directory', Settings_Frame, 'Initial file picker directory:', ('Monospace', 9), 'w', 15, 5)

Default_Directory_Entry = Entry('Default_Directory', Settings_Frame, 'normal', 0, 12, 'we', (15, 120))
Default_Directory_Entry.insert(tk.END, initial_directory)

# Creates the 'Help' frame
Help_Frame = ttk.Frame(window)
Help_Frame.grid(row=3, rowspan=6, column=0, columnspan=7, sticky='nesw', padx=5)
Help_Frame.grid_columnconfigure(0, weight=1)

create_label('Help', Help_Frame, '\nNot sure how to use Vidar GUI?', ('Monospace', 13))

create_text('Usage_Help_Text', Help_Frame, [
    ('Check out ', None),
    ('the Usage Guide', 'https://github.com/ethical-haquer/Thor_GUI#usage'),
    ('.', None)
])

create_label('Help_3', Help_Frame, '\nFound an issue?', ('Monospace', 13))

create_text('Report', Help_Frame, [
    ("If it isn't listed ", None),
    ('here', 'https://github.com/ethical-haquer/Vidar#known-bugs'),
    (', you can ', None),
    ('report it', 'https://github.com/ethical-haquer/Vidar/issues/new/choose'),
    ('.', None)
])

# Creates the 'About' frame
About_Frame = ttk.Frame(window)
About_Frame.grid(row=3, rowspan=6, column=0, columnspan=7, sticky='nesw', padx=5)
About_Frame.grid_columnconfigure(0, weight=1)

create_label('Vidar', About_Frame, 'Vidar', ('Monospace', 13))

create_label('Vidar_GUI_Version', About_Frame, f'{version}')

create_label('Vidar_Description', About_Frame, "A rewrite of the Thor Flash Utility in Python with a GUI ")

create_text('Vidar_Websites', About_Frame, [
    ('GitHub', 'https://github.com/ethical-haquer/Vidar'),
    (', ', None),
    ('XDA', 'https://xdaforums.com/t/thor-gui-a-gui-for-the-thor-flash-utility-samsung-flash-tool.4636402/')
])

create_label('Built_Around', About_Frame, 'Built around the:')

create_label('Thor', About_Frame, '\nThor Flash Utility', ('Monospace', 13))

create_label('Thor_Version', About_Frame, 'v1.0.4')

create_label('Thor_Description', About_Frame, 'An alternative to Heimdall')

create_text('Thor_Websites', About_Frame, [
    ('GitHub', 'https://github.com/Samsung-Loki/Thor'),
    (', ', None),
    ('XDA', 'https://forum.xda-developers.com/t/dev-thor-flash-utility-the-new-samsung-flash-tool.4597355/')
])

create_label('Credits', About_Frame, '\nCredits:', ('Monospace', 13))

create_text('TheAirBlow', About_Frame, [
    ('TheAirBlow', 'https://github.com/TheAirBlow'),
    (' for the ', None),
    ('Thor Flash Utility', None)
])

create_text('rdbende', About_Frame, [
    ('rdbende', 'https://github.com/rdbende'),
    (' for the ', None),
    ('Sun Valley tkk theme', 'https://github.com/rdbende/Sun-Valley-ttk-theme')
])

create_text('ethical_haquer', About_Frame, [
    ('Myself, ', None),
    ('ethical_haquer', 'https://github.com/ethical-haquer'),
    (', for Vidar GUI', None)
])

create_label('Disclaimer', About_Frame, '\nVidar comes with absolutely no warranty.', ('Monospace', 9))

create_label('Disclaimer_2', About_Frame, 'See the GNU General Public License, version 3 or later for details.', ('Monospace', 9))

create_label('Disclaimer_3', About_Frame, '\nThor Flash Utility comes with absolutely no warranty.', ('Monospace', 9))

create_label('Disclaimer_4', About_Frame, 'See the Mozilla Public License, version 2 or later for details.', ('Monospace', 9))

# Configures the tags for coloring the output text
Output_Text.tag_configure('green', foreground='#26A269')
Output_Text.tag_configure('yellow', foreground='#E9AD0C')
Output_Text.tag_configure('red', foreground='#F66151')
Output_Text.tag_configure('blue', foreground='#33C7DE')
Output_Text.tag_configure('green_italic', foreground='#26A269', font=('Monospace', 9, 'italic'))
Output_Text.tag_configure('orange', foreground='#E9AD0C')
Output_Text.tag_configure('dark_blue', foreground='#2A7BDE')

# Raises the 'Log' frame to top on start-up
toggle_frame('Log')

# Binds the on_window_close function to the window's close event
window.protocol('WM_DELETE_WINDOW', on_window_close)

# Sets what theme to use
sv_ttk.set_theme(theme)

# Creates tooltips for buttons and things
#if tooltips == True:
#    create_tooltips()

# Shows the setup window if first_run == True
if first_run == True:
    window.after(0,create_startup_window)

log([
    (f'Welcome to Vidar GUI {version}!', 'green'),
    ("Type 'help' for list of commands.", 'green'),
    ("To start off, type 'connect' to initiate a connection.", 'green')
])

# Runs the Tkinter event loop
window.mainloop()
