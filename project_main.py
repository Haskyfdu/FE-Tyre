#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

from algorithms.algorithm_main import blueprint_main
from flask import Flask


app_test = Flask(__name__)
app_test.register_blueprint(blueprint_main)


if __name__ == '__main__':

    app_test.run(host="127.0.0.1", port=7001, debug=False)

