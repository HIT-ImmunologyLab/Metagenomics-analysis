#coding:utf-8
import os
import subprocess

LOCAL = 1 #LOCAL代表目前程序的运行状态，为1时代表程序在本地调试，为0代表程序在服务器中运行

'''
函数名称：getGI
传入参数：字符串s。s是表格文件中的一行信息。
返回值：一个字符串，代表从s中提取到的GI信息
'''
def getGI(s):
    p1 = s.find('GI')+3
    if p1<3:
        p1 = s.find('gi')+3
    for i in range(p1,len(s)):
        if s[i] == '|':
            p2 = i
            break
    return s[p1:p2]
'''
函数名称：getEntry
传入参数：字符串gi。gi代表某蛋白质序列的gi编号
返回值：一个字符串，为gi编号对应的蛋白质序列。
注意，该函数只有在存放有blast数据库的环境中运行才可以，否则会报错
'''
def getEntry(gi):
    p = subprocess.Popen("blastdbcmd -entry "+gi, shell=True, stdout=subprocess.PIPE) #新建一个进程，利用blastdbcmd指令查询gi编号
    out = p.stdout.readlines()  #out即为数据库查询的返回结果
    if len(out)==0:  #查询失败
        return "ERROR"
    que = ""
    for s in out: #将out中所有行全部拼接在一起
        que+=s[:-1]
    l = len(que)
    pos = 0
    for i in range(len(que)-2,-1,-1):
        if que[i].isupper():
            pos = i
        else:
            break 
    if abs(pos-(len(que)-2))<=2:  #查询失败
        return "ERROR"
    #print(pos)
    return que[int(pos):]

if LOCAL: #打开存有阳性蛋白质GI数据的文件并读取
    data = open("posSetGI.txt",'r')
else:
    data = open("/zrom/zkj/posSetGI.txt",'r')
table1 = data.readlines() 
f1 = open("posSet.txt",'w')
for s in table1: 
    que = getEntry(s) #搜索条目
    if que == "ERROR":
        continue
    f1.write(que+'\n') #将搜索到的蛋白质序列信息存入文件中
f1.close()
data.close()
#与上面的操作类似
if LOCAL:
    data2 = open("negSetGI.txt",'r')
else:
    data2 = open("/zrom/zkj/negSetGI.txt",'r')
table2 = data2.readlines() 
f2 = open("negSet.txt",'w')
for s in table2: 
    que = getEntry(s)
    if que == "ERROR":
        continue
    f2.write(que+'\n')
f2.close()
data2.close()
