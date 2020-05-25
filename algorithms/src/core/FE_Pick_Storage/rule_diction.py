#!/usr/bin/env python
# -*- coding: utf-8 -*-


import math
# ======================================================================================================
# remember to add the fee_extra_sum


def f110(price_parameter, order_info):
    """
    Y[110] weight count, [<=, <=, ..., <=, >]
    Step charges
    weight = real_weight?
    """
    weight = order_info['weight']
    if weight <= price_parameter['val'][0]:
        fee = price_parameter['fee'][0]
    else:
        i = len([n for n in price_parameter['val'] if n <= weight]) - 1
        fee = weight*price_parameter['fee'][i] + price_parameter['quick_calculation_deductions'][i]
    return fee


def f111(price_parameter, order_info):
    """
    Y[111] weight count, [<=, <=, ..., <=, <=]
    Step charges
    weight = real_weight?  Too heavy?
    """
    weight = order_info['weight']
    if weight <= price_parameter['val'][0]:
        fee = price_parameter['fee'][0]
    elif weight > price_parameter['val'][-1]:
        fee = -1
    else:
        i = len([n for n in price_parameter['val'] if n <= weight]) - 1
        fee = weight*price_parameter['fee'][i] + price_parameter['quick_calculation_deductions'][i]
    return fee


def f112(price_parameter, order_info):
    """
    Y[112] weight count, [>=, <=]
    if val[0] <= weight <= val[1], weight * fee[1]
    weight = real_weight?
    Error: 112, Too heavy or light?
    """
    weight = order_info['weight']
    if price_parameter['val'][0] <= weight <= price_parameter['val'][1]:
        fee = weight * price_parameter['fee'][1]
    else:
        fee = -1
    return fee


def f114(price_parameter, order_info):
    """
    Y[114] weight count, [<=, <, <]
    if weight <= val[0], fee[0]
    if val[0] < weight < val[1], (weight - 1) * fee[1] + fee[0]
    if weight > val[1], (weight - val[1]) * fee[2] + (val[1] - 1) * fee[1] + fee[0]
    weight = math.ceil(real_weight * 2) / 2 if real_weight < 100, count by 0.5
    weight = int(real_weight + 0.5) if real_weight >= 100, rounding
    """
    real_weight = order_info['weight']
    if real_weight < 100:
        weight = math.ceil(real_weight * 2) / 2
    else:
        weight = int(real_weight + 0.5)
    if weight < 1:
        fee = price_parameter['fee'][0]
    elif weight < 30:
        fee = price_parameter['quick_calculation_deductions'][0] + (weight - 1) * price_parameter['fee'][1]
    else:
        fee = price_parameter['quick_calculation_deductions'][1] + (weight - 30) * price_parameter['fee'][2]
    return fee


def f116(price_parameter, order_info):
    """
    Y[116] weight count, 2 cases, 2 bounds, [<=, <=]
    if weight <= val[0], fee[0]
    if val[0] < weight <= val[1], (weight - val[0]) * fee[1] + fee[0]
    weight = real_weight?
    "Error: 116, Too heavy"
    """
    weight = order_info['weight']
    if weight <= price_parameter['val'][0]:
        fee = price_parameter['fee'][0]
    elif weight <= price_parameter['val'][1]:
        fee = price_parameter['quick_calculation_deductions'][0] + \
              (weight-price_parameter['val'][0])*price_parameter['fee'][1]
    else:
        fee = -1
    return fee


def f117(price_parameter, order_info):
    """
    Y[117] weight count, [<=, >]
    if weight <= val[0],fee[0]
    if weight > val[0], (weight - val[0]) * fee[1] + fee[0]
    """
    weight = order_info['weight']
    if weight <= price_parameter['val'][0]:
        fee = price_parameter['fee'][0]
    else:
        fee = price_parameter['quick_calculation_deductions'][0] + \
              (weight-price_parameter['val'][0])*price_parameter['fee'][1]
    return fee


def f140(price_parameter, order_info):
    """
    Y[140] weight count, []
    weight * fee[0]
    weight = real_weight?
    """
    weight = order_info['weight']
    fee = weight * price_parameter['fee'][0]
    return fee


def f180(price_parameter, order_info):
    """
    Y[180] weight count, [<=, <=]
    if weight <= val[0], fee[0]
    if val[0] < weight <= val[1], (weight - val[0]) * fee[1] + fee[0]
    weight = real_weight?
    What is the difference between 116 and 180 ?????
    "Error: 180, Too heavy"
    """
    weight = order_info['weight']
    if weight <= price_parameter['val'][0]:
        fee = price_parameter['fee'][0]
    elif weight <= price_parameter['val'][1]:
        fee = price_parameter['quick_calculation_deductions'][0] + \
              (weight - price_parameter['val'][0]) * price_parameter['fee'][1]
    else:
        fee = -1
    return fee


def f181(price_parameter, order_info):
    """
    Y[181] weight count, [<=, >]
    if weight <= val[0], fee[0]
    if weight > val[0], (weight - val[0]) * fee[1] + fee[0]
    weight = real_weight?
    """
    weight = order_info['weight']
    if weight <= price_parameter['val'][0]:
        fee = price_parameter['fee'][0]
    else:
        fee = price_parameter['quick_calculation_deductions'][0] + \
              (weight - price_parameter['val'][0]) * price_parameter['fee'][1]
    return fee


def f190(price_parameter, order_info):
    """
    Y[190] weight count, [<=, >]
    if weight <= val[0], fee[0]
    if weight > val[0], (weight - val[0]) * fee[1] + fee[0]
    weight = real_weight?
    What is the difference between 117 and 181 and 190 ?????
    """
    weight = order_info['weight']
    if weight <= price_parameter['val'][0]:
        fee = price_parameter['fee'][0]
    else:
        fee = price_parameter['quick_calculation_deductions'][0] + \
               (weight - price_parameter['val'][0]) * price_parameter['fee'][1]
    return fee

# ======================================================================================================


def f220(price_parameter, order_info):
    """
    Y[220] volume count
    volume * fee[0]
    volume = real_volume?
    """
    volume = order_info['volume']
    fee = volume * price_parameter['fee'][0]
    return fee


def f221(price_parameter, order_info):
    """
    Y[221] volume count
    if volume <= val[0], volume * fee[0]
    volume = real_volume?
    Error: 221, Too huge
    """
    volume = order_info['volume']
    if volume <= price_parameter['val'][0]:
        fee = price_parameter['fee'][0]
    else:
        fee = -1
    return fee


def f270(price_parameter, order_info):
    """
    Y[270] volume count
    if volume <= val[0], volume * fee[0]
    volume = real_volume?
     """
    volume = order_info['volume']
    fee = volume * price_parameter['fee'][0]
    return fee

# ======================================================================================================


def f330(price_parameter, order_info):
    """
    Y[330] number count
    number * fee[0]
    """
    quantity = order_info['quantity']
    fee = quantity * price_parameter['fee'][0]
    return fee


def f331(price_parameter, order_info):
    """
    Y[331] number count
    if number <= val[0], number * fee[0]
    if number > val[0], number * fee[1]
    """
    quantity = order_info['quantity']
    if quantity <= price_parameter['val'][0]:
        fee = quantity * price_parameter['fee'][0]
    else:
        fee = price_parameter['quick_calculation_deductions'][0] + \
              (quantity - price_parameter['val'][0]) * price_parameter['fee'][1]
    return fee


def f332(price_parameter, order_info):
    """
    Y[332] number count
    if number <= 100, number * fee[0]
    if number > 100, number * fee[1]
    """
    quantity = order_info['quantity']
    if quantity <= 100:
        fee = quantity * price_parameter['fee'][0]
    else:
        fee = price_parameter['quick_calculation_deductions'][0] + \
              (quantity - 100) * price_parameter['fee'][1]
    return fee


def f360(price_parameter, order_info):
    """
    Y[360] number count
    number * fee[0]
    What is the difference between 117 and 181 and 190 ?????
    """
    quantity = order_info['quantity']
    fee = quantity * price_parameter['fee'][0]
    return fee


def f361(price_parameter, order_info):
    """
    Y[361] number count
    if brand <> 'hankook', number * fee[0]
    if brand == 'hankook', number * fee[1]
    """
    quantity = order_info['quantity']
    fee = quantity * price_parameter['fee'][0]
    # fee = quantity * 4
    return fee
    # if brand == 'hankook':
    #     return number * price_parameter['fee'][1]
    # else:
    #     return number * price_parameter['fee'][0]

# ======================================================================================================


def f470(price_parameter, order_info):
    """
    Y[470] cube(volume) count
    if cube <= 0.5, cube * fee[0]
    if cube > 0.5, (cube - 0.5) * fee[1] + fee[0]
    cube = real_cube?
    """
    volume = order_info['volume']
    if volume <= 0.5:
        fee = volume * price_parameter['fee'][0]
    else:
        fee = price_parameter['quick_calculation_deductions'][0] + \
              (volume - 0.5) * price_parameter['fee'][1]
    return fee

# ======================================================================================================


def f770(price_parameter, order_info):
    """
    Y[770] number count
    if number <= 100
    if number > 100
    What is the difference between 332 and 770 ?????
    """
    quantity = order_info['quantity']
    if quantity <= 100:
        fee = quantity * price_parameter['fee'][0]
    else:
        fee = price_parameter['quick_calculation_deductions'][0] + \
               (quantity - 100) * price_parameter['fee'][1]
    return fee


# ======================================================================================================

rule_function_dict = {110: f110, 111: f111, 112: f112, 114: f114, 116: f116,
                      117: f117, 140: f140, 180: f180, 181: f181, 190: f190,
                      220: f220, 221: f221, 270: f270,
                      330: f330, 331: f331, 332: f332, 360: f360, 361: f361,
                      470: f470,
                      770: f770}
# ======================================================================================================


"""
N[119] weight count,
    elif city_from == '上海市' and logistics == 'YTO' and type_id == 1 
    and algo_list == [1, 1, 9, 9] and cond == ['<=', '>', '<=', '>'] and val == [1, 1, 1, 1]:
N[113] weight count, 1 case, 2 bounds, >=val[0] and <=val[1]
    weight * fee[1] + fee[0]
    weight = real_weight?
N[115] weight count, 2 cases, 2 bounds,
     if weight <= val[0], fee[0]
     if val[0] < weight < val[1], (weight - val[0]) * fee[1] + fee[0]
     weight = real_weight?
N[141] weight count, 1 case, lower-bound
    if weight >= val[0], weight * fee[0]
    weight = real_weight?
N[271] volume count
    volume * fee[0]
    volume = real_volume?
    """
