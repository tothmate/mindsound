from socket import socket, AF_INET, SOCK_STREAM
from json import dumps, loads
from time import sleep
from random import randint
from phue import Bridge


def next():
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(('127.0.0.1', 13854))
	s.send(dumps({'enableRawOutput': False, 'format': 'Json'}))

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
		sleep(1/512.0)

from phue import Bridge
b = Bridge('192.168.2.104')
b.connect()
#l1 = b.lights[0]
#l1.transitiontime = 0
#l1.saturation = 255

l2 = b.lights[1]
l2.transitiontime = 10
l2.saturation = 255

l3 = b.lights[2]
l3.transitiontime = 10
l3.saturation = 255

buf = []

for input in next():
	#if 'blinkStrength' in input:
	#	l1.on = False
	#	sleep(0.2)
	#	l1.on = True
	#if 'rawEeg' in input:
	#	buf.append(abs(int(input['rawEeg'])))
	#	if len(buf) == 256:
	#		l1.hue = (sum(buf) / float(len(buf))) / 2048 * 65535
	#		print l1.hue
	#		buf = []
	if 'eSense' in input:
		print input['eSense']
		#l2.hue = input['eSense']['attention'] / 100.0 * 32000
		#l3.hue = (input['eSense']['meditation'] / 100.0 * 25000) + 30000
		att = input['eSense']['attention']
		med = input['eSense']['meditation']
		bri = 255 - (med / 100.0 * 255)
		sat = (med + att) / 200.0 * 255
		b.set_light([2, 3], {'transitiontime': 10, 'bri': int(bri), 'sat': int(sat), 'hue': 48000})




