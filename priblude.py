#! /usr/bin/env python

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction
import socket,os,time
import xerox
#import keyboard

#menu_dir='g:/_BACKUP/Dropbox/Projects/preblude/menu'
menu_dir='/home/nikto/projects/priblude/menu'
p='' #hover flag

def menu_constructor(m,d): #m - menu object, d - directory to observe, full path
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
			a.triggered.connect(lambda check,value=f: t(value))
			# a.hovered.connect(lambda value=f: hover(value))
			m.addAction(a)

def t(value):
#  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#  sock.sendto(bytes(value, 'UTF-8'), (UDP_IP, UDP_PORT))
	#print('file name '+value+' code '+ str(os.system('xclip -i < '+value)))
	with open(value, 'r',encoding='utf-8') as file:
		lines=file.read()
		print(lines)
		lines.replace('\r','\n')
		xerox.copy(lines[:-1],xsel=True)
			
	#with open(value, 'r', encoding='utf-8') as g:
		#lines=[]
		#for line in g:
			#lines.append(line)
		#print(lines)
		
		#if len(lines)>1:
			#for i in range(len(lines)-1):
				#for j in range(0,int(len(lines[i])),10):
					#keyboard.write(lines[i][j:j+10])
					#time.sleep(0.01)
				#keyboard.write('\n')
				##time.sleep(len(lines[i])*0.01)
		#if len(lines)>0: keyboard.write(lines[-1])
		#else: print('empty file '+value)
# def hover(value):
# 	global p
# 	if value != p:
# 		print(value.encode('utf-8'))
# 		p=value

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
