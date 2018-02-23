#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/5 21:26
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : filterContigsOrReadsByLength.py
# @Software: PyCharm


"""
参数1：待处理的文件名称
参数2：过滤长度下界

"""
import os
import time
import sys

if __name__=="__main__":

    time_start=time.time()

    source=[]

    # rootdir=os.getcwd()
    #
    # for parent,dirnames,filenames in os.walk(rootdir):
    #     for filename in filenames:
    #         if(filename[-13:]=="Contigs.fasta"):
    #             source.append(filename)
    source.append(sys.argv[1])
    length=int(sys.argv[2])

    ref_lines=[]
    contig=[]
    heads=set()
    valid=False
    for file in source:
        with open(file) as f:
            lines=f.readlines()
            for i in range(0,len(lines)):
                if(lines[i][0]=='>'):
                    if(len(contig)):
                        ref_lines.append(contig)
                    contig=[]
                    if(int(lines[i].split(' ')[1])>=length):
                        contig.append(lines[i])
                        heads.add(lines[i])
                        valid=True
                    else:
                        valid=False
                elif(valid==True):
                    contig.append(lines[i])
        if(len(contig)>=2):
            ref_lines.append(contig)





    out_file=open(sys.argv[1]+"filter.by.length."+sys.argv[2]+".fasta",'w')
    for co in ref_lines:
        out_file.writelines(co)

    print("Time use:",time.time()-time_start)
