#! /usr/bin/env python

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction
import socket,os,time
import xerox
#import keyboard

#menu_dir='g:/_BACKUP/Dropbox/Projects/preblude/menu'
menu_dir='/home/nikto/projects/priblude/menu'
p='' #hover flag

def menu_constructor(m,d):
	"""
	Construct a hierarchical menu for a given directory structure.
	The function recursively explores the directories and files within the specified directory 'd', adding them to the menu 'm' as submenus for directories and actions for files. Actions are connected to a trigger function 'read_file'.

	Parameters:
    m (QMenu): The parent menu instance to which the submenus or actions will be added.
    d (str): The full path to the directory which needs to be observed to construct the menu.

	Returns:
    None: The function modifies the 'm' menu in-place, adding submenus and actions based on the directory content.
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
	This function opens the file at the specified path in read mode, reads the content, prints it to the console, and then copies the content to the system clipboard (excluding the last character for formatting purposes).

	Parameters:
    value (str): The full path to the file that needs to be read.

	Returns:
    None: The function prints the contents of the file to the console and copies the contents to the clipboard.
	"""
	with open(value, 'r',encoding='utf-8') as file:
		lines=file.read()
		print(lines)
		lines.replace('\r','\n')
		xerox.copy(lines[:-1],xsel=True)

class RightClickMenu(QMenu):
	def __init__(self, parent=None):
		QMenu.__init__(self, '', parent)
		#self.setStyleSheet("{hith: 200px}")
		print("Begin to construct menu")
		menu_constructor(self,menu_dir)
		print("Menu construction finished")
		
class SystemTrayIcon(QSystemTrayIcon):
	def __init__(self, parent=None):
		QSystemTrayIcon.__init__(self, parent)
		self.setIcon(QtGui.QIcon("gnomeradio.xpm"))

		self.right_menu = RightClickMenu()
		#self.right_menu = LeftClickMenu()
		self.setContextMenu(self.right_menu)
		print("Set context menu")

		self.activated.connect(self.onTrayIconActivated)
		print("onTray activated")
# WHEEL EVENT EXAMPLE
		#class SystrayWheelEventObject(QtCore.QObject):
			#def eventFilter(self, object, event):
				#if type(event)==QtGui.QWheelEvent:
					#if event.delta() > 0:
						#sendudp("s51153\n")
					#else:
						#sendudp("s53201\n")
					#event.accept()
					#return True
				#return False

		#self.eventObj=SystrayWheelEventObject()
		#self.installEventFilter(self.eventObj)
	
#	QSystemTrayIcon.Trigger.activate.connect(self.right_menu.exec(QtGui.QCursor.pos()))
	def s(self):
		#print('hotkey')
		self.right_menu.exec(QtGui.QCursor.pos())
	
	def onTrayIconActivated(self, reason):
		if reason == QSystemTrayIcon.DoubleClick:
			print("doubleclick")
		if reason == QSystemTrayIcon.Unknown:
			print("Unknown")
		if reason == QSystemTrayIcon.Context:
			print("Context")
		if reason == QSystemTrayIcon.MiddleClick:
			print("MiddleClick")
		if reason == QSystemTrayIcon.Trigger:
			print("Trigger")
			self.right_menu.exec(QtGui.QCursor.pos())

	def welcome(self):
		self.showMessage("Hello", "I should be aware of both buttons")

	def show(self):
		QSystemTrayIcon.show(self)
		print("Begin")
		self.right_menu.exec(QtGui.QCursor.pos())

		print("end")

#		QSystemTrayIcon.right_menu.popup()
		#QtCore.QTimer.singleShot(100, self.welcome)



if __name__ == "__main__":
	app = QApplication([])
	tray = SystemTrayIcon()
	print("SystemTrayIcon finished")
	tray.show()
	
	#keyboard.add_hotkey('alt+/', tray.s, args=(), suppress=False,timeout=0, trigger_on_release=True)
	#keyboard.add_hotkey('ctrl+alt+;',lambda: app.exit(0), args=(), suppress=False,timeout=0, trigger_on_release=True)
	#keyboard.hook(lambda x: print(x))
	#app.exec_()
	
	#tray.s
	#app.exit(0)
