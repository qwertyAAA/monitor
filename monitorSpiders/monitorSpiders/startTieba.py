from scrapy import cmdline
# import singleton
import os


# if __name__ == '__main__':
#     cmdline.execute("scrapy crawl tieba".split())
# def start_tieba():
#     os.chdir("D:\\monitorSpiders\\monitorSpiders")
#     # cmdline.execute("scrapy crawl weibo".split())
#     os.system("scrapy crawl tieba")


def Singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton

@Singleton
class Starter(object):

    def start_tieba(self):
        os.chdir("D:\\monitor\\monitorSpiders\\monitorSpiders")
        os.system("scrapy crawl tieba")



tieba = Starter()
# tieba3 = Starter()
# print(tieba2,tieba3)

if __name__ == '__main__':
    tieba.start_tieba()
