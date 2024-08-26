import socket
import threading
import logging
import signal
import sys
import os

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 12345))
MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS', 5))
running = True
threads = []

def handle_client(c):
    try:
        message = c.recv(1024)
        logging.debug(f'Client received: {message}')
        c.send(b'Echo:' + message)
    except Exception as e:
        logging.error(f'Error handling client: {e}')
    finally:
        c.close()

def signal_handler(sig, frame):
    global running
    print("\nShutting down the server...")
    running = False
    for t in threads:
        t.join()
    sys.exit(0)

def main_socket():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('app.log', encoding='utf-8', mode='a')

    # Create formatters and add them to handlers
    formatter = logging.Formatter('{asctime} - {levelname} - {message}', style='{', datefmt='%Y-%m-%d %H:%M')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(MAX_CONNECTIONS)  # Put the socket into listening mode

    signal.signal(signal.SIGINT, signal_handler)

    print("Server is running. Press Ctrl+C to stop.")

    while running:
        try:
            c, addr = s.accept()
            logger.debug(f'Got connection from: {addr}')
            t = threading.Thread(target=handle_client, args=(c,))
            t.start()
            threads.append(t)
        except Exception as e:
            logger.error(f'Error accepting connections: {e}')
            break

if __name__ == "__main__":
    main_socket()

