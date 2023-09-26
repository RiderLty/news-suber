import json
import os
from utils.watcher import list_news
from tinydb import Query, TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
from utils.notifier import notify_me


config = {
    "name": "安徽人事考试网",
    "url": "http://www.apta.gov.cn/",
    "type": "xml",
    "href": "/html/body/table/tr/td[1]/div/table/tr/td/a/@href",
    "title": "/html/body/table/tr/td[1]/div/table/tr/td/a/@title"
}

if __name__ == "__main__":
    print(json.dumps(list_news(config),indent=4,ensure_ascii=False))
