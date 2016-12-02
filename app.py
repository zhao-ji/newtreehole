#!/usr/bin/env python
# coding: utf8

import json

import logbook

from flask import Flask
from flask import request

from api import fanfou_get, fanfou_post

app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_timeline():
    # 扶梯式翻页
    max_id = request.args.get("max_id", None)
    count = request.args.get("count", 20)

    # 电梯式翻页
    page = request.args.get("page", 0)

    if page:
        timeline = fanfou_get("statuses/user_timeline", page=page, mode='lite')
    else:
        timeline = fanfou_get(
            "statuses/user_timeline",
            max_id=max_id,
            count=count,
            mode='lite',
        )
    talks = []
    for talk in timeline:
        i = {
            "id": talk["id"],
            "content": talk["text"],
            "created_at": " ".join(talk["created_at"].split(" ")[:4]),
            "from": talk["source"],
            "location": talk["location"],
        }
        talks.append(i)
    return json.dumps(talks), 200, None


@app.route("/", methods=['POST'])
def create_talk():
    talk = request.form["content"]
    ret = fanfou_post(
        "statuses/update",
        status=talk,
        source="weixin",
        mode='lite',
        location='weixin'
    )
    return json.dumps(ret), 201, None


if __name__ == '__main__':
    from os.path import abspath, exists, dirname, join

    server_log_file = join(dirname(abspath(__file__)), "record.log")
    if not exists(server_log_file):
        open(server_log_file, "w").close()

    local_log = logbook.FileHandler(server_log_file)
    local_log.format_string = (
        u'[{record.time:%H:%M:%S}] '
        u'lineno:{record.lineno} '
        u'{record.level_name}:{record.message}')
    local_log.push_application()

    # app.run(host='127.0.0.1', port=10005)
    app.run(host='0.0.0.0', port=10005, debug=True, use_reloader=True)
