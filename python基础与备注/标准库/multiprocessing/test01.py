from multiprocessing import Process


def foo():
    print('hello')


if __name__ == "__main__":
    p = Process(target=foo)
    p.start()
