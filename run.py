from multiprocessing import Process
from os import system
import time

def run():
    p1 = Process(target=system, args=('python GUI.py',))
    p2 = Process(target=system, args=('python GUI.py',))
    p3 = Process(target=system, args=('python GUI.py',))
    p4 = Process(target=system, args=('python GUI.py',))
    p5 = Process(target=system, args=('python GUI.py',))
    p1.start()
    time.sleep(0.2)
    p2.start()
    time.sleep(0.2)
    p3.start()
    time.sleep(0.2)
    p4.start()
    time.sleep(0.2)
    p5.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

if __name__ == '__main__':
    run()