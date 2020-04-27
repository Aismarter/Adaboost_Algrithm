#coding=utf-8


def loadData1(filename):
    fr = open(filename)
    numFeat = len(fr.readline().strip().split(','))-3
    dataMat = []
    labelMat = []
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split(',')
        for i in range(numFeat):
            lineArr.append(float(curLine[i+2]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat


def loadData2(filename):
    fr = open(filename)
    numFeat = len(fr.readline().strip().split(','))-1  # 读取行数 并做处理 返回的值 是各方数据的个数的列表
    dataMat = []
    labelMat = []
    for line in fr.readlines():
        lineArr = []
        curline = line.strip().split(',')  # 数据的操作
        for i in range(numFeat):
            lineArr.append(float(curline[i+1]))  # 行向量
        dataMat.append(lineArr)
        labelMat.append(float(curline[0]))
    return dataMat, labelMat   # 生成数据和标签

