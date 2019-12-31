#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2019 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

from algorithms.algorithm_io import ImportData, ExportResults
from algorithms.src.basic.class_tictoc import TicToc
from algorithms.src.core.FE_Pick_Storage.automatic_loading import automatic_loading
from flask import jsonify


def run_pick(date):

    TicToc.tic()
    order_list = ImportData.read(filename='order_list_'+date+'.json')
    receiver_dict = ImportData.read(filename='receiver_dict.json')
    inventory_dict = ImportData.read(filename='inventory_dict_'+date+'.json')
    result, inventory_dict = automatic_loading(order_list=order_list,
                                               inventory_dict=inventory_dict,
                                               receiver_dict=receiver_dict)
    TicToc.toc()
    ExportResults.write(result, filename='result_'+date+'.json')
    ExportResults.write(inventory_dict, filename='inventory_dict_' + date + '.json')
    print('Optimization completed, the output file: data/output/result_'+date+'.json')
    return result


if __name__ == '__main__':

    run_pick('2019-12-30')
