import socket
import sys

class Ng_PlayerClient:
	def __init__(self, sock):
		self._s = sock

	def send(self, data):
		socket.socket.send(self._s, data)

class NetGame:
	def __init__(self):
		self.state

class NetEntity:
	def __init__(self):
		self.x
		self.y

class NetPlayer(NetEntity):
	def __init__(self):
		self.id

class NetProjectile(NetEntity):
	def __init__(self):
		self.owner_id

def main():
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("127.0.0.1", 6669))
	s.setblocking(False) # s.settimeout(1)

	while True:
		try:
			data, addr = s.recvfrom(1024)
		except BlockingIOError: # TimeoutError
			continue
		else:
			print(f"Received '{data.decode('UTF-8')}' from {':'.join(map(str, addr))}")
			s.sendto(data, addr)
			print(f"Sent '{data.decode('UTF-8')}' to {':'.join(map(str, addr))}")

	return 0

if __name__ == "__main__":
	sys.exit(main())