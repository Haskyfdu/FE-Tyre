#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

import pymysql
import pandas as pd


def sql_read(sqll):
    conn = pymysql.connect(host='106.75.233.19', port=3307, user='aifuyi', passwd='1qaz2wsx', db='mw_transport')
    data_return = pd.read_sql(sql=sqll, con=conn)
    return data_return


def get_data():
    data_main_origin = sql_read("SELECT * FROM mw_transport.mwt_contract_pricing_rule where pricing_id != 058 and pricing_id != 098;")
    # data_main_origin = sql_read("SELECT * FROM mw_transport.mwt_contract_pricing_rule;")
    data_info_origin = sql_read("SELECT * FROM mw_transport.mwt_contract_pricing;")
    data_name_origin = sql_read("SELECT * FROM mw_transport.mwt_contract;")
    data_scope_origin = sql_read("SELECT * FROM mw_transport.mwt_contract_rule_scope;")
    return data_main_origin, data_info_origin, data_name_origin, data_scope_origin


def data_select(data_main_origin, data_info_origin, data_name_origin, data_scope_origin):
    data_main_origin_sub = data_main_origin[['id', 'pricing_id', 'code', 'is_round', 'abbr', 'desc',
                                             'type_id', 'algo', 'cond', 'val', 'fee',
                                             'fee_least', 'fee_handling', 'fee_delivery', 'fee_receipt']]
    data_info_origin_sub = data_info_origin[['contract_id', 'code', 'prov', 'city', 'dist', 'address']]
    data_name_origin_sub = data_name_origin[['code', 'abbr']]
    # data_scope_oringin_sub = data_scope_origin[['pricing_id', 'rule_id', 'prov', 'city', 'dist']]
    data_main = data_main_origin_sub.rename(columns={'pricing_id': 'pricing_id_1', 'code': 'pricing_id_2',
                                                     'is_round': 'pricing_id_3'})
    data_info = data_info_origin_sub.rename(columns={'contract_id': 'logistics', 'code': 'pricing_id_1',
                                                     'prov': 'prov_from', 'city': 'city_from', 'dist': 'dist_from'})
    data_name = data_name_origin_sub.rename(columns={'code': 'logistics', 'abbr': 'logistics_zh'})
    # data_scope = data_scope_oringin_sub.rename(columns={'pricing_id': 'pricing_id_1s', 'rule_id': 'pricing_id_2s',
    #                                                     'prov': 'prov_to', 'city': 'city_to', 'dist': 'dist_to'})
    # data_main['destiny'] = data_main['desc'] + data_main['abbr'] * data_main['desc'].isnull()
    data_main['pricing_id'] = data_main['pricing_id_1'] + data_main['pricing_id_2']
    data_main = data_main.merge(data_info, left_on='pricing_id_1', right_on='pricing_id_1', how='left')
    data_main = data_main.merge(data_name, left_on='logistics', right_on='logistics', how='left')
    # data_main = data_main.merge(data_scope, left_on='pricing_id', right_on='pricing_id', how='left')
    data_main.where(data_main.isnull(), None)
    data_main.where(data_main.isna(), None)

    # mydata = data_main.groupby(['city_from', 'desc', 'pricing_id_1'])
    mydata = data_main.groupby(['pricing_id_1', 'pricing_id_2'])
    data_dict = dict(list(mydata))
    pricing_size = mydata.size().values
    return data_dict, pricing_size


def list2int_diff(list_data):
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
    data_info = {'type': price_type, 'city_from': fee_info[1], 'logistics': fee_info[2], 'logistics_zh': fee_info[3],
                 'city_to': fee_info[4], 'origin_id': fee_info[5], 'cond': fee_info[6], 'val': fee_info[7],
                 'fee': fee_info[8], 'fee_least': fee_info[9], 'fee_handling': fee_info[10],
                 'fee_delivery': fee_info[12]}

    data_info['fee_accumulation'] = data_info['fee']
    data_info['fee_extra_sum'] = \
        max(0, fee_info[9]) + max(0, fee_info[10]) + max(0, fee_info[11]) + max(0, fee_info[12])

    data_key = fee_info[0][0] + fee_info[0][1]
    dict_program[data_key] = data_info

    dict_development.setdefault(price_type, [])
    dict_development[price_type] += [fee_info]
    # dict_development[price_type].append(fee_info)
    return dict_program, dict_development


def data_processing():
    data_main_origin, data_info_origin, data_name_origin, data_scope_origin = get_data()
    data_dict, pricing_size = data_select(data_main_origin, data_info_origin, data_name_origin, data_scope_origin)
    result_development = {}
    result_program = {}

    for i, p in enumerate(data_dict):

        logistics = strs2str_same(data_dict[p]['logistics'].tolist())
        logistics_zh = strs2str_same(data_dict[p]['logistics_zh'].tolist())
        city_from = strs2str_ifok(data_dict[p]['city_from'].tolist())
        # city_to = strs2str(data_dict[p]['city_to'].tolist())
        desc = strs2str_ifok(data_dict[p]['desc'].tolist())
        origin_id = data_dict[p]['id'].tolist()
        pricing_id = strs2str_ifok(data_dict[p]['pricing_id'].tolist())

        size = pricing_size[i]
        type_id_list = data_dict[p]['type_id'].tolist()
        algo_list = data_dict[p]['algo'].tolist()
        cond = data_dict[p]['cond'].tolist()
        fee = data_dict[p]['fee'].tolist()

        type_id = list2int_same(type_id_list)
        algo = list2int_same(algo_list)
        val = list2int_ifok(data_dict[p]['val'].tolist())

        fee_least = list2int_diff(data_dict[p]['fee_least'].tolist())
        fee_handling = list2int_diff(data_dict[p]['fee_handling'].tolist())
        fee_delivery = list2int_diff(data_dict[p]['fee_delivery'].tolist())
        fee_receipt = list2int_diff(data_dict[p]['fee_receipt'].tolist())

        fee_info = [p, city_from, logistics, logistics_zh, desc,  # index info
                    origin_id,  # for development
                    cond, val, fee,  # type feature
                    fee_least, fee_handling, fee_delivery, fee_receipt,  # extra fee
                    ]

        # add a function about effectiveness check
        if type_id == -1 or algo == -1:
            if type_id == 3 and algo_list == [3, 5] and cond == ['<=', '>'] and val[0] == val[1] > 0:
                result_program, result_development = data_save2dict(331, fee_info, result_program, result_development)
            elif city_from == '成都市' and logistics == 'SF' and type_id == 1 and algo_list == [1, 1, 4] \
                    and cond == ['<=', '<', '>='] and val == [1, 30, 30]:
                result_program, result_development = data_save2dict(114, fee_info, result_program, result_development)
            elif city_from == '上海市' and logistics == 'YTO' and type_id == 1 \
                    and algo_list == [1, 1, 9, 9] and cond == ['<=', '>', '<=', '>'] and val == [1, 1, 1, 1]:
                result_program, result_development = data_save2dict(119, fee_info, result_program, result_development)
            else:
                result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
        elif type_id == 1:
            if algo == 1:
                if size > 2:
                    if city_from == '上海市' and logistics == 'KYE' and cond == (['<='] * (size - 1) + ['>']) \
                            and (val[size-2] == val[size-1]) and len(set(val)) == (size - 1):
                        result_program, result_development = data_save2dict(110, fee_info, result_program, result_development)
                    elif cond == (['<='] * size) and len(set(val)) == size:
                        result_program, result_development = data_save2dict(111, fee_info, result_program, result_development)
                    else:
                        result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
                elif size == 2:
                    if city_from == '上海市' and logistics == 'SF' and cond == ['>=', '<='] and val[0] < val[1] and fee[0] == 0:
                        result_program, result_development = data_save2dict(112, fee_info, result_program, result_development)
                    elif cond == ['>=', '<='] and val[0] < val[1] and fee[0] > 0:
                        result_program, result_development = data_save2dict(113, fee_info, result_program, result_development)
                    elif cond == ['<=', '<'] and val[0] < val[1]:
                        result_program, result_development = data_save2dict(115, fee_info, result_program, result_development)
                    elif cond == ['<=', '<='] and val[0] < val[1]:
                        result_program, result_development = data_save2dict(116, fee_info, result_program, result_development)
                    elif cond == ['<=', '>'] and val[0] == val[1]:
                        result_program, result_development = data_save2dict(117, fee_info, result_program, result_development)
                    else:
                        result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
                else:
                    result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
            elif algo == 4:
                if cond == [None]:
                    result_program, result_development = data_save2dict(140, fee_info, result_program, result_development)
                elif cond == ['>=']:
                    result_program, result_development = data_save2dict(141, fee_info, result_program, result_development)
                else:
                    result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
            elif algo == 8:
                if cond == ['<=', '<='] and val[0] < val[1]:
                    result_program, result_development = data_save2dict(180, fee_info, result_program, result_development)
                elif cond == ['<=', '>'] and val[0] == val[1]:
                    result_program, result_development = data_save2dict(181, fee_info, result_program, result_development)
                else:
                    result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
            elif algo == 9:
                if cond == ['<=', '>'] and val == [1, 1]:
                    result_program, result_development = data_save2dict(190, fee_info, result_program, result_development)
                else:
                    result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
            else:
                result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
        elif type_id == 2:
            if algo == 2 and cond == [None]:
                result_program, result_development = data_save2dict(220, fee_info, result_program, result_development)
            elif algo == 2 and cond == ['<=']:
                result_program, result_development = data_save2dict(221, fee_info, result_program, result_development)
            elif algo == 7 and (cond == [None] or cond == ['']):
                result_program, result_development = data_save2dict(270, fee_info, result_program, result_development)
            elif logistics == 'HENAN56' and algo == 7 and size > 1 and cond == [None] * size:
                result_program, result_development = data_save2dict(271, fee_info, result_program, result_development)
            else:
                result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
        elif type_id == 3:
            if algo == 3:
                if size == 1 and cond == [None]:
                    result_program, result_development = data_save2dict(330, fee_info, result_program, result_development)
                elif size == 2 and cond == ['<=', '>'] and val[0] == val[1] == 1:
                    result_program, result_development = data_save2dict(331, fee_info, result_program, result_development)
                elif logistics == 'FX56' and cond == ['<=:qty&>=:qty', '<=:qty'] and val == ['{qty=100,qty=30}', '{qty=100}']:
                    result_program, result_development = data_save2dict(332, fee_info, result_program, result_development)
                else:
                    result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
            elif algo == 5:
                result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
            elif algo == 6:
                if size == 1 and cond == [None]:
                    result_program, result_development = data_save2dict(360, fee_info, result_program, result_development)
                elif size == 2 and cond == ['<>', '=='] and val == ['hankook', 'hankook']:
                    result_program, result_development = data_save2dict(361, fee_info, result_program, result_development)
                else:
                    result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
            else:
                result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
        elif type_id == 4:
            if algo == 7 and logistics == 'YUHUI56' and cond == ['<=:cobe', '>:cobe'] and val == ['{cube=0.5}', '{cube=0.5}']:
                result_program, result_development = data_save2dict(470, fee_info, result_program, result_development)
            else:
                result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
        elif type_id == 7:
            if logistics == 'WL56(SD)' and algo == 7 and cond == ['>:qty&>:price', '<=:qty', '>:qty&<=:price'] \
                    and val == ['{qty=100,price=80}', '{qty=100}', '{qty=100,price=80}']:
                result_program, result_development = data_save2dict(770, fee_info, result_program, result_development)
            else:
                result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
        else:
            result_program, result_development = data_save2dict(999, fee_info, result_program, result_development)
    return result_program, result_development, data_dict

