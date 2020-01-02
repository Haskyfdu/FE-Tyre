#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

from collections import defaultdict
import math
data_info = defaultdict(str)
# ========================================================================================================================
# remember to add the fee_extra_sum


def f110(price_parameter, real_weight, real_volume, real_number):
    weight = real_weight
    if weight <= price_parameter['val'][0]:
        return price_parameter['fee'][0]
    else:
        for i, p in enumerate(price_parameter['val']):
            if weight <= p:
                fee = (weight - price_parameter['val'][i-1]) * price_parameter['fee'][i] + \
                      price_parameter['fee_accumulation'][i-1]
                return fee
        return (weight - price_parameter['val'][i]) * price_parameter['fee'][i] + price_parameter['fee_accumulation'][i-1]
# Y[110] weight count, [<=, <=, ..., <=, >]
#     Step charges
#     weight = real_weight?


def f111(price_parameter, real_weight, real_volume, real_number):
    weight = real_weight
    if weight <= price_parameter['val'][0]:
        return price_parameter['fee'][0]
    else:
        for i, p in enumerate(price_parameter['val']):
            if weight <= p:
                fee = (weight - price_parameter['val'][i-1]) * price_parameter['fee'][i] + \
                      price_parameter['fee_accumulation'][i-1]
                return fee
    return "Error: 111, Too heavy"
# Y[111] weight count, [<=, <=, ..., <=, <=]
#     Step charges
#     weight = real_weight?


def f112(price_parameter, real_weight, real_volume, real_number):
    weight = real_weight
    if price_parameter['val'][0] <= weight <= price_parameter['val'][1]:
        return weight * price_parameter['fee'][1]
    else:
        return "Error: 112, Too heavy or light"
# Y[112] weight count, [>=, <=]
#     if val[0] <= weight <= val[1], weight * fee[1]
#     weight = real_weight?


def f114(price_parameter, real_weight, real_volume, real_number):
    if real_weight < 100:
        weight = math.ceil(real_weight * 2) / 2
    else:
        weight = int(real_weight + 0.5)
    if weight < 1:
        return price_parameter['fee'][0]
    elif weight < 30:
        return price_parameter['fee_accumulation'][0] + (weight - 1) * price_parameter['fee'][1]
    else:
        return price_parameter['fee_accumulation'][1] + (weight - 30) * price_parameter['fee'][2]
# Y[114] weight count, [<=, <, <]
#     if weight <= val[0], fee[0]
#     if val[0] < weight < val[1], (weight - 1) * fee[1] + fee[0]
#     if weight > val[1], (weight - val[1]) * fee[2] + (val[1] - 1) * fee[1] + fee[0]
#     weight = math.ceil(real_weight * 2) / 2 if real_weight < 100, count by 0.5
#     weight = int(real_weight + 0.5) if real_weight >= 100, rounding


def f116(price_parameter, real_weight, real_volume, real_number):
    weight = real_weight
    if weight <= price_parameter['val'][0]:
        return price_parameter['fee'][0]
    elif weight <= price_parameter['val'][1]:
        return price_parameter['fee_accumulation'][0] + (weight - price_parameter['val'][0]) * price_parameter['fee'][1]
    else:
        return "Error: 116, Too heavy"
# Y[116] weight count, 2 cases, 2 bounds, [<=, <=]
#     if weight <= val[0], fee[0]
#     if val[0] < weight <= val[1], (weight - val[0]) * fee[1] + fee[0]
#     weight = real_weight?


def f117(price_parameter, real_weight, real_volume, real_number):
    weight = real_weight
    if weight <= price_parameter['val'][0]:
        return price_parameter['fee'][0]
    else:
        return price_parameter['fee_accumulation'][0] + (weight - price_parameter['val'][0]) * price_parameter['fee'][1]
# Y[117] weight count, [<=, >]
#     if weight <= val[0],fee[0]
#     if weight > val[0], (weight - val[0]) * fee[1] + fee[0]


def f140(price_parameter, real_weight, real_volume, real_number):
    weight = real_weight
    return weight * price_parameter['fee'][0]
# Y[140] weight count, []
#     weight * fee[0]
#     weight = real_weight?


def f180(price_parameter, real_weight, real_volume, real_number):
    weight = real_weight
    if weight <= price_parameter['val'][0]:
        return price_parameter['fee'][0]
    elif weight <= price_parameter['val'][1]:
        return price_parameter['fee_accumulation'][0] + (weight - price_parameter['val'][0]) * price_parameter['fee'][1]
    else:
        return "Error: 180, Too heavy"
# Y[180] weight count, [<=, <=]
#     if weight <= val[0], fee[0]
#     if val[0] < weight <= val[1], (weight - val[0]) * fee[1] + fee[0]
#     weight = real_weight?
#  What is the difference between 116 and 180 ?????


def f181(price_parameter, real_weight, real_volume, real_number):
    weight = real_weight
    if weight <= price_parameter['val'][0]:
        return price_parameter['fee'][0]
    else:
        return price_parameter['fee_accumulation'][0] + (weight - price_parameter['val'][0]) * price_parameter['fee'][1]
# Y[181] weight count, [<=, >]
#     if weight <= val[0], fee[0]
#     if weight > val[0], (weight - val[0]) * fee[1] + fee[0]
#     weight = real_weight?


def f190(price_parameter, real_weight, real_volume, real_number):
    weight = real_weight
    if weight <= price_parameter['val'][0]:
        return price_parameter['fee'][0]
    else:
        return price_parameter['fee_accumulation'][0] + (weight - price_parameter['val'][0]) * price_parameter['fee'][1]
# Y[190] weight count, [<=, >]
#     if weight <= val[0], fee[0]
#     if weight > val[0], (weight - val[0]) * fee[1] + fee[0]
#     weight = real_weight?
#  What is the difference between 117 and 181 and 190 ?????
# ------------------------------------------------------------------------------------------------------------------------


def f220(price_parameter, real_weight, real_volume, real_number):
    volume = real_volume
    return volume * price_parameter['fee'][0]
# Y[220] volume count
#     volume * fee[0]
#     volume = real_volume?


def f221(price_parameter, real_weight, real_volume, real_number):
    volume = real_volume
    if volume <= price_parameter['val'][0]:
        return price_parameter['fee'][0]
    else:
        return "Error: 221, Too huge"
# Y[221] volume count
#     if volume <= val[0], volume * fee[0]
#     volume = real_volume?


def f270(price_parameter, real_weight, real_volume, real_number):
    volume = real_volume
    return volume * price_parameter['fee'][0]
# Y[270] volume count
#     if volume <= val[0], volume * fee[0]
#     volume = real_volume?
# ------------------------------------------------------------------------------------------------------------------------


def f330(price_parameter, real_weight, real_volume, real_number):
    number = real_number
    return number * price_parameter['fee'][0]
# Y[330] number count
#     number * fee[0]


def f331(price_parameter, real_weight, real_volume, real_number):
    number = real_number
    if number <= price_parameter['val'][0]:
        return number * price_parameter['fee'][0]
    else:
        return price_parameter['fee_accumulation'][0] + (number - price_parameter['val'][0]) * price_parameter['fee'][1]
# Y[331] number count
#     if number <= val[0], number * fee[0]
#     if number > val[0], number * fee[1]


def f332(price_parameter, real_weight, real_volume, real_number):
    number = real_number
    if number <= 100:
        return number * price_parameter['fee'][0]
    else:
        return price_parameter['fee_accumulation'][0] + (number - 100) * price_parameter['fee'][1]
# Y[332] number count
#     if number <= 100, number * fee[0]
#     if number > 100, number * fee[1]


def f360(price_parameter, real_weight, real_volume, real_number):
    number = real_number
    return number * price_parameter['fee'][0]
# Y[360] number count
#     number * fee[0]
#  What is the difference between 117 and 181 and 190 ?????


def f361(price_parameter, real_weight, real_volume, real_number):
    number = real_number
    return number * 4
    # if brand == 'hankook':
    #     return number * price_parameter['fee'][1]
    # else:
    #     return number * price_parameter['fee'][0]
# Y[361] number count
#     if brand <> 'hankook', number * fee[0]
#     if brand == 'hankook', number * fee[1]


def f470(price_parameter, real_weight, real_volume, real_number):
    volume = real_volume
    if volume <= 0.5:
        return volume * price_parameter['fee'][0]
    else:
        return price_parameter['fee_accumulation'][0] + (volume - 0.5) * price_parameter['fee'][1]
# Y[470] cube(volume) count
#     if cube <= 0.5, cube * fee[0]
#     if cube > 0.5, (cube - 0.5) * fee[1] + fee[0]
#     cube = real_cube?


def f770(price_parameter, real_weight, real_volume, real_number):
    number = real_number
    if number <= 100:
        return number * price_parameter['fee'][0]
    else:
        return price_parameter['fee_accumulation'][0] + (number - 100) * price_parameter['fee'][1]
# Y[770] number count
#     if number <= 100
#     if number > 100
#  What is the difference between 332 and 770 ?????


def f999(price_parameter, real_weight, real_volume, real_number):
    return "Error: 999, unsolved case"
# Y[999] error


rule_function_dict = {110: f110, 111: f111, 112: f112, 114: f114, 116: f116, 117: f117, 140: f140, 180: f180,
                      181: f181, 190: f190, 220: f220, 221: f221, 270: f270, 330: f330, 331: f331, 332: f332,
                      360: f360, 361: f361, 470: f470, 770: f770, 999: f999}
# ------------------------------------------------------------------------------------------------------------------------
# ========================================================================================================================


# N[119] weight count,
#     elif city_from == '上海市' and logistics == 'YTO' and type_id == 1 \
#     and algo_list == [1, 1, 9, 9] and cond == ['<=', '>', '<=', '>'] and val == [1, 1, 1, 1]:
# N[113] weight count, 1 case, 2 bounds, >=val[0] and <=val[1]
#     weight * fee[1] + fee[0]
#     weight = real_weight?
# N[115] weight count, 2 cases, 2 bounds,
#      if weight <= val[0], fee[0]
#      if val[0] < weight < val[1], (weight - val[0]) * fee[1] + fee[0]
#      weight = real_weight?
# N[141] weight count, 1 case, lower-bound
#     if weight >= val[0], weight * fee[0]
#     weight = real_weight?
# N[271] volume count
#     volume * fee[0]
#     volume = real_volume?
# ========================================================================================================================