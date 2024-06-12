import socket
import threading

# قائمة الحسابات البنكية المحفوظة على السيرفر
accounts = [
    {'name': 'ibraheem', 'pin': '1234', 'balance': 1000.0},
    {'name': 'ali', 'pin': '5678', 'balance': 2000.0}
]

# تابع لمعالجة اتصالات العملاء
def handle_client(csocket):
    try:
        csocket.sendall(b'Welcome to the Bank ATM!\nEnter your name: ')
        name = csocket.recv(1024).decode().strip()

        # البحث عن الحساب باستخدام الاسم
        account = next((acc for acc in accounts if acc['name'] == name), None)
        if account is None:
            csocket.sendall(b'Invalid name.\n')
            csocket.close()
            return

        csocket.sendall(b'Enter PIN: ')
        pin = csocket.recv(1024).decode().strip()

        if account['pin'] != pin:
            csocket.sendall(b'Invalid PIN.\n')
            csocket.close()
            return

        csocket.sendall(b'Authenticated successfully.\n')

        while True:
            csocket.sendall(b'\nChoose an option:\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Exit\n')
            option = csocket.recv(1024).decode().strip()

            if option == '1':
                balance = account['balance']
                csocket.sendall(f'Your balance is: ${balance}\n'.encode())

            elif option == '2':
                csocket.sendall(b'Enter amount to deposit: ')
                amount = float(csocket.recv(1024).decode().strip())
                account['balance'] += amount
                csocket.sendall(f'Successfully deposited ${amount}. Your new balance is ${account["balance"]}\n'.encode())

            elif option == '3':
                csocket.sendall(b'Enter amount to withdraw: ')
                amount = float(csocket.recv(1024).decode().strip())
                if amount > account['balance']:
                    csocket.sendall(b'Insufficient funds.\n')
                else:
                    account['balance'] -= amount
                    csocket.sendall(f'Successfully withdrew ${amount}. Your new balance is ${account["balance"]}\n'.encode())

            elif option == '4':
                csocket.sendall(f'Your final balance is ${account["balance"]}\n'.encode())
                break

            else:
                csocket.sendall(b'Invalid option. Please try again.\n')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        csocket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 1234))
server_socket.listen(5)
print("Server listening on port 1234")

while True:
    csocket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    threading.Thread(target=handle_client, args=(csocket,)).start()

