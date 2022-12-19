import socket, select, string, sys, json, os,heapq
import ctrl

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


#Helper function (formatting)
# def display() :
# 	you="\33[33m\33[1m"+" You: "+"\33[0m"
# 	sys.stdout.write(you)
# 	sys.stdout.flush()


def init_json(andar):
	for tipo in andar.values():
		if type(tipo) == list:
			for item in tipo:
				item["state"] = "0"

	return andar


def handle_recv(data, local_config, fila_prioridade):
	s = data.split(";")
	d = str(s[1])
	d = d.replace("'", '"')
	d = json.loads(d)

	if local_config["nome"] == s[0]:
		ctrl.handle_recv(d, local_config, fila_prioridade)

def main():

	if len(sys.argv) < 2:
		print("[-] Arquivo de configuracao deve ser informado!")
	else:
		try:
			file_config = open(sys.argv[1])
			local_config = json.load(file_config)
			local_config = init_json(local_config)
			file_config.close()
		except:
			print("[-] Arquivo de configuracao nao encontrado!")
			sys.exit()

	# ip_server = local_config["ip_servidor_central"]
	ip_server = "127.0.0.1"
	# port_server = local_config["porta_servidor_central"]
	port_server = 5001

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	
	# connecting host
	try :
		s.connect((ip_server, port_server))
	except :
		print("[-] Erro, nao foi possivel se conectar ao servidor")
		sys.exit()

	#if connected
	s.send(json.dumps(local_config, ensure_ascii=False).encode())

	fila_prioridade = FilaDePrioridade()

	while 1:
		socket_list = [s]

		# Get the list of sockets which are readable
		rList, wList, error_list = select.select(socket_list , [], [], 0.1)
		
		for sock in rList:
			#incoming message from server
			if sock == s:
				data = sock.recv(4096).decode()
				if not data :
					print('[-] Erro, voce foi desconectado do servidor inesperadamente')
					sys.exit()
				else :
					handle_recv(data, local_config, fila_prioridade)


		ctrl.ctrl(fila_prioridade, local_config)
		if not fila_prioridade.isEmpty():
			s.send(fila_prioridade.remover().encode())


if __name__ == "__main__":
	main()