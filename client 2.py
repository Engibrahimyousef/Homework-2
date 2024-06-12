import socket


csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
csocket.connect(('127.0.0.1', 1234))

while True:
    response = csocket.recv(4096).decode()
    print(response, end='')

    if "Enter your name" in response or "Enter PIN" in response or "Choose an option" in response or "Enter amount" in response:
        message = input()
        csocket.send(message.encode())
    elif "Your final balance" in response:
        break

csocket.close()
