#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/5 21:26
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : Cut_500bp_for_Rayout.py
# @Software: PyCharm


"""
This litte script will cut off the contigs shorter than 500bp in Ray-meta result
Note that the file should named with "Contigs.fasta"
"""
import os
import time
if __name__=="__main__":

    time_start=time.time()

    source=[]

    rootdir=os.getcwd()

    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            if(filename[-13:]=="Contigs.fasta"):
                source.append(filename)


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
                    if(int(lines[i].split(' ')[1])>=500):
                        contig.append(lines[i])
                        heads.add(lines[i])
                        valid=True
                    else:
                        valid=False
                elif(valid==True):
                    contig.append(lines[i])





    out_file=open("Contigs.cut.500bp.fasta",'w')
    for co in ref_lines:
        out_file.writelines(co)

    print(time.time()-time_start)
