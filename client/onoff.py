from gpiozero import LED

def turn_led(data_dict):
	led = LED(data_dict["gpio"])

	if data_dict["state"] == "1":
		led.on()
		return True
	elif data_dict["state"] == "0":
		led.off()
		return True

	return False
