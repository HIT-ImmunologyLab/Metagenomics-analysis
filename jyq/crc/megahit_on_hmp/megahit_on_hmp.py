#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/6 7:59
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : megahit_on_hmp.py
# @Software: PyCharm

"""
This script will run megahit on PE reads. If you need to run this script on other databases, you may need to edit line 44,46  corresponding to the reads files.
Note that you may need to change the env(line 20,21) corresponding. Put the script on the root of workdir and run: python megahit_on_hmp.py
"""
import subprocess
import time
import os

thread = 20
rootdir = os.getcwd()
new_env = os.environ.copy()
new_env['MRKDUP'] = '/home/qiusuo/picard-tools-1.77/MarkDuplicates.jar'
new_env['PATH'] = "/home/qiusuo/miniconda3/bin:/home/qiusuo/miniconda3/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/bin:/home/qiusuo/img/ext4_utils_new:/home/qiusuo/SeqPrep:/home/qiusuo/Trimmomatic-0.36:/home/qiusuo/my_interproscan/interproscan-5.25-64.0:/home/qiusuo/hmmer-3.1b2-linux-intel-x86_64/binaries:/home/qiusuo/FragGeneScan1.30:/home/qiusuo/megahit_v1.1.1_LINUX_CPUONLY_x86_64-bin:/home/qiusuo/crAss_v2.1:/home/qiusuo/bbmap:/home/qiusuo/COCACOLA-python:/home/qiusuo/bowtie2-2.3.2:/home/qiusuo/bowtie2-2.3.2/scripts:/home/qiusuo/samtools-1.2:/home/qiusuo/CONCOCT-master/scripts:/home/qiusuo/ncbi-blast-2.6.0+/bin:/home/qiusuo/miniconda3/envs/qiime2-2017.6/bin:/home/qiusuo/miniconda3/envs/qiime1/bin:/home/qiusuo/blast:/usr/local/sbin:/usr/sbin:/home/qiusuo/SeqPrep:/home/qiusuo/Trimmomatic-0.36:/home/qiusuo/my_interproscan/interproscan-5.25-64.0:/home/qiusuo/hmmer-3.1b2-linux-intel-x86_64/binaries:/home/qiusuo/FragGeneScan1.30:/home/qiusuo/megahit_v1.1.1_LINUX_CPUONLY_x86_64-bin:/home/qiusuo/crAss_v2.1:/home/qiusuo/bbmap:/home/qiusuo/COCACOLA-python:/home/qiusuo/bowtie2-2.3.2:/home/qiusuo/bowtie2-2.3.2/scripts:/home/qiusuo/samtools-1.2:/home/qiusuo/CONCOCT-master/scripts:/home/qiusuo/ncbi-blast-2.6.0+/bin:/home/qiusuo/miniconda3/envs/qiime2-2017.6/bin:/home/qiusuo/miniconda3/envs/qiime1/bin:/home/qiusuo/blast:/home/qiusuo/.local/bin:/home/qiusuo/bin"


def check_and_delete(table):
    finished = 0
    cpy_table = table
    for x in table:
        if (x.poll() == 0):
            finished = finished + 1
            cpy_table.remove(x)
    table = cpy_table
    return finished


if __name__ == "__main__":


    rootdir = os.getcwd()
    source_1 = []
    source_2 = []
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            filename = os.path.join(parent, filename)
            if (filename[-7:] == "1.fastq"):
                source_1.append(filename)
            if (filename[-7:] == "2.fastq"):
                source_2.append(filename)

    thread = min(len(source_1), thread)

    cmd = "rm -rf contigs && megahit " + "--num-cpu-threads " + thread + " "
    for i in range(len(source_1)):
        cmd = cmd + "-1 "
        cmd = cmd + source_1[i] + ' '
        cmd = cmd + "-2 "
        cmd = cmd + source_2[i] + ' '
    cmd = cmd + "-o " + os.getcwd() + "/contigs/ 1> megahit_log 2>&1"
    print(cmd)
    subprocess.call(cmd, shell=True, env=new_env)
    print("Generate contigs finish")

