'''
Vidar - Like the Thor Flash Utility, but written in Python and with a GUI
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

from rich import print

version = "Pre-Alpha"

protocol = None

commands = [
    ("disconnect", "disconnect"),
    ("printPit", "print_pit"),
    ("debug", "enable_debug"),
    ("devParse", "devparse"),
    ("connect", "connect"),
    ("write", "write"),
    ("read", "read"),
    ("begin", "begin"),
    ("end", "end")
]

def get_description(command):
    if command == "disconnect":
        return "disconnect - Closes the current connection"
    elif command == "printPit":
        return "printPit <filename> - Prints PIT contents in human readable form"
    elif command == "debug":
        return "debug [on/off] - enables or disables debug log level"
    elif command == "devParse":
        return "devParse <path> - Parse a /dev/bus/usb file for debug purposes"
    elif command == "connect":
        return "connect - Initializes a connection"
    elif command == "write":
        return "write [string/int/bytes] <content> - Send a packet of specified type"
    elif command == "read":
        return "read <amount> - Spits out raw bytes from the device"
    elif command == "begin":
        return "begin [odin] - Begins a session with chosen protocol"
    elif command == "end":
        return "end - Ends the current protocol session and shuts the device down if possible"
    else:
        print(f"get_description was unable to provide the description for the '{command}' command")

print(f"[#26A269]Welcome to Vidar Shell {version}![/]")
print("[#26A269]Type '[#33DA7A]help[/]' for list of commands.[/]")
print("[#26A269]To start off, type '[#33DA7A]connect[/]' to initiate a connection.[/]")

while True:
    entered_command = input("shell> ")
    if entered_command == "quit" or entered_command == "exit":
        print("[#E9AD0C]Goodbye![/]")
        break
    if entered_command == "help":
        if protocol == None:
            print("[#26A269][bold][italic]Note: beggining a protocol session unlocks new commands for you to use[/][/][/]")
            print("[#26A269][bold][italic]Note: they can also override the default commands for extension purposes[/][/][/]")
        print("[#E9AD0C]\[required] {optional} - option list[/]")
        print("[#E9AD0C]<required> (optional) - usual argument[/]")
        print(f"[#26A269]Total commands: {(len(commands) + 2)}[/]")
        print("[#33C7DE]exit - Closes the shell, quit also works[/]")
        for command, function in commands:
            description = get_description(command)
            if protocol == None:
                print(f"[#33C7DE]{description}[/]")
