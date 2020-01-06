#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

from algorithms.algorithm_io import ImportData
from project_config import AlgorithmConfig
try:
    from algorithms.src.core.FE_Pick_Storage import rule_diction
except ImportError:
    from algorithms.lib.core.FE_Pick_Storage import rule_diction


def price_calculator(pricing_id, rule_id, weight, volume, quantity):
    result_program = ImportData.read(filepath=AlgorithmConfig['Path']['Input_Data_Path_Pick'],
                                     filename='pricing_rule.json')
    if (str(pricing_id) + str(rule_id)) in result_program:
        price_parameter = result_program[str(pricing_id) + str(rule_id)]
        if price_parameter['type'] == 999:
            fee = -1
        else:
            fee = rule_diction.rule_function_dict[price_parameter['type']](price_parameter=price_parameter,
                                                                           order_info={'weight': weight,
                                                                                       'volume': volume,
                                                                                       'quantity': quantity})
    else:
        return -1
    if isinstance(fee, str) or not (isinstance(price_parameter['fee_least'], float)
                                    or isinstance(price_parameter['fee_least'], int)):
        return -1
    else:
        return max(fee + price_parameter['fee_extra_sum'], price_parameter['fee_least'])


if __name__ == '__main__':

    print(price_calculator('001', '002', 12, 3, 6))
