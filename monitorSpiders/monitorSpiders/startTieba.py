from scrapy import cmdline
import os


# if __name__ == '__main__':
#     cmdline.execute("scrapy crawl tieba".split())
def start_tieba():
    os.chdir("D:\\monitorSpiders\\monitorSpiders")
    # cmdline.execute("scrapy crawl weibo".split())
    os.system("scrapy crawl tieba")


class Starter(object):

    def __init__(self):
        self.keywords = []

    @staticmethod
    def start_tieba():
        os.chdir("D:\\monitor\\monitorSpiders\\monitorSpiders")
        os.system("scrapy crawl tieba")

    def set_keywords(self, args):
        self.keywords = args

    def get_keywords(self):
        return self.keywords


tieba = Starter()

if __name__ == '__main__':
    tieba.start_tieba()
