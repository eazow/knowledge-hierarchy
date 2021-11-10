import time
from multiprocessing import Pool

PROCESSES_NUM = 5


def process(i):
    print(f"process {i} start")
    time.sleep(1)
    print(f"process {i} end")


if __name__ == "__main__":
    print("start")

    pool = Pool(PROCESSES_NUM)

    for i in range(PROCESSES_NUM):
        pool.apply_async(func=process, args=(i,))

    pool.close()
    pool.join()

    print("end")
