import time
import os


class Starter(object):

    def __init__(self):
        self.keywords = []

    @staticmethod
    def start_weibo():
        os.chdir("D:\\monitor\\monitorSpiders\\monitorSpiders")
        os.system("scrapy crawl weibo")

    def set_keywords(self, args):
        self.keywords = args

    def get_keywords(self):
        return self.keywords


starter = Starter()
if __name__ == '__main__':
    while True:
        starter.start_weibo()
        time.sleep(60)