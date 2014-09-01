import os

confs={}

def loadConfig(path):
	with open(path) as f:
		for line in f:
			[key, val] = line[:-1].split('=')
			confs[key] = val


def sessionFilePath():
	return os.path.expanduser(confs['session_store_path'])

loadConfig(os.path.expanduser('~/.termsshrc'))

