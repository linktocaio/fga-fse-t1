import conn, menu, time
from threading import Thread

if __name__ == "__main__":

	thread = Thread(target = conn.server_init)
	thread.start() 
	menu.main()
	thread.join()
	print("[-] exiting")