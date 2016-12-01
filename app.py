#!/usr/bin/env python
# coding: utf8

import logbook

from flask import abort
from flask import Flask
from flask import request

from api import get, post

app = Flask(__name__)


@app.route("/", methods=['GET'])
def select():
	# 扶梯式翻页
    max_id = request.args.get("max_id", None)
	count = request.args.get("count", 20)

	# 电梯式翻页
	page = request.args.get("page", 1)


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

    app.run(host='127.0.0.1', port=10005)
