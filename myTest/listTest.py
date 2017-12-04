l = ['A', 'B', 'C']

def func(some_list):
    some_list.pop()

if __name__ == '__main__':
    print(l)
    func(l)
    print(l)