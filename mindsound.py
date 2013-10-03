from socket import socket, AF_INET, SOCK_STREAM
from json import dumps, loads
from pyo import Server, VarPort, Sine
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


def fake_next():
	while True:
		yield {'rawEeg': randint(-2047, 2048)}
		sleep(0.1)


_ = Server().boot().start()
fr = VarPort(value=500, time=0.2)
sl = Sine(freq=fr, mul=0.5).out()

for input in next():
	if 'rawEeg' in input:
		fr.value = input['rawEeg'] + 400
