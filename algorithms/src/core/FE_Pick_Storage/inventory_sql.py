#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

import pymysql
import json


def sql_wms_inventory_list(sql):                 # SQL查询库存
    con = pymysql.connect(
        host='47.96.144.127',
        port=3306,
        user='afy_logistics',
        passwd='1qaz2wsx',
        db='logistics_wms'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    cur.execute(sql)      # 执行sql
    inventory_dict = {}   # 新建空字典
    while True:
        inventory_data = cur.fetchone()  # 获取一条数据 元组
        if not inventory_data:
            break  # 如果抓取的数据为None,退出循环
        if inventory_data[11] is not None:
            valid = inventory_data[11]
        else:
            valid = 0
        if inventory_data[12] is not None:
            block = inventory_data[12]
        else:
            block = 0
        use_stock = max(valid - block, 0)
        if inventory_data[6] == '5ND601307C RCO':
            print(inventory_data[6])
        if inventory_dict.__contains__(inventory_data[6]):
            if inventory_dict[inventory_data[6]].__contains__(inventory_data[2]):
                inventory_dict[inventory_data[6]][inventory_data[2]] += use_stock  # 将数据录入
            else:
                inventory_dict[inventory_data[6]].update({inventory_data[2]: use_stock})
        else:
            inventory_dict.update({inventory_data[6]: {inventory_data[2]: use_stock}})
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return inventory_dict


if __name__ == '__main__':

    wms_inventory_list_data = sql_wms_inventory_list("SELECT * FROM logistics_wms.wms_stock where status=1 and flag=1;")
    json_str = json.dumps(wms_inventory_list_data, indent=4, ensure_ascii=False)
    with open('wms_inventory_list_dict.json', 'w') as json_file:
        json_file.write(json_str)
