#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

from algorithms.algorithm_io import ExportResults

parameters_dict = {'station_num_per_route_max': 25,
                   'volume_limit': 10,
                   'weight_limit': 2000,
                   'time_limit': 10,
                   'iteration_times': 1000,
                   'start_point': {'station_id': '000003',
                                   'lng': 121.30409,
                                   'lat': 31.352371,
                                   'volume': 0,
                                   'weight': 0,
                                   'num': 0}}

ExportResults.write(parameters_dict, filename='parameters.json')
