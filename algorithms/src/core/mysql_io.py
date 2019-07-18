import pymysql
import json


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
    while True:
        receiver = cur.fetchone()  # 获取一条数据 元组转列表
        if not receiver:
            break  # 如果抓取的数据为None,退出循环
        if receiver[6] is None:
            prov = '无'
        else:
            prov = receiver[6]
        if receiver[7] is None:
            city = '无'
        else:
            city = receiver[7]
        if receiver[9] is None:
            address = '无'
        else:
            address = receiver[9]
        if receiver[22] is None:
            storage_id = -1
        else:
            storage_id = receiver[22]
        receiver_dict.update({receiver[2]: {'Name': receiver[3], 'Prov': prov, 'City': city,
                                            'Address': address, 'shipper_id': receiver[15],
                                            'status': receiver[21], 'storage_id': storage_id,
                                            'creat_time': str(receiver[20])}})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return receiver_dict


def sql_order(sql):
    con = pymysql.connect(
        host='47.96.144.127',
        port=3306,
        user='afy_logistics',
        passwd='1qaz2wsx',
        db='logistics_oms'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    cur.execute(sql)      # 执行sql
    order_dict = {}    # 新建空字典
    while True:
        order = cur.fetchone()  # 获取一条数据 元组转列表
        if not order:
            break  # 如果抓取的数据为None,退出循环
        if order[8] is not None and order[10] is not None:
            if order[13] is None:
                parts_core = '无'
            else:
                parts_core = order[13]
            order_dict.update({order[4]: {'priority': order[2], 'type_id': order[3], 'parts_core': parts_core,
                                          'shipper_id': order[5], 'receiver_id': order[6],
                                          'business': order[12], 'channel': order[15],
                                          'flag': order[16], 'status': order[21],
                                          'remark': order[17],
                                          'ord_time': str(order[8]),
                                          'confirm_time': str(order[7]),
                                          'ship_time': str(order[10])}})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return order_dict


def sql_ship(sql):
    con = pymysql.connect(
        host='47.96.144.127',
        port=3306,
        user='afy_logistics',
        passwd='1qaz2wsx',
        db='logistics_oms'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    cur.execute(sql)      # 执行sql
    ship_dict = {}    # 新建空字典
    while True:
        ship = cur.fetchone()  # 获取一条数据 元组转列表
        if not ship:
            break  # 如果抓取的数据为None,退出循环
        ship_dict.update({ship[2]: {'Name': ship[5], 'type_id': ship[4],
                                    'flag': ship[13], 'status': ship[17]}})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return ship_dict


def sql_order_list(sql):
    con = pymysql.connect(
        host='47.96.144.127',
        port=3306,
        user='afy_logistics',
        passwd='1qaz2wsx',
        db='logistics_oms'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    cur.execute(sql)      # 执行sql
    order_list_dict = {}    # 新建空字典
    while True:
        order_list = cur.fetchone()  # 获取一条数据 元组
        if not order_list:
            break  # 如果抓取的数据为None,退出循环
        if order_list[8] is None:
            cube = 0
        else:
            cube = order_list[8]
        if order_list[9] is None:
            weight = 0
        else:
            weight = order_list[9]
        if order_list[11] is None:
            remark = '无'
        else:
            remark = order_list[11]
        if not (order_list_dict.__contains__(order_list[2])):
            order_list_dict[order_list[2]] = {}
        order_list_dict[order_list[2]].update({order_list[3]: {'cargo_id': order_list[4],
                                                               'cargo_desc': order_list[5],
                                                               'cargo_spec': order_list[6],
                                                               'cube': cube,
                                                               'weight': weight,
                                                               'quantity': order_list[10],
                                                               'remark': remark,
                                                               'status': order_list[12],
                                                               'flag': order_list[13]}})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return order_list_dict


def sql_receiver_transport(sql):
    con = pymysql.connect(
        host='47.96.144.127',
        port=3306,
        user='afy_logistics',
        passwd='1qaz2wsx',
        db='logistics_oms'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    cur.execute(sql)      # 执行sql
    receiver_transport_dict = {}    # 新建空字典
    while True:
        receiver_transport = cur.fetchone()  # 获取一条数据 元组
        if not receiver_transport:
            break  # 如果抓取的数据为None,退出循环
        if receiver_transport[14] is None:
            delivery_price = 0
        else:
            delivery_price = float(receiver_transport[14])
        if receiver_transport[17] is None:
            duration = 0
        else:
            duration = float(receiver_transport[17])
        if receiver_transport[18] is None:
            receipt_price = 0
        else:
            receipt_price = float(receiver_transport[18])
        if receiver_transport[19] is None:
            min_price = 0
        else:
            min_price = float(receiver_transport[19])
        if receiver_transport[6] == "<=":
            text = '起步'
        else:
            text = '计价'
        if not (receiver_transport_dict.__contains__(receiver_transport[2])):
            receiver_transport_dict[receiver_transport[2]] = {}
        if not (receiver_transport_dict[receiver_transport[2]].__contains__(receiver_transport[3])):
            receiver_transport_dict[receiver_transport[2]][receiver_transport[3]] = {'Name': receiver_transport[4]}
        if not (receiver_transport_dict[receiver_transport[2]][receiver_transport[3]]
                .__contains__(receiver_transport[5])):
            receiver_transport_dict[receiver_transport[2]][receiver_transport[3]][receiver_transport[5]] = {}
        receiver_transport_dict[receiver_transport[2]][receiver_transport[3]][receiver_transport[5]].update\
            ({'val': float(receiver_transport[7]), text: float(receiver_transport[9]),
              'delivery_price': delivery_price, 'duration': duration,
              'receipt_price': receipt_price, 'min_price': min_price})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return receiver_transport_dict


def sql_tms_order(sql):
    con = pymysql.connect(
        host='47.96.144.127',
        port=3306,
        user='afy_logistics',
        passwd='1qaz2wsx',
        db='logistics_tms'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    cur.execute(sql)      # 执行sql
    tms_order_dict = {}    # 新建空字典
    while True:
        tms_order = cur.fetchone()  # 获取一条数据 元组
        if not tms_order:
            break  # 如果抓取的数据为None,退出循环
        if not (tms_order_dict.__contains__(tms_order[1])):
            tms_order_dict[tms_order[1]] = {}
        tms_order_dict[tms_order[1]].update({'origin': tms_order[4],
                                             'destination': tms_order[5],
                                             'freight': int(tms_order[7]),
                                             'freight_mode': int(tms_order[8]),
                                             'transport_type': int(tms_order[16]),
                                             'carrier_id': tms_order[17]})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return tms_order_dict


def sql_tms_order_list(sql):
    con = pymysql.connect(
        host='47.96.144.127',
        port=3306,
        user='afy_logistics',
        passwd='1qaz2wsx',
        db='logistics_tms'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    cur.execute(sql)      # 执行sql
    tms_order_list_dict = {}    # 新建空字典
    while True:
        tms_order_list = cur.fetchone()  # 获取一条数据 元组
        if not tms_order_list:
            break  # 如果抓取的数据为None,退出循环
        tms_order_list_dict.update({tms_order_list[24]: tms_order_list[2]})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return tms_order_list_dict


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
        if inventory_data[15] is not None:
            stock = inventory_data[15]
        elif inventory_data[14] is not None:
            stock = inventory_data[14]
        elif inventory_data[13] is not None:
            stock = inventory_data[13]
        elif inventory_data[12] is not None:
            stock = inventory_data[12]
        else:
            stock = 0
        if inventory_dict.__contains__(inventory_data[8]):
            if inventory_dict[inventory_data[8]].__contains__(inventory_data[2]):
                if inventory_dict[inventory_data[8]][inventory_data[2]][0] < inventory_data[3]:
                    inventory_dict[inventory_data[8]][inventory_data[2]] = [inventory_data[3], stock]  # 将数据录入
            else:
                inventory_dict[inventory_data[8]].update({inventory_data[2]: [inventory_data[3], stock]})
        else:
            inventory_dict.update({inventory_data[8]: {inventory_data[2]: [inventory_data[3], stock]}})
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return inventory_dict


if __name__ == '__main__':
    # 输入
    order_data = sql_order("SELECT * FROM logistics_oms.oms_shipper_order where confirm_date > '2019-07-02 00:00:00' "
                           "and eid = 'aifuyi';")
    json_str = json.dumps(order_data, indent=4, ensure_ascii=False)
    with open('order_dict.json', 'w') as json_file:
        json_file.write(json_str)  # 输出为order_dict

    order_list_data = sql_order_list(
        "SELECT * FROM logistics_oms.oms_shipper_order_list where create_time > '2019-07-02 00:00:00' "
        "and status > 0 and eid = 'aifuyi';")
    json_str = json.dumps(order_list_data, indent=4, ensure_ascii=False)
    with open('order_list_dict.json', 'w') as json_file:
        json_file.write(json_str)  # 输出为order_list_dict

    ship_data = sql_ship("SELECT * FROM logistics_oms.oms_shipper where eid = 'aifuyi';")
    json_str = json.dumps(ship_data, indent=4, ensure_ascii=False)
    with open('ship_dict.json', 'w') as json_file:
        json_file.write(json_str)  # 输出为ship_dict

    receiver_data = sql_receiver("SELECT * FROM logistics_oms.oms_receiver where status > 0 and eid = 'aifuyi';")
    json_str = json.dumps(receiver_data, indent=4, ensure_ascii=False)
    with open('receiver_dict.json', 'w') as json_file:
        json_file.write(json_str)  # 输出为receiver_dict

    receiver_transport_data = sql_receiver_transport("SELECT * FROM logistics_oms.oms_receiver_transport where "
                                                     "status>0 and eid = 'aifuyi';")
    json_str = json.dumps(receiver_transport_data, indent=4, ensure_ascii=False)
    with open('receiver_transport_dict.json', 'w') as json_file:
        json_file.write(json_str)  # 输出为receiver_transport_dict

    tms_order_data = sql_tms_order("SELECT * FROM logistics_tms.tms_order where ship_time > '2019-06-10'"
                                   "and eid = 'aifuyi';")
    json_str = json.dumps(tms_order_data, indent=4, ensure_ascii=False)
    with open('tms_order_dict.json', 'w') as json_file:
        json_file.write(json_str)  # 输出为tms_order_dict

    tms_order_list_data = sql_tms_order_list("SELECT * FROM logistics_tms.tms_order_list where eid = 'aifuyi';")
    json_str = json.dumps(tms_order_list_data, indent=4, ensure_ascii=False)
    with open('tms_order_list_dict.json', 'w') as json_file:
        json_file.write(json_str)

    wms_inventory_list_data = sql_wms_inventory_list("SELECT * FROM logistics_wms.wms_inventory_list "
                                                     "where inventory  > '20190501000';")
    json_str = json.dumps(wms_inventory_list_data, indent=4, ensure_ascii=False)
    with open('wms_inventory_list_dict.json', 'w') as json_file:
        json_file.write(json_str)