# coding:unicode_escape
import requests
from lxml import etree
from pyquery import PyQuery as pq
from app.models.main import Movie
import datetime
from app import create_app
from app.extensions import db
app = create_app("default")
app.app_context().push()



headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Connection": "keep-alive",
"Cookie": "__mta=255105335.1570076842046.1570077068498.1570077098181.7; " \
          "_lxsdk_cuid=16d8fdf0140c8-086739cf53eb49-1d3d6b55-13c680-16d8fdf0140c8; uuid_n_v=v1; uuid=175FA4F0E59611E99BA7457F9B3430D3C417C342ED904B37A0AC1C8389C4320C; "
          "_csrf=82aba2029d2509f73e1ae91deceb06509e25aa4ae977120b612285194192641e; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; "
          "_lxsdk=175FA4F0E59611E99BA7457F9B3430D3C417C342ED904B37A0AC1C8389C4320C; ci=1; __mta=255105335.1570076842046.1570076869979.1570077063750.6; "
          "_lxsdk_s=16d8fdf0142-569-fb7-999%7C%7C49",
"Host": "maoyan.com",
"Referer": "https://maoyan.com/board/4",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User": "?1",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}


def get_bod(num):
    url = "https://maoyan.com/board/4?offset={}".format(num)
    response = requests.get(url, headers=headers).content
    bod = str(response, encoding="utf-8")
    html = etree.HTML(bod)
    doc = pq(html)
    title = doc('dl dd')
    return title

def get_movie_list_dict(title):
    movie_list = []
    for i in range(0, 10):
        name = title.eq(i).find("p").eq(0).text()
        actor = title.eq(i).find("p").eq(1).text()[3:]
        up_time = title.eq(i).find("p").eq(2).text()[5:15]
        if len(up_time) < 6:
            up_time = up_time+'-'+"01-01"
        score = title.eq(i).find("p").eq(-1).text()
        img = title.eq(i).find("img").eq(1).attr("data-src")
        movie_list.append(
            Movie(img=img, name=name, actor=actor, up_time=up_time, score=score)
            )
    return movie_list

def main():
    result = []
    for i in range(0, 91, 10):
        title = get_bod(i)
        movie_list = get_movie_list_dict(title)
        result += movie_list
    db.session.bulk_save_objects(result)
    db.session.commit()
    return result


if __name__ == "__main__":
    dou = main()
    print(dou)
    pass
    # movie_list = main()
    # print(movie_list)
