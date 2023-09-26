

import os
import threading
import requests


def notify_via_http(title: str, text: str) -> None:
    res = requests.get(
        url=os.environ.get("MACRODROID_URL","http://www.baidu.com"),
        params={
            "title": title,
            "text": text,
        }
    )
    print(res.text)


def notify_me(newsList):
    for news in newsList:
        print("notify",news["title"])
        # notify_via_http(news["href"],news["title"])
        threading.Thread(target=notify_via_http, args=(news["title"], news["href"])).start()

if __name__ == "__main__":
    notify_via_http("我是文字", "这是标题")
