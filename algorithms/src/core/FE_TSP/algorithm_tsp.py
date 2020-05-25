#!/usr/bin/env python
# -*- coding: utf-8 -*-


from algorithms.algorithm_io import ImportData, ExportResults
from project_config import AlgorithmConfig
try:
    from algorithms.src.basic.class_tictoc import TicToc
    from algorithms.src.core.FE_TSP.calculate_route import calculate_route
except ImportError:
    from algorithms.lib.basic.class_tictoc import TicToc
    from algorithms.lib.core.FE_TSP.calculate_route import calculate_route


def run_tsp(date):

    TicToc.tic()
    stations_list = ImportData.read(filepath=AlgorithmConfig['Path']['Input_Data_Path_TSP'],
                                    filename='station_list_'+date+'.json')
    distance_matrix = ImportData.read(filepath=AlgorithmConfig['Path']['Input_Data_Path_TSP'],
                                      filename='distance_matrix.json')
    parameters = ImportData.read(filepath=AlgorithmConfig['Path']['Input_Data_Path_TSP'],
                                 filename='parameters.json')
    route, distance, time_used, volume, weight, station_num \
        = calculate_route(distance_dict=distance_matrix, stations=stations_list, parameters=parameters)
    TicToc.toc()
    ExportResults.write(result=route,
                        filepath=AlgorithmConfig['Path']['Output_Data_Path_TSP'],
                        filename='route_'+date+'.json')
    print('Optimization completed, the output file:',
          AlgorithmConfig['Path']['Output_Data_Path_TSP']+'/route_'+date+'.json')
    return route, distance, time_used, volume, weight, station_num


if __name__ == '__main__':

    run_tsp('2019-11-26')
