#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

import json
import _thread
from flask import jsonify, request, Blueprint
from algorithms.src.core.FE_TSP.algorithm_tsp import run_tsp
from algorithms.src.core.FE_Pick_Storage.algorithm_pick import run_pick


blueprint_main = Blueprint(name='blueprint_main', import_name=__name__)


@blueprint_main.route('/', methods=['GET', 'POST'])
def algorithm_main():
    print('Algorithm started')
    if request.method == 'GET':
        return jsonify({"description": "Algorithm Post Request Service", "status": "UP"})
    elif request.method == 'POST':
        json_post_information = json.loads(request.get_data())
        if 'Task' in json_post_information and json_post_information['Task'] == 'TSP':
            _thread.start_new_thread(run_tsp, (json_post_information['Date'], ))
            return jsonify({"running status": 'success'})
        elif 'Task' in json_post_information and json_post_information['Task'] == 'Pick':
            _thread.start_new_thread(run_pick, (json_post_information['Date'],))
            return jsonify({"running status": 'success'})
        else:
            # todo: add new task function
            raise ValueError('The Task can only be "TSP" currently.')
    else:
        return 'Algorithm post request failed'
