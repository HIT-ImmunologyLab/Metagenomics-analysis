#!/usr/bin/env python
# coding=utf-8
import sklearn #python机器学习相关的库，里面内置了ANN分类器
import os
from sklearn.neural_network import MLPClassifier #MLPClassifier即为sklearn库中的ANN分类器
import matplotlib.pyplot as plt   #matplotlib是用来化ROC曲线的

RATE = 0.9 #0.9代表十折交叉验证，即训练集占总数据集的90%

Amino_Table = ['G','A','V','L','I','F','P','W','S','Y','C','M','D','N','Q','E','T','K','R','H'] #这个是氨基酸表，一会儿计算氨基酸频率是要用到的

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
Vec = [] #存放训练集
Y = []  #存放训练集的标签
posTestset = [] #存放阳性测试集
negTestset = [] #存放阴性测试集
f1 = open('posSet.txt','r') #posSet.txt中存储了训练所需的阳性数据集，posSet.txt中每一行都是一个蛋白质序列（即大写英文字母组成的字符串）
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

f2 = open('negSet.txt','r') #这个是阴性数据集，和上面的阳性数据集的处理方法是一样的
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
'''
下面是分类的核心部分。
MLPClassifier为sklearn库中内建的ANN分类器。具体参数的作用可以参考下面网址中的说明。
http://scikit-learn.org/dev/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier
http://scikit-learn.org/dev/modules/neural_networks_supervised.html#neural-networks-supervised
每个参数可以在使用时根据具体情况适当调整
'''
#---------------classify-----------------
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(50, 15), random_state=1)
clf.fit(Vec,Y)
'''
下面利用已经训练好的ANN跑测试集，评估算法的优劣性并绘制出ROC曲线图
'''
#---------------Testing------------------
posPre = clf.predict_proba(posTestset) #利用内建的predict_proba对阳性测试集中的每个向量进行预测
negPre = clf.predict_proba(negTestset) #利用内建的predict_proba对阴性测试集中的每个向量进行预测
print(posPre) #输出预测结果
print(negPre)
l = []
xx = []  #存储FPR值
yy = []  #存储TPR值
for d in range(0,101): #TP、FN、TN、FP、FPR、TPR每个变量的意义和它的名字是一致的，用来绘制ROC图像
    T = float(d)*0.01 #T代表当前的分类阈值，我们把每个预测值大于T的都认为是阳性，反之是阴性
    print(T)
    TP = 0
    FN = 0
    TN = 0
    FP = 0
    R = 0
    W = 0
    for v in posPre: #根据TP、FN、TN、FP的定义计算它们的值
        if v[1]>T:  #真阳性 
            TP+=1
            R+=1
        else:  
            FN+=1   #假阴性
            W+=1
    for v in negPre:
        if v[1]<=T:  
            TN+=1   #真阴性
            R+=1
        else:
            FP+=1   #假阳性
            W+=1
    FPR = float(FP)/float(FP+TN)   #计算FPR和TPR
    TPR = float(TP)/float(TP+FN)
    xx.append(FPR) 
    yy.append(TPR)
    l.append([FPR,TPR]) #将FPR和对应的TPR存储起来
plt.plot(xx,yy) #利用上面的计算结果绘制ROC曲线
plt.legend()
plt.show()
#print(xx)
#print(yy)
#print("正确率："+str(float(R)/float(R+W)*100.0)+"%")

