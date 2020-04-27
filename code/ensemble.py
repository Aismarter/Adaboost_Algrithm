# coding=utf-8

from sklearn import preprocessing  # preprocessing方法包 按比例缩放、中心化、归一化、二值化等操作
from sklearn import svm
import numpy
import math
import dataProcess


def diff1(y1, y2):  #
    right = 0
    length = len(y1)
    for i in range(length):
        if y1[i] >= 0.5 and y2[i] >= 0.5:
            # and 表示从左到右计算表达式，若所有值均为真，则返回最后一个值，若存在假，返回第一个假值
            right += 1
        if y1[i] < 0.5 and y2[i] < 0.5:
            right += 1
    return right


def diff2(y1, y2):
    right = 0
    length = len(y1)
    for i in range(length):
        if y1[i] == y2[i]:
            right += 1
    return right


class Adaboost():

    def __init__(self, numOfInter, x, y):
        self.xArr = x
        self.yArr = y
        # 根据集合分开训练集和测试集
        rowNum = len(y)
        singleNum = math.ceil(rowNum / 5)   # 返回x上限作为一个积分
        testNum = singleNum * 4
        self.TestXarr = []
        self.TestYarr = []
        self.TrainXarr = []
        self.TrainYarr = []
        trainNum = rowNum - testNum
        for i in range(int(singleNum)):  # 初始化样本权重分布
            if 5 * i >= rowNum - 1:
                break
            self.TrainXarr.append(x[5 * i])  #
            self.TrainYarr.append(y[5 * i])
            if 5 * i + 1 >= rowNum - 1:
                break
            self.TrainXarr.append(x[5 * i + 1])
            self.TrainYarr.append(y[5 * i + 1])
            if 5 * i + 2 >= rowNum - 1:
                break
            self.TrainXarr.append(x[5 * i + 2])
            self.TrainYarr.append(y[5 * i + 2])
            if 5 * i + 3 >= rowNum - 1:
                break
            self.TrainXarr.append(x[5 * i + 3])
            self.TrainYarr.append(y[5 * i + 3])
            if 5 * i + 4 >= rowNum - 1:
                break
            self.TestXarr.append(x[5 * i + 4])
            self.TestYarr.append(y[5 * i + 4])
        self.NumofClassifier = numOfInter

    def AdaboostTrain(self, wk_list, x, y):
        NumofData = numpy.shape(x)[0]
        # typelist = ['linear', 'rbf','sigmoid']
        typelist = wk_list
        g_list = []  # 弱分类器的权重
        weight_array = numpy.zeros((NumofData, 1))
        weight_array[:, 0] = 1.0 / NumofData
        for t in range(self.NumofClassifier):  # 基于分布训练不同的分类器
            min_err_rate = 1
            temp_weight = []
            g = []
            for w in wk_list:
                print(w)
                # 分类器的类型
                # type = typelist[w[0]]
                type = w
                para_c = w[1]
                para_gamma = w[2]
                # svmp = svm.SVC(kernel = type, C = para_c,gamma = para_gamma)
                svmp = svm.SVC(kernel=type)
                svmp.fit(x, y, sample_weight=weight_array[:, 0])   # 首先先训练出一个基学习器
                prediction = svmp.predict(x)
                err_rate = sum(weight_array[prediction != y])
                err_rate = err_rate / sum(weight_array)

                if err_rate == 0:  # 再对基学习器表现对训练样本的分布进行调整
                    g_list = []
                    # g.append(w[0])
                    # g.append(w[1])
                    # g.append(w[2])
                    # g.append(1)
                    # g_list.append(g)
                    g.append(typelist.index(w))
                    g.append(1)
                    return g_list

                if err_rate < min_err_rate:
                    min_err_rate = err_rate
                    best_prediction = prediction
                    besttype = typelist.index(type)
                    best_c = para_c
                    best_pamma = para_gamma
            print(min_err_rate)
            if min_err_rate > 0.5:   # 检查当前生成的分类器效果是否比基分类器好
                print('error rate is larger than 0.5')
                return g_list

            alpha = 0.5 * numpy.log((1 - min_err_rate) / min_err_rate)  # 使基学习器做错的训练在后续受到更多的关注
            g.append(besttype)
            g.append(alpha)
            g_list.append(g)

            # 更新权重
            weight_array[best_prediction == y] = weight_array[best_prediction == y] * numpy.exp(-alpha)  # 降低正确的权重
            # 基于调整后的分布来训练下一个基学习器
            weight_array[best_prediction != y] = weight_array[best_prediction != y] * numpy.exp(alpha)  # 增加错误权重
            weight_array = weight_array / sum(weight_array)  # 将不同的训练器的效果按照一定比例加起来

        return g_list

    def AdaboostTest(self, g_list, xTest, xTrain, yTrain, type_list):
        N = numpy.shape(xTest)[0]
        typelist = type_list
        alpha_array = [0] * N
        for g in g_list:
            type = typelist[g[0]]
            # svmp = svm.SVC(kernel = type , C = 0.01, gamma = para_gamma)
            svmp = svm.SVC(kernel=type)
            print(numpy.shape(xTrain))
            print(numpy.shape(yTrain))
            svmp.fit(xTrain, yTrain)
            prediction = svmp.predict(xTest)
            alpha_array = alpha_array + prediction * g[1]
        return alpha_array


if __name__ == '__main__':
    xArr, yArr = dataProcess.loadData1('clean1.data')
    xArr, yArr = dataProcess.loadData2('wine.data.txt')
    # xArr = regularize(xArr)

    xArr = preprocessing.scale(xArr)
    adaboost = Adaboost(10, xArr, yArr)

    wk_list = ['linear']
    '''for i in range(2):
        for j in range(2):
            w1 = [0] * 3
            w2 = [0] * 3
            #0代表linear, 1代表rbf
            w1[0] = 0
            w2[0] = 1
            w1[1] = 10 ** (i-1)
            w2[1] = 10 ** (i-1)
            w1[2] = 10 ** (j-1)
            w2[2] = 10 ** (j-1)
            wk_list.append(w1)
            wk_list.append(w2)
        '''
    g_list = adaboost.AdaboostTrain(wk_list, adaboost.TrainXarr, adaboost.TrainYarr)
    yPredict = adaboost.AdaboostTest(g_list, adaboost.TestXarr, adaboost.TrainXarr, adaboost.TrainYarr, wk_list)
    rightnum = diff1(yPredict, adaboost.TestYarr)
    print('num:' + str(rightnum))
    print('tested num:' + str(len(yPredict)))
    print('集成正确率:' + str((1.0 * rightnum / len(yPredict))))
