#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/11/21 2:21 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : ui_centralizer.py
# @Project : prize
import math
from tkinter import Misc, Tk


def centralize(win: Misc, width, height):
    """
    centralize a tk/Toplevel window
    """
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = math.ceil((screen_width - width) / 2)
    y = math.ceil((screen_height - height) / 2)
    win.geometry("%dx%d+%d+%d" % (width, height, x, y))


def left(win: Misc, base_win: Tk, width, height):
    """
    display the win on the left hand side of base_win
    """
    base_x = base_win.winfo_pointerx()
    base_y = base_win.winfo_pointery()
    x = base_x - width
    if x < 0:
        x = 0
    y = base_y
    win.geometry("%dx%d+%d+%d" % (width, height, x, y))


def right(win: Misc, base_win: Tk, width, height):
    """
    display the win on the right hand side of base_win
    """
    base_x = base_win.winfo_pointerx()
    base_y = base_win.winfo_pointery()
    delta_width = base_win.winfo_width()
    x = base_x + delta_width
    if x >= base_win.winfo_screenwidth():
        x = base_win.winfo_screenwidth() - width
    y = base_y
    win.geometry("%dx%d+%d+%d" % (width, height, x, y))
