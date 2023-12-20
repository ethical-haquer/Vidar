# Vidar

A rewrite of the [Thor Flash Utility](https://github.com/Samsung-Loki/Thor) in Python with a GUI. It is currently under development and not usable. Once it is in a working state, this repository will be deleted and it will become [Thor GUI](https://github.com/ethical-haquer/Thor_GUI) v0.5.0. Also, starting with the release of Thor GUI v0.5.0, Thor GUI will be renamed Vidar. 

### Why Vidar?

In Norse mythology, [Vidar](https://en.wikipedia.org/wiki/V%C3%AD%C3%B0arr) is one of Odin's sons, and is one of Thor's brothers.

### What will Vidar be like when it's finished?

Vidar will look just like Thor GUI, but instead of using Thor externally, it will be self-contained. Basically, Vidar will be like Thor written in Python and then combined with Thor GUI.

## Disclaimer

Currently, Vidar is in a Pre-Alpha stage. That means it is under development and not ready for end users.

## Known Bugs

- Toggling theme doesn't do anything.

## Implemented Thor commands

- [x] help
- [x] exit / quit

# Development
Want to contribute code or test things out? Follow the below directions to get Vidar up and running on your system.

**NOTE:** Vidar is in a pre-alpha state for a reason. It's not ready for actual use, but rather for testing and development.

## Prerequisites

### Python

If you're on Linux, you probably already have Python installed. Look [here](https://wiki.python.org/moin/BeginnersGuide/Download) if you don't.

### rich

```
python -m pip install rich
```

## GUI Prerequisites

### Tkinter

You probably already have Tkinter installed, but if you get "ModuleNotFoundError: No module named 'tkinter'", do this:

Debian-based distros:

```
sudo apt-get install python3-tk
```

Fedora:

```
sudo dnf install python3-tkinter
```

### Sun Valley ttk theme

```
pip install sv-ttk
```

### tkinter-tooltip

```
pip install tkinter-tooltip
```

### tkinterdnd2-universal

```
pip install tkinterdnd2-universal
```

### To install all of the above Python packages

```
pip install sv-ttk tkinter-tooltip tkinterdnd2-universal
```

## Installation
+ First off, be sure to have the above prerequisites. If you will be using the GUI, also install the GUI prerequisites.
+ Click the green "<> Code" button above.
+ Click the "Download ZIP" button.
+ Extract the newly downloaded "Vidar-main.zip" file.
+ Then, to run the CLI Vidar:
  
  ```
  python3 PATH/TO/vidar.py
  ```

+ Likewise, to run Vidar GUI:
  
  ```
  python3 PATH/TO/vidar-gui.py
  ```
  
+ Have fun testing!

## License

Vidar is licensed under GPLv3. Please see [`LICENSE`](./LICENSE) for the full license text.




