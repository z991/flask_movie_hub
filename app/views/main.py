from flask import Blueprint, render_template, current_app, request
from app.models.main import Movie
from sqlalchemy import desc
import requests
import json

main = Blueprint('main', __name__)


@main.route('/top_100/')
def top_100():
    data = request.args
    request_url = request.base_url
    print("request_url", request_url)
    page = data.get("pn", 1)
    wd = data.get("wd")
    order = data.get("order")
    try:
        page = int(page)
    except Exception as e:
        page = 1
    movie_query = Movie.query.filter()
    if order == "score":
        movie_query = movie_query.order_by(Movie.score)
    if order == "-score":
        movie_query = movie_query.order_by(desc(Movie.score))
    if wd:
        # 模糊搜索
        wd = '%{}%'.format(wd)
        movie_query = movie_query.filter(Movie.name.like(wd)).paginate(page, error_out=False)
    else:
        movie_query = movie_query.filter_by().paginate(page, error_out=False)
    return render_template('main/movie_index.html', movie_query=movie_query, pn_order_wd={"wd": wd, "pn": page, "order":order}, top_menu="active")


@main.route('/')
def index():
    # 获取猫眼电影
    url = "http://m.maoyan.com/ajax/movieOnInfoList?token="
    headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "_lxsdk_cuid=16d8fdf0140c8-086739cf53eb49-1d3d6b55-13c680-16d8fdf0140c8; uuid_n_v=v1; iuuid=3D426F90E59611E98548718B8C06F66F9461466CD5A24A22BF33C615336FEB9D; __mta=255105335.1570076842046.1570077063750.1570327769693.7; ci=1%2C%E5%8C%97%E4%BA%AC; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk=3D426F90E59611E98548718B8C06F66F9461466CD5A24A22BF33C615336FEB9D; selectci=; webp=true; __mta=255105335.1570076842046.1570327769693.1571135905863.8; _lxsdk_s=16dcf1e9619-2cf-ba7-5ce%7C%7C1",
            "Host": "m.maoyan.com",
            "If-None-Match": "W/'15d8-C4+r13En6RVsExgZBvMrgg'",
            "Referer": "http://m.maoyan.com/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
    }
    content = requests.get(url=url, headers=headers).content
    bod = str(content, encoding="utf-8")
    bod = json.loads(bod)
    movieList = bod.get("movieList")
    return render_template('main/hot_maoyan.html', movieList=movieList, maoyan_menu="active")
