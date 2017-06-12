import xlwt
x=[]
y=[]
for i in range(0,1000,20):
    for j in range(0,1000,20):
        x.append(i)
        y.append(j)

#print(xy[0][1])

def write_excel():     
    f=xlwt.Workbook()     
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)     
    for i in range(0,len(x)):         
        sheet1.write(i,0,x[i])         
        sheet1.write(i,1,y[i])                                  
    f.save(r"E:\复杂度分析\point.xls") 
write_excel()