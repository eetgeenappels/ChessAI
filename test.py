
import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 10203)
client_socket.connect(server_address)

while True:

    # Receive and print the welcome message from the server
    message = client_socket.recv(1024).decode()
    print(f'Received from server: {message}')

    client_socket.send(b'{"2":1}')
    input('Press Enter to continue...')

# Close the connection
client_socket.close()