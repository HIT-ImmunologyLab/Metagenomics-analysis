#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/6 7:57
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : Find_contig_by_id.py
# @Software: PyCharm

"""
This little script finds a particular contig by contigs-ID
Note that you may need change the file name at line 13 and contigs-ID at line 17
"""
with open("final.contigs.fasta") as f:
	lines=f.readlines()
	collect=[]
	for i in range(0,len(lines),2):
		if(lines[i][:len(">k119_476076 ")]==">k119_476076 "):
			collect.append(lines[i])
			collect.append(lines[i+1])
			break
	print(collect)