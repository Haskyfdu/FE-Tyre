#!/usr/bin/env python
# -*- coding: utf-8 -*-


import copy
from algorithms.src.basic.class_tictoc import TicToc
from algorithms.src.core.FE_TSP.class_FE_tsp_ga import FE_tsp_ga

Station_num_per_route_max = 4
Volume_limit = 999
Weight_limit = 999
Time_limit = 10
Iteration_times = 1000
Start_point = {'station_id': '0007714793_mdbxGrgFmTzYXMfTIRlHwCybWmfKlsIe',
               'lng': 121.30409,
               'lat': 31.352371,
               'volume': 0,
               'weight': 0,
               'num': 0}


def calculate_route(distance_dict, stations):
    k = len(stations) // Station_num_per_route_max
    add_times = 0
    route, distance, time_used, volume, weight, station_num = None, None, None, None, None, None
    while add_times < 30:  # just to prevent the endless loop
        route = []
        for i in range(k + 1):
            route.append([copy.copy(Start_point)])
        # TicToc.tic()
        ans = FE_tsp_ga(data=[copy.copy(Start_point)] * (k + 1) + stations,
                        distance_matrix=distance_dict,
                        volume_limit=Volume_limit,
                        time_limit=Time_limit,
                        weight_limit=Weight_limit,
                        iteration_times=Iteration_times)
        # TicToc.toc()
        raw_route = ans['route']
        distance = ans['distance']
        time_used = ans['time']
        volume = ans['volume']
        weight = ans['weight']
        station_num = ans['station_num']
        j = 0
        for i in range(len(raw_route)):
            if raw_route[i]['station_id'] == Start_point['station_id']:
                j += 1
            else:
                route[j].append(raw_route[i])
        # del the degraded solution
        del_list_index = []
        for i in range(len(route)):
            if len(route[i]) == 1 and route[i][0]['station_id'] == Start_point['station_id']:
                del_list_index.append(i)
        for i in range(len(del_list_index)):
            j = del_list_index[len(del_list_index) - 1 - i]
            # print('del', route[k], distance[k], time[k], volume[k], weight[k], station_num[k])
            del route[j]
            del distance[j]
            del time_used[j]
            del volume[j]
            del weight[j]
            del station_num[j]
        # check that the solution satisfies the constraint. if not, resolve
        if len(time_used) > 0 and max(time_used) <= Time_limit \
                and max(volume) <= Volume_limit \
                and max(weight) <= Weight_limit:
            break
        else:
            k += 1
            add_times += 1
    for i in range(len(route)):
        route[i][0]['station_id'] = '上海仓'
    return route, distance, time_used, volume, weight, station_num


if __name__ == '__main__':

    stations_list = [{'id': '2100002',
                      'address': '龙吴路410弄75号4号门',
                      'lng': 121,
                      'lat': 31,
                      'volume': 5,
                      'weight': 5,
                      'num': 10,
                      'order_id': '123456789'},
                     {'id': '2100003',
                      'address': '龙吴路410弄75号4号门',
                      'lng': 121,
                      'lat': 31,
                      'volume': 5,
                      'weight': 5,
                      'num': 10,
                      'order_id': '123456789'},
                     ]

    distance_matrix = {'2100002': {'上海仓': [1000, 100],
                                   '2100003': [1000, 100]},
                       '2100003': {'上海仓': [2000, 200],
                                   '2100002': [1000, 100]},
                       '上海仓': {'2100002': [1000, 100], '2100003': [2000, 200]}}

    route_sample, distance_sample, time_used_sample, volume_sample, weight_sample, station_num_sample\
        = calculate_route(distance_matrix, stations_list)
