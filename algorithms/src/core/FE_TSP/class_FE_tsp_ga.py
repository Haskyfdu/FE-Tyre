#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

from algorithms.src.core.FE_TSP.class_ga import GA


class TSP(object):
    def __init__(self, stations_data, distance_matrix, volume_max, time_max, weight_max, life_count=100):
        self.stations = []
        self.distance_matrix = distance_matrix  # {station1: {station2: [distance(m), time(s)]}}
        self.init_stations(stations_data)
        self.lifeCount = life_count
        self.volume_max = volume_max  # the max volume of the vehicle in this route
        self.weight_max = weight_max  # the max weight of the vehicle in this route
        self.time_max = time_max  # the max time of the vehicle in this route
        self.start_point = stations_data[0]  # fix the start point
        self.ga = GA(
            cross_rate=0.7,
            mutation_rate=0.02,
            life_count=self.lifeCount,
            gene_length=len(self.stations),
            match_fun=self.match_function()
        )

    def init_stations(self, data):
        self.stations = data[1:]

    """Calculate phased begin part in function distance"""

    @staticmethod
    def phased_begin(station):
        phased_volume = station['volume']
        phased_weight = station['weight']
        phased_station_num = 1
        return phased_volume, phased_weight, phased_station_num

    """Calculate phased single part in function distance"""

    def phased_step(self, station1, station2, phased_distance, phased_time,
                    phased_volume, phased_weight, phased_station_num):
        if station1['station_id'] in self.distance_matrix \
                and station2['station_id'] in self.distance_matrix[station1['station_id']]:
            phased_distance += self.distance_matrix[station1['station_id']][station2['station_id']][0]
            phased_time += self.distance_matrix[station1['station_id']][station2['station_id']][1]
            phased_volume += station2['volume']
            phased_weight += station2['weight']
            phased_station_num += 1
        else:
            print(station1['station_id'], station2['station_id'])
            raise TypeError('distance matrix bug')
        return phased_distance, phased_time, \
            phased_volume, phased_weight, phased_station_num

    """Information statistics at the end of the route"""

    @staticmethod
    def end_route(distance, time, phased_distance, phased_time, phased_station_num,
                  phased_volume, phased_weight, volume, weight, station_num):
        distance.append(phased_distance)
        time.append(phased_time / 3600 + 0.25 * phased_station_num)
        volume.append(phased_volume)
        weight.append(phased_weight)
        station_num.append(phased_station_num)

    """Check time/volume/weight and return distance_match_used for ga"""

    def check_all(self, distance, time, volume, weight, station_num):
        distance_match_used = sum(distance)
        for i in range(len(distance)):  # check the constraints
            if time[i] > self.time_max or volume[i] > self.volume_max or weight[i] > self.weight_max:
                k = max(time[i] // self.time_max, volume[i] // self.volume_max, weight[i] // self.weight_max)
                distance_match_used += k * distance[i] * 10
        return distance, time, volume, weight, station_num, distance_match_used

    """Calculate the distance while satisfied the constraint """

    def distance(self, order):
        distance, time, volume, weight, station_num = [], [], [], [], []  # initial routes info
        station1 = self.start_point  # initial the first route info
        station2 = self.stations[order[0]]
        phased_distance = (self.distance_matrix[station1['station_id']][station2['station_id']][0])
        phased_time = (self.distance_matrix[station1['station_id']][station2['station_id']][1])  # measure by seconds
        phased_volume, phased_weight, phased_station_num = self.phased_begin(station2)
        if station2['station_id'] == self.start_point['station_id']:  # make sure station1 is the real start point
            distance.append(0)
            time.append(0)       # measure by hours
            volume.append(0)
            weight.append(0)
            station_num.append(0)
        for i in range(0, len(self.stations) - 1):  # calculate each station info
            index1, index2 = order[i], order[i + 1]
            station1, station2 = self.stations[index1], self.stations[index2]
            if station2['station_id'] != self.start_point['station_id']:
                phased_distance, phased_time, phased_volume, phased_weight, phased_station_num = \
                    self.phased_step(station1, station2, phased_distance, phased_time,
                                     phased_volume, phased_weight, phased_station_num)
            else:
                self.end_route(distance, time, phased_distance, phased_time, phased_station_num,
                               phased_volume, phased_weight, volume, weight, station_num)
                phased_distance = 0
                phased_time = 0
                phased_weight = 0
                phased_station_num = 0
                phased_volume = 0
        if self.stations[order[-1]]['station_id'] != self.start_point['station_id']:
            self.end_route(distance, time, phased_distance, phased_time, phased_station_num,
                           phased_volume, phased_weight, volume, weight, station_num)
        else:
            distance.append(0)
            time.append(0)
            volume.append(0)
            weight.append(0)
            station_num.append(0)
        distance, time, volume, weight, station_num, distance_match_used \
            = self.check_all(distance, time, volume, weight, station_num)
        return distance, time, volume, weight, station_num, distance_match_used

    """We want to get the shortest distance, so let match function be 1/d"""

    def match_function(self):
        return lambda life: 1.0 / self.distance(life.gene)[-1]

    """Solver function"""

    def run(self, n=0):
        route = []
        while n > 0:
            self.ga.next()
            n -= 1
        for i in self.ga.best.gene:
            route.append(self.stations[i])
        distance, time, volume, weight, station_num, distance_match_used = self.distance(self.ga.best.gene)
        result = {'route': route,
                  'distance': distance,
                  'time': time,
                  'volume': volume,
                  'weight': weight,
                  'station_num': station_num}
        return result


def FE_tsp_ga(data, distance_matrix, volume_limit, time_limit, weight_limit, iteration_times):
    tsp = TSP(data, distance_matrix, volume_limit, time_limit, weight_limit)
    return tsp.run(iteration_times)
