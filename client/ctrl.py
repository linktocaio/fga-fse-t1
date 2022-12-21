import time
import onoff

time_temp = time.time()

time_smoke = time.time()
last_smoke = False

time_alarm = time.time()
last_alarm = False

def ctrl(fila_prioridade, local_config):
    global time_smoke
    global last_smoke
    global time_temp
    global time_alarm
    global last_alarm

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
        for a in pin:
            if a["type"] == "fumaca":
                to_send = a

        if last_smoke:
            to_send["state"] = "1"
        else:
            to_send["state"] = "0"

        msg += str(to_send) + "\n"
        fila_prioridade.inserir(msg, 1)

    # ALARM
    send_temp = time.time() - time_alarm
    out = local_config["outputs"]

    for i in out:
        if i['tag'] == "alarme":
            if i["state"] == "1":
                if send_temp > 1 and onoff.get_alarm(local_config) != last_alarm:
                    last_alarm = not last_alarm
                    time_alarm = time.time()

                    msg = local_config["nome"] + ";"

                    pin = local_config["inputs"]
                    for a in pin:
                        if a["type"] == "janela" or a["type"] == "porta":
                            to_send = a

                    if last_alarm:
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

    if data_dict["type"] == "alarme":
        handle_alarme(data_dict, local_config, fila_prioridade)
        return



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

def handle_alarme(data_dict, local_config, fila_prioridade):
    msg = ""


    if data_dict["state"] == "1":
        if onoff.get_alarm(local_config) == 0:
            msg += local_config["nome"] + f";{data_dict}\n"

            out = local_config["outputs"]

            for i in out:
                if i['tag'] == "alarme":
                    i["state"] == "1"
                    return

        else:
            return

    if data_dict["state"] == "0":
        msg += local_config["nome"] + f";{data_dict}\n"

        out = local_config["outputs"]

        for i in out:
            if i['tag'] == "alarme":
                i["state"] == "0"
                return
