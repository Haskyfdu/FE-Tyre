#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------


from algorithms.algorithm_main import run


if __name__ == '__main__':

    # 模拟某天订单的自动装配及路径规划
    i = 1
    Date0 = "'2019-07-" + str(i).zfill(2) + " 10:00:00'"
    Date1 = "'2019-07-" + str(i + 1).zfill(2) + " 10:00:00'"
    print(Date0 + '~' + Date1)
    Num_car = 1
    [Result, Route, Error_list, Success_list, Inventory_dict, Cost000, Num_today, Num_in_station], \
    [Result2, Route2, Error_list2, Success_list2, Inventory_dict2, Cost0002, Num_today2, Num_in_station2] \
        = run(Date0, Date1, Num_car)
