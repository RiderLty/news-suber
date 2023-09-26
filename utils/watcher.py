from urllib.parse import urljoin
import requests
from lxml import etree
import jsonpath


def parse_json(jsonData, config):
    # print(jsonData, config)
    hrefList = [urljoin(config["url"], x)
             for x in jsonpath.jsonpath(jsonData, config["href"])]
    titleList = jsonpath.jsonpath(jsonData, config["title"])
    assert len(titleList) == len(hrefList)
    return [
        {
            "title": titleList[i],
            "href":hrefList[i]
        } for i in range(len(titleList))
    ]


def parse_html(htmlText, config):
    htmlIndex = htmlText.index("<html")
    htmlText = htmlText[htmlIndex:]
    # open("./tmp.html", 'w', encoding="UTF-8").write(htmlText)
    page = etree.HTML(htmlText)
    titleList = page.xpath(config["title"])
    hrefList = [urljoin(config["url"], x) for x in page.xpath(config["href"])]
    assert len(titleList) == len(hrefList)
    return [
        {
            "title": titleList[i],
            "href":hrefList[i]
        } for i in range(len(titleList))
    ]


def list_news(config):
    request = requests.get(
        url=config["url"],
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',
        },
        # proxies={
        #     "http": "http://202.55.5.209:8090",
        #     "https": "https://202.55.5.209:8090"
        # }
    )

    if config["type"] == "json":
        data = request.json()
        return parse_json(data, config)
    elif config["type"] == "xml":
        data = request.content.decode(request.apparent_encoding)
        return parse_html(data, config)
    else:
        raise Exception("unknow type")
