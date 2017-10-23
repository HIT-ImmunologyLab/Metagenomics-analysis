# -*- coding: utf-8 -*-
import subprocess
import time
import os

thread=40
rootdir = os.getcwd()
new_env = os.environ.copy()
new_env['MRKDUP'] = '/home/qiusuo/picard-tools-1.77/MarkDuplicates.jar'
new_env['PATH']="/zrom/Fan/pathoscope2/pathoscope:/home/qiusuo/bin:/home/qiusuo/.local/bin:/home/admin01/cdhit:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/media/blast+/bin:/zrom/z-tools/bin:/snap/bin:/home/qiusuo/CONCOCT-master/scripts:/home/qiusuo/bowtie2-2.3.3:/home/qiusuo/CONCOCT-master:/home/qiusuo/CONCOCT-master/scripts:/home/qiusuo/bowtie2-2.3.3:/home/qiusuo/CONCOCT-master:/home/qiusuo/samtools-1.5:/home/qiusuo/bedtools2/bin"

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
    rootdir=os.getcwd()
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
'''
    cmd="bowtie2-build CRC_non_redundant_gene_set.fa align/CRC_non_redundant_gene_set"
    subprocess.call(cmd,shell=True,env=new_env)

    table=[]
    i=0
    for i in range(thread):
#       print(source_1[i])
        sample_name='.'.join(source_1[i].split('.')[:3])
        cmd="bowtie2 -p1 --very-sensitive-local -k 100 --score-min L,0,1.2 -x align/CRC_non_redundant_gene_set -1 "+source_1_abs[i]+" -2 "+source_2_abs[i]+" >align/" +sample_name+".sam 2>align/"+sample_name+".Bowtie.log"
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
                cmd="bowtie2 -p1 --very-sensitive-local -k 100 --score-min L,0,1.2 -x align/CRC_non_redundant_gene_set -1 "+source_1_abs[j]+" -2 "+source_2_abs[j]+" >align/" +sample_name+".sam 2>align/"+sample_name+".Bowtie.log"
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
            
'''
    table=[]
    i=0
    for i in range(thread):
#       print(source_1[i])
        sample_name='.'.join(source_1[i].split('.')[:3])
        # cmd="pathoscope2.py MAP -1 "+source_1[i]+" -2 "+source_2[i]+" -targetRefFiles CRC_non_redundant_gene_set.fa  -outDir pathoscope -outAlign "+sample_name+".sam -expTag "+sample_name
#       print(sample_name) 
#       c
        cmd="pathoscope2.py ID -alignFile align/"+sample_name+".sam -fileType sam -outDir pathoscope -expTag "+sample_name
        print(cmd)
        table.append(subprocess.Popen(cmd,shell=True,env=new_env))
    if(i<len(source_1)-1):
        i=thread    
        while True:
            time.sleep(1)
            finished=check_and_delete(table)
            for j in range(i,min(i+finished,len(source_1))):
                sample_name='.'.join(source_1[j].split('.')[:3])
                cmd="pathoscope2.py ID -alignFile align/"+sample_name+".sam -fileType sam -outDir pathoscope -expTag "+sample_name
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
    
    table=[]
    i=0
    for i in range(thread):
#       print(source_1[i])
        sample_name='.'.join(source_1[i].split('.')[:3])
        cmd="pathoscope2.py  REP -samfile align/updated_"+sample_name+".sam -outDir pathoscope"
        # cmd="pathoscope2.py MAP -1 "+source_1[i]+" -2 "+source_2[i]+" -targetRefFiles CRC_non_redundant_gene_set.fa  -outDir pathoscope -outAlign "+sample_name+".sam -expTag "+sample_name
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
                cmd="pathoscope2.py  REP -samfile align/updated_"+sample_name+".sam -outDir pathoscope"

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
            
