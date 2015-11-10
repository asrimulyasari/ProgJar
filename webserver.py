# ProgJar
Tugas 3

import threading
import socket
import time
import sys

def get_file(nama):
	myfile = open(nama)
	return myfile.read()


class MemprosesClient(threading.Thread):
	def __init__(self,client_socket,client_address,nama):
		self.client_socket = client_socket
		self.client_address = client_address
		self.nama = nama
		threading.Thread.__init__(self)
	
	def run(self):
		message = ''
		while True:
			data = self.client_socket.recv(32)
			if data:
				message = message + data #collect seluruh data yang diterima
				print message
						
				if (message.startswith("GET /1 HTTP/1.1")):
					self.client_socket.send(get_file('air-2.jpg'))
					break

				elif (message.startswith("GET /2 HTTP/1.1")):
					self.client_socket.send(get_file('terjun.jpg'))
					break

				elif (message.startswith("GET /3 HTTP/1.1")):
					self.client_socket.send(get_file('lala.jpg'))
					break

				elif (message.startswith("GET /4 HTTP/1.1")):
					self.client_socket.send(get_file('lili.jpg'))
					break

				elif (message.startswith("GET /5 HTTP/1.1")):
					self.client_socket.send(get_file('sw.jpg'))
					break

				elif (message.endswith("\r\n\r\n")):
					self.client_socket.send(get_file('step_32.jpg'))
					break
			else:
				break
		self.client_socket.close()
		


class Server(threading.Thread):
	def __init__(self):
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = ('localhost',9990)
		self.my_socket.bind(self.server_address)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.listen(1)
		nomor=0
		while (True):
			self.client_socket, self.client_address = self.my_socket.accept()
    			nomor=nomor+1
			#---- menghandle message cari client (Memproses client)
			my_client = MemprosesClient(self.client_socket, self.client_address, 'PROSES NOMOR '+str(nomor))
			my_client.start()
			#----


myserver = Server()
myserver.start()



