import session

class Ssh:
	def start(self, s):
		import os
		cmd = 'ssh_impl.expect'
		# ssh_impl.expect ip user pass encoding
		os.execlp(cmd, cmd, s.ip, s.user, s.passwd, s.encoding)

if __name__ == '__main__':
	Ssh().start(session.Session('develop', '127.0.0.1',
				22, 'cj', '0'))
