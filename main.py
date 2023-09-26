import json
import os
from utils.watcher import list_news
from tinydb import Query, TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
from utils.notifier import notify_me


dbPath = os.path.join(os.path.split(__file__)[0], "db.json")
db = TinyDB(dbPath, storage=CachingMiddleware(JSONStorage))

configsPath = os.path.join(os.path.split(__file__)[0], "configs")
configs = [json.load(open(os.path.join(configsPath, x), 'r', encoding="UTF-8"))
           for x in os.listdir(configsPath)]

if __name__ == "__main__":
    needNotify = []
    for config in configs:
        targetTable = db.table(config["name"])
        records = list_news(config)
        # if len(records) == 0 :
        #     raise Exception("获取网站错误 注意手动查询")
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
                print("notified", rec["title"])
    notify_me(needNotify)
    db.close()
    if os.path.exists("./notified.bin"):
        os.remove("./notified.bin")
    if len(needNotify) == 0:
        pass
    else:
        with open("./notified.bin", "w") as f:
            f.write(f"notified {len(needNotify)}")

