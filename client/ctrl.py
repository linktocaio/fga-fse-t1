import time
import onoff


time_start = time.time()
time_temp = time.time()

i = ""

def ctrl(fila_prioridade, local_config):
    global time_start
    global time_temp
    global i

    send_temp = time.time() - time_temp
    if send_temp > 2:
        time_temp = time.time()
        msg = "Térreo;{'type': 'dth22', 'tag': 'Sensor de Temperatura e Umidade', 'gpio': 20, 'state': '99'}\n"
        fila_prioridade.inserir(msg, 1)

def handle_recv(data_dict, local_config, fila_prioridade):

    if data_dict["type"] == "lampada":
        handle_lampada(data_dict, local_config, fila_prioridade)
        return
    # print(data_dict)


def handle_lampada(data_dict, local_config, fila_prioridade):
    msg = ""
    # input(data_dict)

    if onoff.turn_led(data_dict): #retorno ligar_lampada()
        item_aux = data_dict.copy()

        if item_aux["state"] == "1":
            item_aux["state"] = "0"

        elif item_aux["state"] == "0":
            item_aux["state"] = "1"

        try:
            for value in local_config.values():
                if type(value) == list:
                    for item in value:
                        if item['tag'] == item_aux["tag"]:
                            item['state'] = str(item_aux)
                            break

            msg += local_config["nome"] + f";{data_dict}\n"
            # input(msg)
        except:
            return
        # msg += f";{item_aux}"

        fila_prioridade.inserir(msg, 1)
