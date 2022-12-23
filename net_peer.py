import socket
import sys
import time

class Network:
	class Game:
		def __init__(self):
			self.state

	class Entity:
		def __init__(self):
			self.x
			self.y

	class Player(Entity):
		def __init__(self):
			self.id

	class Projectile(Entity):
		def __init__(self):
			self.owner_id

	class Message:
		"""
		Format:
			check = message[0:4] (Verification for checking packet, should always be \x69\x13\x77\x69)
			length = message[4:8] (Length of total message)
			type = message[8:10] (Type of the message)
			data = message[10:]
		"""
		class GamePing:
			"""
			Format:
				token = data[0:4] (random token)
			"""
			def __init__(self, data):
				self.data = data
				# self.player = Network.Player()

		class PlayerJoin:
			"""
			Format:
				playerId = data[0:1] (ID of the joining player)
			"""
			def __init__(self, data):
				self.data = data
				# self.player = Network.Player()

		class PlayerLeave:
			"""
			Format:
				playerId = data[0:1] (ID of the leaving player)
			"""
			def __init__(self, data):
				self.data = data
				# self.player = Network.Player()

		class EntitySync:
			def __init__(self, data):
				self.data = data
				# self.entity = Network.sEntity()

		types = {0: GamePing, 1: PlayerJoin, 2: PlayerLeave, 3: EntitySync}

		def parse(message):
			pass

	def queue_message():
		pass

def main():
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("127.0.0.1", 6669))
	s.setblocking(False) # s.settimeout(1)

	while True:
		try:
			data, addr = s.recvfrom(1024)
		except BlockingIOError: # TimeoutError
			time.sleep(0.001)
			continue
		else:
			print(f"Received '{data.decode('UTF-8')}' from {':'.join(map(str, addr))}")
			s.sendto(data, addr)
			print(f"Sent '{data.decode('UTF-8')}' to {':'.join(map(str, addr))}")

	return 0

if __name__ == "__main__":
	sys.exit(main())