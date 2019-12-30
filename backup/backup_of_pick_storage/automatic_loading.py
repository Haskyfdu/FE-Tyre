from backup.backup_of_pick_storage import pick_storage


def cost_calculate(dict_use, num):
    if '起步' not in dict_use and '计价' in dict_use:
        dict_use['起步'] = dict_use['计价']
    elif '计价' not in dict_use and '起步' in dict_use:
        dict_use['计价'] = dict_use['起步']
    elif '计价' not in dict_use and '起步' not in dict_use:
        print('承运商价格错误,无起步价与计价')
    if dict_use['计价'] * dict_use['起步'] == 0:
        # print('承运商价格错误,起步价与计价均为0')
        cost_result = 999999999
    else:
        cost_result = dict_use['val'] * dict_use['起步'] + int(num > float(dict_use['val'])) \
                  * (num - dict_use['val']) * dict_use['计价']
    return cost_result


def automatic_loading(order_dict, order_list_dict,
                      storage_lng_lat_dict, receiver_lng_lat_dict, inventory_dict):
    loading_list = {}
    big_order = []
    big_order_check = []
    for order_code in order_dict:   # order_code 订单号
        receiver_id = order_dict[order_code]['receiver_id']
        if order_dict[order_code]['receiver_id'] in receiver_lng_lat_dict:     # 获取站点经纬度
            receiver_lng_lat = receiver_lng_lat_dict[order_dict[order_code]['receiver_id']]
            if receiver_lng_lat == [0, 0]:
                receiver_lng_lat = ([0, 0], '无')
        else:
            receiver_lng_lat = ([0, 0], '无')
        if receiver_id in loading_list:  # 将这个订单录入这个站点之下
            loading_list[receiver_id].update({order_code: {}})
        else:
            loading_list.update({receiver_id: {order_code: {}}})
        if order_code in order_list_dict:
            for order_list_code in order_list_dict[order_code]:    # order_list_code 子订单序列
                cube = max(0.03, order_list_dict[order_code][order_list_code]['cube'])
                weight = max(4.0, order_list_dict[order_code][order_list_code]['weight'])
                quantity = order_list_dict[order_code][order_list_code]['quantity']
                if receiver_lng_lat == ([0, 0], '无'):
                    storage_code = ['收货地址有误或缺失经纬度']
                    loading_list[receiver_id][order_code].update(
                        {order_list_code: {'storage_code': storage_code,
                                           '体积': cube,
                                           '重量': weight,
                                           '条数': quantity,
                                           '订单': order_list_dict[order_code][order_list_code]}})
                elif quantity > 9:
                    big_order.append({'条数': quantity,
                                      '订单': order_list_dict[order_code][order_list_code],
                                      '站点经纬度': receiver_lng_lat,
                                      '订单号': order_code,
                                      '子订单号': order_list_code,
                                      '站点': receiver_id,
                                      '体积': cube,
                                      '重量': weight})
                else:
                    [storage_code, inventory_dict] = pick_storage.pick_storage(
                        order_list_dict[order_code][order_list_code],
                        receiver_lng_lat, storage_lng_lat_dict, inventory_dict)
                    loading_list[receiver_id][order_code].update(
                        {order_list_code: {'storage_code': storage_code,
                                           '体积': cube,
                                           '重量': weight,
                                           '条数': quantity,
                                           '订单': order_list_dict[order_code][order_list_code]}})
                # 录入选取的仓库 以及 订单货物的体积重量数量
        else:
            loading_list[receiver_id].update({order_code: '无订单内容'})
    # big order 排序, 最后依次挑选仓库
    big_order.sort(key=lambda x: (x['条数']))
    for i in range(len(big_order)):
        [storage_code, inventory_dict] = pick_storage.pick_storage(
            big_order[i]['订单'], big_order[i]['站点经纬度'], storage_lng_lat_dict, inventory_dict)
        loading_list[big_order[i]['站点']][big_order[i]['订单号']].update(
            {big_order[i]['子订单号']: {'storage_code': storage_code,
                                    '体积': big_order[i]['体积'],
                                    '重量': big_order[i]['重量'],
                                    '条数': big_order[i]['条数'],
                                    '订单': big_order[i]['订单']}})
        if 'cargo_id' not in big_order[i]['订单']:
            raise TypeError('订单详情缺少key： cargo_id')
        elif big_order[i]['订单']['cargo_id'] in inventory_dict:
            stock_left = inventory_dict[big_order[i]['订单']['cargo_id']]
        else:
            stock_left = 0
        big_order_check.append({'订单号': big_order[i]['订单号'],
                                '子订单号': big_order[i]['子订单号'],
                                '站点': big_order[i]['站点'],
                                '仓库': storage_code,
                                '数量': big_order[i]['条数'],
                                '货号': big_order[i]['订单']['cargo_id'],
                                '剩余库存': stock_left})
    return [loading_list, inventory_dict, big_order_check]


def automatic_transport_plan(loading_list, receiver_transport_dict):
    loading_result = []
    error_list = []
    success_list = []
    for receiver_id in loading_list:  # 对每个站点的订单进行拼单
        cube_sum = {'000003': 0, '000008': 0, '000010': 0, '000011': 0,
                    '000014': 0, '000022': 0, '000001': 0, '000002': 0}
        weight_sum = {'000003': 0, '000008': 0, '000010': 0, '000011': 0,
                      '000014': 0, '000022': 0, '000001': 0, '000002': 0}
        quantity_sum = {'000003': 0, '000008': 0, '000010': 0, '000011': 0,
                        '000014': 0, '000022': 0, '000001': 0, '000002': 0}
        order_use = {'000003': [], '000008': [], '000010': [], '000011': [],
                     '000014': [], '000022': [], '000001': [], '000002': []}
        for order_code in loading_list[receiver_id]:
            if loading_list[receiver_id][order_code] == '无订单内容':
                # print(order_code+'无订单内容')
                error_list.append(order_code+'无订单内容')
            else:
                for order_list_code in loading_list[receiver_id][order_code]:
                    info = loading_list[receiver_id][order_code][order_list_code]['storage_code'][0]
                    order_info = loading_list[receiver_id][order_code][order_list_code]['订单']
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
                        success_list.append(order_code + '-' + order_list_code +
                                            '默认仓库库存不足,将从默认仓库及最近的有库存的 ' +
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
                            storage_code = storage_info[0]
                            cube_sum[storage_code] += loading_list[receiver_id][order_code][order_list_code]['体积'] \
                                * storage_info[1]
                            weight_sum[storage_code] += loading_list[receiver_id][order_code][order_list_code]['重量'] \
                                * storage_info[1]
                            quantity_sum[storage_code] += storage_info[1]
                            order_use[storage_code].append({'订单': order_code,
                                                            '子订单': order_list_code,
                                                            '出货量/订货量': str(storage_info[1]) + '/'
                                                            + str(storage_info_num_all),
                                                            '订单详情': order_info})

        for storage_code in cube_sum:
            if quantity_sum[storage_code] > 0:
                cost = 999999
                transport_use = '无'
                mode_use = '0'
                cost0_use = 999999
                cost1_use = 0
                cost2_use = 0
                mode_dict = {'1': quantity_sum[storage_code],
                             '2': cube_sum[storage_code],
                             '3': weight_sum[storage_code]}
                if receiver_id in receiver_transport_dict:
                    for transport in receiver_transport_dict[receiver_id]:
                        for mode in mode_dict:
                            if mode in receiver_transport_dict[receiver_id][transport]:
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
                                           '发货仓库': storage_code,
                                           '承运商': transport_use,
                                           '模式': mode_use,
                                           '总成本': cost,
                                           '运费': cost0_use,
                                           '送货费': cost1_use,
                                           '回单费': cost2_use,
                                           '数量': quantity_sum[storage_code],
                                           '订单': order_use[storage_code]})
                else:
                    # print(order_code + '无有效承运商')
                    error_list.append(order_code + '-' + receiver_id + '无有效承运商, 将按照默认4元/条价格生成自运订单')
                    loading_result.append({'收货站点': receiver_id,
                                           '发货仓库': storage_code,
                                           '承运商': '自运',
                                           '模式': '自运： 4元/条',
                                           '总成本': 4*quantity_sum[storage_code],
                                           '运费': 4*quantity_sum[storage_code],
                                           '送货费': 0,
                                           '回单费': 0,
                                           '数量': quantity_sum[storage_code],
                                           '订单': order_use[storage_code]})
    loading_result.sort(key=lambda x: (x['发货仓库']))
    return [loading_result, error_list, success_list]
