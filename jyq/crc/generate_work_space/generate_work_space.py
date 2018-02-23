#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/9 21:34
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : generate_work_space.py
# @Software: PyCharm


"""

This script generate work space for crc data .
Need to run in the folder where there consist files named *1.fq *2.fq
Note that if the file doesn't end with fq, edit line 49 and 51 accordingly
"""



import subprocess
import time
import os

thread=40
rootdir = os.getcwd()
new_env = os.environ.copy()
new_env['MRKDUP'] = '/home/qiusuo/picard-tools-1.77/MarkDuplicates.jar'
new_env['PATH']="/home/qiusuo/bin:/home/qiusuo/.local/bin:/home/admin01/cdhit:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/media/blast+/bin:/zrom/z-tools/bin:/snap/bin:/home/qiusuo/CONCOCT-master/scripts:/home/qiusuo/bowtie2-2.3.3:/home/qiusuo/CONCOCT-master:/home/qiusuo/CONCOCT-master/scripts:/home/qiusuo/bowtie2-2.3.3:/home/qiusuo/CONCOCT-master:/home/qiusuo/samtools-1.5:/home/qiusuo/bedtools2/bin"

def check_and_delete(table):
    finished=0
    cpy_table=table
    for x in table:
        if(x.poll()==0):
            finished=finished+1
            cpy_table.remove(x)
    table=cpy_table
    return finished

if __name__=="__main__":

    cmd="mkdir samples"
    subprocess.call(cmd,shell=True,env=new_env)

    rootdir=os.getcwd()
    source_1=[]
    source_2=[]
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            if(filename[-4:]=="1.fq"):
                source_1.append(filename)
            if(filename[-4:]=="2.fq"):
                source_2.append(filename)

    for file in source_2:
    	sample_name='.'.join(file.split('.')[:3])
    	cmd="mkdir  samples/"+sample_name
    	subprocess.call(cmd,shell=True,env=new_env)


    for file in source_1:
    	sample_name='.'.join(file.split('.')[:3])
    	cmd="mv "+file+" samples/"+sample_name+"/"+file
    	subprocess.call(cmd,shell=True,env=new_env)

    for file in source_2:
    	sample_name='.'.join(file.split('.')[:3])
    	cmd="mv "+file+" samples/"+sample_name+"/"+file
    	subprocess.call(cmd,shell=True,env=new_env)
