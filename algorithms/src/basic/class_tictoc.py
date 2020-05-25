#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime


class TicToc(object):
    # for start time: TicToc.tic()
    # for end time: TicToc.toc()

    __tic_time, __toc_time = None, None

    @classmethod
    def tic(cls):
        cls.__tic_time = datetime.now()

    @classmethod
    def toc(cls):
        cls.__toc_time = datetime.now()
        print("\nStarting:            {0}\r".format(cls.__tic_time))
        print("\rFinishing:           {0}\r".format(cls.__toc_time))
        print("\rTask Elapsed Time:   {0}\n".format(cls.__toc_time - cls.__tic_time))
