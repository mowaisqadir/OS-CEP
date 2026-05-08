import threading
import time
import random

# Data
tree = list(range(1, 31))
crate = []
truck = []

CRATE_SIZE = 12

# Sync primitives
mutex_tree = threading.Lock()
mutex_crate = threading.Lock()

crate_empty = threading.Semaphore(CRATE_SIZE)  # empty slots
crate_full = threading.Semaphore(0)            # signal loader

done = False  # pickers finished flag

def Picker(pid):
    global crate

    while True:
        # ---- Step 1: take fruit from tree safely ----
        mutex_tree.acquire()
        if len(tree) == 0:
            mutex_tree.release()
            break
        
        index = random.randint(0, len(tree)-1)
        fruit = tree.pop(index)
        
        mutex_tree.release()

        # ---- Step 2: wait for crate space ----
        crate_empty.acquire()

        # ---- Step 3: put fruit in crate ----
        mutex_crate.acquire()

        crate.append(fruit)
        print(f'Picker {pid} picked fruit {fruit}')
        print(f'Tree: {tree}')
        print(f'Crate: {crate}\n')

        # If crate full → signal loader
        if len(crate) == CRATE_SIZE:
            crate_full.release()

        mutex_crate.release()

        time.sleep(0.2)

    print(f'Picker {pid} finished')


def Loader():
    global crate, done

    while True:
        crate_full.acquire()

        mutex_crate.acquire()

        # If nothing left and done → exit
        if len(crate) == 0 and done:
            mutex_crate.release()
            break

        # Load crate
        old_crate = crate.copy()
        truck.append(old_crate)
        crate.clear()

        print(f'Loader loaded crate: {old_crate}')
        print(f'Crate: {crate}\n')

        mutex_crate.release()

        # reset empty slots
        for _ in range(CRATE_SIZE):
            crate_empty.release()

        if done:
            break

    print('Loader finished')


# ---- Main ----
p1 = threading.Thread(target=Picker, args=[1])
p2 = threading.Thread(target=Picker, args=[2])
p3 = threading.Thread(target=Picker, args=[3])
l1 = threading.Thread(target=Loader)

p1.start()
p2.start()
p3.start()
l1.start()

p1.join()
p2.join()
p3.join()

crate_full.release()
done = True

l1.join()

print('\nDone\n')

print('Truck: ')
for i, j in enumerate(truck):
    print(f'Crate {i+1}: {j}')