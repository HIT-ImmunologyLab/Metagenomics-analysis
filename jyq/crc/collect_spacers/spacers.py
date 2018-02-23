#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/24 12:05
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : collectSpacer.py
# @Software: PyCharm

import sys
import subprocess
import xml.etree.cElementTree as ET
from multiprocessing import Pool
from multiprocessing import Queue,Process
import re


"""
参数定义：
参数1：输出文件名  tsv
参数2：repeat seq file  fa/fq
参数3：reads file  fa/fq
"""

outputFileName=sys.argv[1]
repeatFileName=sys.argv[2]
readFileName=sys.argv[3]

IdToName=dict()
read_id_to_seq=dict()

def changeID(fileName):
    with open(fileName) as f:
        linesFilter=[]
        lines=f.readlines()
        index = 0
        for i in range(0,len(lines),2):
            if(len(lines[i+1])>=70):
                linesFilter.append('>'+str(index)+'\n')
                read_id_to_seq[str(index)] = lines[i + 1][:-1]
                IdToName[str(index)]=lines[i][1:-1]
                index+=1
                linesFilter.append(lines[i+1])

        with open(fileName+"_changed_ID",'w') as fNew:
                fNew.writelines(linesFilter)


if(readFileName[-2:]=="fq"):
    cmd = "/home/qiusuo/amos-3.1.0-rc1/bin/fastq_to_fasta_fast "+readFileName+" >"+readFileName[:-2]+"fa"
    print(cmd)
    subprocess.call(cmd, shell=True)

changeID(readFileName[:-2]+"fa")
cmd = "makeblastdb -in " + readFileName[:-2]+"fa" + "_changed_ID"+" -dbtype nucl -input_type fasta -out " + readFileName[:-2]+"fa" + "_changed_ID" + " -hash_index"
print(cmd)
subprocess.call(cmd, shell=True)


cmd = "blastn -db " + readFileName[:-2]+"fa" + "_changed_ID" + " -num_threads 40 -evalue 1 -gapopen 10 -penalty -1 -gapextend 2 -word_size 7 -dust no -task blastn-short  -outfmt 5 >" + repeatFileName + ".xml 2>err -query " + repeatFileName
print(cmd)
subprocess.call(cmd,shell=True)


header=["read ID","repeat ID1","repeat ID2"," hit 1 location"," hit 2 location"," spacer lengh"," spacer sequence"]
map_hits = dict()
    # text = open(readFileName[:-2] + "fa" + str(i).zfill(2) + ".fa" + ".xml").read()
    # text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u" ", text)
    # root = ET.fromstring(text)
root = ET.parse(repeatFileName + ".xml")

    # BlastOutput_iterations = root.find('BlastOutput_iterations')
    # collection=[]
    # nodes = []
spacers=[]

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

        Hsp = Hit.find('Hit_hsps').find('Hsp')


        if (Hit_def not in map_hits.keys()):
            map_hits[Hit_def] = ([], [])
        # Hsp_evalue = Hsp.find('Hsp_evalue').text
        # identity = str(float(Hsp.find('Hsp_identity').text) / float(Hsp.find('Hsp_align-len').text))
        # coverage = str(float(Hsp.find('Hsp_align-len').text) / float(Iteration_query_len))

        Hsp_hit_from = float(Hsp.find('Hsp_hit-from').text)
        Hsp_hit_to = float(Hsp.find('Hsp_hit-to').text)

        if(Hsp_hit_from<Hsp_hit_to):
            if (Hsp_hit_from == 1 and float(Hsp.find('Hsp_identity').text) > 6):
                map_hits[Hit_def][0].append(
                        [IdToName[Hit_def], Iteration_query,'', (str(Hsp_hit_from), str(Hsp_hit_to)), ("", ""), "",
                         read_id_to_seq[Hit_def], float(Iteration_query_len)])

            if (Hsp_hit_to == float(Hit_len) and float(Hsp.find('Hsp_identity').text) > 6):
                map_hits[Hit_def][1].append(
                    [IdToName[Hit_def], '',Iteration_query, ("", ""), (str(Hsp_hit_from), str(Hsp_hit_to)), "", "",
                     float(Iteration_query_len)])
        else:
            if (Hsp_hit_to == 1 and float(Hsp.find('Hsp_identity').text) > 6):
                map_hits[Hit_def][0].append(
                        [IdToName[Hit_def],Iteration_query, '',(str(Hsp_hit_to), str(Hsp_hit_from)), ("", ""), "",
                         read_id_to_seq[Hit_def], float(Iteration_query_len)])
            if (Hsp_hit_from == float(Hit_len) and float(Hsp.find('Hsp_identity').text) > 6):
                map_hits[Hit_def][1].append(
                        [IdToName[Hit_def],'',Iteration_query, ("", ""), (str(Hsp_hit_to), str(Hsp_hit_from)), "", "",
                         float(Iteration_query_len)])

# print(len(map_hits))
for key in map_hits.keys():
    for start in map_hits[key][0]:
        for end in map_hits[key][1]:
                # print("in 1")
            if(start[-1]+end[-1]>30 and float(end[4][0])-float(start[3][1])>20):
                    # print("in 2")
                t=start[:-1]
                t[2]=end[2]
                t[3]=str(int(float(start[3][0])))+"--"+str(int(float(start[3][1])))
                t[4]=str(int(float(end[4][0])))+"--"+str(int(float(end[4][1])))
                t[5]=str(int(float(end[4][0])-float(start[3][1])))
                t[6]=t[6][int(float(start[3][1])):int(float(end[4][0]))]
                spacers.append('\t'.join(t)+'\n')

with open(outputFileName,'w') as outFile:
    outFile.write('\t'.join(header)+'\n')
    outFile.writelines(spacers)
