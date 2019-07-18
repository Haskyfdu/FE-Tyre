import pymysql
import math
import json

with open("order_dict.json", "r", encoding="utf-8") as order_data:
    Order_dict = json.load(order_data)  # 订单
with open("order_list_dict.json", "r", encoding="utf-8") as order_list_data:
    Order_list_dict = json.load(order_list_data)  # 订单详情
with open("receiver_lng_lat_dict.json", "r", encoding="utf-8") as receiver_lng_lat_data:
    Receiver_lng_lat_dict = json.load(receiver_lng_lat_data)  # 客户地址经纬度
with open("storage_lng_lat_dict.json", "r", encoding="utf-8") as storage_lng_lat_data:
    Storage_lng_lat_dict = json.load(storage_lng_lat_data)  # 仓库经纬度


def sql_tms_order_list(storage_code, cargo_id, quantity):                 # SQL查询库存
    con = pymysql.connect(
        host='47.96.144.127',
        port=3306,
        user='afy_logistics',
        passwd='1qaz2wsx',
        db='logistics_wms'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    sql = "SELECT * FROM logistics_wms.wms_inventory_list where sn = '" + str(cargo_id) \
          + "' and storage = '" + str(storage_code) + "' order by inventory desc;"
    cur.execute(sql)      # 执行sql
    stock_data = cur.fetchone()  # 获取一条数据 元组
    if not stock_data:
        check = False
    else:
        if stock_data[15] is not None:
            stock = stock_data[15]
        elif stock_data[14] is not None:
            stock = stock_data[14]
        elif stock_data[13] is not None:
            stock = stock_data[13]
        elif stock_data[12] is not None:
            stock = stock_data[12]
        else:
            stock = 0
        if stock < quantity:
            check = False
        else:
            check = True
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return check


def distance_sort(receiver_lng_lat, storage_lng_lat_dict):              # 仓库点距离排序
    storage_list_by_distance = []
    distance_list = []
    distance_dict = {}
    for key in storage_lng_lat_dict:
        distance = calculate_distance(receiver_lng_lat, storage_lng_lat_dict[key])
        distance_dict.update({key: distance})
        distance_list.append(distance)
    distance_list.sort()
    for i in range(len(distance_list)):
        for (k, v) in distance_dict.items():
            if abs(v - distance_list[i]) < 0.00000000001:
                storage_list_by_distance.append(k)
                break
    return storage_list_by_distance


def calculate_distance(lng_lat_1, lng_lat_2):               # 计算距离
    earth_radius = 6378137.0
    pi = 3.1415926
    distance = math.acos(math.sin(float(lng_lat_1[1][0:8]) * pi / 180) * math.sin(float(lng_lat_2[1][0:8]) * pi / 180) +
                         math.cos(float(lng_lat_1[1][0:8]) * pi / 180) * math.cos(float(lng_lat_2[1][0:8]) * pi / 180) *
                         math.cos((float(lng_lat_1[0][0:8]) - float(lng_lat_2[0][0:8])) * pi / 180)) * earth_radius
    return distance


def pick_storage(order, receiver_lng_lat, storage_lng_lat_dict):        # 选取仓库
    # cargo_id = order['cargo_id']
    # quantity = order['quantity']
    storage_list_by_distance = distance_sort(receiver_lng_lat, storage_lng_lat_dict)
    for storage_code in storage_list_by_distance:
        if True:                                #sql_tms_order_list(storage_code, cargo_id, quantity):
            storage_code_use = storage_code
            break
    return storage_code_use


