import pyaudio
from time import sleep, time
import SocketServer
from json import dumps
import struct
import threading
import sys
from phue import Bridge

signal = 0

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		global signal
		while True:
			self.request.sendall(dumps({'rawEeg': signal}) +'\r')
			sleep(1024/44100.0)

	def frame_received_callback(self, frame_data, frame_len, timestamp, is_key_frame):
		try:
			self.request.sendall(frame_data[:frame_len])
		except:
			self.alive = False

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

SocketServer.TCPServer.allow_reuse_address = True
server = ThreadedTCPServer(('127.0.0.1', 13854), ThreadedTCPRequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()

pa = pyaudio.PyAudio()
#print pa.get_device_info_by_index(2)
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, input_device_index=2, frames_per_buffer=10240)

b = Bridge('192.168.2.119')
b.connect()
light = b.lights[2]
light.transitiontime = 3
light.hue = 48000
light.saturation = 180
light.on = True

history = []
start = time()

def set_lights():
	last_bri = 0
	while True:
		last_signal, min_signal, max_signal = history[-1], min(history), max(history)
		bri = int((last_signal - min_signal) * 255.0 / max(1, max_signal - min_signal))
		light.brightness = 0 if bri < 127 else 255
		sys.stdout.write("%.6f %d %d %d %d %d \n" % (time() - start, last_signal, min_signal, max_signal, 0 if bri < 127 else 255, bri))
		sleep(0)

light_thread = threading.Thread(target=set_lights)
light_thread.daemon = True

# samplerate/(max_bpm/60*nyquist)
bufferSize = 44100/(200/60*2)
historySize = 10

while True:
	signal = struct.unpack("<%dh" % bufferSize, stream.read(bufferSize))[0]
	if len(history) == historySize - 1:
		light_thread.start()
	if len(history) == historySize:
		history.pop(0)
	history.append(signal)

	#sys.stdout.write("%.6f %d\n" % (time() - start, signal))
	#sys.stdout.flush()
	#if time() - start > 20:
	#	break
