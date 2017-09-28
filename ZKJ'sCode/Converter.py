#!/usr/bin/env python
# coding=utf-8
import xlrd #读取xls文件用的
'''
函数名称：getGI
传入参数：字符串s。s是表格文件中的一行信息。
返回值：一个字符串，代表从s中提取到的GI信息
'''
def getGI(s): 
    p1 = s.find('gi')+3
    if p1<3:
        p1 = s.find('GI')+3
    for i in range(p1,len(s)):
        if s[i] == '|':
            p2 = i
            break
    return s[p1:p2]

data = xlrd.open_workbook('Dataset_S5.xls') # 打开xls文件
table1 = data.sheets()[0] # 打开第一张表
nrows = table1.nrows # 获取表的行数
f1 = open("posSetGI.txt",'w')  #这个是用来保存阳性蛋白质的序列GI信息的
for i in range(nrows):   #遍历每一行并提取信息
    try:
        f1.write(getGI(table1.row_values(i)[0])+'\n')  #将提取到的GI信息保存至文件中
    except:
        print(table1.row_values(i)[0])
f1.close()
table2 = data.sheets()[1] # 打开第二张表
nrows = table2.nrows # 获取表的行数
f2 = open("negSetGI.txt",'w') #这个是用来保存阴性蛋白质的序列GI信息的
for i in range(nrows):  #与上面的操作相同
    f2.write(getGI(table2.row_values(i)[0])+'\n')
f2.close()


