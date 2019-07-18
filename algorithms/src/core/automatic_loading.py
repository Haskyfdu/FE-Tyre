from algorithms.src.core import pick_storage


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
    for ii in range(len(receiver_id)):
        if receiver_id[ii] == '_':
            j = ii
            break
    return receiver_id[0:j]


def automatic_loading(order_dict, order_list_dict,
                      storage_lng_lat_dict, receiver_lng_lat_dict, inventory_dict):
    loading_list = {}
    for order_code in order_dict:   # order_code 订单号
        receiver_id = check_receiver_id(order_dict[order_code]['receiver_id'])  # 获取receiver_id 同时防止乱码
        if receiver_lng_lat_dict.__contains__(order_dict[order_code]['receiver_id']):  # 获取站点经纬度
            receiver_lng_lat = receiver_lng_lat_dict[order_dict[order_code]['receiver_id']]
            if receiver_lng_lat == [0, 0]:
                receiver_lng_lat = ([0, 0], '无')
        else:
            receiver_lng_lat = ([0, 0], '无')
        if loading_list.__contains__(receiver_id):  # 将这个订单录入这个站点之下
            loading_list[receiver_id].update({order_code: {}})
        else:
            loading_list.update({receiver_id: {order_code: {}}})
        if order_list_dict.__contains__(order_code):
            for order_list_code in order_list_dict[order_code]:    # order_list_code 子订单序列
                cube = max(0.03, order_list_dict[order_code][order_list_code]['cube'])
                weight = max(4.0, order_list_dict[order_code][order_list_code]['weight'])
                quantity = order_list_dict[order_code][order_list_code]['quantity']
                if receiver_lng_lat == ([0, 0], '无'):
                    storage_code = ['收货地址有误或缺失经纬度']
                else:
                    [storage_code, inventory_dict] = pick_storage.pick_storage(
                        order_list_dict[order_code][order_list_code],
                        receiver_lng_lat, storage_lng_lat_dict, inventory_dict)
                loading_list[receiver_id][order_code].update(
                    {order_list_code: {'storage_code': storage_code,
                                       '体积': cube, '重量': weight, '条数': quantity}})
                # 录入选取的仓库 以及 订单货物的体积重量数量
        else:
            loading_list[receiver_id].update({order_code: '无订单内容'})
    return [loading_list, inventory_dict]


def automatic_transport_plan(loading_list, receiver_transport_dict):
    loading_result = []
    error_list = []
    success_list = []
    storage_use_dict = {'000003': 0,
                        '000008': 1,
                        '000010': 2,
                        '000011': 3,
                        '000014': 4,
                        '000022': 5,
                        '000001': 6,
                        '000002': 7,}
    storage0_use_dict = {0: '000003',
                         1: '000008',
                         2: '000010',
                         3: '000011',
                         4: '000014',
                         5: '000022',
                         6: '000001',
                         7: '000002'}
    for receiver_id in loading_list:  # 对每个站点的订单进行拼单
        cube_sum = [0, 0, 0, 0, 0, 0, 0, 0]
        weight_sum = [0, 0, 0, 0, 0, 0, 0, 0]
        quantity_sum = [0, 0, 0, 0, 0, 0, 0, 0]
        order_use = [[], [], [], [], [], [], [], []]
        for order_code in loading_list[receiver_id]:
            if loading_list[receiver_id][order_code] == '无订单内容':
                # print(order_code+'无订单内容')
                error_list.append(order_code+'无订单内容')
            else:
                for order_list_code in loading_list[receiver_id][order_code]:
                    info = loading_list[receiver_id][order_code][order_list_code]['storage_code'][0]
                    storage_code_len = len(loading_list[receiver_id][order_code][order_list_code]['storage_code'])
                    plan = 0
                    if info == '收货地址有误或缺失经纬度':
                        # print(order_code + '收货地址有误或缺失经纬度')
                        error_list.append(order_code + '收货地址有误或缺失经纬度')
                    elif info == '查无此货':
                        # print(order_code + '-' + order_list_code + '查无此货/cargo_id错误')
                        error_list.append(order_code + '-' + order_list_code + '查无此货/cargo_id错误')
                    elif info == '所有仓库库存总和不足':
                        # print(order_code + '-' + order_list_code + '所有仓库库存总和不足')
                        error_list.append(order_code + '-' + order_list_code + '所有仓库库存总和不足')
                    elif info == '无默认仓库':
                        plan = 1
                        if storage_code_len == 2:
                            # print(order_code + '-' + order_list_code + '无默认仓库,将从最近的有库存的仓库发货')
                            success_list.append(order_code + '-' + order_list_code + '无默认仓库,将从最近的有库存的仓库发货')
                        elif storage_code_len > 2:
                            # print(order_code + '-' + order_list_code + '无默认仓库,将从最近的有库存的 ' +
                            #       str(storage_code_len - 1) + ' 个仓库拆单发货')
                            success_list.append(order_code + '-' + order_list_code + '无默认仓库,将从最近的有库存的 ' +
                                                str(storage_code_len - 1) + ' 个仓库拆单发货')
                    elif info == '默认仓库库存足够':
                        plan = 1
                        # print(order_code + '-' + order_list_code + '将从默认仓库发货')
                        success_list.append(order_code + '-' + order_list_code + '将从默认仓库发货')
                    elif info == '默认仓库断货':
                        plan = 1
                        if storage_code_len == 2:
                            # print(order_code + '-' + order_list_code + '默认仓库断货,将从最近的有库存的仓库发货')
                            success_list.append(order_code + '-' + order_list_code + '默认仓库断货,将从最近的有库存的仓库发货')
                        elif storage_code_len > 2:
                            # print(order_code + '-' + order_list_code + '默认仓库断货,将从最近的有库存的 ' +
                            #       str(storage_code_len - 1) + ' 个仓库拆单发货')
                            success_list.append(order_code + '-' + order_list_code + '默认仓库断货,将从最近的有库存的 ' +
                                                str(storage_code_len - 1) + ' 个仓库拆单发货')
                    elif info == '默认仓库查无此货':
                        plan = 1
                        if storage_code_len == 2:
                            # print(order_code + '-' + order_list_code + '默认仓库查无此货,将从最近的有库存的仓库发货')
                            success_list.append(order_code + '-' + order_list_code + '默认仓库断货,将从最近的有库存的仓库发货')
                        elif storage_code_len > 2:
                            # print(order_code + '-' + order_list_code + '默认仓库查无此货,将从最近的有库存的 ' +
                            #       str(storage_code_len - 1) + ' 个仓库拆单发货')
                            success_list.append(order_code + '-' + order_list_code + '默认仓库查无此货,将从最近的有库存的 ' +
                                              str(storage_code_len - 1) + ' 个仓库拆单发货')
                    elif info == '默认仓库库存不足':
                        plan = 1
                        # print(order_code + '-' + order_list_code + '默认仓库库存不足,将从默认仓库及最近的有库存的 ' +
                        #       str(storage_code_len - 2) + ' 个仓库拆单发货')
                        success_list.append(order_code + '-' + order_list_code + '默认仓库库存不足,将从默认仓库及最近的有库存的 ' +
                                            str(storage_code_len - 2) + ' 个仓库拆单发货')
                    else:
                        print('BUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    if plan == 1:
                        storage_info_num_all = 0
                        for i in range(1, storage_code_len):
                            storage_info = loading_list[receiver_id][order_code][order_list_code]['storage_code'][i]
                            storage_info_num_all += storage_info[1]
                        for i in range(1, storage_code_len):
                            storage_info = loading_list[receiver_id][order_code][order_list_code]['storage_code'][i]
                            storage_num = storage_use_dict[storage_info[0]]
                            cube_sum[storage_num] += loading_list[receiver_id][order_code][order_list_code]['体积'] * \
                                                     storage_info[1]
                            weight_sum[storage_num] += loading_list[receiver_id][order_code][order_list_code]['重量'] * \
                                                     storage_info[1]
                            quantity_sum[storage_num] += storage_info[1]
                            order_use[storage_num].append([order_code, order_list_code,
                                                           str(storage_info[1]) + '/' + str(storage_info_num_all)])

        for storage_num in range(8):
            if quantity_sum[storage_num] > 0:
                cost = 999999
                transport_use = '无'
                mode_use = '0'
                cost0_use = 999999
                cost1_use = 0
                cost2_use = 0
                mode_dict = {'1': quantity_sum[storage_num],
                             '2': cube_sum[storage_num],
                             '3': weight_sum[storage_num]}
                if receiver_transport_dict.__contains__(receiver_id):
                    for transport in receiver_transport_dict[receiver_id]:
                        for mode in mode_dict:
                            if receiver_transport_dict[receiver_id][transport].__contains__(mode):
                                price_dict = receiver_transport_dict[receiver_id][transport][mode]
                                cost0 = max(float(price_dict['min_price']), cost_calculate(price_dict, mode_dict[mode]))
                                cost1 = price_dict['delivery_price']
                                cost2 = price_dict['receipt_price']
                                if (cost0+cost1+cost2) < cost:
                                    cost = cost0+cost1+cost2
                                    cost0_use = cost0
                                    cost1_use = cost1
                                    cost2_use = cost2
                                    mode_use = mode
                                    transport_use = transport
                    loading_result.append({'收货站点': receiver_id,
                                           '发货仓库': storage0_use_dict[storage_num],
                                           '承运商': transport_use,
                                           '模式': mode_use,
                                           '总成本': cost,
                                           '运费': cost0_use,
                                           '送货费': cost1_use,
                                           '回单费': cost2_use,
                                           '数量': quantity_sum[storage_num],
                                           '订单': order_use[storage_num]})
                else:
                    # print(order_code + '无有效承运商')
                    error_list.append(order_code + '-' + receiver_id + '无有效承运商, 将按照默认4元/条价格生成自运订单')
                    loading_result.append({'收货站点': receiver_id,
                                           '发货仓库': storage0_use_dict[storage_num],
                                           '承运商': '自运',
                                           '模式': '自运： 4元/条',
                                           '总成本': 4*quantity_sum[storage_num],
                                           '运费': 4*quantity_sum[storage_num],
                                           '送货费': 0,
                                           '回单费': 0,
                                           '数量': quantity_sum[storage_num],
                                           '订单': order_use[storage_num]})
    return [loading_result, error_list, success_list]


