#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2019 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

import json
from flask import jsonify, request, Blueprint
from algorithms.algorithm_tsp import run_tsp


blueprint_main = Blueprint(name='blueprint_main', import_name=__name__)


@blueprint_main.route('/run', methods=['GET', 'POST'])
def algorithm_main():
    print('Algorithm started')
    if request.method == 'GET':
        return jsonify({"description": "Algorithm Post Request", "status": "UP"})
    elif request.method == 'POST':
        json_post_information = json.loads(request.get_data())
        if 'Task' in json_post_information and json_post_information['Task'] == 'TSP':
            import _thread
            _thread.start_new_thread(run_tsp, (json_post_information['Date'], ))
            return jsonify({"running status": 'success'})
        else:
            # todo: add new task function
            raise ValueError('The Task can only be "TSP" currently.')
    else:
        return 'Algorithm post request failed'
