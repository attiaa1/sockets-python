import socket

HOST = 'localhost'
PORT = 12345

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, server')
        data = s.recv(1024)
        print(f'Received {data}')

if __name__ == "__main__":
    client()

