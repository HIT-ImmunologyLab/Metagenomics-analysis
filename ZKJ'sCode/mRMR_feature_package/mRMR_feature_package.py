# coding=utf-8
import csv
import os     
import matplotlib.pyplot as plt
import subprocess
import select  
import time  
import signal 
import random
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA   #做PCA，用来画图
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import math

def csv_converter(csvfilename='orf_on_samples_filter_p_0.01（大于60%）.csv',outputfilename='dataset.txt'):
    #csv_reader = csv.reader(open('orf_on_samples_filter_p_0.01（大于60%）.csv', encoding='utf-8'))
    csv_reader = csv.reader(open(csvfilename))
    fout = open(outputfilename,'w')
    tot = 0
    for row in csv_reader:
        tot+=1
        if tot == 1:
            f2 = open('featureDict.txt','w')
            header = row
            tot = 0
            for name in header:
                tot += 1
                if tot < 3:
                    continue
                f2.write(str(tot-2)+' '+str(name)+'\n')
            f2.close()
            continue
        tot2 = 0
        for cor in row:
            tot2 += 1
            if tot2 == 1:
                continue
            if 'control' in cor:
                fout.write('1')
                continue
            if 'case' in cor:
                fout.write('0')
                continue
            fout.write(','+cor)
        fout.write('\n')
    fout.close()

def mRMR(datasetFilename='dataset.txt',FEAS = 180):
    f = open(datasetFilename,'r')  #打开数据集文件
    dataset = f.readlines()
    f.close()
    vecs = []
    features = []
    for line in dataset:
        vecs.append(line.split(','))
    fout = open('mRMRtrainingset.txt','w') 
    fout.write('label')
    for i in range(len(vecs[0])-1):
        fout.write(',f'+str(i))
    fout.write('\n')
    for vec in vecs:
        for i in range(len(vec)):
            fout.write(str(float(vec[i])))
            if i!=(len(vec)-1):
                fout.write(',')
        fout.write('\n')
    fout.close()
    p = subprocess.Popen("pwd", shell=True, stdout=subprocess.PIPE) #获取程序路径
    path = p.stdout.readlines()[0][0:-1]
    mrmr = subprocess.Popen('./mrmr -i '+path+'/mRMRtrainingset.txt -v 20000 -n '+str(FEAS),stdout=subprocess.PIPE,shell = True)  #子进程调用mrmr算法
    while 1:  #等待子进程运行结束
        if mrmr.poll() is not None: 
            break   
    mRMRoutputs = mrmr.stdout.readlines()
    print('mRMRoutputs:'+str(len(mRMRoutputs)))
    #mRMRfile.close()
    finded = 0
    for line in mRMRoutputs:  #根据mrmr算法的输出来获取满足条件的特征集
        if finded == 2:
            features.append(int(line.split('\t')[1]))  #将符合条件的特征加入特征集中
            if len(line.split('\t')) < 3:
                print('ERROR')
        if len(features) == FEAS:
            break
        if '*** mRMR features ***' in line:
            finded = 1
        if (finded == 1) and ('Fea' in line):
            finded = 2
    return features
    #print(features)

def OutputToFiles(features):   #将结果输出至文件
    f = open('Best_Feas.txt','w')
    for fea in features:
        f.write(str(fea)+'\n')
    f.close()

def InputFromFiles(Best_FeasFilename='Best_Feas.txt'):  #从文件中读取特征集  'Best_Feas.txt'
    f = open(Best_FeasFilename,'r')
    data = f.readlines()
    features = []
    for fea in data:
        features.append(int(fea))
    f.close()
    return features

def converter(fList,vec):
    return [vec[f] for f in fList]

def mkdataset(fList,datasetFilename='dataset.txt',OutputToFile = 0,POSLABEL = 1.0):  #根据特征集fList，构建svm训练及评估所用的数据集,"dataset.txt"
    f = open(datasetFilename,'r')
    dataset = f.readlines()
    f.close()
    vecs = []
    new_posdata = []
    new_negdata = []
    for line in dataset:
        str_v = line.split(',')
        v = [float(cor) for cor in str_v]
        new_v = converter(fList,v)
        zero = 1
        for c in new_v:
            if c != 0:
                zero = 0
                break
        if zero == 1:
            continue
        if v[0] == POSLABEL:
            new_posdata.append(new_v)
        else:
            new_negdata.append(new_v)
    if OutputToFile == 1:  #写入文件中
        f2 = open('svmpos_in.txt','w')
        for v in new_posdata:
            f2.write(str(v)+'\n')
        f2.close()
        f3 = open('svmneg_in.txt','w')
        for v in new_negdata:
            f3.write(str(v)+'\n')
        f3.close()
        f4 = open('featureList.txt','w')
        for x in fList:
            f4.write(str(x)+'\n')
        f4.close()
    return new_posdata,new_negdata

def mkXYset(datapool,x,y,testset,label,RATE = 0.8):
    l = len(datapool)
    tot = 0
    for vec in datapool:
        tot += 1
        if tot <= l*RATE:
            x.append(vec)
            y.append(label)
        else:
            testset.append(vec)

def swap(x,y,p1,p2):
    x[p1],x[p2] = x[p2],x[p1]
    y[p1],y[p2] = y[p2],y[p1]

def Random_Permutation(x,y):  #将数据集随机打乱，提高分类的准确率
    l = len(x)
    for i in range(2*l):
        p1 = random.randint(0,l-1)
        p2 = random.randint(0,l-1)
        swap(x,y,p1,p2)

def classify(Vec,Y):
    clf = LinearDiscriminantAnalysis()
    clf.fit(Vec,Y)
    return clf
    
def get_k_fold_Cross_Validation_classifier(Vec,Y,k):
    len_X = len(Vec)
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
                testx.append(Vec[num])
                testy.append(Y[num])
                continue
            x.append(Vec[num])
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

def k_fold_Cross_Validation_classifier(X,Y,k):
    ACC = 0.0
    clfs,testsets=get_k_fold_Cross_Validation_classifier(X,Y,k)
    for i in range(len(clfs)):
        testx,testy = testsets[i]
        ACC += calcACC(clfs[i],testx,testy)
    ACC /= 10
    return ACC
    
def LDATesting(posData,negData,POSLABEL = 1.0,NEGLABEL = 0.0):   #线性判别分析+留一交叉验证
    X = []
    Y = []
    posTestset = []
    negTestset = []  
    mkXYset(posData,X,Y,posTestset,POSLABEL)   #获取数据集
    mkXYset(negData,X,Y,negTestset,NEGLABEL)
    Random_Permutation(X,Y)
    len_X = len(X)
    len_Y = len(Y)
    TP = 0
    FN = 0
    TN = 0
    FP = 0
    R = 0
    W = 0
    for i in range(len_X):
        x = []
        y = []
        for j in range(len_X):
            if i==j:
                continue
            x.append(X[j])
            y.append(Y[j])
        clf = LinearDiscriminantAnalysis() #LDA分类器
        clf.fit(x,y)
        v = clf.predict([X[i]])[0] 
        if Y[i] == POSLABEL:
            if v == POSLABEL:  #真阳性 
                TP+=1
                R+=1
            else:  
                FN+=1   #假阴性
                W+=1
        if Y[i] == NEGLABEL:
            if v == NEGLABEL:  
                TN+=1   #真阴性
                R+=1
            else:
                FP+=1   #假阳性
                W+=1
    FPR = float(FP)/float(FP+TN)   #计算FPR和TPR
    TPR = float(TP)/float(TP+FN)
    zi = float(TP*TN-FP*FN)
    sss = float((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    mu = math.sqrt(sss)  
    ACC = float(R)/float(R+W) 
    if float(mu) > 0:
        MCC = float(zi)/float(mu)
    else:
        MCC = 0 #ERROR 
    return ACC,MCC
    
def ChooseFea(fList,features,fea_ACC,fea_Set,datasetFilename='dataset.txt'):   #根据准确率上升最大原则，挑选一个新的特征加入原有的特征集fList中，并且返回加入新特征后的准确率
    Best_ACC = 0
    Best_F = 0
    for f in features:
        #Best_ACC = 0
        if f in fList:
            continue
        l = [int(F) for F in fList]
        #for F in fList:
        #    l.append(F)
        l.append(int(f))
        posData,negData = mkdataset(l,datasetFilename)
        New_ACC,New_MCC = LDATesting(posData,negData)
        if New_ACC > Best_ACC:
            Best_ACC = New_ACC
            Best_F = f
    fList.append(Best_F)
    fea_Set.append([x for x in fList])
    fea_ACC.append(Best_ACC)
    return Best_ACC

def IncSearch(features,datasetFilename='dataset.txt'): 
    fList = []
    fea_ACC = []
    fea_Set = []
    Best_ACC = 0
    tot = 0
    while 1:   #不断地挑选新特征，直到全选进去
        New_ACC=ChooseFea(fList,features,fea_ACC,fea_Set,datasetFilename='dataset.txt')
        tot += 1
        print('ACC_'+str(tot)+':'+str(New_ACC))
        if New_ACC>Best_ACC:
            Best_ACC = New_ACC
        #print('Best_ACC:'+str(Best_ACC))
        if len(fList) == len(features):
            for i in range(len(fea_ACC)):
                t = i
                print("Fea_ACC_"+str(t)+':'+str(fea_ACC[t]))
                if fea_ACC[t] == Best_ACC:
                    print('FeaList_Len:'+str(len(fea_Set[t])))
                    return fea_Set[t]
    #return fList

def getVec(str): #读入str中的向量
    s = str.strip().lstrip("[").rstrip("]").split(',')
    #print(s)
    vec = []
    for cor in s:
        vec.append(float(cor))
    #print(vec)
    #quit()
    return vec 

def loadDataSet(filename): #从文件中加载数据集，其中参数filename指定了文件名
    f = open(filename,"r")
    data = f.readlines()
    f.close()
    dataset = []
    for line in data:
        #print(getVec(line))
        dataset.append(getVec(line))
    #print(dataset)
    return dataset

def mkDataset_forSVM(datapool,x,y,testset,label,RATE = 0.8): #根据读取到的数据集生成训练集和测试集
    l = len(datapool)
    tot = 0
    for vec in datapool:
        tot += 1
        if tot <= l*RATE:
            x.append(vec)
            y.append(label)
        else:
            testset.append(vec)

def Draw_subplot(set1,label1,set2,label2):
    fig, ax = plt.subplots(2,1)
    x1_1 = []
    x2_1 = []
    y1_1 = []
    y2_1 = []
    x1_2 = []
    x2_2 = []
    y1_2 = []
    y2_2 = []
    tot = 0
    for v1 in set1:
        if label1[tot] == 0:
            x1_1.append(v1[0])
            y1_1.append(v1[1])
        else:
            x1_2.append(v1[0])
            y1_2.append(v1[1])        
        tot += 1
    tot = 0    
    for v2 in set2:
        if label2[tot] == 0:
            x2_1.append(v2[0])
            y2_1.append(v2[1])
        else:
            x2_2.append(v2[0])
            y2_2.append(v2[1])
        tot += 1
    si = 20
    ax[0].scatter(x1_1,y1_1,color = 'b',s = si)
    ax[0].scatter(x1_2,y1_2,color = 'r',s = si)
    ax[1].scatter(x2_1,y2_1,color = 'b',s = si)
    ax[1].scatter(x2_2,y2_2,color = 'r',s = si)
    plt.show()

def svm_classifier(svmpos_inFilename="svmpos_in.txt",svmneg_inFilename="svmneg_in.txt"):    #"svmpos_in.txt","svmneg_in.txt"
    X = []
    Y = []
    vaild_X = []
    vaild_Y = []
    test_X = []
    test_Y = []
    posTestset = []
    negTestset = []
    pos_predict = []
    neg_predict = []
    Alldata = []
    posData = []
    negData = []
    posData_old = loadDataSet(svmpos_inFilename)
    negData_old = loadDataSet(svmneg_inFilename)
    Alldata=preprocessing.scale(posData_old + negData_old)  #归一化处理，非常重要
    posData = Alldata[:len(posData_old)]
    negData = Alldata[len(posData_old):]
    mkDataset_forSVM(posData,X,Y,posTestset,1)
    mkDataset_forSVM(negData,X,Y,negTestset,0)
    #Random_Permutation(X,Y)    #数据随机排列，建议初始数据分布有规律时使用
    l = []
    xx = []  #存储FPR值
    yy = []  #存储TPR值
    len_X = len(X)
    len_Y = len(Y)
    outputfile = open("svm_result.txt","w")
    posPre = []
    negPre = []
    SVM_Classifiers=SVC(C=1.0, cache_size=500, class_weight=None, coef0=0.0,decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',max_iter=-1,probability=True) #如果需要调参请在此处进行调参，传入不同的参数即可构建不同的svm
    SVM_Classifiers.fit(X,Y)
    posPre=SVM_Classifiers.predict_proba(posTestset)
    negPre=SVM_Classifiers.predict_proba(negTestset)
    for d in range(0,1001): #TP、FN、TN、FP、FPR、TPR每个变量的意义和它的名字是一致的，用来绘制ROC图像
        T = float(d)*0.001 #T代表当前的分类阈值，我们把每个预测值大于T的都认为是阳性，反之是阴性
        TP = 0
        FN = 0
        TN = 0
        FP = 0
        R = 0
        W = 0
        num = 0
        for v in posPre: #根据TP、FN、TN、FP的定义计算它们的值
            if v[1]>T:  #真阳性 
                TP+=1
                R+=1
                pos_predict.append(posTestset[num])
            else:  
                FN+=1   #假阴性
                W+=1
                neg_predict.append(posTestset[num])
            num += 1
        num = 0
        for v in negPre:
            if v[1]<=T:  
                neg_predict.append(negTestset[num])
                TN+=1   #真阴性
                R+=1
            else:
                pos_predict.append(negTestset[num])
                FP+=1   #假阳性
                W+=1
            num += 1
        FPR = float(FP)/float(FP+TN)   #计算FPR和TPR
        TPR = float(TP)/float(TP+FN)
        if T == 0.5:  #记录正确率
            print('Correct Rate:'+str(float(R)/float(R+W)*100.0)+"%")
            outputfile.write('Correct Rate:'+str(float(R)/float(R+W)*100.0)+"%\n")
            zi = float(TP*TN-FP*FN)
            sss = float((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
            mu = math.sqrt(sss)    
            if float(mu) > 0:
                MCC = float(zi)/float(mu)
            else:
                MCC = 0 #ERROR   
            outputfile.write('MCC:'+str(MCC)+"\n")
        xx.append(FPR) 
        yy.append(TPR)
        l.append([FPR,TPR]) #将FPR和对应的TPR存储起来
    outputfile.close()
    pca=PCA(n_components=2)   #PCA降维
    newposTestset=pca.fit_transform(posTestset)
    pca_2=PCA(n_components=2)
    newnegTestset=pca.fit_transform(negTestset)
    set1 = []
    label1 = []
    label2 = []
    tot = 0
    for v in newposTestset:
        set1.append(v)
        label1.append(1)
        label2.append(posPre[tot][1]>0.5)
        tot += 1
    tot = 0
    for v in newnegTestset:
        set1.append(v)
        label1.append(0)
        label2.append(posPre[tot][1]<=0.5)
        tot += 1
    Draw_subplot(set1,label1,set1,label2)
    plt.plot(xx,yy) #利用上面的计算结果绘制ROC曲线
    plt.legend()
    plt.show()  

def InputFromFiles_Chi_square(datasetFilename = "dataset.txt"):  #从文件中读取特征集
    f = open(datasetFilename,'r')
    dataset = f.readlines()
    f.close()
    vecs = []
    new_posdata = []
    new_negdata = []
    for line in dataset:
        str_v = line.split(',')
        v = [float(cor) for cor in str_v]
        new_v = v
        zero = 1
        for c in new_v:
            if c != 0:
                zero = 0
                break
        if zero == 1:
            continue
        Alldata.append(v)
        Feas = len(v)
        if v[0] == POSLABEL:
            new_posdata.append(new_v)
            labels.append(POSLABEL)
        else:
            new_negdata.append(new_v)
            labels.append(NEGLABEL)
        return Alldata, labels
            
def ChooseFea_Chi_square(number,Alldata, labels):   #根据准确率上升最大原则，挑选一个新的特征加入原有的特征集fList中，并且返回加入新特征后的准确率
    Best_ACC = 0
    Best_F = 0
    newdataset = SelectKBest(chi2, k=number).fit_transform(Alldata, labels)
    posData = []
    negData = []
    for i in range(len(labels)):
        if lables[i] == POSLABEL:
            posData.append(newdatset[i])
        else:
            negData.append(newdataset[i])
    Best_ACC,New_MCC = LDATesting(posData,negData)
    return Best_ACC,newdataset

def IncSearch_Chi_square(Alldata, labels): 
    fList = []
    Best_ACC = 0
    tot = 0
    bestdataset = []
    while 1:   #不断地挑选新特征，直到全选进去
        tot += 1
        newdataset = []
        New_ACC,newdataset=ChooseFea_Chi_square(tot,Alldata, labels)
        print('ACC_'+str(tot)+':'+str(New_ACC))
        if New_ACC>Best_ACC:
            Best_ACC = New_ACC
            bestdataset = newdataset
        #print('Best_ACC:'+str(Best_ACC))
        if tot == Feas:
            return bestdataset
    return bestdataset

def mkdataset_Chi_square(bestdataset,OutputToFile = 0):  #根据特征集fList，构建svm训练及评估所用的数据集
    if OutputToFile == 1:  #写入文件中
        f2 = open('svmpos_in.txt','w')
        f3 = open('svmneg_in.txt','w')
        for i in range(len(labels)):
            if lables[i] == POSLABEL:
                #f2.write(str(newdatset[i])+'\n')
                f2.write('['+str(newdatset[i][0]))
                for cor in newdatset[i][1:]:
                    f2.write(',')
                    f2.write(str(cor))
                f2.write(']\n')  
            else:
                f3.write('['+str(newdatset[i][0]))
                for cor in newdatset[i][1:]:
                    f3.write(',')
                    f3.write(str(cor))
                f3.write(']\n')
        f2.close()
        f3.close()
    return new_posdata,new_negdata

def run_MRMR(datasetFilename='dataset.txt',FEAS = 180):
    features=mRMR(datasetFilename,FEAS)
    OutputToFiles(features)

def Fea_DataSetMaker(datasetFilename="dataset.txt",Best_FeasFilename='Best_Feas.txt'):
    features=InputFromFiles(Best_FeasFilename)  #读入文件
    Best_Feas = IncSearch(features,datasetFilename)  #挑选特征
    print(Best_Feas)
    mkdataset(Best_Feas,datasetFilename, OutputToFile = 1)  #构建数据集
    
def Fea_DataSetMaker_Chi_square(Best_FeasFilename,datasetFilename="dataset.txt"):   
    Alldata, labels=InputFromFiles_Chi_square(datasetFilename)  #读入文件
    bestdataset = []
    bestdataset = IncSearch_Chi_square(Alldata, labels)  #挑选特征
    mkdataset_Chi_square(bestdataset, OutputToFile = 1)  #构建数据集

def task2_work():
    csv_converter()
    run_MRMR()
    Fea_DataSetMaker()
    svm_classifier()

if __name__ =='__main__':
    task2_work()
