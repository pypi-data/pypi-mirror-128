#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/11/11 1:53 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : test.py
# @Project : prize


from tkinter import *
from tkinter import simpledialog

root = Tk()
root.title('simpledialog')
root.resizable(0, 0)


def open_simpledialog():
    d = simpledialog.SimpleDialog(root, title='Simpledialog', text='调用simpledialog.SimpleDialog函数',
                                  buttons=["确定", "取消", "退出"], default=0, cancel=3)
    print(d.go())  # 获取用户单击对话框的哪个按钮或关闭对话框返回canncel指定的值。


Button(root, text='打开Simpledialog', command=open_simpledialog).pack(side=LEFT, ipadx=5, ipady=5, padx=5, pady=5)


def open_integer():
    ask1 = simpledialog.askinteger("猜岁数", "你猜我今年几岁:", initialvalue=3, minvalue=1, maxvalue=10)
    print(ask1)


def open_float():
    simpledialog.askfloat("猜体重", "你猜我我体重多少公斤:", initialvalue=27.3, minvalue=10, maxvalue=50)


def open_string():
    simpledialog.askstring("猜名字", "你猜我叫什么名字:", initialvalue='Jack Ma')


Button(root, text='输入整数对话框', command=open_integer).pack(side=LEFT, ipadx=5, ipady=5, padx=5, pady=5)
Button(root, text='输入浮点数对话框', command=open_float).pack(side=LEFT, ipadx=5, ipady=5, padx=5, pady=5)
Button(root, text='输入字符对话框', command=open_string).pack(side=LEFT, ipadx=5, ipady=5, padx=5, pady=5)
root.mainloop()