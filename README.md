# the Priblude

This Python script generates interactive context menus based on the contents of a specified directory.
This script can be utilized both as a standalone command-line interface (CLI) application and as an imported module in other Python scripts.
This script is designed to operate **exclusively on Linux platforms**, and there are **no current plans** to extend functionality **to Windows** systems.
Nevertheless if someone will try it on Windows - it's their own affair.

## Features
- **Dynamic Context Menu:** Automatically constructs a context menu that reflects the structure of a specified directory.
- **File Operations:** Includes functionality to read files directly from the system tray and copy their content to the clipboard.
- **Customizable:** Extendable via a directory structure which the script watches to construct menus.
**Note:** To add string **without new line** in the end, add one new line(s) (cat > file , copy-paste whatever you need, press enter and ctrl-c). If you still **need a new line** in the end of the copied line(s) - just add to enters in the end.

# BONUS FEATURE
There's a menu folder with my commands I've gathered for more than 20 years living in Linux... Please use it with pleasure, but at your own risk. I take no responsibility for your use of this.
It includes mostly bash/python onelines, but also there're python and js bookmarklets, vim tricks and big maybe something else I don't even recall myself.
Howbeit, it's merely an example of how can you use it. It's structorized to directories so it's easy to reach it **for me**, however, I believe it would be better for everyone to create their own personalized setup.

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
