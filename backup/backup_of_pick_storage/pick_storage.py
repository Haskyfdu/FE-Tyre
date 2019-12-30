import math


def distance_sort(receiver_lng_lat, storage_lng_lat_dict):              # 仓库点距离排序
    storage_list_by_distance = []
    distance_list = []
    distance_dict = {}
    for key in storage_lng_lat_dict:
        if receiver_lng_lat[0] == 0:
            print('bug')
        distance = calculate_distance(receiver_lng_lat[0], storage_lng_lat_dict[key])
        distance_dict.update({key: distance})
        distance_list.append(distance)
    distance_list.sort()
    for i in range(len(distance_list)):
        for (k, v) in distance_dict.items():
            if abs(v - distance_list[i]) < 0.1 and k != receiver_lng_lat[1]:
                storage_list_by_distance.append(k)
                break
    if receiver_lng_lat[1] in ['000003', '000008', '000010', '000011', '000014', '000022']:
        storage_list_by_distance2 = [receiver_lng_lat[1]] + storage_list_by_distance
    else:
        receiver_lng_lat[1] = '无默认仓库'
        storage_list_by_distance2 = [receiver_lng_lat[1]] + storage_list_by_distance
    return storage_list_by_distance2


def calculate_distance(lng_lat_1, lng_lat_2):               # 计算距离
    earth_radius = 6378137.0
    pi = 3.1415926
    if not (isinstance(lng_lat_1, list) and isinstance(lng_lat_2, list)):
        print('bug')
    distance = math.acos(math.sin(lng_lat_1[1] * pi / 180) * math.sin(lng_lat_2[1] * pi / 180) +
                         math.cos(lng_lat_1[1] * pi / 180) * math.cos(lng_lat_2[1] * pi / 180) *
                         math.cos((lng_lat_1[0] - lng_lat_2[0]) * pi / 180)) * earth_radius
    return distance


def pick_storage(order, receiver_lng_lat, storage_lng_lat_dict, inventory_dict):        # 选取仓库
    cargo_id = order['cargo_id']
    quantity = order['quantity']
    storage_code_use = []
    inventory_num = 0
    storage_list_by_distance = distance_sort(receiver_lng_lat, storage_lng_lat_dict)
    if cargo_id in inventory_dict:
        for i in range(len(storage_list_by_distance)):
            storage_code = storage_list_by_distance[i]
            if storage_code in inventory_dict[cargo_id]:
                inventory_num += max(inventory_dict[cargo_id][storage_code], 0)
        if inventory_num < quantity:
            storage_code_use.append('所有仓库库存总和不足')
        else:
            storage_code = storage_list_by_distance[0]
            if storage_code == '无默认仓库':
                storage_code_use.append('无默认仓库')
            else:
                if storage_code in inventory_dict[cargo_id]:
                    if quantity <= inventory_dict[cargo_id][storage_code]:
                        storage_code_use.append('默认仓库库存足够')
                    elif inventory_dict[cargo_id][storage_code] == 0:
                        storage_code_use.append('默认仓库断货')
                    else:
                        storage_code_use.append('默认仓库库存不足')
                else:
                    storage_code_use.append('默认仓库查无此货')
        if inventory_num >= quantity:
            i = 0
            while quantity > 0:
                storage_code = storage_list_by_distance[i]
                if storage_code in inventory_dict[cargo_id]:
                    if quantity <= inventory_dict[cargo_id][storage_code]:
                        storage_code_use.append([storage_code, quantity])
                        quantity = 0
                    else:
                        if inventory_dict[cargo_id][storage_code] > 0:
                            storage_code_use.append([storage_code, inventory_dict[cargo_id][storage_code]])
                            quantity = quantity - inventory_dict[cargo_id][storage_code]
                            inventory_dict[cargo_id][storage_code] = 0
                i += 1
    else:
        storage_code_use.append('查无此货')
    return [storage_code_use, inventory_dict]


if __name__ == '__main__':

    order_sample = {"cargo_id": "ZTS-215-606-GV-CT1",
                    "cargo_desc": "进马5",
                    "cargo_spec": "215/60R16 95V PC2 CS #",
                    "cube": 0.07,
                    "weight": 12.12,
                    "quantity": 40.0,
                    "remark": "intra_sn:3568350000;label:;datetime:",
                    "status": 1,
                    "flag": 13}
    receiver_lng_lat_sample = [[119.65779, 29.120558], "无默认仓库"]
    storage_lng_lat_dict_sample = {"000003": [121.30409, 31.352371],
                                   "000008": [113.35696, 23.274183],
                                   "000010": [116.84531, 39.808054],
                                   "000011": [104.24989, 30.745081],
                                   "000014": [114.08502, 30.631004],
                                   "000022": [120.19554, 30.394239]}
    inventory_dict_sample = {"ZTS-215-606-GV-CT1": {"000011": 10,
                                                    "000003": -56,
                                                    "000008": 4,
                                                    "000010": 2,
                                                    "000014": 28}}
    storage_code_use_sample, inventory_dict_sample = pick_storage(order_sample,
                                                                  receiver_lng_lat_sample,
                                                                  storage_lng_lat_dict_sample,
                                                                  inventory_dict_sample)
