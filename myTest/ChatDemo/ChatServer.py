# Tcp Chat server
# refer to https://www.cnblogs.com/hazir/p/python_chat_room.html

import socket, select


# Function to broadcast chat messages to all connected clients
def broadcast_data(sock, message):
    # Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(bytes(message, encoding='utf-8'))
            except:
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)


if __name__ == "__main__":
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = 5000

    server_socket = socket.socket()
    server_socket.bind(("127.0.0.1", PORT))
    server_socket.listen(10)  # max length of waiting queue is 10

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
    print("Chat server started on port " + str(PORT))

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
        for sock in read_sockets:
            # New connection
            if sock == server_socket:  # 如果得到读事件的是server_socket的话, 这说明可能有新的连接请求
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
            else:  # some incoming new chat msg
                try:
                    data = str(sock.recv(RECV_BUFFER), encoding='utf-8')
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()
