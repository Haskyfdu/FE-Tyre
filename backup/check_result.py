import json

with open("tms_order_dict.json", "r", encoding="utf-8") as tms_order_data:
    Old_order_dict = json.load(tms_order_data)  # 人工装配
with open("result.json", "r", encoding="utf-8") as result_data:
    Auto_order = json.load(result_data)  # 自动装配
with open("tms_order_list_dict.json", "r", encoding="utf-8") as tms_order_list_data:
    Code_change = json.load(tms_order_list_data)  # Code转order_id
with open("receiver_dict.json", "r", encoding="utf-8") as receiver_data:
    Receiver_dict = json.load(receiver_data)  # 人工装配

j = 0
k = 0
kk = 0
check = []
for i in range(len(Auto_order)):
    auto_result = Auto_order[i]
    if Code_change.__contains__(auto_result['订单号']):
        if Old_order_dict.__contains__(Code_change[auto_result['订单号']]) and \
                (Receiver_dict[auto_result['收货地']]['Prov'][0:2] == '上海'):
            j = j + 1
            if auto_result['承运商'] == Old_order_dict[Code_change[auto_result['订单号']]]['carrier_id']:
                kk = kk + 1
                sc = 1
            else:
                sc = 0
            check.append({'订单号': auto_result['订单号'],
                          '是否一致': sc,
                          '人工': Old_order_dict[Code_change[auto_result['订单号']]]['carrier_id'],
                          '自动': auto_result['承运商'],
                          '人工运费': Old_order_dict[Code_change[auto_result['订单号']]]['freight'],
                          '自动运费': auto_result['总成本'],
                          '人工MODE': Old_order_dict[Code_change[auto_result['订单号']]]['freight_mode'],
                          '自动MODE': auto_result['Mode'],
                          '收货地': auto_result['收货地']})

json_str = json.dumps(check, indent=4, ensure_ascii=False)
with open('result_in_SH.json', 'w') as json_file:
    json_file.write(json_str)  # 输出为result_in_SH
