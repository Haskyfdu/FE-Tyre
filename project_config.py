#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------


import os


class Config(object):
    def __class_getitem__(cls, item):
        return getattr(cls, item)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        self.key = value


class ProjectConfig(Config):
    Global = {
        'Task_Id': None,
        'I/O_Mode': ['Json', 'Json'],
        'Config_File': os.path.realpath(__file__),
    }

    Path = {
        'Project_Path': os.path.dirname(Global['Config_File']),
        'Data_Path': os.path.join(os.path.dirname(Global['Config_File']), 'data'),
        'Log_Path': os.path.join(os.path.dirname(Global['Config_File']), 'logs'),
        'Static_Path': os.path.join(os.path.dirname(Global['Config_File']), 'static'),
        'Templates_Path': os.path.join(os.path.dirname(Global['Config_File']), 'templates'),
    }


class AlgorithmConfig(Config):
    Parameter = {
        'Valid_Space_Threshold': 0.9,
        'Category_List': ['food', 'chemical', 'metal', 'coal', 'agricultural', 'construction', 'tissue'],
    }

    Path = {
        'Algorithm_Path': os.path.join(ProjectConfig['Path']['Project_Path'], 'algorithms'),
        'Input_Data_Path': os.path.join(ProjectConfig['Path']['Data_Path'], 'input'),
        'Output_Data_Path': os.path.join(ProjectConfig['Path']['Data_Path'], 'output'),
    }
