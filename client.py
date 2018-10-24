import socket
import time
import hashlib
# import cv2

SERVER = "192.168.102.121"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


hash_1 = client.recv(40)
print("\nFrom Server :", hash_1.decode())

time.sleep(2)
list_pass_recv = client.recv(20000)

list_pass = str(list_pass_recv[:-1].decode()).split(';')

print("\nTamanho do banco de hashs recebido:", len(list_pass))

pass_sha1 = []
for i in range(len(list_pass)):
    pass_sha1.append(((hashlib.sha1(list_pass[i].encode()).hexdigest())))

val = True
while val:

    for i in range(len(pass_sha1)):
        if (hash_1.decode() == pass_sha1[i]):
            string = "Hash found, bro!!! A senha é: {}".format(list_pass[i])
            print(string)
            client.send(string.encode())
            # Display image
            # img = cv2.imread('im-fuck.jpeg')
            # cv2.imshow('Achei o Hash', img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            val = False
            break
        if((i + 1) == len(pass_sha1)):
            print("\nA senha não está nesse segmento de hashs.")
            string = "Puts, do not found, bro."
            client.send(string.encode())
            val = False

time.sleep(1)
client.close()
