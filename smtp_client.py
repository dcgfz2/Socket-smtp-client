from socket import *
import ssl
import base64

msg = "MESSAGE HERE"

endmsg = "\r\n.\r\n"

sender = 'SENDER HERE'
password = 'PASS HERE'

rcpt = 'RECP HERE'

#Mail server of choice
mailserver = 'MAILSERVER HERE'
serverPort = 587

#Socket connection to server via TCP

clientSocket = socket(AF_INET, SOCK_STREAM)


clientSocket.connect((mailserver, serverPort))

recv = clientSocket.recv(1024).decode()

print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

#Helo command with server response

heloCommand = 'EHLO\r\n'

clientSocket.send(heloCommand.encode())

recvl = clientSocket.recv(1024).decode()

print(recvl)

if recvl[:3] != '250':
    print('250 reply not received from server.')

#Send STARTTLS
clientSocket.send('STARTTLS\r\n'.encode())
#clientSocket = ssl.wrap_socket(clientSocket)

recvl = clientSocket.recv(1024).decode()

print(recvl)

#Resend Helo from TLS
clientSocket = ssl.wrap_socket(clientSocket)

clientSocket.send(heloCommand.encode())

recvl = clientSocket.recv(1024).decode()

print(recvl)

#Send AUTH
clientSocket.send('AUTH LOGIN\r\n'.encode())

recvl = clientSocket.recv(1024).decode()

print(recvl)

#Send USERNAME
encoded = base64.b64encode(sender.encode())
clientSocket.send((encoded.decode() + '\r\n').encode())

recvl = clientSocket.recv(1024).decode()

print(recvl)

#Send PASSWORD
encoded = base64.b64encode(password.encode())
clientSocket.send((encoded.decode() + '\r\n').encode())

recvl = clientSocket.recv(1024).decode()

print(recvl)

#Send MAIL FROM

clientSocket.send(str('MAIL FROM: '+ sender + '\r\n').encode())

recvl = clientSocket.recv(1024).decode()
print(recvl)

#Send RCPT TO
clientSocket.send(str('RCPT TO: '+ rcpt + '\r\n').encode())

recvl = clientSocket.recv(1024).decode()
print(recvl)

#Send DATA
clientSocket.send('DATA\r\n'.encode())

recvl = clientSocket.recv(1024).decode()
print(recvl)

#Send message
clientSocket.send(msg.encode())
#Message End
clientSocket.send(endmsg.encode())

#Send Quit
clientSocket.send('QUIT'.encode())

recvl = clientSocket.recv(1024).decode()
print(recvl)
