from gpiozero import LED
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