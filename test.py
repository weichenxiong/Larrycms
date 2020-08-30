import xlwt
import xlrd
import time


def createTestNum():

    d = ["1", "2", "3", "4", "5", "6", "7"]

    return d

def getExcelCol():
    try:
        myWorkbook = xlrd.open_workbook("student.xls")
        mySheets = myWorkbook.sheets()                 #获取工作表list。
        mySheet = mySheets[0]                          #通过索引顺序获取。
        mySheet = myWorkbook.sheet_by_index(0)         #通过索引顺序获取。
        mySheet = myWorkbook.sheet_by_name(u'sheet1')  #通过名称获取。
        nrows = mySheet.nrows
        ncols = mySheet.ncols
        print(str(nrows) + "行", str(ncols) + "列")
        return nrows
    except:
        book = xlwt.Workbook() #创建Excel
        sheet = book.add_sheet('sheet1') #创建sheet页
        title = ['编号','姓名','语文成绩','数学成绩','英语成绩','总分','平均分'] #把表头名称放入list里面
         #循环把表头写入
        row = 0 
        for t in title:
            sheet.write(0,row,t)
            row += 1
        book.save('student.xls')
        return getExcelCol()

def createExcle():

    book = xlwt.Workbook() #创建Excel
    sheet = book.add_sheet(u'sheet1') #创建sheet页
    
    num = createTestNum()
    data = [
        num
        ]
    print(data)
    title = ['编号','姓名','语文成绩','数学成绩','英语成绩','总分','平均分'] #把表头名称放入list里面

    # #循环把表头写入
    row = 0 
    for t in title:
        sheet.write(0,row,t)
        row+=1

    # row = 1 #列
   # 去读取数据的行数
    row = getExcelCol()
    print("rows:",row)
    for d in data:  #控制行
        col = 0
        for one in d:#控制每一列
            print(one)
            sheet.write(row,col,one) #row代表行，col代表列
            col+=1
        row+=1
    book.save('student.xls')
   
if __name__ == "__main__":
    
# for i in range(5):
#     time.sleep(5)
#     createExcle()
# getExcelCol()
# getExcelCol()
    createExcle()