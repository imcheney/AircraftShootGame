import socket

sk = socket.socket()
sk.connect(("127.0.0.1", 8080))
flag = True
while flag == True:
    msg = input("Your msg? if you want to quit, type exit;")
    if (msg == 'exit') or (msg == 'close server'):
        flag = False
    sk.sendall(bytes(msg, encoding='utf-8'))
    reply = str(sk.recv(1024), encoding="utf-8")
    print("server reply: %s" % (reply))
sk.close()
