# ProgJar
#Tugas 2

# chatserver.py
 
import sys
import socket
import select

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009
aa = []
username = []
index = 0
MAPPING = {}
DECODE = {}

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) tersambung" % addr
                 
                broadcast(server_socket, sockfd, "[%s, %s] bergabung dalam chatting room\n" % addr)
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data: 
			cmd = data.split()
			global MAPPING
			MAPPING[cmd[0]]=sockfd
			global DECODE
			DECODE[sockfd]=cmd[0]
			if cmd[2] =="menuju" :
				send_to(cmd[3],cmd)
			elif cmd[2] =="list" :
				userlist(sock,server_socket)		              
			elif cmd[2]=="semua" :
				data2 = "\n" + cmd[0] + " : "
				count = 0
				while count !=len(cmd):
					if count >2:
						data2 += (cmd[count]+" ")
					count+=1
				data2 += "\n"
				broadcast(server_socket, sock, "\r"+data2 )
			else:
					broadcast1()
                        # there is something in the socket
			data2 =sock.recv(5)
			#print "dapet : ",data2
#fitur login
			if data2 =='login ' :
				username.append(sock.recv(5))
				list.append(sock)
			# print "Username" ,username.pop()
			if data2 =='send' :
	       			data3=sock.recv(5)
				#print"index ", username.index(data3)
				#print "oke"
				tujuan=aa[username.index(data3)]
				#print tujuan
				data4=sock.recv(RECV_BUFFER)
				#print data4
				sock.sendto(data4,tujuan)
				print tujuan
			if data2 =='list' :
				for index in range(len(username)) :
					sock.send("\n")
					sock.send(username[index])
					# print username[index]
			if data2 =='broadcast' :
				data4=sock.recv(RECV_BUFFER)
				bb=aa.index(sock.getpeername())
				print bb
				#print aa.index(bb)

                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                    #else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) sedang offline\n" % addr) 

                # exception 
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) sedang offline\n" % addr)
                    continue

    server_socket.close()
    
# broadcast semua pesan ke client yg sedang tersambung
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:

def send_to(destination,message):
	data = "\n"+message[0] + " : "
	count = 0
	while count!=len(message):
		if count>3 :
			data+=(message[count]+" ")
		count +=1
	data += "\n"
	socket = MAPPING[destination]
	try :
		socket.send(data)
	except :
		socket.close()
		if socket in SOCKET_LIST :
			SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())         
