#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------
from algorithms.algorithm_io import ImportData, ExportResults
from flask import Flask, jsonify, request, Blueprint
import json
import os


try:
    from algorithms.src.basic.tictoc import TicToc
    from algorithms.src.core import pick_storage
    from algorithms.src.core import automatic_loading
    from algorithms.src.core import intra_city
    from algorithms.src.core import mysql_io
    from algorithms.src.core import mysql_io_af
except ImportError:
    from algorithms.lib.basic.tictoc import TicToc
    from algorithms.lib.core import pick_storage
    from algorithms.lib.core import automatic_loading
    from algorithms.lib.core import intra_city
    from algorithms.lib.core import mysql_io
    from algorithms.lib.core import mysql_io_af

# app = Flask(__name__)
blueprint_main = Blueprint(name='blueprint_main', import_name=__name__)


def update_order(sql):
    order_data = mysql_io.sql_order(sql)
    print('{0} 更新成功'.format('order_data'))
    print('共计' + str(len(order_data)) + '个订单')
    return order_data


def update_order2(sql):
    order_data_af = mysql_io_af.sql_order(sql)
    print('{0} 更新成功'.format('order_data_af'))
    print('共计' + str(len(order_data_af)) + '个订单')
    return order_data_af


def update_order_list(sql):
    order_list_data = mysql_io.sql_order_list(sql)
    print('{0} 更新成功'.format('order_list_data'))
    return order_list_data


def update_order_list2(sql):
    order_list_data_af = mysql_io_af.sql_order_list(sql)
    print('{0} 更新成功'.format('order_list_data_af'))
    return order_list_data_af


def update_inventory_list(sql):
    print('读取库存中...')
    inventory_data = mysql_io.sql_wms_inventory_list(sql)
    print('{0} 更新成功'.format('wms_inventory_data'))
    return inventory_data


def update_inventory_list2(sql):
    print('读取库存中...')
    inventory_data_af = mysql_io_af.sql_wms_inventory_list(sql)
    print('{0} 更新成功'.format('wms_inventory_data_af'))
    return inventory_data_af


def run(date0, date1='2999-01-01', num_car=1):

    TicToc.tic()

    print('==================================aifuyi========================================')

    receiver_transport_dict = ImportData.read(filename='receiver_transport_dict.json')  # 承运商
    receiver_lng_lat_dict = ImportData.read(filename='receiver_lng_lat_dict.json')  # 客户地址经纬度
    storage_lng_lat_dict = ImportData.read(filename='storage_lng_lat_dict.json')  # 仓库经纬度

    print('================================================================================')

    # order_dict = update_order(
    #     "SELECT * FROM logistics_oms.oms_shipper_order where confirm_date > " + date0 +
    #     " and confirm_date < " + date1 + " and status = 1 and eid = 'aifuyi';")
    order_dict = update_order(
        'SELECT * FROM logistics_oms.oms_shipper_order where confirm_date > "' + date0 +
        '" and status = 1 and eid = "aifuyi";')
    # 订单
    # order_list_dict = update_order_list(
    #     "SELECT * FROM logistics_oms.oms_shipper_order_list where create_time > " + date0 +
    #     " and create_time < " + date1 + " and status = 1 and eid = 'aifuyi';")
    order_list_dict = update_order_list(
        'SELECT * FROM logistics_oms.oms_shipper_order_list where create_time > "' + date0 +
        '" and status = 1 and eid = "aifuyi";')
    # 订单详情
    inventory_dict = update_inventory_list(
        "SELECT * FROM logistics_wms.wms_inventory_list where inventory > '20190501000' and eid = 'aifuyi';")
    # 库存
    loading_list, inventory_dict = \
        automatic_loading.automatic_loading(order_dict, order_list_dict, storage_lng_lat_dict,
                                            receiver_lng_lat_dict, inventory_dict)
    automatic_loading_result, error_list, success_list = \
        automatic_loading.automatic_transport_plan(loading_list, receiver_transport_dict)

    print('================================================================================')

    ExportResults.write(automatic_loading_result, filename='automatic_loading_result.json')
    print('共计生成' + str(len(automatic_loading_result)) + '个运单')
    ExportResults.write(error_list, filename='error_list.json')
    print('共计' + str(len(error_list)) + '个子订单信息错误')
    ExportResults.write(success_list, filename='success_list.json')
    print('共计' + str(len(success_list)) + '个子订单自动装配成功')
    ExportResults.write(inventory_dict, filename='inventory_dict.json')

    print('================================================================================')

    route_result, cost000, num_today, num_in_station = \
        intra_city.intra_city_service(automatic_loading_result, receiver_lng_lat_dict, num_car)
    ExportResults.write(route_result, filename='route_result.json')
    print('共计' + str(num_today) + '个站点')
    if route_result:
        print('总路程约' + str(int(round(1.2 * route_result[0][1] / 1000))) + '公里')

    print('================================================================================')

    print('==================================af============================================')

    receiver_transport_dict2 = ImportData.read(filename='receiver_transport_dict2.json')  # 承运商
    receiver_lng_lat_dict2 = ImportData.read(filename='receiver_lng_lat_dict2.json')  # 客户地址经纬度
    storage_lng_lat_dict2 = ImportData.read(filename='storage_lng_lat_dict2.json')  # 仓库经纬度

    print('================================================================================')

    order_dict2 = update_order2(
        "SELECT * FROM logistics_oms.oms_shipper_order where confirm_date > " + date0 +
        " and confirm_date < " + date1 + " and status = 1 and eid = 'af' and priority = 0;")
    # 订单
    order_list_dict2 = update_order_list2(
        "SELECT * FROM logistics_oms.oms_shipper_order_list where create_time > " + date0 +
        " and create_time < " + date1 + " and status = 1 and eid = 'af';")
    # 订单详情
    inventory_dict2 = update_inventory_list2(
        "SELECT * FROM logistics_wms.wms_inventory_list where inventory > '20190501000' and eid = 'af';")
    # 库存
    loading_list2, inventory_dict2 = \
        automatic_loading.automatic_loading(order_dict2, order_list_dict2, storage_lng_lat_dict2,
                                            receiver_lng_lat_dict2, inventory_dict2)
    automatic_loading_result2, error_list2, success_list2 = \
        automatic_loading.automatic_transport_plan(loading_list2, receiver_transport_dict2)

    print('================================================================================')

    ExportResults.write(automatic_loading_result2, filename='automatic_loading_result2.json')
    print('共计生成' + str(len(automatic_loading_result2)) + '个运单')
    ExportResults.write(error_list2, filename='error_list2.json')
    print('共计' + str(len(error_list2)) + '个子订单信息错误')
    ExportResults.write(success_list2, filename='success_list2.json')
    print('共计' + str(len(success_list2)) + '个子订单自动装配成功')
    ExportResults.write(inventory_dict2, filename='inventory_dict2.json')

    print('================================================================================')

    route_result2, cost0002, num_today2, num_in_station2 = \
        intra_city.intra_city_service(automatic_loading_result2, receiver_lng_lat_dict2, num_car)
    ExportResults.write(route_result2, filename='route_result2.json')
    print('共计' + str(num_today2) + '个站点')
    if route_result2:
        print('总路程约' + str(int(round(1.2*route_result2[0][1]/1000))) + '公里')

    print('================================================================================')

    TicToc.toc()
    recall_info = '算法已完成'
    final_recall(recall_info)
    return [[automatic_loading_result, route_result, error_list, success_list,
             inventory_dict, cost000, num_today, num_in_station],
            [automatic_loading_result2, route_result2, error_list2, success_list2,
             inventory_dict2, cost0002, num_today2, num_in_station2]]


@blueprint_main.route('/run', methods=['GET', 'POST'])
def algorithm_main():
    print('Algorithm started')
    if request.method == 'GET':
        return jsonify({"description": "Algorithm Post Request", "status": "UP"})
    elif request.method == 'POST':
        json_post_information = json.loads(request.get_data())
        import _thread
        _thread.start_new_thread(run, (json_post_information, ))
        return jsonify({"running status": 'success'})
    else:
        return 'Algorithm post request failed'


def final_recall(recall_info):
    output_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) \
                 + '/FE-Tyre/data/output/'
    # request.post(url='http://10.135.80.122:8090/zzpwarndata/api/ai/warnData/log/update',
    #              json=output_dir)
    print(output_dir)
    print(recall_info)


def flask_test():
    url = 'http://127.0.0.1:9000/clean'
    data = '2019-07-22'
    rq = request.post(url=url, json=data)
    print(rq.text)


if __name__ == '__main__':

    app_test = Flask(__name__)
    app_test.register_blueprint(blueprint_main)
    app_test.run(host="127.0.0.1", port=9000, debug=False)
    #
    #  Cost_default = []
    #  Num_station = []
    #  Cost_default2 = []
    #  Num_station2 = []
    #  for i in range(1, 2):
    #      Date0 = "'2019-07-" + str(i).zfill(2) + " 10:00:00'"
    #      Date1 = "'2019-07-" + str(i+1).zfill(2) + " 10:00:00'"
    #      print(Date0 + '~' + Date1)
    #      [Result, Route, Error_list, Success_list, Inventory_dict, Cost000, Num_today, Num_in_station], \
    #      [Result2, Route2, Error_list2, Success_list2, Inventory_dict2, Cost0002, Num_today2, Num_in_station2] \
    #          = run(Date0, Date1)
    #      Cost_default.append(Cost000)
    #      Num_station.append(Num_today)
    #      Cost_default2.append(Cost0002)
    #      Num_station2.append(Num_today2)
