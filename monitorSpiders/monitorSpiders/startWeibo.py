import os
import time
import redis


class Starter(object):
    @staticmethod
    def start_weibo():
        os.chdir("/opt/monitor/monitorSpiders/monitorSpiders")
        os.system("scrapy crawl weibo")


starter = Starter()
if __name__ == '__main__':
    starter.start_weibo()
