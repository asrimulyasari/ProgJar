# ProgJar
#Tugas 2

# chatclient.py

import sys
import socket
import select
import time
import string

host = 'localhost'
port = 9999
 
def client():
     
    # membuat TCP/IP socket
	x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # terhubung dengan remote host
	try :
		x.connect((host, port))
	except :
		print 'Klien gagal terhubung'
		sys.exit()
     
	print 'Klien sudah terhubung. Silahkan mengobrol :)'
	sys.stdout.write(' '); sys.stdout.flush()
     
	while True:
		socket_list = [sys.stdin, x]
		 
		# Get the list sockets which are readable
		ready_to_read,ready_to_write,in_error = select.select(socket_list, [], [])
		 
		for sock in ready_to_read:      
		
			if sock == x:
				# incoming message from remote server, x
				data = sock.recv(4096)
				if not data :
					print '\nDisconnected from chat server'
					sys.exit()
				else :
					sys.stdout.write(data)
					sys.stdout.write(' '); sys.stdout.flush()     
			
			else :
				# user memasukkan pesan
				msg = []
				temp = sys.stdin.readline()
				temp1 = string.split(temp[:-1])
				
				d=len(temp1)
				if temp1[0]=="login" :
					if d>2:
						print('Username salah')
					elif d<2:
						print('Login memerlukan username')
					else:
						x.send(temp)
				
				elif temp1[0]=="list" :
					if d>1:
						print('Perintah salah')
					else:
						x.send(temp)

				elif temp1[0]=="sendto" :
					if d<3:
						print('Perintah salah')
					else:
						x.send(temp)
						
				elif temp1[0]=="sendtoall" :
					if d<2:
						print('Perintah salah')
					else:
						x.send(temp)
						
				else:
					print ('Perintah salah')

				sys.stdout.write(' '); sys.stdout.flush() 

client()
