#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/3 18:58
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : Count_PE.py
# @Software: PyCharm


"""
This script count the PE num using samtools

Note that you may need change the env in line 23
"""
import subprocess
import time
import os

thread = 20  #parallel program num
rootdir = os.getcwd()
new_env = os.environ.copy()
new_env['MRKDUP'] = '/home/qiusuo/picard-tools-1.77/MarkDuplicates.jar'
new_env['PATH'] = "/home/qiusuo/miniconda3/bin:/home/qiusuo/miniconda3/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/bin:/home/qiusuo/img/ext4_utils_new:/home/qiusuo/SeqPrep:/home/qiusuo/Trimmomatic-0.36:/home/qiusuo/my_interproscan/interproscan-5.25-64.0:/home/qiusuo/hmmer-3.1b2-linux-intel-x86_64/binaries:/home/qiusuo/FragGeneScan1.30:/home/qiusuo/megahit_v1.1.1_LINUX_CPUONLY_x86_64-bin:/home/qiusuo/crAss_v2.1:/home/qiusuo/bbmap:/home/qiusuo/COCACOLA-python:/home/qiusuo/bowtie2-2.3.2:/home/qiusuo/bowtie2-2.3.2/scripts:/home/qiusuo/samtools-1.2:/home/qiusuo/CONCOCT-master/scripts:/home/qiusuo/ncbi-blast-2.6.0+/bin:/home/qiusuo/miniconda3/envs/qiime2-2017.6/bin:/home/qiusuo/miniconda3/envs/qiime1/bin:/home/qiusuo/blast:/usr/local/sbin:/usr/sbin:/home/qiusuo/SeqPrep:/home/qiusuo/Trimmomatic-0.36:/home/qiusuo/my_interproscan/interproscan-5.25-64.0:/home/qiusuo/hmmer-3.1b2-linux-intel-x86_64/binaries:/home/qiusuo/FragGeneScan1.30:/home/qiusuo/megahit_v1.1.1_LINUX_CPUONLY_x86_64-bin:/home/qiusuo/crAss_v2.1:/home/qiusuo/bbmap:/home/qiusuo/COCACOLA-python:/home/qiusuo/bowtie2-2.3.2:/home/qiusuo/bowtie2-2.3.2/scripts:/home/qiusuo/samtools-1.2:/home/qiusuo/CONCOCT-master/scripts:/home/qiusuo/ncbi-blast-2.6.0+/bin:/home/qiusuo/miniconda3/envs/qiime2-2017.6/bin:/home/qiusuo/miniconda3/envs/qiime1/bin:/home/qiusuo/blast:/home/qiusuo/.local/bin:/home/qiusuo/bin"

sum = 0


def check_and_delete(table):

    """

    :param table: The current task queue(parallel running)
    :return: finished task(s)
    """
    finished = 0
    table_cpy = table
    for x in table:
        if (x.poll() == 0):
            out, err = x.communicate()
            sum += int(out)
            finished = finished + 1
            table_cpy.remove(x)
    table = table_cpy
    return finished


if __name__ == "__main__":

    source = []
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            filename = os.path.join(parent, filename)
            if (filename[-4:] == ".bam"):
                source.append(filename)

    thread = min(len(source), thread)
    i = 0

    table = []
    for i in range(thread):
        cmd = "samtools flagstat " + source[i] + " | grep 'properly paired' | cut -d ' ' -f1"
        print(cmd)
        table.append(subprocess.Popen(cmd, shell=True, env=new_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    if (i < len(source) - 1):
        i = thread
        while True:
            time.sleep(1)
            finished = check_and_delete(table)
            for j in range(i, min(i + finished, len(source))):
                cmd = "samtools flagstat " + source[j] + " | grep 'properly paired' | cut -d ' ' -f1"
                print(cmd)
                table.append(subprocess.Popen(cmd, shell=True, env=new_env))
            i = min(i + finished, len(source))
            if (i >= len(source)):
                for x in table:
                    out, err = x.communicate()
                    sum += int(out)
                break
    else:
        for i in range(len(source)):
            out, err = table[i].communicate()
            sum += int(out)


    print(sum)
