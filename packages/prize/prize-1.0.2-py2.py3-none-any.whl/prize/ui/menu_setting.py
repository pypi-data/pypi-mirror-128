#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/10/9 9:24 上午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : menu_setting.py
# @Project : absentee
import os
import sys
import platform
import tkinter.messagebox as mb
import renxianqi.shortcut as sc
from prize import setting
from prize.pip_trigger import upgrade

POPUP_TITLE = "[Prize抽奖小工具]"


def show_copyright():
    message = """
工具采用Apache License，请放心免费使用！
版本：%s
开发者：雷学委
作者网站：https://blog.csdn.net/geeklevin
社区信息：https://py4ever.gitee.io/
欢迎关注公众号【雷学委】，加入Python开发者阵营！
    """ % (setting.VERSION)
    mb.showinfo(POPUP_TITLE, message)


def make_shortcut():
    os_name = platform.system()
    if os_name == "Windows" or "Win" in os_name:
        binpath = sys.argv[0]
        if not binpath.endswith(".exe"):
            binpath = binpath + ".exe"
        title = "Prize抽奖小工具"
        status = sc.create_shortcut(binpath, title, "一个方便的抽奖工具")
        if status:
            mb.showinfo(POPUP_TITLE, "【" + title + "】快捷方式创建成功！")
        else:
            mb.showerror(POPUP_TITLE, "抱歉，当前系统不支持创建快捷方式。")
    else:
        mb.showinfo(POPUP_TITLE, "抱歉，仅支持Windows系统创建快捷方式！")



def trigger_upgrade():
    upgrade()


def show_about():
    message = """
操作说明：
界面从上到下。
1）用户可以从把评论列表直接复制到上面的白色文本框内。
2）点击生成卡片，这会更新到参与抽奖的全部个体。
抽奖可以点击'重新抽奖按钮'
抽奖个体卡片会随机点亮，每一个卡片小格子都会闪亮（变红）
直接抽取到幸运名单，仅支持抽取一个幸运个体获得奖品。
3）支持定时抽奖功能，进入【更多配置】-> 【定时抽奖】进行配置
4）如果有多个奖项，可以多次点击【重新抽奖】
有其他改进建议可以找qq：【Python全栈技术学习交流】：https://jq.qq.com/?_wv=1027&k=ISjeG32x 
    """
    mb.showinfo(POPUP_TITLE, message)
