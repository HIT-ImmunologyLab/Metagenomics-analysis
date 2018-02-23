#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/4 10:33
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : ranksum.py
# @Software: PyCharm

"""
This script caculate the rank-sum between case and control groups
"""

from scipy import stats
import os
#file to refer

file=[]
for parent, dirnames, filenames in os.walk("./case"):
	for filename in filenames:
		file.append(filename)


# file=["spf_order.txt","spf_phylum.txt","spf_species.txt","spf_genus.txt","spf_familly.txt","spf_class.txt"]

"""
    This for loop caculate ranksum on per level
"""
for cur_file in file:

	visited=set()
	case_dict=dict()
	control_dict=dict()
	result=dict()

	with open("case/"+cur_file) as spf:
		lines=spf.readlines()
		for line in lines:
			case_dict[line.split('\t')[0]]=line.split('\t')[1:]

	with open("control/"+cur_file) as spf:
		lines=spf.readlines()
		for line in lines:
			control_dict[line.split('\t')[0]]=line.split('\t')[1:]

	for key in case_dict.keys():
		if(key not in visited):
			visited.add(key)
			x=case_dict[key]
			if(key in control_dict.keys()):
				y=control_dict[key]
			else:
				y=[0.0 for i in range(50)]
			w,p=stats.ranksums(x, y)
			result[key]=(w,p)

	for key in control_dict.keys():
		if(key not in visited):
			visited.add(key)
			x=control_dict[key]
			if(key in case_dict.keys()):
				y=case_dict[key]
			else:
				y=[0.0 for i in range(50)]
			w,p=stats.ranksums(x, y)
			result[key]=(w,p)


	with open(cur_file.split('_')[1].split('.')[0]+"ranksums.txt",'w') as outfile:
		outfile.write(cur_file.split('_')[1].split('.')[0]+'\t'+'w\tp-value\n')
		for key in result.keys():
			outfile.write(key+'\t'+str(result[key][0])+'\t'+str(result[key][1])+'\n')
