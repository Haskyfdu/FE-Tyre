#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

import json
try:
    from algorithms.src.core.FE_Pick_Storage import rule_collect
except ImportError:
    from algorithms.lib.core.FE_Pick_Storage import rule_collect


output_program, output_development, data_dict = rule_collect.data_processing()
with open('../../../../data/input/pick/pricing_rule.json', 'w', encoding='utf-8') as file_obj:
    json.dump(output_program, file_obj, indent=4, ensure_ascii=False)
