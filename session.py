"""
key session property
"""

class InvalidFormat(Exception):
	pass

def make_session(line):
	opts = line.split(' ')
	if 6 != len(opts):
		raise InvalidFormat 
	return Session(opts[0], opts[1], opts[2], opts[3], opts[4], opts[5])


class Session:
	def __init__(self, name, ip, port, user, passwd, encoding='utf-8'):
		self.name, self.ip, self.port = name, ip, port
		self.user, self.passwd, self.encoding = user, passwd, encoding
	def __str__(self):
		return '%s %s %s %s %s %s'%(self.name,self.ip,self.port,
				self.user,self.passwd,self.encoding)
	def tostr(self):
		return self.__str__()
		
if __name__ == '__main__':
	s = Session('develop', '192.168.1.1', 1234, 'zw', '123')
	print(s.tostr() + '\n')

