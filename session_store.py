"""
store sessions
"""

import session

class SessionStore:
	def __init__(self):
		self.sessions = {}
	def add(self, session):
		self.sessions[session.name] = session
	def delete(self, name):
		self.sessions[name] = None
	def getSessions(self):
		return [x for x in self.sessions.values() if x != None]
	# name ip port uname passwd encoding
	def load(self, path):
		self.path = path
		for line in open(path):
			line = line[:-1] # erase '\n' 
			self.add(session.make_session(line))
	def save(self, path=None):
		if path is None:
			save_path = self.path
		else:
			save_path = path
		with open(save_path, 'w') as f:
			for s in self.sessions():
				f.write(s.tostr() + '\n')

if __name__ == '__main__':
	store = SessionStore()
	store.load('example/session0')
	store.save('example/session1')


