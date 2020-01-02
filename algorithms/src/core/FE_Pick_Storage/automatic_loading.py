#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

try:
    from algorithms.src.core.FE_Pick_Storage.calculate_pricing import price_calculator
except ImportError:
    from algorithms.lib.core.FE_Pick_Storage.calculate_pricing import price_calculator



# BigNum = 9

def automatic_loading(order_list, inventory_dict, receiver_dict):
    loading_list = {}
    # big_order = []
    # big_order_check = []
    for order_code in order_list:
        receiver_id = order_list[order_code]['receiver_id']
        for order_detail_code in order_list[order_code]['order_detail']:
            order_detail_info = order_list[order_code]['order_detail'][order_detail_code]
            # if order_detail_info['quantity'] > BigNum:
            #     big_order.append({'quantity': order_detail_info['quantity'],
            #                       'receiver_id': receiver_id,
            #                       '体积': cube,
            #                       '重量': weight})
            quantity = order_detail_info['quantity']
            volume = order_detail_info['quantity'] * order_detail_info['cube']
            weight = order_detail_info['quantity'] * order_detail_info['weight']
            cargo_id = order_detail_info['cargo_id']
            if receiver_id in loading_list:
                loading_list[receiver_id].append({'quantity': quantity,
                                                  'volume': volume,
                                                  'weight': weight,
                                                  'cargo_id': cargo_id,
                                                  'order_code': order_code,
                                                  'order_detail_code': order_detail_code})
            else:
                loading_list.update({receiver_id: [{'quantity': quantity,
                                                    'volume': volume,
                                                    'weight': weight,
                                                    'cargo_id': cargo_id,
                                                    'order_code': order_code,
                                                    'order_detail_code': order_detail_code}]})
    c = 0
    for receiver_id in loading_list:
        print(c/len(loading_list))
        c += 1
        for order in loading_list[receiver_id]:
            cargo_id = order['cargo_id']
            min_fee = -1
            plan = {}
            if receiver_id in receiver_dict:
                for transport in receiver_dict[receiver_id]['pick']:
                    storage_id = transport['storage']
                    if cargo_id in inventory_dict:
                        if storage_id in inventory_dict[cargo_id] \
                                and inventory_dict[cargo_id][storage_id] >= order['quantity']:
                            fee = price_calculator(quantity=order['quantity'],
                                                   volume=order['volume'],
                                                   weight=order['weight'],
                                                   pricing_id=transport['pricing_id'],
                                                   rule_id=transport['rule_id'])
                            if fee < min_fee or min_fee < 0:
                                min_fee = fee
                                plan = transport
                    else:
                        plan = {'pricing_id': None,
                                'storage': None,
                                'fee_all': None}
                        order.update({'remark': 'no cargo_id'})
                if plan == {}:
                    order.update({'transport': None,
                                  'remark': 'sold out'})
                else:
                    order.update({'transport': plan['pricing_id'],
                                  'storage': plan['storage'],
                                  'fee_all': min_fee})
                    if plan['storage'] is not None:
                        inventory_dict[cargo_id][plan['storage']] -= order['quantity']
            else:
                order.update({'transport': None,
                              'remark': 'no receiver_id'})
    loading_list = better(loading_list)  # todo
    return loading_list, inventory_dict


def better(loading_list):
    # todo
    return loading_list
