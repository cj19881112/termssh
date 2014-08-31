#!/usr/bin/env python

import curses
import session_store
import session
import ssh

_win = ''

def endall():
	curses.nocbreak()
	_win.keypad(0)
	curses.echo()
	curses.endwin()

class Win:
	def __init__(self, parent, x, y, w, h, title):
		self.x, self.y = x, y
		self.w, self.h = w, h
		self.win = parent.subwin(h, w, y, x)
		self.win.border()
		pos = w / 2 - len(title) / 2
		self.win.addstr(0, pos, title)
	def draw(self):
		pass
	def handleKey(self, k):
		pass

class ActionPane(Win):
	def __init__(self, parent, x, y, w, h, title=''):
		Win.__init__(self, parent, x, y, w, h, title)
		self.btnOffset = 10
		self.btnSpace = 3
		self.selectBtn = -1
		self.buttons = ['  ADD  ', ' DELETE ']
	def draw(self):
		off = self.btnOffset
		for i, btn in enumerate(self.buttons):
			if self.selectBtn == i:
				self.win.addstr(1, off, btn, curses.A_REVERSE);
			else:
				self.win.addstr(1, off, btn);
			off = off + self.btnSpace + len(btn)
	def handleKey(self):
		pass
	
class MainPane(Win):
	def __init__(self, parent, x, y, w, h, title=''):
		Win.__init__(self, parent, x, y, w, h, title)
		self.cap = self.h-2
		self.first = 0
		self.selected = 0
		self.basicOff = 3

	def handleKey(self, k):
		if ord('\n') == k:
			s = self.sstore.getSessions()[self.selected]
			endall()
			ssh.Ssh().start(s)	
		elif curses.KEY_UP == k or ord('k') == k:
			if self.selected == self.first:
				self.scrollUp()
			else:
				self.selected = self.selected - 1

		elif curses.KEY_DOWN == k or ord('j') == k:
			last = self.first + self.cap
			total = len(self.sstore.getSessions())
			if last > total:
				last = total
			if self.selected == last - 1:
				self.scrollDown()
			else:
				self.selected = self.selected + 1

	def draw(self):
		ss = self.sstore.getSessions()

		first = self.first
		last = first + self.cap
		if last > len(ss):
			last = len(ss)

		for i in range(first, last):
			self.drawSession(i, ss[i])

		self.win.refresh()
	
	def drawSession(self, pos, s):
		if self.selected == pos:
			self.win.addstr(pos+1, self.basicOff, s.tostr(), 
					curses.A_REVERSE)
		else:
			self.win.addstr(pos+1, self.basicOff, s.tostr())

	def setSessionStore(self, sstore):
		self.sstore = sstore

	def scrollUp(self):
		pass
	def scrollDown(self):
		pass

class PropPane(Win):
	def __init__(self, parent, x, y, w, h, title=''):
		Win.__init__(self, parent, x, y, w, h, title)

class MainWin:
	def __init__(self, sessionpath, title='[TERM SSH]'):
		# set locale
		import locale
		locale.setlocale(locale.LC_ALL, '')

		# init default screen
		global _win
		_win = self.stdscr = stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		stdscr.keypad(1)
		stdscr.border(0)
		curses.curs_set(0)

		# set title
		(y, x) = stdscr.getmaxyx()
		stdscr.addstr(y-1, x/2-len(title)/2, title)

		self.width, self.height = x, y

		# create main panel
		mainX, mainY = 1, 1
		mainW, mainH = self.width * 3 / 5, self.height-5
		self.mainPane = MainPane(stdscr, mainX, mainY, 
				mainW, mainH, 'SESSION LIST')

		# create property panel
		propX, propY = mainX + mainW + 1, 1
		propW, propH = self.width - mainW - 3, mainH
		self.propPane = PropPane(stdscr, propX, propY, 
				propW, propH, 'PROPERTY')

		# create action panel
		actX, actY = 1, self.height - 4
		actW, actH = self.width-2, 3
		self.actPane= ActionPane(stdscr, actX, actY, actW, actH)

		self.selectedPane = self.mainPane

		# dummy store
		sstore = session_store.SessionStore()

		sstore.add(session.Session('0','127.0.0.1', 21, 'cj', '0'))
		sstore.add(session.Session('1','127.0.0.1', 21, 'zw', '0'))
		sstore.add(session.Session('2','127.0.0.1', 21, 'hw', '0'))
		sstore.add(session.Session('3','127.0.0.1', 21, 'ww', '0'))

		self.mainPane.setSessionStore(sstore)

	def loop(self):
		stdscr = self.stdscr
		while True:
			self.actPane.draw()
			self.propPane.draw()
			self.mainPane.draw()
			stdscr.refresh()

			k = stdscr.getch()
			if ord('\t') == k:
				shiftPane()
			elif curses.KEY_F3 == k:
				break
			else:
				self.selectedPane.handleKey(k)
		endall()
	def shiftPane(self):
		pass	
	
if __name__ == '__main__':
	pane = MainWin('')
	pane.loop()




