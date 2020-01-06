import pymysql
import pandas as pd


def sql_read(sql_command):
    conn = pymysql.connect(host='106.75.233.19', port=3307, user='aifuyi', passwd='1qaz2wsx', db='mw_transport')
    data_return = pd.read_sql(sql=sql_command, con=conn)
    return data_return


def get_data():
    # data_main_origin =
    # sql_read("SELECT * FROM mw_transport.mwt_contract_pricing_rule where pricing_id != 058 and pricing_id != 098;")
    data_main_origin = sql_read("SELECT * FROM mw_transport.mwt_contract_pricing_rule;")
    data_info_origin = sql_read("SELECT * FROM mw_transport.mwt_contract_pricing;")
    data_name_origin = sql_read("SELECT * FROM mw_transport.mwt_contract;")
    data_scope_origin = sql_read("SELECT * FROM mw_transport.mwt_contract_rule_scope;")
    return data_main_origin, data_info_origin, data_name_origin, data_scope_origin


def data_select(data_main_origin, data_info_origin, data_name_origin):
    data_main_origin_sub = data_main_origin[['id', 'pricing_id', 'code', 'is_round', 'abbr', 'desc',
                                             'type_id', 'algo', 'cond', 'val', 'fee',
                                             'fee_least', 'fee_handling', 'fee_delivery', 'fee_receipt']]
    data_info_origin_sub = data_info_origin[['contract_id', 'code', 'prov', 'city', 'dist', 'address']]
    data_name_origin_sub = data_name_origin[['code', 'abbr']]
    data_main = data_main_origin_sub.rename(columns={'pricing_id': 'pricing_id_1', 'code': 'pricing_id_2',
                                                     'is_round': 'pricing_id_3'})
    data_info = data_info_origin_sub.rename(columns={'contract_id': 'logistics', 'code': 'pricing_id_1',
                                                     'prov': 'prov_from', 'city': 'city_from', 'dist': 'dist_from'})
    data_name = data_name_origin_sub.rename(columns={'code': 'logistics', 'abbr': 'logistics_zh'})
    data_main = data_main.merge(data_info, left_on='pricing_id_1', right_on='pricing_id_1', how='left')
    data_main = data_main.merge(data_name, left_on='logistics', right_on='logistics', how='left')

    data_main.where(data_main.isnull(), None)
    data_main.where(data_main.isna(), None)

    mydata = data_main.groupby(['pricing_id_1', 'pricing_id_2'])
    data_dict = dict(list(mydata))
    pricing_size = mydata.size().values
    return data_dict, pricing_size


def list2int_first(list_data):
    if list_data == [list_data[0]] + [0] * (len(list_data) - 1):
        return list_data[0]
    else:
        return -1


def list2int_same(list_data):
    if len(set(list_data)) == 1:
        return list_data[0]
    else:
        return -1


def list2int_ifok(list_data):
    list_return = list_data.copy()
    for i, p in enumerate(list_data):
        if p.isdigit():
            list_return[i] = int(p)
    return list_return


def strs2str_ifok(list_string):
    if list_string == [list_string[0]] * len(list_string):
        return list_string[0]
    else:
        return list_string


def strs2str_same(list_string):
    if list_string == [list_string[0]] * len(list_string):
        return list_string[0]
    else:
        return -1


def data_save2dict(price_type, fee_info, dict_program, dict_development):
    fee_info['type'] = price_type

    data_key = str(fee_info['key'][0]) + str(fee_info['key'][1])
    dict_program[data_key] = fee_info

    dict_development.setdefault(price_type, [])
    dict_development[price_type] += [fee_info]

    return dict_program, dict_development


def data_processing():
    data_main_origin, data_info_origin, data_name_origin, data_scope_origin = get_data()
    data_dict, pricing_size = data_select(data_main_origin, data_info_origin, data_name_origin)
    dict_development = {}
    dict_program = {}

    for i, p in enumerate(data_dict):

        size = pricing_size[i]
        fee_info = {
            'key': p,
            'logistics': strs2str_same(data_dict[p]['logistics'].tolist()),
            'logistics_zh': strs2str_same(data_dict[p]['logistics_zh'].tolist()),
            'city_from': strs2str_ifok(data_dict[p]['city_from'].tolist()),
            'city_to': strs2str_ifok(data_dict[p]['desc'].tolist()),
            'origin_id': data_dict[p]['id'].tolist(),
            'type_id_list': data_dict[p]['type_id'].tolist(),
            'algo_list': data_dict[p]['algo'].tolist(),
            'cond': data_dict[p]['cond'].tolist(),
            'fee': data_dict[p]['fee'].tolist(),
            'val': list2int_ifok(data_dict[p]['val'].tolist()),
            'fee_least': list2int_first(data_dict[p]['fee_least'].tolist()),
            'fee_handling': list2int_first(data_dict[p]['fee_handling'].tolist()),
            'fee_delivery': list2int_first(data_dict[p]['fee_delivery'].tolist()),
            'fee_receipt': list2int_first(data_dict[p]['fee_receipt'].tolist())
        }

        fee_info['type_id'] = list2int_same(fee_info['type_id_list'])
        fee_info['algo'] = list2int_same(fee_info['algo_list'])
        fee_info['fee_accumulation'] = fee_info['fee'].copy()
        if fee_info['fee_handling'] != -1 and fee_info['fee_delivery'] != -1 and fee_info['fee_receipt'] != -1:
            fee_info['fee_extra_sum'] = fee_info['fee_handling'] + fee_info['fee_delivery'] + fee_info['fee_receipt']
        else:
            fee_info['fee_extra_sum'] = -1

        # add a function about effectiveness check
        if fee_info['type_id'] == -1 or fee_info['algo'] == -1:
            if fee_info['type_id'] == 3 \
                    and fee_info['algo_list'] == [3, 5] \
                    and fee_info['cond'] == ['<=', '>'] \
                    and fee_info['val'][0] == fee_info['val'][1] > 0:
                dict_program, dict_development = data_save2dict(331, fee_info, dict_program, dict_development)
            elif fee_info['city_from'] == '成都市' \
                    and fee_info['logistics'] == 'SF' \
                    and fee_info['type_id'] == 1 \
                    and fee_info['algo_list'] == [1, 1, 4] \
                    and fee_info['cond'] == ['<=', '<', '>='] \
                    and fee_info['val'] == [1, 30, 30]:
                fee_info['fee_accumulation'] = \
                    [fee_info['fee'][0] -
                     fee_info['val'][0] * fee_info['fee'][1],
                     fee_info['fee_accumulation'][0] +
                     fee_info['val'][1] * fee_info['fee'][1] -
                     fee_info['val'][1] * fee_info['fee'][2]]
                dict_program, dict_development = data_save2dict(114, fee_info, dict_program, dict_development)
            elif fee_info['city_from'] == '上海市' \
                    and fee_info['logistics'] == 'YTO' \
                    and fee_info['type_id'] == 1 \
                    and fee_info['algo_list'] == [1, 1, 9, 9] \
                    and fee_info['cond'] == ['<=', '>', '<=', '>'] \
                    and fee_info['val'] == [1, 1, 1, 1]:
                dict_program, dict_development = data_save2dict(119, fee_info, dict_program, dict_development)
            else:
                dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
        elif fee_info['type_id'] == 1:
            if fee_info['algo'] == 1:
                if size > 2:
                    if fee_info['city_from'] == '上海市' \
                            and fee_info['logistics'] == 'KYE' \
                            and fee_info['cond'] == (['<='] * (size - 1) + ['>']) \
                            and (fee_info['val'][size - 2] == fee_info['val'][size - 1]) \
                            and len(set(fee_info['val'])) == (size - 1):
                        fee_info['fee_accumulation'][0] = \
                            fee_info['fee'][0] - \
                            fee_info['val'][0] * fee_info['fee'][1]
                        for q in range(1, len(fee_info['fee_accumulation']) - 1):
                            fee_info['fee_accumulation'][q] = \
                                fee_info['fee_accumulation'][q-1] + \
                                fee_info['val'][q] * fee_info['fee'][q] - \
                                fee_info['val'][q] * fee_info['fee'][q+1]
                        dict_program, dict_development = data_save2dict(110, fee_info, dict_program, dict_development)
                    elif fee_info['cond'] == (['<='] * size) \
                            and len(set(fee_info['val'])) == size:
                        fee_info['fee_accumulation'][0] = \
                            fee_info['fee'][0] - \
                            fee_info['val'][0] * fee_info['fee'][1]
                        for q in range(1, len(fee_info['fee_accumulation']) - 1):
                            fee_info['fee_accumulation'][q] = \
                                fee_info['fee_accumulation'][q - 1] + \
                                fee_info['val'][q] * fee_info['fee'][q] - \
                                fee_info['val'][q] * fee_info['fee'][q + 1]
                        dict_program, dict_development = data_save2dict(111, fee_info, dict_program, dict_development)
                    else:
                        dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
                elif size == 2:
                    if fee_info['city_from'] == '上海市' \
                            and fee_info['logistics'] == 'SF' \
                            and fee_info['cond'] == ['>=', '<='] \
                            and fee_info['val'][0] < fee_info['val'][1] \
                            and fee_info['fee'][0] == 0:
                        dict_program, dict_development = data_save2dict(112, fee_info, dict_program, dict_development)
                    elif fee_info['cond'] == ['>=', '<='] \
                            and fee_info['val'][0] < fee_info['val'][1] \
                            and fee_info['fee'][0] > 0:
                        dict_program, dict_development = data_save2dict(113, fee_info, dict_program, dict_development)
                    elif fee_info['cond'] == ['<=', '<'] \
                            and fee_info['val'][0] < fee_info['val'][1]:
                        dict_program, dict_development = data_save2dict(115, fee_info, dict_program, dict_development)
                    elif fee_info['cond'] == ['<=', '<='] \
                            and fee_info['val'][0] < fee_info['val'][1]:
                        fee_info['fee_accumulation'][0] = \
                            fee_info['fee'][0] - \
                            fee_info['val'][0] * fee_info['fee'][1]
                        dict_program, dict_development = data_save2dict(116, fee_info, dict_program, dict_development)
                    elif fee_info['cond'] == ['<=', '>'] \
                            and fee_info['val'][0] == fee_info['val'][1]:
                        fee_info['fee_accumulation'][0] = \
                            fee_info['fee'][0] - \
                            fee_info['val'][0] * fee_info['fee'][1]
                        dict_program, dict_development = data_save2dict(117, fee_info, dict_program, dict_development)
                    else:
                        dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
                else:
                    dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
            elif fee_info['algo'] == 4:
                if fee_info['cond'] == [None]:
                    dict_program, dict_development = data_save2dict(140, fee_info, dict_program, dict_development)
                elif fee_info['cond'] == ['>=']:
                    dict_program, dict_development = data_save2dict(141, fee_info, dict_program, dict_development)
                else:
                    dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
            elif fee_info['algo'] == 8:
                if fee_info['cond'] == ['<=', '<='] \
                        and fee_info['val'][0] < fee_info['val'][1]:
                    fee_info['fee_accumulation'][0] = \
                        fee_info['fee'][0] - \
                        fee_info['val'][0] * fee_info['fee'][1]
                    dict_program, dict_development = data_save2dict(180, fee_info, dict_program, dict_development)
                elif fee_info['cond'] == ['<=', '>'] \
                        and fee_info['val'][0] == fee_info['val'][1]:
                    fee_info['fee_accumulation'][0] = \
                        fee_info['fee'][0] - \
                        fee_info['val'][0] * fee_info['fee'][1]
                    dict_program, dict_development = data_save2dict(181, fee_info, dict_program, dict_development)
                else:
                    dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
            elif fee_info['algo'] == 9:
                if fee_info['cond'] == ['<=', '>'] \
                        and fee_info['val'] == [1, 1]:
                    fee_info['fee_accumulation'][0] = \
                        fee_info['fee'][0] - \
                        fee_info['val'][0] * fee_info['fee'][1]
                    dict_program, dict_development = data_save2dict(190, fee_info, dict_program, dict_development)
                else:
                    dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
            else:
                dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
        elif fee_info['type_id'] == 2:
            if fee_info['algo'] == 2 \
                    and fee_info['cond'] == [None]:
                dict_program, dict_development = data_save2dict(220, fee_info, dict_program, dict_development)
            elif fee_info['algo'] == 2 \
                    and fee_info['cond'] == ['<=']:
                dict_program, dict_development = data_save2dict(221, fee_info, dict_program, dict_development)
            elif fee_info['algo'] == 7 \
                    and (fee_info['cond'] == [None]
                         or fee_info['cond'] == ['']):
                dict_program, dict_development = data_save2dict(270, fee_info, dict_program, dict_development)
            elif fee_info['logistics'] == 'HENAN56' \
                    and fee_info['algo'] == 7 \
                    and size > 1 \
                    and fee_info['cond'] == [None] * size:
                dict_program, dict_development = data_save2dict(271, fee_info, dict_program, dict_development)
            else:
                dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
        elif fee_info['type_id'] == 3:
            if fee_info['algo'] == 3:
                if size == 1 \
                        and fee_info['cond'] == [None]:
                    dict_program, dict_development = data_save2dict(330, fee_info, dict_program, dict_development)
                elif size == 2 \
                        and fee_info['cond'] == ['<=', '>'] \
                        and fee_info['val'][0] == fee_info['val'][1] == 1:
                    fee_info['fee_accumulation'][0] = \
                        fee_info['fee'][0] - \
                        fee_info['val'][0] * fee_info['fee'][1]
                    dict_program, dict_development = data_save2dict(331, fee_info, dict_program, dict_development)
                elif fee_info['logistics'] == 'FX56' \
                        and fee_info['cond'] == ['<=:qty&>=:qty', '<=:qty'] \
                        and fee_info['val'] == ['{qty=100,qty=30}', '{qty=100}']:
                    dict_program, dict_development = data_save2dict(332, fee_info, dict_program, dict_development)
                else:
                    dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
            elif fee_info['algo'] == 5:
                dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
            elif fee_info['algo'] == 6:
                if size == 1 and fee_info['cond'] == [None]:
                    dict_program, dict_development = data_save2dict(360, fee_info, dict_program, dict_development)
                elif size == 2 \
                        and fee_info['cond'] == ['<>', '=='] \
                        and fee_info['val'] == ['hankook', 'hankook']:
                    dict_program, dict_development = data_save2dict(361, fee_info, dict_program, dict_development)
                else:
                    dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
            else:
                dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
        elif fee_info['type_id'] == 4:
            if fee_info['algo'] == 7 \
                    and fee_info['logistics'] == 'YUHUI56' \
                    and fee_info['cond'] == ['<=:cobe', '>:cobe'] \
                    and fee_info['val'] == ['{cube=0.5}', '{cube=0.5}']:
                dict_program, dict_development = data_save2dict(470, fee_info, dict_program, dict_development)
            else:
                dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
        elif fee_info['type_id'] == 7:
            if fee_info['logistics'] == 'WL56(SD)' \
                    and fee_info['algo'] == 7 \
                    and fee_info['cond'] == ['>:qty&>:price', '<=:qty', '>:qty&<=:price'] \
                    and fee_info['val'] == ['{qty=100,price=80}', '{qty=100}', '{qty=100,price=80}']:
                dict_program, dict_development = data_save2dict(770, fee_info, dict_program, dict_development)
            else:
                dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
        else:
            dict_program, dict_development = data_save2dict(999, fee_info, dict_program, dict_development)
    return dict_program, dict_development, data_dict
