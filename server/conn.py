import socket, select, json, sys, heapq

connected_list = []
server_socket = None
record = {}

qwe = 1
def display() :
	global qwe
	qwe +=1 
	you="\33[33m\33[1m"+" You: "+"\33[0m" + str(qwe)
	sys.stdout.write(you)
	sys.stdout.flush()


class FilaDePrioridade:

	def __init__(self):
		self._fila = []
		self._indice = 0

	def inserir(self, item, prioridade):
		heapq.heappush(self._fila, (-prioridade, self._indice, item))
		self._indice += 1

	def remover(self):
		return heapq.heappop(self._fila)[-1]

	def isEmpty(self):
		return len(self._fila) == 0

fila_prioridade = FilaDePrioridade()

#Function to send message to all connected clients
def send_to_all (sock, message):
	global connected_list
	global server_socket
	#Message not forwarded to server and sender itself
	message = message.encode()
	for socket in connected_list:
		if socket != server_socket and socket != sock:
			try:
				socket.send(message)
			except:
				# if connection not available
				socket.close()
				connected_list.remove(socket)

def update(andar, msg):
	s = msg.split(";")
	d = str(s[1])
	d = d.replace("'", '"')
	d = json.loads(d)

	if andar["nome"] == s[0]:
		for tipo in andar.values():
			if type(tipo) == list:
				for item in tipo:
					if item["tag"] == d['tag']:
						item['state'] = d['state']

def server_init():

	global connected_list
	global server_socket
	
	#dictionary to store address corresponding to username
	global record
	# List to keep track of socket descriptors
	
	buffer = 4096
	port = 5001

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse port after ctrl+c
	server_socket.bind(("localhost", port))
	server_socket.listen(10) #listen atmost 10 connection at one time

	# Add server socket to the list of readable connections
	connected_list.append(server_socket)

	print("[i] Server Online")

	while 1:
		socket_list = [sys.stdin] + connected_list
        # Get the list sockets which are ready to be read through select
		rList, wList, error_sockets = select.select(socket_list, [], [], 0.1)
		# send_to_all(server_socket, "test")

		for sock in rList:
			#New connection
			if sock == server_socket:
				# Handle the case in which there is a new connection recieved through server_socket
				sockfd, addr = server_socket.accept()

				new_conn_conf_file = sockfd.recv(buffer).decode()
				new_client_conf = json.loads(new_conn_conf_file)

				connected_list.append(sockfd)
				record[addr] = ""
				# print("record and conn list ", record, connected_list)
                
                #if repeated username
				if new_client_conf in record.values():
					sockfd.send(f"\n[-] Andar com essas configuracoes ja conectado ao servidor, {addr}\n".encode())
					del record[addr]
					connected_list.remove(sockfd)
					sockfd.close()
					continue

				else:
                    #add name and address
					record[addr] = new_client_conf
					print("\n[+] Novo andar conectado: (%s, %s)" % addr," [",record[addr]["nome"],"]\n")
					# sockfd.send("\33[32m\r\33[1m Welcome to chat room. Enter 'tata' anytime to exit\n\33[0m".encode())
					# send_to_all(sockfd, "\33[32m\33[1m\r "+name+" joined the conversation \n\33[0m")

			#Some incoming message from a client
			else:
				# Data from client
				try:
					data1 = sock.recv(buffer).decode()
					# print( "sock is: ",sock)
					data = data1[:data1.index("\n")] # para nao entrar em loop ao interromper o client com ctrl+c
					# print "\ndata received: ",data
                    
                    #get addr of client sending the message
					i, p = sock.getpeername()
					update(record[(i,p)], data1)
					# print("[+] Comando recebido de (%s, %s)" % (i,p)," [",record[(i,p)]["nome"],"] :", data)
					
					# if data == "tata":
					# 	msg="\r\33[1m"+"\33[31m "+record[(i,p)]+" left the conversation \33[0m\n"
					# 	send_to_all(sock,msg)
					# 	print("Client (%s, %s) is offline" % (i,p)," [",record[(i,p)],"]")
					# 	del record[(i,p)]
					# 	connected_list.remove(sock)
					# 	sock.close()
					# 	continue

					# else:
					# 	msg="\r\33[1m"+"\33[35m "+record[(i,p)]+": "+"\33[0m"+data+"\n"
					# 	send_to_all(sock,msg)
            
                #abrupt user exit
				except:
					try:
						(i, p) = sock.getpeername()
						# send_to_all(sock, "\r\33[31m \33[1m"+record[(i,p)]+" left the conversation unexpectedly\33[0m\n")
						print("\n[-] Andar desconectado: (%s, %s)" % addr," [",record[(i,p)]["nome"],"]\n")
						del record[(i, p)]
						connected_list.remove(sock)
						sock.close()
						continue
					
					#send mensage to clients
					except:
						if not fila_prioridade.isEmpty():
							msg = fila_prioridade.remover()
							send_to_all(sock, msg)
						# msg=sys.stdin.readline()
						# send_to_all(sock, msg)
						
		# display()

	server_socket.close()
