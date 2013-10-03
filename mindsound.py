from socket import socket, AF_INET, SOCK_STREAM
from json import dumps, loads
from pyo import Server, VarPort, SineLoop
from math import log
from time import sleep
from random import randint


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


_ = Server().boot().start()

fr = VarPort(value=0, time=0.2)
sl = SineLoop(freq=fr, mul=0.5).out()

for input in next():
	if 'rawEeg' in input:
		fr.value = input['rawEeg'] + 400