#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/6 7:45
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : Download_nr.py
# @Software: PyCharm


"""
This script will download nr
Note that you may need to change the threads in line 15 corresponding to your network speed.  Experimental, 40 threads is suitable to 100 bmps.
"""

thread=40


import subprocess
import time

def check_and_delete(table):
    finished=0
    table_cpy = table
    for x in table:
        if(x.poll()==0):
            finished=finished+1
            table_cpy.remove(x)
    table=table_cpy
    return finished


source=[]
for i in range(73):
	s=str(i).zfill(2)
	source.append("ftp://ftp.ncbi.nlm.nih.gov/blast/db/nr."+s+".tar.gz")


thread=min(len(source),thread)
i=0
table=[]
for i in range(thread):
    cmd="axel "+source[i]
    print(cmd)
    table.append(subprocess.Popen(cmd,shell=True,env=new_env))
if(i<len(source)-1):
    i=thread
    while True:
        time.sleep(1)
        finished=check_and_delete(table)
        for j in range(i,min(i+finished,len(source))):
            cmd="axel "+source[j]
            print(cmd)
            table.append(subprocess.Popen(cmd,shell=True,env=new_env))
        i=min(i+finished,len(source))
        if(i==len(source)):
            for x in table:
                x.wait()
            break
else:
    for i in range(len(source)):
        table[i].wait()
