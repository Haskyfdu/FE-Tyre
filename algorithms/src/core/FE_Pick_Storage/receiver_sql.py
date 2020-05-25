#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pymysql


def sql_receiver(sql):
    con = pymysql.connect(
        host='47.96.144.127',
        port=3306,
        user='afy_logistics',
        passwd='1qaz2wsx',
        db='logistics_oms'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    cur.execute(sql)      # 执行sql
    receiver_dict = {}    # 新建空字典
    receiver_missing_list = []
    while True:
        i = 0
        receiver = cur.fetchone()  # 获取一条数据 元组转列表
        if not receiver:
            break  # 如果抓取的数据为None,退出循环
        if receiver[6] is None or len(receiver[6]) == 0:
            prov = ''
            # print(receiver, 'lost prov')
            receiver_missing_list.append(receiver[0:12])
            i = 1
        elif receiver[6][-1] == '省' or receiver[6][-1] == '市':
            prov = receiver[6][0:-1]
        else:
            prov = receiver[6]
        if receiver[7] is None or len(receiver[7]) == 0:
            city = ''
            # print(receiver, 'lost city')
            receiver_missing_list.append(receiver[0:12])
            i = 1
        elif receiver[7][-1] == '省' or receiver[7][-1] == '市':
            city = receiver[7][0:-1]
        else:
            city = receiver[7]
        if receiver[9] is None:
            address = ''
        else:
            address = receiver[9]
        if receiver[22] is None:
            storage_id = -1
        else:
            storage_id = receiver[22]
        if i == 0:
            receiver_dict.update({receiver[2]: {
                'Name': receiver[3], 'Tel': receiver[4],
                'Prov': prov, 'City': city, 'Address': address,
                'status': receiver[21]}})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return receiver_dict, receiver_missing_list


if __name__ == '__main__':

    receiver_data, receiver_missing_list_data = sql_receiver(
        "SELECT * FROM logistics_oms.oms_receiver where status > 0 and eid = 'aifuyi';")
    # json_str = json.dumps(receiver_data, indent=4, ensure_ascii=False)
    # with open('../../../../data/input/receiver_dict.json', 'w') as json_file:
    #     json_file.write(json_str)  # 输出为receiver_dict
    # json_str = json.dumps(receiver_missing_list_data, indent=4, ensure_ascii=False)
    # with open('../../../../data/input/receiver_missing_list.json', 'w') as json_file:
    #     json_file.write(json_str)
