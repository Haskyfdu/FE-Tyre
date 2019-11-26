#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------


import os
import json
import traceback
import requests
# from utils.log import Log
from project_config import AlgorithmConfig, ProjectConfig


# ==================================================================================================================================================


class ImportData(object):

    @classmethod
    def read(cls, filepath=AlgorithmConfig['Path']['Input_Data_Path'], filename='cache.json'):
        try:
            if ProjectConfig['Global']['I/O_Mode'][0] == 'Json':
                with open(os.path.join(filepath, filename), 'r', encoding='utf-8') as json_input_file:
                    raw_data = json.load(json_input_file)
            elif ProjectConfig['Global']['I/O_Mode'][0] == 'Database':
                # Todo: fill after database built
                pass
            else:
                raise IOError
            # print('{0} 读入成功'.format(filename))
            # Log.Information('{0} 读入成功'.format(filename))
        except IOError:
            print('{0} 读入失败'.format(filename))
            print(traceback.format_exc())
            # Log.Warning('{0} 读入失败'.format(filename))
            # Log.Error(traceback.format_exc())
        return raw_data


class ExportResults(object):

    @classmethod
    def write(cls, result, filepath=AlgorithmConfig['Path']['Output_Data_Path'], filename='cache.json'):
        try:
            if ProjectConfig['Global']['I/O_Mode'][1] == 'Json':
                with open(os.path.join(filepath, filename), 'w', encoding='utf-8') as json_output_file:
                    json.dump(result, json_output_file, indent=4, ensure_ascii=False)
            elif ProjectConfig['Global']['I/O_Mode'][1] == 'Database':
                # Todo: fill after database built
                pass
            else:
                raise IOError
            # print(json.dumps(result, ensure_ascii=False, indent=4))
            # print('{0} 写出成功'.format(filename))
            # Log.Information(json.dumps(result, ensure_ascii=False, indent=4))
            # Log.Information('{0} 写出成功'.format(filename))
        except IOError:
            print('{0} 写出失败'.format(filename))
            print(traceback.format_exc())
            # Log.Warning('{0} 写出失败'.format(filename))
            # Log.Error(traceback.format_exc())

    @classmethod
    def post(cls, result, post_url):
        try:
            response = requests.post(url=post_url, json=result)
            print('{0} post 成功'.format(post_url))
            print(response.text)
            # Log.Information('{0} post 成功'.format(post_url))
            # Log.Information(response.text)
        except IOError:
            print('{0} post 失败'.format(post_url))
            print(traceback.format_exc())
            # Log.Warning('{0} post 失败'.format(post_url))
            # Log.Error(traceback.format_exc())
