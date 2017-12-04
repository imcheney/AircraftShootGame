"""
游戏服务器
"""

# 部分代码源自Tcp Chat server
# refer to https://www.cnblogs.com/hazir/p/python_chat_room.html
import socket, select

flag = True
def start_game(start_list):
    if len(start_list) != 2:
        print('error')
        return -1
    player1 = start_list.pop()
    player2 = start_list.pop()
    print("server starts game!")
    reply1 = "start_game1\r"  # 客户端接收到start_game时应该启动游戏窗口
    reply2 = "start_game2\r"
    player1.send(bytes(reply1, encoding="utf-8"))
    player2.send(bytes(reply2, encoding="utf-8"))
    global mode
    mode = "game"
    return [player1, player2]


# Function to broadcast chat messages to all connected clients
def broadcast_data(sock, message, recv_list):
    # Do not send the message to master socket and the client who has send us the message
    # print("recv_list: ", recv_list)
    # print("msg to be sent: ", message)
    for socket in recv_list:
        if socket != server_socket and socket != sock:
            try:
                socket.send(bytes(message, encoding='utf-8'))
            except:
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                recv_list.remove(socket)


if __name__ == "__main__":
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    GAME_LIST = []
    START_LIST = []
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = 5001

    server_socket = socket.socket()
    server_socket.bind(("127.0.0.1", PORT))
    server_socket.listen(10)  # max length of waiting queue is 10

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
    print("Chat server started on port " + str(PORT))
    mode = "chat"
    while flag:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
        for sock in read_sockets:
            # New connection
            if sock == server_socket:  # 如果得到读事件的是server_socket的话, 这说明可能有新的连接请求
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr, CONNECTION_LIST)
            else:  # some incoming new chat msg
                try:
                    data = str(sock.recv(RECV_BUFFER), encoding='utf-8')
                    if (data) and (mode == "chat"):
                        if data.strip() == "start_game":
                            START_LIST.append(sock)  # 说明这个sock fd代表的player要求要开始游戏
                            print('append sock!')
                            print('len of START_LIST: ', len(START_LIST))
                            if len(START_LIST) >= 2:
                                GAME_LIST = start_game(START_LIST)
                                mode = "game"
                                continue
                        # print("CONNECTION_LIST: ", CONNECTION_LIST)
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data, CONNECTION_LIST)
                    else:  # mode == "game"
                        if data and (data.strip() != "game_over"):
                            # print(data)
                            # print("sock:", sock)
                            # print("GAME_LIST", GAME_LIST)
                            broadcast_data(sock, data.strip(), GAME_LIST)  # 1, input sock, 2, msg 3, 接收的list
                        else:  # game_over
                            # print(data)
                            broadcast_data(sock, data, GAME_LIST)
                            flag = False
                            continue
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr, CONNECTION_LIST)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()
