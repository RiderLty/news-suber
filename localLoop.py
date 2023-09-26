import json
import os
from time import sleep, time
from utils.watcher import list_news
from tinydb import Query, TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
from utils.notifier import notify_me




if __name__ == "__main__":
    while True:
        try:
            dbPath = os.path.join(os.path.split(__file__)[0], "db.json")
            db = TinyDB(dbPath, storage=CachingMiddleware(JSONStorage))
            configsPath = os.path.join(os.path.split(__file__)[0], "configs")
            configs = [json.load(open(os.path.join(configsPath, x), 'r', encoding="UTF-8"))
                    for x in os.listdir(configsPath)]
            needNotify = []
            for config in configs:
                targetTable = db.table(config["name"])
                records = list_news(config)
                if len(records) == 0 :
                    print("获取网站错误 注意手动查询")
                for rec in records:
                    if len(targetTable.search(Query().href == rec["href"])) == 0:
                        targetTable.insert(rec)
                        needNotify.append({
                            "name": config["name"],
                            "host": config["url"],
                            "title": rec["title"],
                            "href": rec["href"],
                        })
                    else:
                        print("notified",rec["title"])
            
            notify_me(needNotify)
            db.close()
            sleep(5*60)
        except Exception as e:
            print(e)