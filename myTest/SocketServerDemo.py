import socket

sk = socket.socket()  # refer to https://www.cnblogs.com/hazir/p/python_socket_programming.html
sk.bind(("127.0.0.1", 8080))
sk.listen(5)  # 等待accept队列的最大长度为5
flag = True
msg = ""
while flag:
    if msg == 'close server':
        flag = False
    conn, address = sk.accept()
    while True:
        msg = str(conn.recv(1024), encoding='utf-8')
        print("Got msg (%s) from %s;" % (msg, conn))
        if (msg == 'exit') or (msg == "close server"):
            break
        else:
            reply = "Hello world!"
            conn.send(bytes(reply, encoding="utf-8"))
    conn.close()
sk.close()
