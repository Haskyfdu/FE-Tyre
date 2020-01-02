#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

import json
try:
    from algorithms.src.core.FE_Pick_Storage.receiver_sql import sql_receiver
    from algorithms.src.core.FE_Pick_Storage.pricing_scope_sql import sql_receiver_transport_pick1
    from algorithms.src.core.FE_Pick_Storage.inventory_sql import sql_wms_inventory_list
except ImportError:
    from algorithms.lib.core.FE_Pick_Storage.receiver_sql import sql_receiver
    from algorithms.lib.core.FE_Pick_Storage.pricing_scope_sql import sql_receiver_transport_pick1
    from algorithms.lib.core.FE_Pick_Storage.inventory_sql import sql_wms_inventory_list


data = sql_receiver_transport_pick1("SELECT * FROM mw_transport.mwt_contract_rule_scope;")
receiver_data, receiver_missing_list_data = sql_receiver(
        "SELECT * FROM logistics_oms.oms_receiver where status > 0 and eid = 'aifuyi';")
wms_inventory_list_data = sql_wms_inventory_list("SELECT * FROM logistics_wms.wms_stock where status=1 and flag=1;")

for receiver_id in receiver_data:
    prov = receiver_data[receiver_id]['Prov']
    city = receiver_data[receiver_id]['City']
    address = receiver_data[receiver_id]['Address']
    name = receiver_data[receiver_id]['Name']
    receiver_data[receiver_id].update({'pick': []})
    for pricing_info in data:
        if pricing_info['prov'] == prov:
            if pricing_info['city'] == '' and pricing_info['dist'] == '' and pricing_info['street'] == '':
                receiver_data[receiver_id]['pick'].append(pricing_info)
            elif pricing_info['city'] == city:
                if pricing_info['dist'] != '' or pricing_info['street'] != '':
                    if pricing_info['dist'] in address and pricing_info['street'] in address:
                        receiver_data[receiver_id]['pick'].append(pricing_info)
                else:
                    receiver_data[receiver_id]['pick'].append(pricing_info)

json_str = json.dumps(receiver_data, indent=4, ensure_ascii=False)
with open('../../../../data/input/pick/receiver_dict.json', 'w') as json_file:
    json_file.write(json_str)  # 输出为receiver_dict
json_str = json.dumps(receiver_missing_list_data, indent=4, ensure_ascii=False)
with open('../../../../data/input/receiver_missing_list.json', 'w') as json_file:
    json_file.write(json_str)
json_str = json.dumps(wms_inventory_list_data, indent=4, ensure_ascii=False)
with open('inventory_dict.json', 'w') as json_file:
    json_file.write(json_str)
