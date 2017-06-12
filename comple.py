import xlrd
import xlwt
from math import sqrt
from scipy.spatial import cKDTree

"read data"
book=xlrd.open_workbook(r"E:\复杂度分析\复杂度分析\20度天线30步长组采样度覆盖次数.xls")
#book=xlrd.open_workbook(r"E:\中移动\test.xlsx")
table=book.sheet_by_index(0)
nrows=table.nrows
#print (nrows)


sump=216#状态总数
step=30#采样点间隔
x=[]
y=[]
p1=[]
p_1=[]
data=[]

for clonum in range(0,nrows):
    data.append(table.row_values(clonum))
#print(data[0])


"read longitude"
for i in range(0,len(data)):
    x.append(data[i][0])
    y.append(data[i][1])
    p1.append(data[i][2])
    p_1.append(sump-data[i][2])

    
#print(len(x))
    
#print(lon[0])
"read latitude"
xmax=max(x)
xmin=min(x)
ymax=max(y)
ymin=min(y)
    
#print(lat[0])
#生成所有采样点kdtree，以寻找该采样点分形算法范围
areaxy=list(zip(x,y))
#print(len(areaxy))
kdTree_xy=cKDTree(areaxy)
#print(kdTree_areaxy)
def get_point(x1,y1):
    areaxyfin=[]
    for j in kdTree_xy.query_ball_point([x1,y1],step*sqrt(2)):
        #print(j)
        areaxyfin.append([x[j],y[j],p1[j],p_1[j]])
    return (areaxyfin)
#print(get_point(x[0],y[0]))

th=[2,1000,1200,1400,1600,1800,2000,2500,4000,6000]  #复杂度阈值门限
def complexity(x1,y1,th1):
    points=get_point(x1,y1)#附近点 [0]是x,[1]是y,[2]是符合次数[3]是不符合次数
    comv2=[]
    for index,item in enumerate(points):
        #print(index,item)
        #j[2]是符合次数,j[3]是不符合次数
        #comv1是单点复杂度
        if item[0]==x1:
            comv1=item[2]*item[3]
        else:
            comv2.append(item[2]*item[3])
    comv2max=max(comv2)
    comv2min=min(comv2)
    u=max(comv1+1,comv2max)    
    b=min(comv1-1,comv2min)    
    complexv=u-b
    if complexv >= th1:
        caiyong=1
        flag=None
    else :
        caiyong=0
        if item[2]>item[3]:    
            flag=1
        else:    
            flag=0
        
    
       
    return x1,y1,complexv,caiyong,flag
    
    
def xyfinjudge(x1,y1,caiyong,flag):
    if caiyong==1:
        return(x1,y1,flag)

        
def write_excel(xfin,yfin,complexfin,caiyongfin,flagfin,th12):
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    for i in range(0,len(xfin)):
        sheet1.write(i,0,xfin[i])
        sheet1.write(i,1,yfin[i])
        sheet1.write(i,2,complexfin[i]) 
        sheet1.write(i,3,caiyongfin[i])
        sheet1.write(i,4,flagfin[i])
    
    f.save(r"C:\Users\Bear\Desktop\新建文件夹 (3)\20度天线30步长组最终采样点%d.xls"%th12)




def main():
    for thv in th:
        xfin=[]
        yfin=[]
        complexfin=[]
        caiyongfin=[]
        flagfin=[]
        for i in range(len(x)):
            xfinp,yfinp,complexvp,caiyongp,flagp=complexity(x[i],y[i],thv)
            xfin.append(xfinp)
            yfin.append(yfinp)
            complexfin.append(complexvp)
            caiyongfin.append(caiyongp)
            flagfin.append(flagp)
        '''
        print(xfin[:10])
        print(yfin[:10])
        print(complexfin[:10])
        print(caiyongfin[:10])
        print(flagfin[:10])
        '''
        print(thv)
        write_excel(xfin,yfin,complexfin,caiyongfin,flagfin,thv)
    
        
if __name__ == "__main__":      
    main()
