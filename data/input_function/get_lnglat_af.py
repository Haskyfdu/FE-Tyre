import requests
import json


base = 'http://restapi.amap.com/v3/geocode/geo'
address_data = [{'code': '000002', 'name': '上海嘉定', 'address': '上海市嘉定区博学路288号', 'lng_lat': [0, 0]},
                {'code': '000001', 'name': '上海浦东', 'address': '上海市罗山路5007号', 'lng_lat': [0, 0]}]

'''
for i in range(0, len(address_data)):
    address = address_data[i]['address']
    parameters = {'address': address, 'key': 'cc232bb87d144d2f1ebfe08b8481aadb'}
    response = requests.get(base, parameters)
    answer = response.json()
    address_data[i]['lng_lat'][0] = float(answer['geocodes'][0]['location'][0:9])
    address_data[i]['lng_lat'][1] = float(answer['geocodes'][0]['location'][11:20])

json_str = json.dumps(address_data, indent=4, ensure_ascii=False)
with open('storage_address_data2.json', 'w') as json_file:
    json_file.write(json_str)
storage_lng_lat_dict = {}
for i in range(len(address_data)):
    storage_lng_lat_dict.update({address_data[i]['code']: address_data[i]['lng_lat']})
json_str = json.dumps(storage_lng_lat_dict, indent=4, ensure_ascii=False)
with open('storage_lng_lat_dict2.json', 'w') as json_file:
    json_file.write(json_str)

'''

with open("receiver_dict2.json", "r", encoding="utf-8") as receiver_data:
    Receiver_dict = json.load(receiver_data)  # 订单地址

receiver_lng_lat_dict = {}
num = 0
wrong_num = 0
for key in Receiver_dict:
    if num > 8400:
        keyword = 'a22303754d8aa5c4a235a887f1034c34'
    elif num > 5600:
        keyword = '1d9dd3612ab3b3d3d62b819c51f1a76c'
    elif num > 2800:
        keyword = '556863faa89e2232688586bde4c21557'
    else:
        keyword = 'afb8e16263f769ab82cd0edd4274380c'
    address = Receiver_dict[key]['Address']
    parameters = {'address': address, 'key': keyword}
    response = requests.get(base, parameters)
    answer = response.json()
    if answer['status'] == '1' and len(answer['geocodes']) > 0:
        receiver_lng_lat_dict.update({key: [[float(answer['geocodes'][0]['location'][0:9]),
                                            float(answer['geocodes'][0]['location'][11:20])],
                                            Receiver_dict[key]["storage_id"]]})
    else:
        receiver_lng_lat_dict.update({key: [[0, 0], '无']})
        wrong_num = wrong_num + 1
    num = num + 1
print('num =', num)
print('wrong_num =', wrong_num)

json_str = json.dumps(receiver_lng_lat_dict, indent=4, ensure_ascii=False)
with open('receiver_lng_lat_dict2.json', 'w') as json_file:
    json_file.write(json_str)
