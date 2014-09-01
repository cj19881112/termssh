import curses
import curses.ascii

class TextField:
	def __init__(self, parent, title, x, y, n):
		self.parent, self.title = parent, title + ': '
		self.x, self.y, self.n = x, y, n
		self.content, self.edit = 'K.O.', False
		self.maxContent = self.n - len(self.title)

	def editable(self, st):
		self.edit = st
		self.parent.move(self.y, self.x + len(self.title))

	def handleKey(self, k):
		if curses.ascii.isalpha(k) or ord(' ') == k:
			if len(self.content) < self.maxContent:
				self.content = self.content + chr(k)
		else:
			if curses.KEY_BACKSPACE == k and len(self.content) > 0:
				self.content = self.content[:-1]
	
	def padding(self):
		return ' ' * (self.n - len(self.title+self.content))

	def draw(self):
		self.parent.addstr(self.y, self.x, self.title)
		if self.edit:
			self.parent.addstr(self.y, self.x+len(self.title), 
					self.content + self.padding(), curses.A_REVERSE)
		else:
			self.parent.addstr(self.y, self.x+len(self.title),
					self.content + self.padding())
	
	def getstr(self):
		return self.content


def endall():
	curses.nocbreak()
	scr.keypad(0)
	curses.echo()
	curses.endwin()

if __name__ == '__main__':
	import locale
	locale.setlocale(locale.LC_ALL, '')

	scr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	scr.keypad(1)
	scr.border(0)
	curses.curs_set(0)
	scr.border(0)
	#############################
	tb = TextField(scr, 'addr', 10, 10, 20)
	tb.editable(True)
	while True:
		tb.draw()
		scr.refresh()
		k = scr.getch()		
		if curses.KEY_F4 == k:
			break
		elif ord('\n') == k:
			break;
		else:
			tb.handleKey(k)
	#############################
	endall()
	print(tb.getstr())






