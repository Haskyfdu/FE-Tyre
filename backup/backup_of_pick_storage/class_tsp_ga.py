#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random
import math
import json
from datetime import datetime


class GA(object):
    # 遗传算法类

    def __init__(self, aCrossRate, aMutationRate, aLifeCount, aGeneLength, aMatchFun=lambda life: 1):
        self.crossRate = aCrossRate  # 交叉概率
        self.mutationRate = aMutationRate  # 突变概率
        self.lifeCount = aLifeCount  # 种群数量，就是每次我们在多少个城市序列里筛选，这里初始化为100
        self.geneLength = aGeneLength  # 其实就是城市数量
        self.matchFun = aMatchFun  # 适配函数
        self.lives = []  # 种群
        self.best = None  # 保存这一代中最好的个体
        self.generation = 1  # 一开始的是第一代
        self.crossCount = 0  # 一开始还没交叉过，所以交叉次数是0
        self.mutationCount = 0  # 一开始还没变异过，所以变异次数是0
        self.bounds = 0.0  # 适配值之和，用于选择时计算概率

        self.init_population()  # 初始化种群

    def init_population(self):
        # 初始化种群
        self.lives = []
        for i in range(self.lifeCount):
            # gene = [0,1,…… ,self.geneLength-1]
            # 事实就是0到33
            gene = list(range(self.geneLength))
            # 将0到33序列的所有元素随机排序得到一个新的序列
            random.shuffle(gene)
            # Life这个类就是一个基因序列，初始化life的时候,两个参数，一个是序列gene，一个是这个序列的初始适应度值
            # 因为适应度值越大，越可能被选择，所以一开始种群里的所有基因都被初始化为-1
            life = Life(gene)
            # 把生成的这个基因序列life填进种群集合里
            self.lives.append(life)

    def judge(self):
        """评估，计算每一个个体的适配值"""
        # 适配值之和，用于选择时计算概率
        self.bounds = 0.0
        # 假设种群中的第一个基因被选中
        self.best = self.lives[0]
        for life in self.lives:
            life.score = self.matchFun(life)
            self.bounds += life.score
            # 如果新基因的适配值大于原先的best基因，就更新best基因
            if self.best.score < life.score:
                self.best = life

    def cross(self, parent1, parent2):
        """交叉"""
        index1 = random.randint(0, self.geneLength - 1)
        index2 = random.randint(index1, self.geneLength - 1)
        tempGene = parent2.gene[index1:index2]  # 交叉的基因片段
        newGene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                newGene.extend(tempGene)  # 插入基因片段
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        self.crossCount += 1
        return newGene

    def mutation(self, gene):
        """突变"""
        # 相当于取得0到self.geneLength - 1之间的一个数，包括0和self.geneLength - 1
        index1 = random.randint(0, self.geneLength - 1)
        index2 = random.randint(0, self.geneLength - 1)
        # 把这两个位置的城市互换
        gene[index1], gene[index2] = gene[index2], gene[index1]
        # 突变次数加1
        self.mutationCount += 1
        return gene

    def getOne(self):
        """选择一个个体"""
        # 产生0到（适配值之和）之间的任何一个实数
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life

        raise Exception("选择错误", self.bounds)

    def newChild(self):
        """产生新后的"""
        parent1 = self.getOne()
        rate = random.random()

        # 按概率交叉
        if rate < self.crossRate:
            # 交叉
            parent2 = self.getOne()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1.gene

        # 按概率突变
        rate = random.random()
        if rate < self.mutationRate:
            gene = self.mutation(gene)

        return Life(gene)

    def next(self):
        """产生下一代"""
        self.judge()  # 评估，计算每一个个体的适配值
        newLives = []
        newLives.append(self.best)  # 把最好的个体加入下一代
        while len(newLives) < self.lifeCount:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1


SCORE_NONE = -1


class Life(object):
    """个体类"""
    def __init__(self, aGene=None):
        self.gene = aGene
        self.score = SCORE_NONE


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



