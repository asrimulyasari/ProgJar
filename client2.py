# ProgJar
#Tugas 2

# chatclient.py

import sys
import socket
import select
 
def chat_client():
    if(len(sys.argv) < 3) :
        print 'Usage : python chatclient.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    print 'anda tersambung, silahkan masuk terlebih dahulu'
    print 'untuk masuk, silahkan ketikkan login dengan huruf kecil'
    cin=raw_input()
    if cin == "login" :
	sys.stdout.write('ketikkan nama anda '); sys.stdout.flush()
	cin=raw_input()
	if cin == '' :
	   sys.exit()
	try :
           s.connect((host, port))
	except :
           print 'Unable to connect'
           sys.exit()
	print 'ketikkan tujuan [nama] [pesan] untuk mengirim pesan kepada orang tertentu'
	print 'ketikkan semua [pesan] untuk mengirim pesan ke semua pengguna aktif'
	print 'list untuk melihat pengguna aktif'
	print 'anda dapat mengirim pesan'
	sys.stdout.write(cin+" : "); sys.stdout.flush()
	s.send(cin+" : "+cin)     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write(cin+" : "); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
		msg = cin+ " : "+msg
                s.send(msg)
                sys.stdout.write(cin+" : "); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())
