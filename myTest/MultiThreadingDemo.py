# coding=utf-8
import threading
from time import ctime, sleep


def listen(song):
    for i in range(2):
        print("I was listening to %s. %s" % (song, ctime()))
        sleep(5)


def watch(movie):
    for i in range(2):
        print("I was watching %s! %s" % (movie, ctime()))
        sleep(5)


threads = []
t1 = threading.Thread(target=listen, args=('爱情买卖',))
threads.append(t1)
t2 = threading.Thread(target=watch, args=('阿凡达',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join() # join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞。如果没有这行代码的话, 整个程序看起来会提前结束.

    print("all over %s" % ctime())

