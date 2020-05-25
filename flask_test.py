#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


def flask_test(request_url):
    data = {'Date': '2019-11-26', 'Task': 'TSP'}
    rq = requests.post(url=request_url, json=data)
    print(rq.text)


if __name__ == '__main__':
    flask_test(request_url='http://127.0.0.1:7001/')
    # flask_test(request_url='http://vrp.omnies.com')
