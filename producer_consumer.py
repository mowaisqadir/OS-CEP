import threading 
import time

buffer_size = 4
buffer = []

full = threading.Semaphore(0)
empty = threading.Semaphore(buffer_size)
mutex = threading.Lock()

def producer():
    for i in range(10):
        empty.acquire()
        mutex.acquire()
        
        item = f"item-{i}"
        buffer.append(item)
        print(f'Item {i} Produced, Buffer:{buffer}')
        
        mutex.release()
        full.release()
        time.sleep(0.3)

def consumer():
    for i in range(10):
        full.acquire()
        mutex.acquire()
        
        item = f"item-{i}"
        buffer.pop(0)
        print(f'Item {i} Consumed, Buffer:{buffer}')
        
        mutex.release()
        empty.release()
        time.sleep(0.3)

print()

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)

t1.start()
t2.start()

t1.join()
t2.join()

print()