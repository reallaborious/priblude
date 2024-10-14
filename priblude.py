#! /usr/bin/env python

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction
import socket,os,time
import xerox
import logging


def menu_constructor(m,d):
	"""
	Construct a hierarchical menu for a given directory structure.

	Parameters:
    m (QMenu): The parent menu instance to which the submenus or actions will be added.
    d (str): The full path to the directory which needs to be observed to construct the menu.

	Returns:
    None: The function modifies the 'm' menu in-place, adding submenus and actions based on the directory content.

	The function recursively explores the directories and files within the specified directory 'd', adding them to the menu 'm' as submenus for directories and actions for files. Actions are connected to a trigger function 'read_file'.
	"""

	dirs = os.listdir(d)
	files = [ i for i in dirs if os.path.isfile(d+'/'+i) ]
	files.sort()
	dirs = [ i for i in dirs if i not in files ]
	dirs.sort()
	dirs += files
	for i in dirs:
		f=d+'/'+i
		if os.path.isdir(f):
			s=QMenu(i,m)
			menu_constructor(s,f)
			m.addMenu(s)
		else:
			a=QAction(i,m)
			a.triggered.connect(lambda check,value=f: read_file(value))
			# a.hovered.connect(lambda value=f: hover(value))
			# It was an experiment with adding notes on hover. The experiment has failed, but let this string be here for posterity.
			m.addAction(a)

def read_file(value):
	"""
	Read and print the contents of a specified file, copying its content to the clipboard.

	Parameters:
    value (str): The full path to the file that needs to be read.

	Returns:
    None: The function prints the contents of the file to the console and copies the contents to the clipboard.

	This function opens the file at the specified path in read mode, reads the content, prints it to the console, and then copies the content to the system clipboard (excluding the last character for formatting purposes).
	"""
	with open(value, 'r',encoding='utf-8') as file:
		lines=file.read()
		logging.info(lines)
		lines.replace('\r','\n')
		xerox.copy(lines[:-1],xsel=True)

class RightClickMenu(QMenu):
	"""
    Initializes and constructs a custom right-click context menu.

    This class extends QMenu to create a context menu that initializes by reading a directory 
    structure from a predefined path and using it to build the menu options.

    Parameters:
    - parent (QWidget, optional): The parent widget for this menu. Default is None.
 
    Returns:
    - None: The constructor initializes the menu, it does not return any value.

    Upon initialization, it constructs the context menu by reading from 'menu_dir' (a global variable 
    that should hold the directory path), calls the 'menu_constructor' function to populate the menu,
    and prints the menu construction process to the console.
    """
	
	def __init__(self, menu_dir, parent=None):
		QMenu.__init__(self, '', parent)
		#self.setStyleSheet("{hith: 200px}")
		logging.debug("Begin to construct menu")
		menu_constructor(self,menu_dir)
		logging.debug("Menu construction finished")
		
class SystemTrayIcon(QSystemTrayIcon):
	"""
    System Tray Icon class for creating and managing a system tray application.

    This class extends QSystemTrayIcon to provide functionality specific to the application, such as
    setting custom icons, handling various tray events, and setting up a context menu from the RightClickMenu class.

    Parameters:
    - parent (QWidget, optional): The parent widget of the tray icon. Default is None.

    Upon instantiation, this class sets up the icon, initializes the right-click context menu, and connects signal
    handlers to manage tray icon activations such as double clicks and context menu invocation.
    """

	def __init__(self, menu_dir, parent=None):
		"""
		Initializes a new instance of the SystemTrayIcon class, configuring the icon and the right-click menu.

		Parameters:
		- parent (QWidget, optional): The parent widget of the tray icon. Default is None.
		- menu_dir (string): The directory where the menu files are stored

		During initialization, an icon is set, a custom right-click menu is initialized, and connections 
		are made to handle tray icon activation events. Prints to the console document the steps of the setting process.
		"""
		QSystemTrayIcon.__init__(self, parent)
		self.setIcon(QtGui.QIcon("gnomeradio.xpm"))

		self.right_menu = RightClickMenu(menu_dir=menu_dir)
		self.setContextMenu(self.right_menu)
		logging.debug("Set context menu")

		self.activated.connect(self.onTrayIconActivated)
		logging.debug("onTray activated")

	def s(self):
		"""
        Show the custom context menu at the current cursor position.
        """
		self.right_menu.exec(QtGui.QCursor.pos())
	
	def onTrayIconActivated(self, reason):
		"""
        Handle various tray icon activation reasons.

        Parameters:
        - reason (QSystemTrayIcon.ActivationReason): Enum value describing the reason the tray icon was activated.

        Supported activation reasons include DoubleClick, Unknown, Context, MiddleClick, and Trigger. 
        Outputs a message to the console depending on the reason and potentially shows the context menu.
        """
		if reason == QSystemTrayIcon.DoubleClick:
			logging.debug("doubleclick")
		if reason == QSystemTrayIcon.Unknown:
			logging.debug("Unknown")
		if reason == QSystemTrayIcon.Context:
			logging.debug("Context")
		if reason == QSystemTrayIcon.MiddleClick:
			logging.debug("MiddleClick")
		if reason == QSystemTrayIcon.Trigger:
			logging.debug("Trigger")
			self.right_menu.exec(QtGui.QCursor.pos())

	def welcome(self):
		"""
        Show a welcome message to the user using the system tray notification.
        """
		self.showMessage("Hello", "I should be aware of both buttons")

	def show(self):
		"""
        Show the tray icon and immediately try to execute the context menu.
        
        This function also prints operation messages to the console to track the process.
        """
		QSystemTrayIcon.show(self)
		logging.debug("Begin")
		self.right_menu.exec(QtGui.QCursor.pos())

		logging.debug("end")



if __name__ == "__main__":
	import click

	@click.command(help='''
Creates an interactive system tray icon that generates context menus on-the-fly from a specified directory, offering functionalities corresponding to files and subdirectories found therein.

menu_dir	The directory containing the system tray menu configuration. If not specified, it defaults to './menu' relative to the current working directory.
''')
	@click.argument('menu_dir', required=False, default=None)
	@click.option('-v','--verbose', is_flag=True, default=False, help="Enable verbose mode.")
	@click.option('-q','--quiet', is_flag=True, default=False, help="Enable quiet mode (only error messages)")
	def run_cli(menu_dir,verbose,quiet):
		"""
		This function sets up a system tray application. It allows for specifying a directory for menu configurations; if not provided, it defaults to the 'menu' subdirectory in the current working directory. The function checks if the provided or default directory exists and exits if it does not. It also supports a verbose mode for additional console output.

		Parameters:
		- menu_dir (str, optional): The directory containing the system tray menu configuration. If not specified, it defaults to './menu' relative to the current working directory.
		- verbose (bool): If set to True, enables verbose output in the console to trace the operations being performed.

		Raises:
		- SystemExit: If the menu directory does not exist, the application will exit with an error message.

		Usage:
		- Without any arguments, the script attempts to use the default menu directory './menu' in the current working directory.
		- If --verbose is used, additional debug information will be printed during execution.
		"""
		if verbose and quiet:
			raise click.UsageError("--verbose and --quiet options cannot be used together.")
		elif verbose: log_level=logging.DEBUG
		elif quiet: log_level=logging.ERROR
		else: log_level=logging.INFO
		logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)s: %(message)s')
		logging.debug('Verbose mode is enabled.')
		
		if not menu_dir:
			menu_dir = os.getcwd() + "/menu"
			logging.debug(f"No menu_dir set, trying to get {menu_dir}")
		if not os.path.isdir(menu_dir):
			logging.error(f"{menu_dir} doesn't exist, exiting...")
			raise
		else:
			logging.debug(f"{menu_dir} exists.")
		app = QApplication([])
		tray = SystemTrayIcon(menu_dir=menu_dir)
		logging.debug("SystemTrayIcon finished")
		tray.show()

	run_cli()
