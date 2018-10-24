import socket, threading
import hashlib
import time


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, cont):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self._cont = cont
        print('\n_______________________________________________________\n')
        print("New connection added: ", clientAddress)
        print("Server connections:", self._cont)

    def run(self):

        with open('password.txt', 'r') as arq:
            list_password = []
            for line in arq:
                list_password.append(line[:-1])

        hash = "6521"
        hash = hashlib.sha1(hash.encode()).hexdigest()
        print("\nHash:", hash)

        self.csocket.sendall(hash.encode())

        div = int(len(list_password)/5)

        envia_pass = []
        for i in range(len(list_password)):
            envia_pass.append(list_password[i]+';')

        for i in range(len(envia_pass[div * (self._cont - 1): div * self._cont])):
            self.csocket.sendall(envia_pass[div * (self._cont - 1): div * self._cont][i].encode())

        while True:
            data = self.csocket.recv(1024)
            msg = data.decode()
            aux = msg.split(";")[-1]
            print("\nfrom client {}:".format(clientAddress), msg)
            break
        print("\nClient at ", clientAddress, " disconnected...")
        time.sleep(1)
        self.csocket.close()


LOCALHOST = "192.168.102.121"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("\nServer started")
print("Waiting for client request..")
time.sleep(0.2)

cont = 0
while True:
    cont+=1
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock, cont)
    newthread.start()
