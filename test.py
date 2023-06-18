import time
import threading
import multiprocessing


def count(name):
    for i in range(1, 100000000):
        pass


start = time.time()
num_list = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"]
mylist = list(map(str.lower, num_list))
print(mylist)

# if __name__ == "__main__":
#     t_list = []
#     for i in range(4):
#         t = multiprocessing.Process(target=count, args=(i,))
#         t.start()
#         t_list.append(t)

#     for j in t_list:
#         j.join()
#     end = time.time()

#     print("수행시간: %f 초"  % (end - start))

# if __name__ == "__main__":
#     cpu_count = multiprocessing.cpu_count()

#     t = multiprocessing.Pool(processes=cpu_count)
#     t.map(count, num_list)
#     t.close()
#     t.join()

#     end = time.time()
#     print("cpu_count:", cpu_count)
#     print("수행시간: %f 초" % (end - start))
