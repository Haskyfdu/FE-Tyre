#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

from algorithms.algorithm_io import ImportData, ExportResults
try:
    from algorithms.src.basic.class_tictoc import TicToc
    from algorithms.src.core.FE_Pick_Storage.automatic_loading import automatic_loading
    from algorithms.src.core.FE_Pick_Storage.inventory_sql import sql_wms_inventory_list
except ImportError:
    from algorithms.lib.basic.class_tictoc import TicToc
    from algorithms.lib.core.FE_Pick_Storage.automatic_loading import automatic_loading
    from algorithms.lib.core.FE_Pick_Storage.inventory_sql import sql_wms_inventory_list


def run_pick(date):

    TicToc.tic()
    order_list = ImportData.read(filename='order_list_'+date+'.json')
    receiver_dict = ImportData.read(filename='receiver_dict.json')
    inventory_dict = sql_wms_inventory_list("SELECT * FROM logistics_wms.wms_stock where status=1 and flag=1;")
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
