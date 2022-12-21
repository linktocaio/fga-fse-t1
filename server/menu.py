import conn

temp = 0
hum = 0

def print_info(temperature, humidity, people_counter):
	print("\n====== Dados ======\n")
	print("Temperatura: ", temperature)
	print("Umidade: ", humidity)
	print("Contador de Pessoas: ", people_counter)
	print("\n====== ===== ======\n")


def clear():
	print(chr(27) + "[2J")

def main():
	while True:
		msg = ""
		i = 0
		foo = {}
		clear()
		print_info(temp, hum,0)

		main_list = conn.record.copy()

		for client in main_list:
			foo[main_list[client]["nome"]] = main_list[client]

		if len(foo) > 0:
			print("configuracoes do andar: ")

		for key in foo.keys():
			print(i+1, "- %s" % key)
			i+=1
		
		print("\n0 - Atualizar")
		print("X - Sair\n")

		opt_main = input()
		try: 
			opt_main = int(opt_main)
			if opt_main > i or opt_main < 0:
				clear()
				input("digite opcao valida")
				continue
			if opt_main == 0:
				continue

			keys = list(foo.keys())
			menu_andar(foo[keys[opt_main-1]], f"{keys[opt_main-1]};")
			
		except:
			if opt_main == "x":
				break
			# clear()
			# input("except")
			

def menu_andar(andar, msg):
	clear()
	tipos = []
	
	for tipo in andar.values():
		if type(tipo) == list:
			for item in tipo:
				if item['type'] not in tipos:
					tipos.append(item['type'])

	i = 0
	for item in tipos:
		print(i+1, "- %s" % item)
		i+=1

	print("\n0 - Voltar\n")

	try: 
		opt_andar = int(input())

		if opt_andar > i or opt_andar < 0:
			clear()
			if opt_andar != 0:
				input("digite opcao valida")
			return
		
		if opt_andar == 0:
			return

		items = []
		for tipo in andar.values():
			if type(tipo) == list:
				for item in tipo:
					if item['type'] == tipos[opt_andar-1]:
						items.append(item)

		menu_tipo(items, msg)
	except:
		pass
		# clear()
		# input("except")
	

def menu_tipo(items, msg):
	clear()
	i = 0
	for item in items:
		print(i+1, "- %s" % item["tag"], "- %s" % item["state"])
		i+=1

	print("\n0 - Voltar\n")

	opt_tipo = input("> ")
	try: 
		opt_tipo = int(opt_tipo)
		if opt_tipo > i or opt_tipo < 0:
			clear()
			if opt_tipo != 0:
				input("digite opcao valida")
			return
			
		if opt_tipo == 0:
			return

		item_aux = items[opt_tipo-1].copy()

		if item_aux["state"] == "1":
			item_aux["state"] = "0"

		elif item_aux["state"] == "0":
			item_aux["state"] = "1"

		msg = f"{msg}{item_aux};"

		conn.fila_prioridade.inserir(msg, 1)

	except:
		pass
		# clear()
		# input("except")