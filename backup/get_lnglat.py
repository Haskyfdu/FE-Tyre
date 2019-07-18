import requests
import json


base = 'http://restapi.amap.com/v3/geocode/geo'
address_data = [{'code': '000003', 'name': '上海', 'address': '上海市嘉定区博学路288号', 'lng_lat': [0, 0]},
           {'code': '000008', 'name': '广州', 'address': '广东省广州市白云区太和镇上南村龙森仓储', 'lng_lat': [0, 0]},
           {'code': '000010', 'name': '北京', 'address': '北京市通州区西集镇杜柳棵南500米（中都物流有限公司）', 'lng_lat': [0, 0]},
           {'code': '000011', 'name': '成都', 'address': '成都市新都区兴业大道1088号', 'lng_lat': [0, 0]},
           {'code': '000014', 'name': '武汉', 'address': '武汉市东西湖区东吴大道新城十七路17号澳卡科技园内', 'lng_lat': [0, 0]},
           {'code': '000022', 'name': '杭州', 'address': '浙江省杭州市拱墅区石塘工业园区临一街108号5幢3楼', 'lng_lat': [0, 0]}]

for i in range(0, len(address_data)):
    address = address_data[i]['address']
    parameters = {'address': address, 'key': 'cc232bb87d144d2f1ebfe08b8481aadb'}
    response = requests.get(base, parameters)
    answer = response.json()
    address_data[i]['lng_lat'][0] = answer['geocodes'][0]['location'][0:10]
    address_data[i]['lng_lat'][1] = answer['geocodes'][0]['location'][11:21]

json_str = json.dumps(address_data, indent=4, ensure_ascii=False)
with open('storage_address_data.json', 'w') as json_file:
    json_file.write(json_str)

storage_lng_lat_dict = {}
for i in range(len(address_data)):
    storage_lng_lat_dict.update({address_data[i]['code']: address_data[i]['lng_lat']})
json_str = json.dumps(storage_lng_lat_dict, indent=4, ensure_ascii=False)
with open('storage_lng_lat_dict.json', 'w') as json_file:
    json_file.write(json_str)

with open("receiver_dict.json", "r", encoding="utf-8") as receiver_data:
    Receiver_dict = json.load(receiver_data)  # 订单地址

receiver_lng_lat_dict = {}
for key in Receiver_dict:
    address = Receiver_dict[key]['Address']
    parameters = {'address': address, 'key': 'cc232bb87d144d2f1ebfe08b8481aadb'}
    response = requests.get(base, parameters)
    answer = response.json()
    if answer['status'] == '1':
        if len(answer['geocodes']) > 0:
            receiver_lng_lat_dict.update({key: [answer['geocodes'][0]['location'][0:10],
                                                answer['geocodes'][0]['location'][11:21]]})


json_str = json.dumps(receiver_lng_lat_dict, indent=4, ensure_ascii=False)
with open('receiver_lng_lat_dict.json', 'w') as json_file:
    json_file.write(json_str)
