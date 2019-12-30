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
            volume = order_detail_info['quantity'] * order_detail_info['volume']
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
    for receiver_id in loading_list:
        for order in loading_list[receiver_id]:
            cargo_id = order['cargo_id']
            min_fee = -1
            plan = {}
            for transport in receiver_dict[receiver_id]['pick']:
                storage_id = transport['storage']
                if inventory_dict[cargo_id][storage_id]['quantity'] >= order['quantity']:
                    fee = calculate_fee_step1(quantity=order['quantity'],
                                              volume=order['volume'],
                                              weight=order['weight'],
                                              pricing_id=transport['pricing_id'],
                                              rule_id=transport['rule_id'])
                    if fee < min_fee or min_fee < 0:
                        min_fee = fee
                        plan = transport
            order.update({'transport': plan['pricing_id'],
                          'storage': plan['storage_id'],
                          'fee_all': min_fee})
    loading_list = better(loading_list)  # todo
    return loading_list


def calculate_fee_step1(quantity, volume, weight, pricing_id, rule_id):
    # todo
    return 0


def better(loading_list):
    # todo
    return loading_list
