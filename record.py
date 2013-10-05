from socket import socket, AF_INET, SOCK_STREAM
from json import dumps, loads


def next():
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(('127.0.0.1', 13854))
	s.send(dumps({'enableRawOutput': True, 'format': 'Json'}))

	while True:
		buf = ''
		cur = s.recv(1)
		while cur != '\r':
			buf += cur
			cur = s.recv(1)
		try:
			yield loads(buf)
		except ValueError:
			pass


for input in next():
	if 'rawEeg' in input:
		print input['rawEeg']
