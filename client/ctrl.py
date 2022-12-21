import time
import onoff

time_smoke = time.time()
time_temp = time.time()
last_smoke = False

def ctrl(fila_prioridade, local_config):
    global time_smoke
    global time_temp
    global last_smoke

    # TEMP
    send_temp = time.time() - time_temp
    if send_temp > 2:
        time_temp = time.time()

        msg = local_config["nome"] + ";"
        to_send = local_config["sensor_temperatura"][0]

        to_send["state"] = onoff.get_TH(local_config)
        msg += str(to_send) + "\n"
        fila_prioridade.inserir(msg, 1)

    # SMOKE
    send_temp = time.time() - time_smoke
    if send_temp > 1 and onoff.get_smoke(local_config) != last_smoke:
        last_smoke = not last_smoke
        time_smoke = time.time()

        msg = local_config["nome"] + ";"

        pin = local_config["inputs"]
        for a in pin["inputs"]:
            if a["type"] == "fumaca":
                to_send = a

        if last_smoke:
            to_send["state"] = "1"
        else:
            to_send["state"] = "0"

        msg += str(to_send) + "\n"
        fila_prioridade.inserir(msg, 1)

def handle_recv(data_dict, local_config, fila_prioridade):

    if data_dict["type"] == "lampada":
        handle_lampada(data_dict, local_config, fila_prioridade)
        return
    
    if data_dict["type"] == "projetor":
        handle_projetor(data_dict, local_config, fila_prioridade)
        return

    if data_dict["type"] == "ar-condicionado":
        handle_ar(data_dict, local_config, fila_prioridade)
        return

    # if data_dict["type"] == "alarme":
    #     handle_lampada(data_dict, local_config, fila_prioridade)
    #     return
    # print(data_dict)


def handle_lampada(data_dict, local_config, fila_prioridade):
    msg = ""

    if onoff.turn_led(data_dict):
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
        except:
            return

        fila_prioridade.inserir(msg, 1)

def handle_projetor(data_dict, local_config, fila_prioridade):
    msg = ""

    if onoff.turn_led(data_dict):
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
        except:
            return

        fila_prioridade.inserir(msg, 1)

def handle_ar(data_dict, local_config, fila_prioridade):
    msg = ""

    if onoff.turn_led(data_dict):
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
        except:
            return

        fila_prioridade.inserir(msg, 1)