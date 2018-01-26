# -*- coding: utf-8 -*-
import subprocess
import time
import os
import sys

thread=int(sys.argv[1])
rootdir = os.getcwd()
new_env = os.environ.copy()
new_env['MRKDUP'] = '/home/qiusuo/picard-tools-1.77/MarkDuplicates.jar'
new_env['mpa_dir'] = '/zrom/Fan/metaphlan2'
new_env['PATH']="/zrom/Fan/metaphlan2:/zrom/Fan/pathoscope2/pathoscope:/home/qiusuo/bin:/home/qiusuo/.local/bin:/home/admin01/cdhit:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/media/blast+/bin:/zrom/z-tools/bin:/snap/bin:/home/qiusuo/CONCOCT-master/scripts:/home/qiusuo/bowtie2-2.3.3:/home/qiusuo/CONCOCT-master:/home/qiusuo/CONCOCT-master/scripts:/home/qiusuo/bowtie2-2.3.3:/home/qiusuo/CONCOCT-master:/home/qiusuo/samtools-1.5:/home/qiusuo/bedtools2/bin"

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
    rootdir="/zrom/DownloadGutData/CRCDataSide/case/selected"
    source_1=[]
    source_2=[]
    source_1_abs=[]
    source_2_abs=[]
    for parent,dirnames,filenames in os.walk(rootdir):    
        for filename in filenames:
            if(filename[-4:]=="1.fq"):   
                source_1.append(filename)
                source_1_abs.append(os.path.join(parent,filename))
            if(filename[-4:]=="2.fq"):   
                source_2.append(filename)
                source_2_abs.append(os.path.join(parent,filename))
#    print(len(source_1),len(source_2))
    thread=min(thread,len(source_1))

    table=[]
    i=0
    for i in range(thread):
#       print(source_1[i])
        sample_name='.'.join(source_1[i].split('.')[:3])
        cmd="bowtie2 --sam-no-hd --sam-no-sq --no-unal --very-sensitive -x /zrom/Fan/metaphlan2/db_v20/mpa_v20_m200 -1 "+source_1_abs[i]+" -2 "+source_2_abs[i]+" >align/"+sample_name+"_metaphlan2.sam 2>align/"+sample_name+".metaphlan2.Bowtie.log"
#       print(sample_name) 
        print(cmd)
        table.append(subprocess.Popen(cmd,shell=True,env=new_env))
    if(i<len(source_1)-1):
        i=thread    
        while True:
            time.sleep(1)
            finished=check_and_delete(table)
            for j in range(i,min(i+finished,len(source_1))):
                sample_name='.'.join(source_1[j].split('.')[:3])
                cmd="bowtie2 --sam-no-hd --sam-no-sq --no-unal --very-sensitive -x /zrom/Fan/metaphlan2/db_v20/mpa_v20_m200 -1 "+source_1_abs[i]+" -2 "+source_2_abs[i]+" >align/"+sample_name+"_metaphlan2.sam 2>align/"+sample_name+".metaphlan2.Bowtie.log"
                print(cmd)
                table.append(subprocess.Popen(cmd,shell=True,env=new_env))
            i=min(i+finished,len(source_1))
            if(i==len(source_1)):
                for x in table:
                    x.wait()
                
                break
    else:
        for i in range(len(source_1)):
            table[i].wait()
                

 
    table=[]
    i=0
    for i in range(thread):
#       print(source_1[i])
        sample_name='.'.join(source_1[i].split('.')[:3])
        # cmd="pathoscope2.py MAP -1 "+source_1[i]+" -2 "+source_2[i]+" -targetRefFiles CRC_non_redundant_gene_set.fa  -outDir pathoscope -outAlign "+sample_name+".sam -expTag "+sample_name
#       print(sample_name) 
#       c
        cmd="metaphlan2.py -t rel_ab --tax_lev s align/"+sample_name+"_metaphlan2.sam --input_type sam > align_marker_abundance_table/case_"+sample_name+"_metaphlan2_abundance.txt"
        print(cmd)
        table.append(subprocess.Popen(cmd,shell=True,env=new_env))
    if(i<len(source_1)-1):
        i=thread    
        while True:
            time.sleep(1)
            finished=check_and_delete(table)
            for j in range(i,min(i+finished,len(source_1))):
                sample_name='.'.join(source_1[j].split('.')[:3])
                cmd="metaphlan2.py -t rel_ab --tax_lev s align/"+sample_name+"_metaphlan2.sam --input_type sam > align_marker_abundance_table/case_"+sample_name+"_metaphlan2_abundance.txt"
                # cmd="pathoscope2.py MAP -1 "+source_1[j]+" -2 "+source_2[j]+" -targetRefFiles CRC_non_redundant_gene_set.fa  -outDir pathoscope -outAlign "+sample_name+".sam -expTag "+sample_name
                print(cmd)
                table.append(subprocess.Popen(cmd,shell=True,env=new_env))
            i=min(i+finished,len(source_1))
            if(i==len(source_1)):
                for x in table:
                    x.wait()
                
                break
    else:
        for i in range(len(source_1)):
            table[i].wait()    


    
    i=0
    cmd="python /zrom/Fan/metaphlan2/utils/merge_metaphlan_tables.py "
    for i in range(len(source_1)):
        sample_name='.'.join(source_1[i].split('.')[:3])
        cmd+=" align_marker_abundance_table/case_"+sample_name+"_metaphlan2_abundance.txt"
    cmd+= "> align_marker_abundance_table/case_merged_metaphlan2_rel_ab_abundance_table.txt"
    subprocess.call(cmd,shell=True,env=new_env)




