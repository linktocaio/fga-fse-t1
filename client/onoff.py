from gpiozero import LED, InputDevice
import Adafruit_DHT

def turn_led(data_dict):
	led = LED(data_dict["gpio"])

	if data_dict["state"] == "1":
		led.on()
		return True
	elif data_dict["state"] == "0":
		led.off()
		return True

	return False

def turn_projetor(data_dict):
	led = LED(data_dict["gpio"])

	if data_dict["state"] == "1":
		led.on()
		return True
	elif data_dict["state"] == "0":
		led.off()
		return True

	return False

def turn_ar(data_dict):
	led = LED(data_dict["gpio"])

	if data_dict["state"] == "1":
		led.on()
		return True
	elif data_dict["state"] == "0":
		led.off()
		return True

	return False

def get_TH(local_config):
	pin = local_config["sensor_temperatura"][0]
	pin = pin["gpio"]

	dht = Adafruit_DHT.DHT22

	humidity, temp = Adafruit_DHT.read_retry(dht, pin)

	if humidity is not None and temp is not None:
		return str(temp) + "," + str(humidity)
	return "erro"

def get_smoke(local_config):
	pin = local_config["inputs"]

	for a in pin:
		if a["type"] == "fumaca":
			pin  = a["gpio"]

	b = InputDevice(pin)
	return b.value

def get_alarm(local_config):
	pin = local_config["inputs"]

	for a in pin:
		if a["type"] == "janela" or a["type"] == "porta":
			pin  = a["gpio"]
			if InputDevice(pin).value == 1:
				return 1

	return 0

