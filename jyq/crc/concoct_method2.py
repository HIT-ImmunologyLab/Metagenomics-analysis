# -*- coding: utf-8 -*-
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
    cmd="cd contigs && bowtie2-build -f *fasta final.contigs.cut.500bp.95%.identity.fa && cd .."
    print(cmd)
    subprocess.call(cmd,shell=True,env=new_env)
    print("Bowtie2-build finish")



    rootdir=os.getcwd()
    source_1=[]
    source_2=[]
    for parent,dirnames,filenames in os.walk(rootdir):    
        for filename in filenames:
            if(filename[-7:]=="1.fasta"):   
                source_1.append(filename)
            if(filename[-7:]=="2.fasta"):   
                source_2.append(filename)
#    print(len(source_1),len(source_2))
    thread=min(thread,len(source_1))
    table=[]
    i=0
    for i in range(thread):
#       print(source_1[i])
        sample_name='.'.join(source_1[i].split('.')[:3])
#       print(sample_name) 
        cmd="bowtie2 --no-mixed -f --fr -x contigs/final.contigs.cut.500bp.95%.identity.fa -1  "+"samples/"+sample_name+'/'+ source_1[i]+" -2 "+"samples/"+sample_name+'/'+source_2[i]+" -S "+sample_name+"_pair.sam -p 1 && "+ "samtools view -b -S "+"samples/"+sample_name+'/'+sample_name+"_pair.sam -o "+"samples/"+sample_name+'/'+sample_name+"_pair.bam && "+"samtools sort -T "+"samples/"+sample_name+'/'+ " -o "+"samples/"+sample_name+'/'+sample_name+"_pair-smds.bam  "+"samples/"+sample_name+'/'+sample_name+"_pair.bam && "+"samtools index "+"samples/"+sample_name+'/'+ " -o "+"samples/"+sample_name+'/'+sample_name+"_pair-smds.bam && "+ "rm *_pair.sam && rm *_pair.bam "
        print(cmd)
        table.append(subprocess.Popen(cmd,shell=True,env=new_env))
    if(i<len(source_1)-1):
        i=thread    
        while True:
            time.sleep(1)
            finished=check_and_delete(table)
            for j in range(i,min(i+finished,len(source_1))):
                sample_name='.'.join(source_1[j].split('.')[:3])
                cmd="bowtie2 --no-mixed -f --fr -x contigs/final.contigs.cut.500bp.95%.identity.fa -1  "+"samples/"+sample_name+'/'+ source_1[j]+" -2 "+"samples/"+sample_name+'/'+source_2[j]+" -S "+sample_name+"_pair.sam -p 1 && "+"samtools view -b -S "+"samples/"+sample_name+'/'+sample_name+"_pair.sam -o "+"samples/"+sample_name+'/'+sample_name+"_pair.bam && "+ "samtools sort -T "+"samples/"+sample_name+'/'+ " -o "+"samples/"+sample_name+'/'+sample_name+"_pair-smds.bam  "+"samples/"+sample_name+'/'+sample_name+"_pair.bam && "+"samtools index "+"samples/"+sample_name+'/'+ " -o "+"samples/"+sample_name+'/'+sample_name+"_pair-smds.bam && " + "rm *_pair.sam && rm *_pair.bam "
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


#     table=[]
#     i=0
#     for i in range(thread):
# #       print(source_1[i])
#         sample_name='.'.join(source_1[i].split('.')[:3])
# #       print(sample_name) 
#         cmd="samtools view -b -S "+"samples/"+sample_name+'/'+sample_name+"_pair.sam -o "+"samples/"+sample_name+'/'+sample_name+"_pair.bam"
#         print(cmd)
#         table.append(subprocess.Popen(cmd,shell=True,env=new_env))
#     if(i<len(source_1)-1):
#         i=thread    
#         while True:
#             time.sleep(1)
#             finished=check_and_delete(table)
#             for j in range(i,min(i+finished,len(source_1))):
#                 sample_name='.'.join(source_1[j].split('.')[:3])
#                 cmd="samtools view -b -S "+"samples/"+sample_name+'/'+sample_name+"_pair.sam -o "+"samples/"+sample_name+'/'+sample_name+"_pair.bam"
#                 print(cmd)
#                 table.append(subprocess.Popen(cmd,shell=True,env=new_env))
#             i=min(i+finished,len(source_1))
#             if(i==len(source_1)):
#                 for x in table:
#                     x.wait()
#                 break
#     else:
#         for i in range(len(source_1)):
#             table[i].wait()


#     table=[]
#     i=0
#     for i in range(thread):
# #       print(source_1[i])
#         sample_name='.'.join(source_1[i].split('.')[:3])
# #       print(sample_name) 
#         cmd="samtools sort -T "+"samples/"+sample_name+'/'+ " -o "+"samples/"+sample_name+'/'+sample_name+"_pair-smds.bam  "+"samples/"+sample_name+'/'+sample_name+"_pair.bam"
#         print(cmd)
#         table.append(subprocess.Popen(cmd,shell=True,env=new_env))
#     if(i<len(source_1)-1):
#         i=thread    
#         while True:
#             time.sleep(1)
#             finished=check_and_delete(table)
#             for j in range(i,min(i+finished,len(source_1))):
#                 sample_name='.'.join(source_1[j].split('.')[:3])
#                 cmd="samtools sort -T "+"samples/"+sample_name+'/'+ " -o "+"samples/"+sample_name+'/'+sample_name+"_pair-smds.bam  "+"samples/"+sample_name+'/'+sample_name+"_pair.bam"
#                 print(cmd)
#                 table.append(subprocess.Popen(cmd,shell=True,env=new_env))
#             i=min(i+finished,len(source_1))
#             if(i==len(source_1)):
#                 for x in table:
#                     x.wait()
#                 print("Map-bowtie2 finish")
#                 break
#     else:
#         for i in range(len(source_1)):
#             table[i].wait()
#             print("Map-bowtie2 finish")


#      table=[]
#     i=0
#     for i in range(thread):
# #       print(source_1[i])
#         sample_name='.'.join(source_1[i].split('.')[:3])
# #       print(sample_name) 
#         cmd="samtools index "+"samples/"+sample_name+'/'+ " -o "+"samples/"+sample_name+'/'+sample_name+"_pair-smds.bam"
#         print(cmd)
#         table.append(subprocess.Popen(cmd,shell=True,env=new_env))
#     if(i<len(source_1)-1):
#         i=thread    
#         while True:
#             time.sleep(1)
#             finished=check_and_delete(table)
#             for j in range(i,min(i+finished,len(source_1))):
#                 sample_name='.'.join(source_1[j].split('.')[:3])
#                 cmd="samtools index "+"samples/"+sample_name+'/'+ " -o "+"samples/"+sample_name+'/'+sample_name+"_pair-smds.bam"
#                 print(cmd)
#                 table.append(subprocess.Popen(cmd,shell=True,env=new_env))
#             i=min(i+finished,len(source_1))
#             if(i==len(source_1)):
#                 for x in table:
#                     x.wait()
#                 print("Map-bowtie2 finish")
#                 break
#     else:
#         for i in range(len(source_1)):
#             table[i].wait()
#             print("Map-bowtie2 finish")





    talbe=[]
    cmd="rm -rf input && mkdir input && python /home/qiusuo/CONCOCT-master/scripts/gen_input_table.py contigs/final.contigs.cut.500bp.95%.identity.fa "
    for i in range(len(source_1)):
        sample_name='.'.join(source_1[i].split('.')[:3])
        cmd=cmd+"samples/"+sample_name+"/"+sample_name+"pair-smds.bam "
    cmd=cmd+"> input/cov_inputtableR.tsv"
    print(cmd)
    gen_input_table=subprocess.call(cmd,shell=True,env=new_env)

