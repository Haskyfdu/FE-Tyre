#!/usr/bin/env python
# -*- coding: utf-8 -*-


from algorithms.algorithm_io import ImportData
try:
    from algorithms.src.core.FE_TSP.class_FE_tsp_ga import FE_tsp_ga
except ImportError:
    from algorithms.lib.core.FE_TSP.class_FE_tsp_ga import FE_tsp_ga


def calculate_route(distance_dict, stations, parameters):
    ImportData()
    k = len(stations) // parameters['station_num_per_route_max']
    add_times = 0
    route, distance, time_used, volume, weight, station_num = None, None, None, None, None, None
    while add_times < 30:  # just to prevent the endless loop
        route = []
        for i in range(k + 1):
            route.append([parameters['start_point'].copy()])
        # TicToc.tic()
        ans = FE_tsp_ga(data=[parameters['start_point'].copy()] * (k + 1) + stations,
                        distance_matrix=distance_dict,
                        volume_limit=parameters['volume_limit'],
                        time_limit=parameters['time_limit'],
                        weight_limit=parameters['weight_limit'],
                        iteration_times=parameters['iteration_times'])
        # TicToc.toc()
        raw_route = ans['route']
        distance = ans['distance']
        time_used = ans['time']
        volume = ans['volume']
        weight = ans['weight']
        station_num = ans['station_num']
        j = 0
        for i in range(len(raw_route)):
            if raw_route[i]['station_id'] == parameters['start_point']['station_id']:
                j += 1
            else:
                route[j].append(raw_route[i])
        # del the degraded solution
        del_list_index = []
        for i in range(len(route)):
            if len(route[i]) == 1 and route[i][0]['station_id'] == parameters['start_point']['station_id']:
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
        if len(time_used) > 0 and max(time_used) <= parameters['time_limit'] \
                and max(volume) <= parameters['volume_limit'] \
                and max(weight) <= parameters['weight_limit']:
            break
        else:
            k += 1
            add_times += 1
    for i in range(len(route)):
        route[i][0].update({'remark': '起点： 上海仓'})
    return route, distance, time_used, volume, weight, station_num


if __name__ == '__main__':

    stations_list = [{'station_id': '2100002',
                      'address': '龙吴路410弄75号4号门',
                      'lng': 121,
                      'lat': 31,
                      'volume': 5,
                      'weight': 5,
                      'num': 10,
                      'order_id': '123456789'},
                     {'station_id': '2100003',
                      'address': '龙吴路410弄75号4号门',
                      'lng': 121,
                      'lat': 31,
                      'volume': 5,
                      'weight': 5,
                      'num': 10,
                      'order_id': '123456789'},
                     ]

    distance_matrix = {'2100002': {'000003': [1000, 100],
                                   '2100003': [1000, 100]},
                       '2100003': {'000003': [2000, 200],
                                   '2100002': [1000, 100]},
                       '000003': {'2100002': [1000, 100], '2100003': [2000, 200]}}

    parameters = {"station_num_per_route_max": 25,
                  "volume_limit": 999,
                  "weight_limit": 999,
                  "time_limit": 10,
                  "iteration_times": 1000,
                  "start_point": {
                      "station_id": "000003",
                      "lng": 121.30409,
                      "lat": 31.352371,
                      "volume": 0,
                      "weight": 0,
                      "num": 0}}

    route_sample, distance_sample, time_used_sample, volume_sample, weight_sample, station_num_sample\
        = calculate_route(distance_dict=distance_matrix, stations=stations_list, parameters=parameters)
