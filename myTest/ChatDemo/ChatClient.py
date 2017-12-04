# telnet program example
import sys

sys.path.append('/Users/cxl/dev/PythonShootGame')
import socket, select, string, sys
import mainGame


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


# main function
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print('Usage : python3 ChatClient.py hostIP portNo')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket()
    s.settimeout(10)

    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print
        'Unable to connect'
        sys.exit()

    print
    'Connected to remote host. Start sending messages'
    prompt()

    while 1:
        rlist = [sys.stdin, s]
        # Get the list sockets which are readable
        read_list, write_list, error_list = select.select(rlist, [], [])
        for sock in read_list:
            # incoming message from remote server
            if sock == s:  # s指的是与服务器的连接fd
                data = str(sock.recv(4096), encoding='utf-8')
                if not data:
                    print('\nDisconnected from chat server\n')
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data)
                    if data.strip()[:-1] == 'start_game':
                        # data = str(sock.recv(4096), encoding='utf-8')
                        assignment = int(data.strip()[-1])
                        mainGame.game_engine(10, assignment, sock)  #seedInit=10 暂时默认这么设置
                    prompt()

            # user entered a message
            else:
                msg = sys.stdin.readline()
                s.send(bytes(msg, encoding="utf-8"))
                prompt()
