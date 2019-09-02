# !/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------


import random
import math
import json
from datetime import datetime


class GA(object):
    # Class for Genetic Algorithm in TSP (Multi-Vehicle with the same starting point)

    def __init__(self, cross_rate, mutation_rate, life_count, gene_length, match_function=lambda life: 1):
        self.crossRate = cross_rate  # crossing probability
        self.mutationRate = mutation_rate  # mutation probability
        self.lifeCount = life_count
        # The number of populations： the number of stations list which we filter each time,
        # Here initialized to 100
        self.geneLength = gene_length  # the number of stations
        self.matchFun = match_function  # match function
        self.lives = []  # population
        self.best = None  # save the best one
        self.generation = 1  # the first generation
        self.crossCount = 0  # count for crossing
        self.mutationCount = 0  # count for mutation
        self.bounds = 0.0  # sum of the match function which we use for calculate probability in choosing

        self.init_population()  # init population

    def init_population(self):
        # init population
        self.lives = []
        for i in range(self.lifeCount):
            gene = list(range(self.geneLength))    # gene = [0,1,…… ,self.geneLength-1]
            random.shuffle(gene)                   # random sorting to get a new sequence
            # Class Life is the gene sequence, init the class by gene and match function
            # The bigger match function, the more chance to be selected. Set be -1 at the beginning.
            life = Life(gene)
            self.lives.append(life)                # append the life into the population

    def judge(self):
        """judge, calculate each one's match function and the best one"""
        self.bounds = 0.0        # sum of the match function which we use for calculate probability in choosing
        self.best = self.lives[0]
        for life in self.lives:
            life.score = self.matchFun(life)
            self.bounds += life.score
            if self.best.score < life.score:
                self.best = life

    def cross(self, parent1, parent2):
        """cross"""
        index_begin = random.randint(0, self.geneLength-1)
        index_end = random.randint(index_begin, self.geneLength-1)
        gene_fragment = parent2.gene[index_begin:index_end]  # crossed gene fragment
        new_gene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index_begin:
                new_gene.extend(gene_fragment)  # add gene fragment
                p1len += 1
            if g not in gene_fragment:
                new_gene.append(g)
                p1len += 1
        self.crossCount += 1
        return new_gene

    def mutation(self, gene):
        """mutation"""
        index1 = random.randint(0, self.geneLength-1)
        index2 = random.randint(0, self.geneLength-1)
        # swap the stations in these two index
        gene[index1], gene[index2] = gene[index2], gene[index1]
        self.mutationCount += 1
        return gene

    def get_one(self):
        """choose an individual life"""
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life
        raise Exception("选择错误", self.bounds)

    def new_child(self):
        """generate new children"""
        parent1 = self.get_one()
        # by crossing probability
        rate = random.random()
        if rate < self.crossRate:
            # 交叉
            parent2 = self.get_one()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1.gene
        #  by mutation probability
        rate = random.random()
        if rate < self.mutationRate:
            gene = self.mutation(gene)
        return Life(gene)

    def next(self):
        """产生下一代"""
        self.judge()  # judge, calculate each one's match function
        new_lives = [self.best]
        while len(new_lives) < self.lifeCount:
            new_lives.append(self.new_child())
        self.lives = new_lives
        self.generation += 1


class Life(object):
    """个体类"""
    def __init__(self, gene=None):
        self.gene = gene
        self.score = -2


class TSP(object):
    def __init__(self, data, aLifeCount=100):
        self.cities = []

        self.init_cities(data)
        self.lifeCount = aLifeCount
        self.ga = GA(
            aCrossRate=0.7,
            aMutationRate=0.02,
            aLifeCount=self.lifeCount,
            aGeneLength=len(self.cities),
            aMatchFun=self.match_function()
        )

    def init_cities(self, data):
        # 这个文件里是34个城市的经纬度

        self.cities = [
            (116.46, 39.92, '北京'), (117.2, 39.13, '天津'), (121.48, 31.22, '上海'),
            (106.54, 29.59, '重庆'), (91.11, 29.97, '拉萨'), (126.63, 45.75, '哈尔滨')
        ]

        self.cities = [
            (116.46, 39.92, '北京'), (117.2, 39.13, '天津'), (121.48, 31.22, '上海'), (106.54, 29.59, '重庆'), (91.11, 29.97, '拉萨'),
            (87.68, 43.77, '乌鲁木齐'), (106.27, 38.47, '银川'), (111.65, 40.82, '呼和浩特'), (108.33, 22.84, '南宁'), (126.63, 45.75, '哈尔滨'),
            (125.35, 43.88, '长春'), (123.38, 41.8, '沈阳'), (114.48, 38.03, '石家庄'), (112.53, 37.87, '太原'), (101.74, 36.56, '西宁'),
            (117.0, 36.65, '济南'), (113.6, 34.76, '郑州'), (118.78, 32.04, '南京'), (117.27, 31.86, '合肥'), (120.19, 30.26, '杭州'),
            (119.3, 26.08, '福州'), (115.89, 28.68, '南昌'), (113.0, 28.21, '长沙'), (114.31, 30.52, '武汉'), (113.23, 23.16, '广州'),
            (121.5, 25.05, '台北'), (110.35, 20.02, '海口'), (103.73, 36.03, '兰州'), (108.95, 34.27, '西安'), (104.06, 30.67, '成都'),
            (106.71, 26.57, '贵阳'), (102.73, 25.04, '昆明'), (114.1, 22.2, '香港'), (113.33, 22.13, '澳门')
        ]

        self.cities = data
        # order是遍历所有城市的一组序列，如[1,2,3,7,6,5,4,8……]

    # distance就是计算这样走要走多长的路

    def distance(self, order):
        distance = 0.0
        # i从-1到32,-1是倒数第一个
        for i in range(-1, len(self.cities) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.cities[index1], self.cities[index2]
            earth_radius = 6378137.0
            pi = 3.1415926
            distance += math.acos(math.sin(city1[1] * pi / 180) * math.sin(city2[1] * pi / 180) +
                                  math.cos(city1[1] * pi / 180) * math.cos(city2[1] * pi / 180) *
                                  math.cos(
                                     (city1[0] - city2[0]) * pi / 180)) * earth_radius
            # distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

        return distance

    # 适应度函数，因为我们要从种群中挑选距离最短的，作为最优解，所以（1/距离）最长的就是我们要求的
    def match_function(self):
        return lambda life: 1.0 / (self.distance(life.gene)+0.0001)

    def run(self, n=0):
        distance = 0
        station = []
        while n > 0:
            self.ga.next()
            distance = self.distance(self.ga.best.gene)
            # print("{0} : {1}".format(self.ga.generation, distance))
            # print(self.ga.best.gene)
            n -= 1

        # print("经过 {0} 次迭代，最优解距离为： {1}".format(self.ga.generation, distance))
        # print("遍历城市顺序为：")
        # print "遍历城市顺序为：", self.ga.best.gene
        # 打印出我们挑选出的这个序列中
        for i in self.ga.best.gene:
        #   print(self.cities[i][2])
            station.append(self.cities[i][2])
        result = [station, distance]
        return result


def tsp_ga_main(data):
    tsp = TSP(data)
    return tsp.run(1000)


if __name__ == '__main__':
    from algorithms.src.basic.tictoc import TicToc

    TicToc.tic()
    with open("TSP_ga_data_set_3.json", "r", encoding="utf-8") as TSP_ga_data_set_data:
        data = json.load(TSP_ga_data_set_data)
    ans = tsp_ga_main(data)
    TicToc.toc()



