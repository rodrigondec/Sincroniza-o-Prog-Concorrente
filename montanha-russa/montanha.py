from threading import Thread


def car():
    pass


def passenger():
    pass


threads = []

t = Thread(name='car', target=car, args=('test',))
threads.append(t)
t.start()

for thread in threads:
    thread.join()
