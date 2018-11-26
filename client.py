from Crypto.PublicKey import RSA
import socket



##################### Get Keys ####################

fd = open("client_key.public",'r')
pub_key = RSA.importKey(fd.read())
fd.close()

fd = open("client_key.private",'r')
pri_key = RSA.importKey(fd.read())
fd.close()

################### Create Socket ###################
IP = raw_input("Enter IP: ")
sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    sockfd.connect((IP,4444))
except:
    print "Server not found"
    exit()

print IP , "Connected"

################ Send and Get Key ####################
sockfd.send(pub_key.exportKey())

server_public_key = sockfd.recv(2048)
print server_public_key
server_public_key = RSA.importKey(server_public_key)

############### recv and send ########################

while(True):
    try:
        msg = raw_input(": ")
        encrypt_msg = server_public_key.encrypt(msg,5031)[0]
        sockfd.send(encrypt_msg)

        if(msg == 'q'):
            break
        encrypt_recv = sockfd.recv(1024)
        recv = pri_key.decrypt(encrypt_recv)
        if(recv == 'q'):
            break

        print recv
    except:
        encrypt_msg = server_public_key.encrypt('q',5031)[0]
        sockfd.send(encrypt_msg)
        break
#####################################################

sockfd.close()

