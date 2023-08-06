#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/11/20 12:10 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : number.py
# @Project : prize



def padding0(data):
    """
    padding '0' into a number.
    so given a number=1, then it return '01'
    """
    if data is None:
        return '00'
    if type(data) == str:
        int_data = int(data)
    else:
        int_data = data
    if int_data < 10:
        return '0' + str(int_data)
    else:
        return str(int_data)
