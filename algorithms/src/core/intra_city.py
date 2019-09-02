from algorithms.src.core import pick_storage
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from algorithms.src.core import class_tsp_ga


def intra_city_collect(result, receiver_lng_lat_dict):
    tsp_ac_data_set = []
    tsp_ac_data_set_big = []
    num_in_station = []
    num_in_station_big = []
    cost000 = 0
    cost000_big = 0
    for i in range(len(result)):
        if result[i]['收货站点'] in receiver_lng_lat_dict:
            lng_lat = [receiver_lng_lat_dict[result[i]['收货站点']][0][0],
                       receiver_lng_lat_dict[result[i]['收货站点']][0][1],
                       result[i]['收货站点']]
            if lng_lat[0:2] != [0, 0] and pick_storage.calculate_distance(
                    lng_lat[0:2], [121.471555, 31.231404]) < 20000:
                if result[i]['数量'] < 50:
                    tsp_ac_data_set.append(lng_lat)
                    num_in_station.append({result[i]['收货站点']: result[i]['数量']})
                    cost000 += 4 * result[i]['数量']
                else:
                    tsp_ac_data_set_big.append(lng_lat)
                    num_in_station_big.append({result[i]['收货站点']: result[i]['数量']})
                    cost000_big += 4 * result[i]['数量']

    # print('上海市区20公里范围内配送：')
    # print('原有成本为' + str(cost000 + cost000_big) + ' ,共计' + str(int(round((cost000 + cost000_big)/4))) + '条轮胎,' +
    #       str(len(num_in_station)+len(num_in_station_big)) + '个站点')
    # print('其中有' + str(len(num_in_station_big)) + '为大额订单,共计' + str(int(round(cost000_big/4))) + '条轮胎')
    return [tsp_ac_data_set, cost000, num_in_station, tsp_ac_data_set_big, cost000_big, num_in_station_big]


def k_means(tsp_ac_data_set, k):
    if tsp_ac_data_set:
        tsp_ac_data_set0 = []
        for i in range(len(tsp_ac_data_set)):
            tsp_ac_data_set0.append(tsp_ac_data_set[i][0:2])
        estimator = KMeans(n_clusters=k)  # 构造聚类器
        estimator.fit(tsp_ac_data_set0)  # 聚类
        label_pred = list(estimator.labels_)    # 获取聚类标签
        x0 = []
        x1 = []
        x2 = []
        x3 = []
        for i in range(len(label_pred)):
            if label_pred[i] == 0:
                x0.append(tsp_ac_data_set0[i])
            if label_pred[i] == 1:
                x1.append(tsp_ac_data_set0[i])
            if label_pred[i] == 2:
                x2.append(tsp_ac_data_set0[i])
            if label_pred[i] == 3:
                x3.append(tsp_ac_data_set0[i])
        x0 = np.array(x0)
        x1 = np.array(x1)
        x2 = np.array(x2)
        x3 = np.array(x3)
        # print(len(x0), len(x1), len(x2), len(x3))
        # plt.figure()
        # plt.scatter(x0[:, 0], x0[:, 1], c="red", marker='o', label='label0')
        # if k > 1:
        #     plt.scatter(x1[:, 0], x1[:, 1], c="green", marker='o', label='label1')
        # if k > 2:
        #     plt.scatter(x2[:, 0], x2[:, 1], c="blue", marker='o', label='label2')
        # if k > 3:
        #     plt.scatter(x3[:, 0], x3[:, 1], c="red", marker='*', label='label3')
        # plt.scatter([121.304099], [31.352371], c="blue", marker='s', label='label4')
        # plt.scatter([121.58845], [31.164603], c="blue", marker='s', label='label5')
        # plt.legend(loc=2)
        # plt.show()
        y0 = []
        y1 = []
        y2 = []
        y3 = []
        for i in range(len(label_pred)):
            if label_pred[i] == 0:
                y0.append(tsp_ac_data_set[i])
            if label_pred[i] == 1:
                y1.append(tsp_ac_data_set[i])
            if label_pred[i] == 2:
                y2.append(tsp_ac_data_set[i])
            if label_pred[i] == 3:
                y3.append(tsp_ac_data_set[i])
        # print(len(y0), len(y1), len(y2), len(y3))
    else:
        y0 = []
        y1 = []
        y2 = []
        y3 = []
        tsp_ac_data_set0 = []
    return [len(tsp_ac_data_set0), [y0, y1, y2, y3]]


def route(data_set, receiver_lng_lat_dict):
    route_result = []
    for i in range(len(data_set)):
        if data_set[i]:
            route_result.append(class_tsp_ga.tsp_ga_main(data_set[i]))
            lng_lat_start = receiver_lng_lat_dict[route_result[i][0][0]][0]
            route_result[i][1] += pick_storage.calculate_distance(lng_lat_start, [121.471555, 31.231404])
    return route_result


def intra_city_service(result, receiver_lng_lat_dict, k):
    tsp_ac_data_set, cost000, num_in_station, tsp_ac_data_set_big, cost000_big, num_in_station_big \
        = intra_city_collect(result, receiver_lng_lat_dict)
    num_station_today, data_set = k_means(tsp_ac_data_set, k)
    num_station_today_big, data_set_big = k_means(tsp_ac_data_set_big, k)
    # print('路线规划中...')
    route_result = route(data_set, receiver_lng_lat_dict)
    route_result_big = route(data_set_big, receiver_lng_lat_dict)
    return [route_result, cost000, num_station_today, num_in_station,
            route_result_big, cost000_big, num_station_today_big, num_in_station_big]
