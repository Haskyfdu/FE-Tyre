#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random


Initial_Score = -1


class Life(object):
    # individual class
    def __init__(self, gene=None):
        self.gene = gene
        self.score = Initial_Score


class GA(object):
    # Genetic Algorithm
    def __init__(self, cross_rate, mutation_rate, life_count, gene_length, match_fun=lambda life: 1.0):
        self.cross_rate = cross_rate  # cross probability
        self.mutation_rate = mutation_rate  # mutation probability
        self.life_count = life_count  # total group number
        # (how many sequences we filter in each time, initialized to 100)
        self.gene_length = gene_length  # length of sequence
        self.match_fun = match_fun  # match function
        self.lives = []  # population
        self.best = None  # save the best individual in this generation
        self.generation = 1  # count of generation
        self.cross_count = 0  # times of cross
        self.mutation_count = 0  # times of mutation
        self.bounds = 0.0  # sum of the adaptation values, used to calculate the probability
        self.init_population()  # initial population

    """Initial population"""
    def init_population(self):
        self.lives = []
        for i in range(self.life_count):
            gene = list(range(self.gene_length))  # randomly sort all elements to get a new sequence
            random.shuffle(gene)
            # Class Life is a gene sequence and have two parameters,
            # one is the sequence gene, and the other is the initial adaptation values of the sequence.
            # Because the greater the adaptation values, the more likely it is to be selected,
            # so all genes in the population are initially initialized to -1.
            life = Life(gene)  # put the life into the population
            self.lives.append(life)

    """Evaluate and calculate the adaptation value of each individual"""
    def judge(self):
        self.bounds = 0.0  # sum of the adaptation values, used to calculate the probability
        self.best = self.lives[0]  # suppose the first gene in the population be selected
        for life in self.lives:
            life.score = self.match_fun(life)
            self.bounds += life.score
            if self.best.score < life.score:  # update the best gene if the adaptation value of the new gene
                self.best = life  # is greater than the original best gene

    """Cross"""
    def cross(self, parent1, parent2):
        index1 = random.randint(0, self.gene_length - 1)
        index2 = random.randint(index1, self.gene_length - 1)
        temp_gene = parent2.gene[index1:index2]  # crossed gene fragment
        new_gene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                new_gene.extend(temp_gene)  # insert gene fragment
                p1len += 1
            if g not in temp_gene:
                new_gene.append(g)
                p1len += 1
        self.cross_count += 1
        return new_gene

    """Mutation"""
    def mutation(self, gene):
        index1 = random.randint(0, self.gene_length - 1)
        index2 = random.randint(0, self.gene_length - 1)
        gene[index1], gene[index2] = gene[index2], gene[index1]  # swap the encoding of these two locations
        self.mutation_count += 1
        return gene

    """Reversal operation for TSP"""
    def reverse(self, gene):
        index1 = random.randint(0, self.gene_length - 1)
        index2 = random.randint(index1, self.gene_length - 1)
        gene_temp = gene[index1:index2 + 1]
        gene_temp.reverse()  # reversed gene fragment
        gene[index1:index2 + 1] = gene_temp
        return gene

    """Choose an individual"""
    def get_one(self):
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life
        raise Exception("Select Error", self.bounds)

    """Create a new individual"""
    def new_child(self):
        parent1 = self.get_one()
        rate = random.random()
        if rate < self.cross_rate:
            parent2 = self.get_one()
            gene = self.cross(parent1, parent2)  # cross by corresponding probability
        else:
            gene = parent1.gene
        rate = random.random()
        if rate < self.mutation_rate:
            gene = self.mutation(gene)  # mutation by corresponding probability
        rate = random.random()
        if rate < self.mutation_rate:
            gene = self.reverse(gene)  # reverse by corresponding probability
        return Life(gene)

    """Create a new generation"""
    def next(self):
        self.judge()  # evaluate and calculate the adaptation value of each individual
        new_lives = [self.best]  # make sure the best one stay in the next generation
        while len(new_lives) < self.life_count:
            new_lives.append(self.new_child())
        self.lives = new_lives
        self.generation += 1