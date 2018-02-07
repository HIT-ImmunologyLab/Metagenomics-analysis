#!/usr/bin/env python
# coding=utf-8
import sklearn #python机器学习相关的库，里面内置了ANN分类器
import os
from sklearn.neural_network import MLPClassifier #MLPClassifier即为sklearn库中的ANN分类器
import matplotlib.pyplot as plt
import subprocess

RATE = 1.0 #0.9代表十折交叉验证，即训练集占总数据集的90%

Amino_Table = ['G','A','V','L','I','F','P','W','S','Y','C','M','D','N','Q','E','T','K','R','H'] #这个是氨基酸表，一会儿计算氨基酸频率是要用到的

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

def ConvertXlsToGIFIle(XlsFilename='Dataset_S5.xls'):
    data = xlrd.open_workbook(XlsFilename) # 打开xls文件
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
    
def convertGItoSeq(posGIFilename="posSetGI.txt",negGIFilename="negSetGI.txt"):
    data = open(posGIFilename,'r')
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
    data2 = open(negGIFilename,'r')
    table2 = data2.readlines() 
    f2 = open("negSet.txt",'w')
    for s in table2: 
        que = getEntry(s)
        if que == "ERROR":
            continue
        f2.write(que+'\n')
    f2.close()
    data2.close()
'''
函数名称：getVec()
传入参数：字符串s。s为一个蛋白质序列（大写字母组成的字符串）
返回值：该函数的返回值为蛋白质序列s中的20种氨基酸的频率，即返回一个20维的向量，向量每一维度代表的氨基酸与Amino_Table中的氨基酸顺序相同
'''
def getVec(s): 
    dic = {}
    for i in s:
        if i in dic: #统计每一种氨基酸的出现次数
            dic[i] += 1.0
        else:
            dic[i] = 1.0
    V=[]
    for Am in Amino_Table:
        if Am not in dic:
            V.append(0.0)
        else:
            V.append(dic[Am]/float(len(s)))
    return V
'''
下面就是数据读入和处理的部分
'''
#------------data processing--------------
def data_processing(posSetFilename="posSet.txt",negSetFilename="negSet.txt"):  #'posSet.txt'    'negSet.txt'
    Vec = [] #存放训练集
    Y = []  #存放训练集的标签
    posTestset = [] #存放阳性测试集
    negTestset = [] #存放阴性测试集
    f1 = open(posSetFilename,'r') #posSet.txt中存储了训练所需的阳性数据集，posSet.txt中每一行都是一个蛋白质序列（即大写英文字母组成的字符串）
    posSet = f1.readlines()
    f1.close()
    num = 0
    for s in posSet: #遍历阳性数据集，将这些蛋白质序列转化为向量并且存起来，而且将测试集和训练集分开存储
        num+=1
        if num<=len(posSet)*RATE:
            Vec.append(getVec(s))
            Y.append(1.0) #阳性的标签为1
        else:
            posTestset.append(getVec(s))

    f2 = open(negSetFilename,'r') #这个是阴性数据集，和上面的阳性数据集的处理方法是一样的
    negSet = f2.readlines()
    f2.close()
    num = 0
    for s in negSet:
        num+=1
        if num<=len(negSet)*RATE:
            Vec.append(getVec(s))
            Y.append(0.0) #阴性的标签为0
        else:
            negTestset.append(getVec(s))
    return Vec,Y,posTestset,negTestset
'''
下面是分类的核心部分。
MLPClassifier为sklearn库中内建的ANN分类器。具体参数的作用可以参考下面网址中的说明。
http://scikit-learn.org/dev/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier
http://scikit-learn.org/dev/modules/neural_networks_supervised.html#neural-networks-supervised
每个参数可以在使用时根据具体情况适当调整
'''
#---------------classify-----------------
def classify(Vec,Y):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(50, 15), random_state=1)
    clf.fit(Vec,Y)
    return clf
#--------------predict-------------------
def predict(clf,predictsetFilename='predictset.txt'):   #'predictset.txt'
    f3 = open(predictsetFilename,'r')
    f4 = open('predictresult.txt','w')
    predictset = f3.readlines()
    f3.close()
    tot = 0
    for s in predictset:
        #print(clf.predict_proba([getVec(s)]))
        tot += 1
        f4.write('gene_'+str(tot)+':\n')
        f4.write('    Non-structural:'+str(clf.predict_proba([getVec(s)])[0][0]))
        f4.write('\n    Structural:'+str(clf.predict_proba([getVec(s)])[0][1]))
        f4.write('\n')
    f4.close()
#---------------Testing------------------
def testing(posPre,negPre):
    xx = []  #存储FPR值
    yy = []  #存储TPR值
    for d in range(0,101):
        T = float(d)*0.01
        TP = 0
        FN = 0
        TN = 0
        FP = 0
        R = 0
        W = 0
        for v in posPre:
            if v>T:
                TP+=1
                R+=1
            else:
                FN+=1
                W+=1
        for v in negPre:
            if v<=T:
                TN+=1
                R+=1
            else:
                FP+=1
                W+=1
        if T == 0.5:
            zi = float(TP*TN-FP*FN)
            shit = float((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
            mu = math.sqrt(shit)    
            MCC = float(zi)/float(mu)
            ACC = float(R)/float(R+W)
        FPR = float(FP)/float(FP+TN)
        TPR = float(TP)/float(TP+FN)
        xx.append(FPR)
        yy.append(TPR)
        return xx,yy,ACC,MCC
        
def get_k_fold_Cross_Validation_classifier(X,Y,k):
    len_X = len(X)
    clfs = []
    testset = []
    for i in range(k):
        p = k-i     #[(p-1)*len/k,p*len/k)
        x = []
        y = []
        testx = []
        testy = []
        for num in range(len_X):
            if (num>=(p-1)*len_X/k) and (num<p*len_X/k):
                testx.append(X[num])
                testy.append(Y[num])
                continue
            x.append(X[num])
            y.append(Y[num])
        testset.append((testx,testy))
        clfs.append(classify(x,y))
    return clfs,testset    

def calcACC(clf,testx,testy):
    Pre = clf.predict(testx)
    R = 0
    for i in range(len(Pre)): 
        if Pre[i] == testy[i]:
            R += 1
    return (float(R)/float(len(testx))) 

def calcFPR_TPR(clf,testx,testy):
    xx = []  #存储FPR值
    yy = []  #存储TPR值
    Pre = clf.predict_proba(testx)
    len_x = len(testx)
    for d in range(0,101):
        T = float(d)*0.01
        TP = 0
        FN = 0
        TN = 0
        FP = 0
        R = 0
        W = 0
        for i in range(len_x):
            v = Pre[i][1]
            if testy[i] > 0.5:
                if v>T:
                    TP+=1
                    R+=1
                else:
                    FN+=1
                    W+=1
            else:
                if v<=T:
                    TN+=1
                    R+=1
                else:
                    FP+=1
                    W+=1
        if T == 0.5:
            zi = float(TP*TN-FP*FN)
            sss = float((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
            mu = math.sqrt(sss)    
            MCC = float(zi)/float(mu)
            ACC = float(R)/float(R+W)
        FPR = float(FP)/float(FP+TN)
        TPR = float(TP)/float(TP+FN)
        xx.append(FPR)
        yy.append(TPR)
        return xx,yy,ACC,MCC,TP,FP,TN,PN

def k_fold_Cross_Validation_classifier(X,Y,k):
    ACC = 0.0
    clfs,testsets=get_k_fold_Cross_Validation_classifier(X,Y,k)
    for i in range(len(clfs)):
        testx,testy = testsets[i]
        ACC += calcACC(clfs[i],testx,testy)
    ACC /= 10
    return ACC
