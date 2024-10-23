# the Priblude

This Python script generates interactive context menus based on the contents of a specified directory.
This script can be utilized both as a standalone command-line interface (CLI) application and as an imported module in other Python scripts.
This script is designed to operate **exclusively on Linux platforms**, and there are **no current plans** to extend functionality **to Windows** systems.

## Features
- **Dynamic Context Menu:** Automatically constructs a context menu that reflects the structure of a specified directory.
- **File Operations:** Includes functionality to read files directly from the system tray and copy their content to the clipboard.
- **Customizable:** Extendable via a directory structure which the script watches to construct menus.

## Requirements
- PyQt5
- Python 3.x
- Additional Python libraries: `logging`, `os`, `socket`, `time`, `xerox`.

## Installation

Ensure you have Python installed, then set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

First time please look at the current help, as I don't plan to update this readme every a new option is added. To get help run (in venv activated):
```bash
python priblude.py -h
