from Crypto.PublicKey import RSA
import socket

################## Get Keys ###################
fd = open("server_key.public",'r')
pub_key = RSA.importKey(fd.read())
fd.close()

fd = open("server_key.private",'r')
pri_key = RSA.importKey(fd.read())
fd.close()

################# Create Socket ##############
sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sockfd.bind(("",4444))
sockfd.listen(1)
clientfd , addr = sockfd.accept()
print addr , "Connected"

################ Send and Recv Keys ############

client_public_key = clientfd.recv(2048)
print client_public_key
client_public_key = RSA.importKey(client_public_key)
clientfd.send(pub_key.exportKey())

################ recv and send messages ##############
while True:
    try:
        recv = clientfd.recv(1024)
        recv = pri_key.decrypt(recv)
        if(recv == 'q'):
            break
        print recv

        msg = raw_input(": ")
        encrypt_msg = client_public_key.encrypt(msg,1320)[0]
        clientfd.send(encrypt_msg)
        if(msg == 'q'):
            encrypt_msg = client_public_key.encrypt('q',1320)[0]
            clientfd.send(encrypt_msg)
            break
    except:
        encrypt_msg = client_public_key.encrypt('q',1320)[0]
        clientfd.send(encrypt_msg)
        break
############################################

sockfd.close()
clientfd.close()

