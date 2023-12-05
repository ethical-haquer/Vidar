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
from time import sleep
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
from time import sleep
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
        ('Enter_Button', 'Send Thor an \'Enter\''),
        ('Space_Button', 'Send Thor a \'Space\''),
        ('Page_Up_Button', 'Send Thor a \'Page Up\''),
        ('Page_Down_Button', 'Send Thor a \'Page Down\''),
        ('BL_Checkbox', 'The Odin archives selected with these check-boxes will be flashed'),
        ('AP_Checkbox', 'The Odin archives selected with these check-boxes will be flashed'),
        ('CP_Checkbox', 'The Odin archives selected with these check-boxes will be flashed'),
        ('CSC_Button', 'The Odin archives selected with these check-boxes will be flashed'),
        ('USERDATA_Checkbox', 'The Odin archives selected with these check-boxes will be flashed'),
        ('BL_Button', 'Select a BL file'),
        ('AP_Button', 'Select an AP file'),
        ('CP_Button', 'Select a CP file'),
        ('CSC_Button', 'Select a SCS file'),
        ('USERDATA_Button', 'Select a USERDATA file'),
        ('BL_Entry', 'Drag and drop a BL file here, or paste it\'s path'),
        ('AP_Entry', 'Drag and drop an AP file here, or paste it\'s path'),
        ('CP_Entry', 'Drag and drop a CP file here, or paste it\'s path'),
        ('CSC_Entry', 'Drag and drop a CSC file here, or paste it\'s path'),
        ('USERDATA_Entry', 'Drag and drop a USERDATA file here, or paste it\'s path'),
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
        print(f'The found \'vidar-gui_settings.pkl\' file was not created by this version of Vidar_GUI, so Vidar GUI is updating it.')
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
    print(f'The \'vidar-gui_settings.pkl\' file was not found in the directory that this program is being run from ({path_to_vidar_gui}), so Vidar GUI is creating it.')
    filed_version = version
    theme = 'light'
    tooltips = 'on'
    sudo = 'off'
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

# Creates the tooltips; as you can see, it is being phased-out
def create_tooltips():
    delay = 0.25
#    ToolTip(button, msg='Connect a device in download mode', delay=delay)
#    ToolTip(Begin_Button, msg='Start an Odin session', delay=delay)
    ToolTip(Command_Entry, msg='You can enter a Thor command here,\nand press enter to send it', delay=delay)
#    ToolTip(Enter_Button, msg='Send Thor an \'Enter\'', delay=delay)
#    ToolTip(Space_Button, msg='Send Thor a \'Space\'', delay=delay)
#    ToolTip(Page_Up_Button, msg='Send Thor a \'Page Up\'', delay=delay)
#    ToolTip(Page_Down_Button, msg='Send Thor a \'Page Down\'', delay=delay)
    ToolTip(BL_Checkbox, msg='The Odin archives selected with these check-boxes will be flashed', delay=delay)
    ToolTip(AP_Checkbox, msg='The Odin archives selected with these check-boxes will be flashed', delay=delay)
    ToolTip(CP_Checkbox, msg='The Odin archives selected with these check-boxes will be flashed', delay=delay)
    ToolTip(CSC_Checkbox, msg='The Odin archives selected with these check-boxes will be flashed', delay=delay)
    ToolTip(USERDATA_Checkbox, msg='The Odin archives selected with these check-boxes will be flashed', delay=delay)
#    ToolTip(BL_Button, msg='Select a BL file', delay=delay)
#    ToolTip(AP_Button, msg='Select an AP file', delay=delay)
#    ToolTip(CP_Button, msg='Select a CP file', delay=delay)
#    ToolTip(CSC_Button, msg='Select a CSC file', delay=delay)
#    ToolTip(USERDATA_Button, msg='Select a USERDATA file', delay=delay)
    ToolTip(BL_Entry, msg='Drag and drop a BL file here, or paste it\'s path', delay=delay)
    ToolTip(AP_Entry, msg='Drag and drop an AP file here, or paste it\'s path', delay=delay)
    ToolTip(CP_Entry, msg='Drag and drop a CP file here, or paste it\'s path', delay=delay)
    ToolTip(CSC_Entry, msg='Drag and drop a CSC file here, or paste it\'s path', delay=delay)
    ToolTip(USERDATA_Entry, msg='Drag and drop a USERDATA file here, or paste it\'s path', delay=delay)
#    ToolTip(Log_Button, msg='Log Tab', delay=delay)
#    ToolTip(Options_Button, msg='Options Tab', delay=delay)
#    ToolTip(Pit_Button, msg='Pit Tab', delay=delay)
#    ToolTip(Settings_Button, msg='Settings Tab', delay=delay)
#    ToolTip(Help_Button, msg='Help Tab', delay=delay)
#    ToolTip(About_Button, msg='About Tab', delay=delay)
#    ToolTip(Apply_Options_Button, msg='Apply the above options', delay=delay)
    ToolTip(Theme_Toggle, msg='Toggle Theme', delay=delay)
    ToolTip(Tooltip_Toggle, msg='Toggle Tooltips', delay=delay)
    ToolTip(Thor_Toggle, msg='Toggle using an internal/external Thor build', delay=delay)
    ToolTip(Thor_Entry, msg="Vidar GUI will look for the external Thor build in this directory", delay=delay)
    ToolTip(Sudo_Toggle, msg='Toggle running Thor with/without sudo', delay=delay)
    ToolTip(Default_Directory_Entry, msg='The file picker will open to this directory', delay=delay)
#    ToolTip(Start_Flash_Button, msg='Start a flash', delay=delay)
#    ToolTip(Reset_Button, msg='Reset the options in the Options Tab to defaults, and clear the Odin archive check-boxes and archive entries', delay=delay)
    
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
        BL_Checkbox_var.set(False)
        AP_Checkbox_var.set(False)
        CP_Checkbox_var.set(False)
        CSC_Checkbox_var.set(False)
        USERDATA_Checkbox_var.set(False)
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

# Opens message-boxes - Used by start_flash
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
        Button_Widget = ttk.Button(Message_Window, text=button_text, command=button_command)
        Button_Widget.grid(row=row, pady=5)
        row = row + 1

# Opens the file picker when an Odin archive button is clicked
def open_file(type):
    global initial_directory
    try:
        def change_theme():
            sv_ttk.set_theme('dark')
            window.attributes('-topmost', 1)
            window.attributes('-topmost', 0)
            i = 0.0
            for i in range(10):
                window.attributes('-alpha', i)
                i = i + 0.1
                sleep(0.1)
#            window.attributes("-alpha", 1)
#            window.deiconify()
#        window.iconify()
#        window.attributes("-alpha", 0)
        i = 1.0
        for i in range(10):
            window.attributes('-alpha', i)
            i = i - 0.1
            sleep(0.1)
            window.update()
        sv_ttk.set_theme('light')
        initialdir = Default_Directory_Entry.get()
        t = Timer(0, change_theme)
        t.start() # after 5 seconds, "hello, world" will be printed
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
                print(f'Selected {type}: \'{file_path}\' with file picker')
        else:
            print(f'Invalid directory - The directory: \'{initialdir}\' does not exist. You can change your initial file picker directory by going to: Settings - Flashing - Initial file picker directory')
            show_message('Invalid directory', f'The directory: \'{initialdir}\' does not exist\nYou can change your initial file picker directory by going to:\nSettings - Flashing - Initial file picker directory', [{'text': 'OK', 'fg': 'black'}], window_size=(480, 140))
#    except ttk.TclError:
#        print('Vidar GUI was closed with the file picker still open - Don\'t do that. :)')
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
        if tooltips == 'on':
            tooltips = 'off'
        elif tooltips == 'off':
            tooltips = 'on'
            create_tooltips()
    elif variable == 'sudo':
        if sudo == 'on':
            sudo = 'off'
        elif sudo == 'off':
            sudo = 'on'
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
            compatibility_message = 'It looks like you\'re using Linux, so you\'re good to go!'
        elif operating_system == 'Windows':
            compatibility_message = 'It looks like you\'re using Windows, so sadly Vidar GUI won\'t work for you.'
        elif operating_system == 'Darwin':
            compatibility_message = 'It looks like you\'re using macOS, so sadly Vidar GUI won\'t work for you.'
        Startup_Window = tk.Toplevel(window)
        Startup_Window.title('Vidar GUI - A GUI for the Thor Flash Utility')
        Startup_Window.wm_transient(window)
        Startup_Window.grab_set()
        Startup_Window.update_idletasks()
        Startup_Window.columnconfigure(0, weight=1)
        Startup_Window.columnconfigure(1, weight=1)

        Label = ttk.Label(Startup_Window, text='Welcome to Vidar GUI!', font=('Monospace', 11), anchor='center')
        Label.grid(row=0, column=0, columnspan=2, pady=9)

        Label2 = ttk.Label(Startup_Window, text='If you\'re not sure how to use Vidar GUI, click the \'Help\' tab.', font=('Monospace', 11), anchor='center')
        Label2.grid(row=2, column=0, columnspan=2, pady=9)

        Label3 = ttk.Label(Startup_Window, text='For info about Vidar GUI, click the \'About\' tab.', font=('Monospace', 11), anchor='center')
        Label3.grid(row=1, column=0, columnspan=2, pady=9)

        Label4 = ttk.Label(Startup_Window, text='Vidar GUI currently only supports Linux.', font=('Monospace', 11), anchor='center')
        Label4.grid(row=3, column=0, columnspan=2, pady=9)

        Label5 = ttk.Label(Startup_Window, text=compatibility_message, font=('Monospace', 11), anchor='center')
        Label5.grid(row=4, column=0, columnspan=2, pady=9)

        Label6 = ttk.Label(Startup_Window, text='Click \'Close\' to close this window, or \'Cancel\' to close Vidar GUI.', font=('Monospace', 11), anchor='center')
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
        def force_stop():
            Thor.sendline('exit')
            Thor.terminate()
            Thor.wait()
            print('Stopped Thor (possibly forcibly)')
            Force_Close_Window.destroy()
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
            if prompt_available == True:
                Thor.sendline('exit')
                Thor.terminate()
                Thor.wait()
                print('Stopped Thor')
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
            elif prompt_available == False:
                Force_Close_Window = tk.Toplevel(window)
                Force_Close_Window.title('Force Stop Thor')
                Force_Close_Window.wm_transient(window)
                Force_Close_Window.grab_set()
                Force_Close_Window.update_idletasks()
                Force_Close_Window.columnconfigure(0, weight=1)
                Force_Close_Window.columnconfigure(1, weight=1)
                width = 786
                height = 132
                x = window.winfo_rootx() + (window.winfo_width() - width) // 2
                y = window.winfo_rooty() + (window.winfo_height() - height) // 2
                Force_Close_Window.geometry(f'{width}x{height}+{x}+{y}')
                Force_Close_Label = ttk.Label(Force_Close_Window, text='The \'shell>\' prompt isn\'t available, so the \'exit\' command can\'t be sent.', font=('Monospace', 11), anchor='center')
                Force_Close_Label.grid(columnspan=2, column=0, row=0, sticky='we', pady=(5,2))
                Force_Close_Label_2 = ttk.Label(Force_Close_Window, text='Thor may be busy, or locked up.', font=('Monospace', 11), anchor='center')
                Force_Close_Label_2.grid(columnspan=2, column=0, row=1, sticky='we', pady=2)
                Force_Close_Label_3 = ttk.Label(Force_Close_Window, text='You may force stop Thor by clicking the \'Force Stop\' button.', font=('Monospace', 11), anchor='center')
                Force_Close_Label_3.grid(columnspan=2, column=0, row=2, sticky='we', pady=2)
                Force_Close_Label_4 = ttk.Label(Force_Close_Window, text='However, if Thor is in the middle of a flash or something, there will be consequences.', font=('Monospace', 11), anchor='center')
                Force_Close_Label_4.grid(columnspan=2, column=0, row=3, sticky='we', padx=5, pady=(0,5))
                Cancel_Force_Stop_Button = ttk.Button(Force_Close_Window, text='Cancel', command=Force_Close_Window.destroy)
                Cancel_Force_Stop_Button.grid(column=0, row=4, sticky='we', pady=5, padx=(5,2.5))
                Force_Stop_Button = ttk.Button(Force_Close_Window, text='Force Stop', command=force_stop)
                Force_Stop_Button.grid(column=1, row=4, sticky='we', pady=5, padx=(2.5,5))
                Force_Close_Window.mainloop()
    except Exception as e:
        print(f'An exception occurred in on_window_close: {e}')

# My first-ever class :)
class Button():
    def __init__(self, name: str, master: ttk.Frame, text: str, command: typ.Callable, state: str = 'normal', 
                column: int = 0, row: int = 0, sticky: str = 'we', padx: int = 5, pady: int = 5, 
                columnspan: int = 1):
        self.button_name = name + '_Button'
        self.button_master = master
        self.button_text = text
        self.button_command = command
        self.button_state = state
        self.button_column = column
        self.button_row = row
        self.button_sticky = sticky
        self.button_padx = padx
        self.button_pady = pady
        self.button_columnspan = columnspan
        self.tooltip_delay = 0.25
        self.button = ttk.Button(self.button_master, text=self.button_text, command=self.button_command, state=self.button_state)
        self.button.grid(column=self.button_column, row=self.button_row, columnspan=self.button_columnspan, sticky=self.button_sticky, padx=self.button_padx, pady=self.button_pady)
        self.create_tooltip(tooltip_list)

    def create_tooltip(self, tooltip_list: typ.Optional[typ.List[typ.Tuple[str, str]]] = None):
        for tooltip_widget, msg in tooltip_list:
            if tooltip_widget == self.button_name:
                ToolTip(self.button, msg=msg, delay=self.tooltip_delay)

    def __getattr__(self, attr):
        return getattr(self.button, attr)

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

Command_Entry = ttk.Entry(window, state='disabled')
Command_Entry.grid(row=1, column=8, columnspan=4, padx=5, sticky='nesw')
Command_Entry.bind('<Return>', lambda event: vidar.run_command(Command_Entry.get(), 'entry'))

Enter_Button = Button('Enter', window, 'Enter', lambda: Thor.send('\n'), 'disabled', 8, 2, 'ew', 5)
Space_Button = Button('Space', window, 'Space', lambda: Thor.send('\x20'), 'disabled', 9, 2, 'ew', (0, 5))
Page_Up_Button = Button('Page_Up', window, 'PgUp', lambda: Thor.send('\x1b[A'), 'disabled', 10, 2, 'ew')
Page_Down_Button = Button('Page_Down', window, 'PgDn', lambda: Thor.send('\x1b[B'), 'disabled', 11, 2, 'ew')
Start_Flash_Button = Button('Start_Flash', window, 'Start', start_flash, 'disabled', 8, 8, 'ew', 0, 5, 2)
Reset_Button =Button('Reset', window, 'Reset', reset, 'normal', 10, 8, 'we', 5, 5, 2)

# Creates the Odin Archive Check-boxes
BL_Checkbox_var = tk.IntVar()
BL_Checkbox = ttk.Checkbutton(window, variable=BL_Checkbox_var)
BL_Checkbox.grid(row=3, column=7)

AP_Checkbox_var = tk.IntVar()
AP_Checkbox = ttk.Checkbutton(window, variable=AP_Checkbox_var)
AP_Checkbox.grid(row=4, column=7)

CP_Checkbox_var = tk.IntVar()
CP_Checkbox = ttk.Checkbutton(window, variable=CP_Checkbox_var)
CP_Checkbox.grid(row=5, column=7)

CSC_Checkbox_var = tk.IntVar()
CSC_Checkbox = ttk.Checkbutton(window, variable=CSC_Checkbox_var)
CSC_Checkbox.grid(row=6, column=7)

USERDATA_Checkbox_var = tk.IntVar()
USERDATA_Checkbox = ttk.Checkbutton(window, variable=USERDATA_Checkbox_var)
USERDATA_Checkbox.grid(row=7, column=7)

# Creates the Odin archive Buttons
BL_Button = Button('BL', window, 'BL', lambda: open_file('BL'), 'normal', 8 , 3, 'we', 4)
AP_Button = Button('AP', window, 'AP', lambda: open_file('AP'), 'normal', 8, 4, 'we', 4)
CP_Button = Button('CP', window, 'CP', lambda: open_file('CP'), 'normal', 8, 5, 'we', 4)
CSC_Button = Button('CSC', window, 'CSC', lambda: open_file('CSC'), 'normal', 8 , 6, 'we', 4)
USERDATA_Button = Button('USERDATA', window, 'USERDATA', lambda: open_file('USERDATA'), 'normal', 8 , 7, 'we', 4)

# Creates the Odin archive Entries
BL_Entry = ttk.Entry(window)
BL_Entry.grid(row=3, column=9, columnspan=3, sticky='we', padx=5)
bind_file_drop(BL_Entry)

AP_Entry = ttk.Entry(window)
AP_Entry.grid(row=4, column=9, columnspan=3, sticky='we', padx=5)
bind_file_drop(AP_Entry)

CP_Entry = ttk.Entry(window)
CP_Entry.grid(row=5, column=9, columnspan=3, sticky='we', padx=5)
bind_file_drop(CP_Entry)

CSC_Entry = ttk.Entry(window)
CSC_Entry.grid(row=6, column=9, columnspan=3, sticky='we', padx=5)
bind_file_drop(CSC_Entry)

USERDATA_Entry = ttk.Entry(window)
USERDATA_Entry.grid(row=7, column=9, columnspan=3, sticky='we', padx=5)
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

NOTE_Label = ttk.Label(Options_Frame, text='NOTE: The \'T Flash\' option is temporarily not supported by Vidar GUI.')
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

EFSClear_Label = ttk.Label(Options_Frame, text='Wipes the EFS partition (WARNING: You better know what you\'re doing!)', cursor='hand2')
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

if tooltips == 'on':
    other_tooltip = 'off'
elif tooltips == 'off':
    other_tooltip = 'on'

if sudo == 'on':
    other_sudo = 'without'
elif sudo == 'off':
    other_sudo = 'with'
    
if thor == "internal":
    other_thor = "an external"
elif thor == "external":
    other_thor = "the internal"

Theme_Toggle = ttk.Checkbutton(Settings_Frame, text=f'{other_theme} theme', style='Switch.TCheckbutton', command=lambda: change_variable('theme'))
Theme_Toggle.grid(row=1, column=0, padx=10, sticky='w')

Tooltip_Toggle = ttk.Checkbutton(Settings_Frame, text=f'Tooltips {other_tooltip}', style='Switch.TCheckbutton', command=lambda: change_variable('tooltips'))
Tooltip_Toggle.grid(row=2, column=0, padx=10, sticky='w')

create_label('Tooltip', Settings_Frame, 'A restart is required to turn off tooltips\n', ('Monospace', 8), 'w', 15)

create_label('Thor', Settings_Frame, 'Thor', ('Monospace', 12), 'w')

Thor_Toggle = ttk.Checkbutton(Settings_Frame, text=f'Use {other_thor} Thor build', style='Switch.TCheckbutton', command=lambda: change_variable('thor'))
Thor_Toggle.grid(row=5, column=0, padx=10, sticky='w')

create_label('Thor_Directory', Settings_Frame, 'Path to external Thor build:', ('Monospace', 9), 'w', 15, 5)

Thor_Entry = ttk.Entry(Settings_Frame)
Thor_Entry.grid(row=7, column=0, padx=(15, 120), sticky='we')
Thor_Entry.insert(tk.END, thor_directory)
if thor == "internal":
    Thor_Entry.configure(state="disabled")

Sudo_Toggle = ttk.Checkbutton(Settings_Frame, text=f'Run Thor {other_sudo} sudo', style='Switch.TCheckbutton', command=lambda: change_variable('sudo'))
Sudo_Toggle.grid(row=8, column=0, padx=10, sticky='w')

create_label('Sudo', Settings_Frame, 'A restart is required if Thor is already running\n', ('Monospace', 8), 'w', 15)

create_label('Flashing', Settings_Frame, 'Flashing', ('Monospace', 12), 'w')

create_label('Default_Directory', Settings_Frame, 'Initial file picker directory:', ('Monospace', 9), 'w', 15, 5)

Default_Directory_Entry = ttk.Entry(Settings_Frame)
Default_Directory_Entry.grid(row=12, column=0, padx=(15, 120), sticky='we')
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
#window.protocol('WM_DELETE_WINDOW', on_window_close)

# Sets what theme to use
sv_ttk.set_theme(theme)

# Creates tooltips for buttons and things
if tooltips == 'on':
    create_tooltips()

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