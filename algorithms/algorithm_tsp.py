#!/usr/bin/env python
# -*- coding: utf-8 -*-


from algorithms.algorithm_io import ImportData, ExportResults
from algorithms.src.basic.class_tictoc import TicToc
from algorithms.src.core.FE_TSP.calculate_route import calculate_route
from flask import jsonify


def run_tsp(date):

    TicToc.tic()
    stations_list = ImportData.read(filename='station_list_'+date+'.json')
    distance_matrix = ImportData.read(filename='distance_matrix.json')
    route, distance, time_used, volume, weight, station_num = calculate_route(distance_matrix, stations_list)
    TicToc.toc()
    ExportResults.write(route, filename='route_'+date+'.json')
    print('Optimization completed, the output file: data/output/route_'+date+'.json')
    return route, distance, time_used, volume, weight, station_num

