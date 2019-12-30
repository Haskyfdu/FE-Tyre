import json
from backup.backup_of_pick_storage import pick_storage

with open("order_dict.json", "r", encoding="utf-8") as order_data:
    Order_dict = json.load(order_data)  # 订单
with open("order_list_dict.json", "r", encoding="utf-8") as order_list_data:
    Order_list_dict = json.load(order_list_data)  # 订单详情
with open("receiver_transport_dict.json", "r", encoding="utf-8") as receiver_transport_data:
    Receiver_transport_dict = json.load(receiver_transport_data)  # 承运商
with open("receiver_lng_lat_dict.json", "r", encoding="utf-8") as receiver_lng_lat_data:
    Receiver_lng_lat_dict = json.load(receiver_lng_lat_data)  # 客户地址经纬度
with open("storage_lng_lat_dict.json", "r", encoding="utf-8") as storage_lng_lat_data:
    Storage_lng_lat_dict = json.load(storage_lng_lat_data)  # 仓库经纬度


def cost_calculate(dict_use, num):
    if not dict_use.__contains__('起步'):
        dict_use['起步'] = dict_use['计价']
    if not dict_use.__contains__('计价'):
        dict_use['计价'] = dict_use['起步']
    if dict_use['计价'] * dict_use['起步'] == 0:
        cost_result = 99999
    else:
        cost_result = dict_use['val'] * dict_use['起步'] + int(num > float(dict_use['val'])) \
                  * (num - dict_use['val']) * dict_use['计价']
    return cost_result


def check_receiver_id(receiver_id):
    j = len(receiver_id)
    for i in range(len(receiver_id)):
        if receiver_id[i] == '_':
            j = i
            break
    return receiver_id[0:j]


def automatic_loading(order_dict, order_list_dict, receiver_transport_dict, storage_lng_lat_dict):
    cost_all = {}
    for key1 in order_dict:                       # key1 订单号
        if order_list_dict.__contains__(key1):
            cube = 0
            weight = 0
            quantity = 0
            cost_all.update({key1: {}})
            for key2 in order_list_dict[key1]:    # key2 订单详情
                cube = cube + order_list_dict[key1][key2]['cube'] * order_list_dict[key1][key2]['quantity']
                weight = weight + order_list_dict[key1][key2]['weight'] * order_list_dict[key1][key2]['quantity']
                quantity = quantity + order_list_dict[key1][key2]['quantity']
            receiver_id = check_receiver_id(order_dict[key1]['receiver_id'])
            receiver_lng_lat = Receiver_lng_lat_dict[order_dict[key1]['receiver_id']]
            storage_code = pick_storage.pick_storage(order_list_dict[key1][key2], receiver_lng_lat, storage_lng_lat_dict)
            cost_all[key1].update({'storage_code': storage_code})
            if receiver_transport_dict.__contains__(receiver_id):
                for key3 in receiver_transport_dict[receiver_id]:      # key3 承运商
                    cost_all[key1].update({key3: {}})
                    if receiver_transport_dict[receiver_id][key3].__contains__('1'):
                        dict1 = receiver_transport_dict[receiver_id][key3]['1']
                        cost = cost_calculate(dict1, quantity)
                        cost1 = max(float(dict1['min_price']), cost)
                        cost_all[key1][key3].update({'1': [cost1, dict1['delivery_price'], dict1['receipt_price']]})
                    if receiver_transport_dict[receiver_id][key3].__contains__('2'):
                        dict2 = receiver_transport_dict[receiver_id][key3]['2']
                        cost = cost_calculate(dict2, cube)
                        cost2 = max(float(dict2['min_price']), cost)
                        cost_all[key1][key3].update({'2': [cost2, dict2['delivery_price'], dict2['receipt_price']]})
                    if receiver_transport_dict[receiver_id][key3].__contains__('3'):
                        dict3 = receiver_transport_dict[receiver_id][key3]['3']
                        cost = cost_calculate(dict3, weight)
                        cost3 = max(float(dict3['min_price']), cost)
                        cost_all[key1][key3].update({'3': [cost3, dict3['delivery_price'], dict3['receipt_price']]})
            else:
                cost_all.update({key1: '地址有误'})
        else:
            cost_all.update({key1: '无订单内容'})
    return cost_all


def normalization(cost_all, order_dict):
    result = []
    for key1 in cost_all:
        if cost_all[key1] == '地址有误':
            result.append({'订单号': key1, '收货地': order_dict[key1]['receiver_id'],
                           '仓库ID': 'receiver_id数据错误', '承运商': 'receiver_id数据错误',
                           'Mode': 0, '总成本': 0, '总运费': 0, '送货费': 0, '回单费': 0})
        elif cost_all[key1] == '无订单内容':
            result.append({'订单号': key1, '收货地': order_dict[key1]['receiver_id'],
                           '仓库ID': '订单list内容缺失', '承运商': '订单list内容缺失',
                           'Mode': 0, '总成本': 0, '总运费': 0, '送货费': 0, '回单费': 0})
        else:
            cost = 99999
            for key2 in cost_all[key1]:
                if key2 != 'storage_code':
                    for key3 in cost_all[key1][key2]:
                        if cost >= sum(cost_all[key1][key2][key3]):
                            mode = key3
                            transport = key2
                            cost = sum(cost_all[key1][key2][key3])
                            cost0 = cost_all[key1][transport][mode][0]
                            cost1 = cost_all[key1][transport][mode][1]
                            cost2 = cost_all[key1][transport][mode][2]
            if cost < 99999:
                result.append({'订单号': key1, '收货地': order_dict[key1]['receiver_id'],
                               '仓库ID': cost_all[key1]['storage_code'], '承运商': transport,
                               'Mode': mode, '总成本': cost,
                               '总运费': cost0, '送货费': cost1, '回单费': cost2})
            else:
                result.append({'订单号': key1, '收货地': order_dict[key1]['receiver_id'],
                               '仓库ID': cost_all[key1]['storage_code'], '承运商': '无有效承运商',
                               'Mode': 0, '总成本': 0,
                               '总运费': 0, '送货费': 0, '回单费': 0})
    return result


Cost_all = automatic_loading(Order_dict, Order_list_dict, Receiver_transport_dict, Storage_lng_lat_dict)
Result = normalization(Cost_all, Order_dict)
json_str = json.dumps(Result, indent=4, ensure_ascii=False)
with open('result.json', 'w') as json_file:
    json_file.write(json_str)  # 输出为result

TSP_ac_data_set1 = []
TSP_ac_data_set2 = []
TSP_ac_data_set3 = []
for i in range(len(Result)):
    if Result[i]['仓库ID'] == '000003':
        if Result[i]['Mode'] == '1':
            TSP_ac_data_set1.append((float(Receiver_lng_lat_dict[Result[i]['收货地']][0]),
                                     float(Receiver_lng_lat_dict[Result[i]['收货地']][1]),
                                     Result[i]['收货地']))
        elif Result[i]['Mode'] == '2':
            TSP_ac_data_set2.append((float(Receiver_lng_lat_dict[Result[i]['收货地']][0]),
                                     float(Receiver_lng_lat_dict[Result[i]['收货地']][1]),
                                     Result[i]['收货地']))
        else:
            TSP_ac_data_set3.append((float(Receiver_lng_lat_dict[Result[i]['收货地']][0]),
                                     float(Receiver_lng_lat_dict[Result[i]['收货地']][1]),
                                     Result[i]['收货地']))

json_str = json.dumps(TSP_ac_data_set1, indent=4, ensure_ascii=False)
with open('TSP_ac_data_set1.json', 'w') as json_file:
    json_file.write(json_str)
json_str = json.dumps(TSP_ac_data_set2, indent=4, ensure_ascii=False)
with open('TSP_ac_data_set2.json', 'w') as json_file:
    json_file.write(json_str)
json_str = json.dumps(TSP_ac_data_set3, indent=4, ensure_ascii=False)
with open('TSP_ac_data_set3.json', 'w') as json_file:
    json_file.write(json_str)
