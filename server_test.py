import socket
import sys
import secrets

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	data = f"Hello! {secrets.token_hex(8)}".encode("UTF-8")
	addr = ("127.0.0.1", 6669)
	s.sendto(data, addr)
	print(f"Sent '{data.decode('UTF-8')}' to {':'.join(map(str, addr))}")
	data, addr = s.recvfrom(1024)
	print(f"Received '{data.decode('UTF-8')}' from {':'.join(map(str, addr))}")
	return 0

if __name__ == "__main__":
	sys.exit(main())