import time


def fn4(x, y):
    time.sleep(0.0001)


def fn3(x):
    for y in range(100):
        fn4(x, y)

def fn2():
    time.sleep(1)


def fn1():
    fn2()

    for x in range(100):
        fn3(x)


def main():
    fn1()
    fn2()


if __name__ == '__main__':
    main()
