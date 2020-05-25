#!/usr/bin/env python
# -*- coding: utf-8 -*-


from algorithms.algorithm_main import blueprint_main
from flask import Flask


app_test = Flask(__name__)
app_test.register_blueprint(blueprint_main)


if __name__ == '__main__':
    app_test.run(host="127.0.0.1", port=7001, debug=False)

    # 模拟某天订单的自动装配及路径规划
    # i = 1
    # Date0 = "'2019-07-" + str(i).zfill(2) + " 10:00:00'"
    # Date1 = "'2019-07-" + str(i + 1).zfill(2) + " 10:00:00'"
    # print(Date0 + '~' + Date1)
    # Num_car = 1
    # [Result, Route, Error_list, Success_list, Inventory_dict, Cost000, Num_today, Num_in_station], \
    # [Result2, Route2, Error_list2, Success_list2, Inventory_dict2, Cost0002, Num_today2, Num_in_station2] \
    #     = run(Date0, Date1, Num_car)
