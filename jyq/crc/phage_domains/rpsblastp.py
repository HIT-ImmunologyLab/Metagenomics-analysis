#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/29 20:54
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : rpsblastp.py
# @Software: PyCharm

import subprocess
import time
import sys
import xml.etree.ElementTree as ET
import re
import os


thread=40

def check_and_delete(table):
    finished=0
    cpy_table=table
    for x in table:
        if(x.poll()==0):
            finished=finished+1
            cpy_table.remove(x)
    table=cpy_table
    return finished

def filter_condition(end,start,Hit_len):
    if((end==Hit_len or start==1) and end-start>=1000):
        return True
    return False


if __name__=="__main__":

    source = []
    with open('/zrom/jobs/list/phagelist') as f:
        lines = f.readlines()
        for line in lines:

            filePath = '/zrom/jobs/viral/' + line[:-1] + '/' + line[:-1] + '.faa'
            if (os.path.exists(filePath)):
                source.append(line)

    # filePath='/zrom/jobs/viral/'+s+'/'+s+'.faa'
    # cmd = "/home/qiusuo/miniconda2/pkgs/blast-2.2.31-1/bin/rpsblast -query "+filePath+" -comp_based_stats 0 -evalue 0.01 -seg no -outfmt 5 -num_threads 1 -db /zrom/z-tools/data/cdd/Cdd -out "+s+".xml "

    thread=min(thread,len(source))
    table=[]
    i=0
    for i in range(thread):
        s=source[i][:-1]
        filePath = '/zrom/jobs/viral/' + s + '/' + s + '.faa'
        cmd = "/home/qiusuo/miniconda2/pkgs/blast-2.2.31-1/bin/rpsblast -query " + filePath + " -comp_based_stats 0 -evalue 0.01 -seg no -outfmt 5 -num_threads 1 -db /zrom/z-tools/data/cdd/Cdd -out " + s + ".xml "
        print(cmd)
        table.append(subprocess.Popen(cmd,shell=True))
    if(i<len(source)-1):
        i=thread
        while True:
            time.sleep(1)
            finished=check_and_delete(table)
            for j in range(i,min(i+finished,len(source))):
                s = source[j][:-1]
                filePath = '/zrom/jobs/viral/' + s + '/' + s + '.faa'
                cmd = "/home/qiusuo/miniconda2/pkgs/blast-2.2.31-1/bin/rpsblast -query " + filePath + " -comp_based_stats 0 -evalue 0.01 -seg no -outfmt 5 -num_threads 1 -db /zrom/z-tools/data/cdd/Cdd -out " + s + ".xml "
                print(cmd)
                table.append(subprocess.Popen(cmd,shell=True))
            i=min(i+finished,len(source))
            if(i==len(source)):
                for x in table:
                    x.wait()
                break
    else:
        for i in range(len(source)):
            table[i].wait()

    # headers = "Contig_ID\tlen\tHit_id\tHit_def\tHit_accession\tHit_len\tHsp_evalue\tidentity\tcoverage"
    headers="RefSeq\tContigID\tdomain\tevalue"
    nodes = []

    for s in source:
        print(s[:-1] + ".xml")
        text = open(s[:-1] + ".xml").read()
        if (len(text) > 10):
            text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u" ", text)
            root = ET.fromstring(text)

            BlastOutput_iterations = root.find('BlastOutput_iterations')
            collection = []

            for Iteration in root.find('BlastOutput_iterations').findall('Iteration'):
                Iteration_hits = Iteration.find('Iteration_hits')
                Iteration_query = str(Iteration.find('Iteration_query-def').text).split(' ')[0]
                Iteration_query_len = Iteration.find('Iteration_query-len').text
                # print("in")

                for Hit in Iteration_hits.findall('Hit'):
                    # print("in")

                    Hit_id = Hit.find('Hit_id').text
                    Hit_def = Hit.find('Hit_def').text
                    Hit_len = Hit.find('Hit_len').text
                    Hit_accession = Hit.find('Hit_accession').text

                    Hsp = Hit.find('Hit_hsps').find('Hsp')

                    Hsp_evalue = Hsp.find('Hsp_evalue').text
                    identity = str(float(Hsp.find('Hsp_identity').text) / float(Hsp.find('Hsp_align-len').text))
                    coverage = str(float(Hsp.find('Hsp_align-len').text) / float(Iteration_query_len))
                    # collection = ["err", "err", "err", "err", "err", "err", "err", "err", "err"]
                    # collection[0] = Iteration_query
                    # collection[1] = Iteration_query_len
                    # collection[2] = Hit_id
                    # collection[3] = Hit_def
                    # collection[4] = Hit_accession
                    # collection[5] = Hit_len
                    # collection[6] = Hsp_evalue
                    # collection[7] = identity
                    # collection[8] = coverage
                    collection=["err", "err", "err", "err"]
                    collection[0]=s[:-1]
                    collection[1]=Iteration_query
                    collection[2]=[]
                    for item in Hit_def.split(','):
                        if(item[:4]=="pfam"):
                            collection[2].append(item)
                    collection[2]=','.join(collection[2])
                    collection[3]=Hsp_evalue
                    # start = float(Hsp.find('Hsp_hit-to').text)
                    # end = float(Hsp.find('Hsp_hit-from').text)
                    # Hit_len = float(Hsp.find('Hit_len').text)

                    nodes.append(collection)
                    # if(filter_condition(end,start,Hit_len)):
                    #     nodes.append(collection)

            # lineage = dict()
            # with open("CRC_control_table_virus.txt") as f:
            #     lines = f.readlines()
            #     for i in range(2, len(lines)):
            #         lineage[lines[i].split('\t')[0]] = lines[i].split('\t')[14:18]
    nnodes = []
    for node in nodes:
        # nnodes.append('\t'.join(node) + '\t'+'\t'.join(lineage[node[0]])+"\n")
        nnodes.append('\t'.join(node))
    # headers = "Contig_ID\tlen\tHit_id\tHit_def\tHit_len\tHsp_evalue\tidentity\tcoverage\tORDER\tFAMILY\tGENUS\tSPECIES"

    with open("phage_domains.txt", 'w') as nf:
        nf.writelines(headers + '\n')
        for node in nnodes:
            nf.writelines(node + "\n")




