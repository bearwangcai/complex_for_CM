# -*- coding=utf-8 -*-
from __future__ import division
import numpy as np
from numpy import sin, cos, pi, log10
import xlrd
import matplotlib.pyplot as plt
# from scipy.spatial import cKDTree
from copy import deepcopy
import xlwt


def antennadata():
    A_P = xlrd.open_workbook(r"E:\复杂度分析\对比数据\testantenna.xlsx")
    A_P_table = A_P.sheets()[0]
    node_x = A_P_table.col_values(0)
    node_y = A_P_table.col_values(1)
    node_h = [30]*9
    node_h_angle = A_P_table.col_values(2)
    node_v_angle = [0]*9

    return node_x, node_y, node_h, node_h_angle, node_v_angle
    
    

    
def getpoints(stepnum,thnum):
    pointp=[]
    P_P = xlrd.open_workbook(r"C:\Users\Bear\Desktop\新建文件夹 (3)\20度天线%d步长组最终采样点%d.xls"%(stepnum,thnum))
    P_P_table = P_P.sheets()[0]
    nrows=P_P_table.nrows
    data=[]
    datatbt=[]
    dataknown=[]
    point_xtbt=[]
    point_ytbt=[]
    point_xknown=[]
    point_yknown=[]
    point_flag=[]
    for clonum in range(0,nrows):
        data.append(P_P_table.row_values(clonum))
    for i in range(len(data)):
        if data[i][3]==1:
            datatbt.append(data[i])
            point_xtbt.append(data[i][0])
            point_ytbt.append(data[i][1])
        else :
            dataknown.append(data[i])
            point_xknown.append(data[i][0])
            point_yknown.append(data[i][1])
            point_flag.append(data[i][4])
    #print(len(point_flag))
    #print(len(point_xknown))
    #print(len(point_xtbt))
    pointnum=len(data)
    return point_xtbt, point_ytbt, point_xknown, point_yknown, point_flag, pointnum
    

    
    

class relative_position:
    '''
    求待测点相对于基站的坐标
    '''
    def __init__(self, Point, Antenna, horizontal_angle, vertical_angle, node_num):
        self.point = Point  # 待测点
        self.antenna = Antenna  # 所符合要求的基站
        self.alpha = np.array(horizontal_angle)/180.*pi  # 水平角
        self.beta = np.array(vertical_angle)/180.*pi  # 下倾角
        self.n = node_num  # 符合要求的基站数


    def direction_down_angle(self):
        # 矩阵化
        mPoint = np.matrix(self.point)
        Point_after = []
        dis = []
        # 循环每个基站
        for i in range(self.n):
            # 旋转矩阵
            R = [[cos(self.alpha[i])*cos(self.beta[i]), -sin(self.alpha[i]), cos(self.alpha[i])*sin(self.beta[i]), 0],
                 [sin(self.alpha[i])*cos(self.beta[i]), cos(self.alpha[i]), sin(self.alpha[i])*sin(self.beta[i]), 0],
                 [-sin(self.beta[i]), 0, cos(self.beta[i]), 0],
                 [0, 0, 0, 1]]
            # 平移矩阵
            T = [[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [-self.antenna[0][i], -self.antenna[1][i], -self.antenna[2][i], 1]]
            mR = np.matrix(R)
            mT = np.matrix(T)
            after = mPoint*mT*mR
            Point_after.append(after)
        Point_after = np.round(Point_after, 100)
        for i in range(len(Point_after)):
            d = np.sqrt((self.antenna[0][i] - self.point[0]) ** 2 +
                          (self.antenna[1][i] - self.point[1]) ** 2 +
                          (self.antenna[2][i] - self.point[2]) ** 2)
            dis.append(d)
        dis = np.round(dis, 5)
        # print Point_after
        # print dis
        return Point_after, dis

def new_point(p, q, h):
    Point = []
    for i in range(len(p)):
        m = [p[i], q[i], h, 1]
        Point.append(m)
    # print Point
    return Point

class relative_angle:
    '''
    求待测点相对于基站的水平角和下倾角
    '''
    def __init__(self, Point_after, node_num):
        self.p_a = Point_after  # 待测点的新坐标
        self.n = node_num  # 符合要求的基站数


    def Angle(self):
        alpha = []
        beta = []
        for i in range(self.n):
            m = np.sqrt(self.p_a[i, 0, 0]**2 + self.p_a[i, 0, 1]**2)
            n = np.sqrt(self.p_a[i, 0, 0]**2 + self.p_a[i, 0, 1]**2 + self.p_a[i, 0, 2]**2)
            if m != 0:
                if self.p_a[i, 0, 1] < 0:
                    a = 360 - np.arccos(self.p_a[i, 0, 0]/m) * 180. / pi
                else:
                    a = np.arccos(self.p_a[i, 0, 0] / m) * 180. / pi
                alpha.append(int(a))
            else:
                alpha.append(0)
            if n != 0:
                b =90 - np.arccos(abs(self.p_a[i, 0, 2])/n)*180./pi
                beta.append(int(b))
            else:
                beta.append(90)
        # print 'The angle with new alpha axis is:', alpha, 'degree'
        # print ' The angle with new beta axis is:', beta, 'degree'
        return alpha, beta

def find_gain():
    Gain = xlrd.open_workbook(r"E:\复杂度分析\对比数据\angle.xlsx")
    Gain_table = Gain.sheets()[0]
    horizontal_data_gain = Gain_table.col_values(1)
    vertical_data_gain = Gain_table.col_values(2)
    return horizontal_data_gain, vertical_data_gain

class calculate:
    def __init__(self, point_after, Point, h_d_g, v_d_g,
                 node_h, alpha, beta, dis, Pt, f, node_num):
        self.p_a = point_after  # 待测点的新坐标
        self.point = Point  # 待测点，后文只求了个挂高
        self.h_d_g = h_d_g  # 水平增益，供查询
        self.v_d_g = v_d_g  # 垂直增益，供查询
        self.n_h = node_h  # 挂高
        self.alpha = alpha  # 相对于基站的新水平角
        self.beta = beta  # 相对于基站的新下倾角
        self.dis = np.array(dis)/1000.  # km
        self.Pt = Pt  # 发射功率
        self.f = f  # 发射频率
        self.n = node_num  # 符合要求的基站数

    def Gain(self):
        '''
        :return: 待测点相对于每个基站的增益
        '''
        Gain = []
        for i in range(self.n):
            a = (pi - abs(self.alpha[i])/180.*pi)/pi*(self.h_d_g[0]-self.v_d_g[self.beta[i]])
            b = abs(self.alpha[i])/180.*(self.h_d_g[179]-self.v_d_g[179-self.beta[i]])
            g = self.h_d_g[self.alpha[i]] - a - b
            Gain.append(g)
        # print '            The gain of point is:', np.round(Gain, 5), 'dBm'
        return Gain

    def Loss(self, C=3):
        '''
        :param C: C=3 for metropolitan areas
        :return: 待测点相对于每个基站的损耗
        '''
        Loss = []
        hR = self.point[2]  # m
        for i in range(self.n):
            hT = self.n_h[i]  # m
            a = (1.1*log10(self.f)-0.7)*hR-(1.56*log10(self.f)-0.8)
            L = 46.3+33.9*log10(self.f)-13.82*log10(hT)-a+(44.9-6.55*log10(hT))*log10(self.dis[i])+C
            Loss.append(L)
        # print '                     The Loss is:', np.round(Loss, 5), 'dB'
        return Loss


    def Rsrp(self):
        '''
        :return: 待测点相对于每个基站的信号强度RSRP
        '''
        RSRP = []
        Gain = self.Gain()
        Loss = self.Loss()
        for i in range(self.n):
            r = self.Pt + Gain[i] - Loss[i]
            RSRP.append(r)
        max1 = max(RSRP)  #dBm
        max2 = 10**(max1/10)
        s = deepcopy(RSRP)
        s1 = np.array(s)
        s2 = sum(10**(s1/10)) - max2 #mW
        sinr = max2/s2
        SINR = 10*log10(sinr)  #dB
        # print '                     The RSRP is:', min(RSRP), 'dBm', '--->', max(RSRP), 'dBm'
        # print 'The RSRP is:', round(max(RSRP), 5), 'dBm'
        # print 'The SINR is:', SINR, 'dB'
        # print '-----'
        return round(max(RSRP), 5), SINR

def write_excel(Num):     
    f=xlwt.Workbook()     
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)     
    for i in range(0,len(Num)):         
        sheet1.write(i,0,point_xtbt[i])         
        sheet1.write(i,1,point_ytbt[i])        
        sheet1.write(i,2,Num[i])          
    f.save(r"C:\Users\Bear\Desktop\2000.xls") 


def all(stepnum,thnum):
    L1 = int(len(node_x) / 9)
    #print(L1)
    angle = [[0.0 for i in range(9)] for j in range(L1)]
    for i in range(0, L1):
        for j in range(9):
            angle[i][j] = node_h_angle[i * 9 + j]
    L = len(point_xtbt)
    Num = []
    numsum=sum(point_flag)
    for k in range(L):
        RSRP = []
        SINR = []
        num = 0
        yes_index = []
        no_index = []
        for j in range(L1):
            r_p = relative_position(Point[k], Antenna, angle[j], node_v_angle, node_num)
            point_after, dis = r_p.direction_down_angle()
            r_a = relative_angle(point_after, node_num)
            alpha, beta = r_a.Angle()
            horizontal_data_gain, vertical_data_gain = find_gain()
            cal = calculate(point_after, Point[k], horizontal_data_gain, vertical_data_gain, node_h, alpha, beta, dis, Pt,
                            f, node_num)
            # gain = cal.Gain()
            # loss = cal.Loss()
            rsrp, sinr = cal.Rsrp()
            RSRP.append(rsrp)
            SINR.append(sinr)
        for i in range(len(RSRP)):
            if RSRP[i] >= -88 and SINR[i] >= -3:
            # if RSRP[i] >= -88:
                num += 1
                yes_index.append(i)
            else:
                no_index.append(i)
        new_yes_x = []
        new_yes_y = []
        new_no_x = []
        new_no_y = []
        '''
        for i in yes_index:
            new_yes_x.append(point_xtbt[i])
            new_yes_y.append(point_ytbt[i])
        for i in no_index:
            new_no_x.append(point_xtbt[i])
            new_no_y.append(point_ytbt[i])
        '''
        numsum+=num
        #print ('The number of >= -88dBm & -3dB:', numsum)
        # print '       The number of >= -88dBm:', num
        #print ('     The times of satisfaction:', len(RSRP))
        #m = round(numsum / pointnum * 100, 2)
        #print ('         The satisfaction rate:', m, '%')
        #Num.append(num)
    print("20度天线%d步长组最终采样点%d.xls"%(stepnum,thnum))
    print ('Through the algorithm, the number of >= -88dBm & -3dB:', numsum)
    m = round(numsum / pointnum * 100, 2)
    print ('         The satisfaction rate:', m, '%')
    #write_excel(Num)
    return (Num)
step=[10,15,20,30]
#stepnum=20
th=[2,1000,1200,1400,1600,1800,2000,2500,4000,6000]
for stepnum in step:
    for thnum in th:
        node_x, node_y, node_h, node_h_angle, node_v_angle = antennadata()
        point_xtbt, point_ytbt, point_xknown, point_yknown, point_flag, pointnum = getpoints(stepnum,thnum)
        x = node_x[:9]
        y = node_y[:9]
        node_num = 9
        Pt = 18.2
        f = 900
        Point = new_point(point_xtbt, point_ytbt, 1.7)
        Antenna = [x, y, node_h, 1]
        all(stepnum,thnum)

