import socket, select, string, sys, json, os

#Helper function (formatting)
def display() :
	you="\33[33m\33[1m"+" You: "+"\33[0m"
	sys.stdout.write(you)
	sys.stdout.flush()

def main():

    if len(sys.argv) < 2:
        print("[-] Arquivo de configuracao deve ser informado!")
    else:
        try:
            file_config = open(sys.argv[1])
            local_config = json.load(file_config)
            file_config.close()
        except:
            print("[-] Arquivo de configuracao nao encontrado!")
            sys.exit()

    # ip_server = local_config["ip_servidor_central"]
    ip_server = "127.0.0.1"
    port_server = local_config["porta_servidor_central"]
    port_server = 5001
    
    #asks for user name
    name = input("\33[34m\33[1m CREATING NEW ID:\n Enter username: \33[0m")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    # connecting host
    try :
        s.connect((ip_server, port_server))
    except :
        print("[-] Erro, nao foi possivel se conectar ao servidor")
        sys.exit()

    #if connected
    s.send(name.encode())
    display()


    while 1:
        socket_list = [s]

        # Get the list of sockets which are readable
        rList, wList, error_list = select.select(socket_list , [], [], 0.5)
        
        for sock in rList:
            #incoming message from server
            if sock == s:
                data = sock.recv(4096).decode()
                if not data :
                    print('[-] Erro, voce foi desconectado do servidor inesperadamente')
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    display()
        
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg.encode())
                display()

        s.send("text\n".encode())
        s.send("text2\n".encode())

        display()

        

if __name__ == "__main__":
    main()