from algorithms.src.core.FE_Pick_Storage.mysql_io import sql_order, sql_order_list
from algorithms.algorithm_io import ImportData
import json


order_data = sql_order("SELECT * FROM logistics_oms.oms_shipper_order "
                       "where confirm_date > '2019-11-26 00:00:00' "
                       "and eid = 'aifuyi';")
order_list_data = sql_order_list("SELECT * FROM logistics_oms.oms_shipper_order_list "
                                 "where create_time > '2019-11-26 00:00:00' "
                                 "and status > 0 and eid = 'aifuyi';")
receiver_dict = ImportData.read(filename='receiver_dict.json')  # 承运商

order_in_SH = []
for order in order_data:
    if '上海' in order_data[order]['parts_core'] and order in order_list_data \
            and ('上海' in receiver_dict[order_data[order]['receiver_id']]['Prov']
                 or '上海' in receiver_dict[order_data[order]['receiver_id']]['Address']):
        order_dict_temp = {'order_id': order}
        order_dict_temp.update({'station_id': order_data[order]['receiver_id']})
        order_details = []
        weight = 0
        volume = 0
        number = 0
        for order_list in order_list_data[order]:
            order_details.append({'cargo_id': order_list_data[order][order_list]['cargo_id'],
                                  'quantity': order_list_data[order][order_list]['quantity'],
                                  'weight': order_list_data[order][order_list]['weight'],
                                  'volume': order_list_data[order][order_list]['cube']})
            weight += order_list_data[order][order_list]['weight'] * \
                order_list_data[order][order_list]['quantity']
            volume += order_list_data[order][order_list]['cube'] * \
                order_list_data[order][order_list]['quantity']
            number += order_list_data[order][order_list]['quantity']
        order_dict_temp.update({'weight': weight, 'volume': volume, 'number': number,
                                'address': 'xxx', 'lng': 121, 'lat': 31,
                                'order_details': order_details})
        order_in_SH.append(order_dict_temp)
print(len(order_in_SH))

json_str = json.dumps(order_in_SH, indent=4, ensure_ascii=False)
with open('order_in_SH.json', 'w') as json_file:
    json_file.write(json_str)
