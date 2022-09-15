import time
from multiprocessing import Pool


def handle(i):
    print(f"process {i} start")
    time.sleep(1)
    print(f"process {i} end")


class MultiprocessProcessor:
    def __init__(self, processes_num):
        self.processes_num = processes_num

    def process(self):
        pool = Pool(self.processes_num)

        for i in range(10):
            pool.apply_async(func=handle, args=(i,))

        pool.close()
        pool.join()

        print("end")


if __name__ == "__main__":
    print("start")

    MultiprocessProcessor(5).process()
