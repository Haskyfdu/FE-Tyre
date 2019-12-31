from algorithms.algorithm_io import ImportData
import json


order_list = ImportData.read(filename='order_dict.json')
order_detail = ImportData.read(filename='order_list_dict.json')

result = {}
for order in order_list:
    if order in order_detail:
        order_list[order].update({'order_detail': order_detail[order]})
        result.update({order: order_list[order]})

json_str = json.dumps(result, indent=4, ensure_ascii=False)
with open('../input/order_list_2019-12-30.json', 'w') as json_file:
    json_file.write(json_str)
