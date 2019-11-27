#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

import requests


def flask_test():
    url = 'http://127.0.0.1:9000/run'
    data = {'Date': '2019-11-26', 'Task': 'TSP'}
    rq = requests.post(url=url, json=data)
    print(rq.text)


if __name__ == '__main__':

    flask_test()
