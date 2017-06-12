import numpy as np
import matplotlib.pyplot as plt
import xlwt
'''
xarea=[]
yarea=[]
for i in range(0,1000,5):
    for j in range(0,1000,5):
        xarea.append(i)
        yarea.append(j)
#xyantenna=[[250.5,210.2],[500.9,680.6],[762.3,275.6]]
'''
antenna=[]
for j in range(-60,60,20):
    for k in range(60,180,20):
        for u in range(180,300,20):
            antenna.append([250.5,210.2,j])
            antenna.append([250.5,210.2,k])
            antenna.append([250.5,210.2,u])
            antenna.append([500.9,680.6,j])
            antenna.append([500.9,680.6,k])
            antenna.append([500.9,680.6,u])
            antenna.append([762.3,275.6,j])
            antenna.append([762.3,275.6,k])
            antenna.append([762.3,275.6,u])
#xyantenna=[[1000/4,1000/4],[2000/3,2000/3],[762.3,275.6]]

#xyarea=np.array(xyarea)
#a=np.array(xyantenna)


#print(xarea)
'''
f1=plt.subplot(111)
plt.scatter(xarea,yarea,s=1,color='b')
plt.plot(a[:,0],a[:,1],'r''^')
label='原始基站位置'
plt.grid()
plt.show()
'''

'''
def write_excel1():
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    for i in range(0,len(xarea)):
        sheet1.write(i,0,xarea[i])
        sheet1.write(i,1,yarea[i])    
    f.save(r"E:\复杂度分析\采样点.xls")
write_excel1()
'''
def write_excel2():
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    for i in range(0,len(antenna)):
        sheet1.write(i,0,antenna[i][0])
        sheet1.write(i,1,antenna[i][1]) 
        sheet1.write(i,2,antenna[i][2])
    f.save(r"E:\复杂度分析\基站坐标.xls")
write_excel2()
