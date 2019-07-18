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
    address_data[i]['lng_lat'][0] = float(answer['geocodes'][0]['location'][0:9])
    address_data[i]['lng_lat'][1] = float(answer['geocodes'][0]['location'][11:20])

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
num = 0
wrong_num = 0
for key in Receiver_dict:
    if num > 8400:
        keyword = 'a14a76f07fbdd572b25d8529af4f546a'
    elif num > 5600:
        keyword = 'cc232bb87d144d2f1ebfe08b8481aadb'
    elif num > 2800:
        keyword = '1e2b21cefffbad0d66c41152db9b453b'
    else:
        keyword = 'b2e23a19857e5195e959b894ec032001'
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
with open('receiver_lng_lat_dict.json', 'w') as json_file:
    json_file.write(json_str)
