#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

from algorithms.algorithm_io import ImportData, ExportResults
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
        fee = rule_diction.rule_function_dict[price_parameter['type']](price_parameter, weight, volume, quantity)
    else:
        return -1
    if isinstance(fee, str):
        return -1
    else:
        return fee + price_parameter['fee_extra_sum']


if __name__ == '__main__':

    print(price_calculator('001', '002', 12, 3, 6))
