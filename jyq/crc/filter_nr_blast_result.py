#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/5 21:17
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : filter_nr_blast_result.py
# @Software: PyCharm


"""
This script will filter nr result by 80% iden. However, this param can be changed by edit the 51th line of the script
Note that the script should be excute where there is result.xml. 
"""


with open("result.xml") as result:
    headers = []
    tails = []
    nodes = []

    lines = result.readlines()
    i = 0

    while i < len(lines):
        if (lines[i][:3] != "<It"):
            headers.append(lines[i])
            i += 1
        else:
            break

    while i < len(lines):
        if (lines[i][:4] != "</Bl"):
            node = []
            while lines[i][:4] != "</It" or len(lines[i]) > 13:
                node.append(lines[i])
                i += 1
            node.append(lines[i])
            i += 1
            nodes.append(node)
            if (lines[i][:3] != "<It"):
                break

    while i < len(lines):
        tails.append(lines[i])
        i += 1

    nnodes = []
    for node in nodes:
        identity = float(node[24].split('>')[1].split('<')[0])
        length = float(node[27].split('>')[1].split('<')[0])
        if (identity / length > 0.8):
            nnodes.append(node)

    with open("result_.xml", 'w') as nf:
        nf.writelines(headers)
        for node in nnodes:
            nf.writelines(node)
        nf.writelines(tails)
