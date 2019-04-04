from PIL import Image,ImageFilter
import pytesseract
import xlwt
import xlrd
import os
from xlutils.copy import copy

xls_row = 1

def orc_text(image_path):
    text = ''

    img = Image.open(image_path)
    img.filter(ImageFilter.CONTOUR)
    img.load()
    text = pytesseract.image_to_string(img, lang='chi_sim').replace(' ','')


    return text

#text = orc_text('D:/python/image/2.png')
#print(text)

def xls_create(xls_path):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)
    '''
    sheet.write(0, 0, '111')  
    sheet.write(0, 1, '777')
    '''
    sheet.write(0, 0, '企业注册号'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 1, '企业名称'.encode('utf-8').decode('utf-8'))
    '''
    sheet.write(0, 2, '类型'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 3, '住所'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 4, '法定代表人'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 5, '成立时间'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 6, '注册资本'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 7, '营业期限'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 8, '营业期限'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 9, '经营范围'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 10, '登记机关'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 11, '核准时间'.encode('utf-8').decode('utf-8'))
    '''
    book.save(xls_path)

#xls_create(r'test1.xls')

def xls_change(xls_path, list):

    old_excel = xlrd.open_workbook(xls_path, formatting_info=True)
    new_excel = copy(old_excel)
    ws = new_excel.get_sheet(0)

    #ws.write(1, 0, '第二行，第一列')
    #ws.write(1, 1, '第二行，第二列')
    #ws.write(1, 2, '第二行，第三列')

    global xls_row
    i = 0
    if len(list)>=12:
        while(i<3):
            ws.write(xls_row, i, list[i].encode('utf-8').decode('utf-8'))
            i+=1
        xls_row +=1
        new_excel.save(xls_path)

def str_dw(text):
    ans_list = []
    list = text.split('\n')
    while '' in list:
        list.remove('')

    #print(list)
    for i in range(len(list)):
        temp_l = list[i].split(':')
        #print(temp_l)
        if(len(temp_l) == 2):
            ans_list.append(temp_l[1])
        else:
            ans_list.append(temp_l[0])
    while '' in ans_list:
        ans_list.remove('')
    print(ans_list)
    #xls_change(r'test1.xls', ans_list)
    return ans_list


rootdir = 'D:\python\image'
file_list = os.listdir(rootdir)
for i in range(0, len(file_list )):
    img_path = os.path.join(rootdir,file_list[i])
    if os.path.isfile(img_path):
        #print(img_path)
        text = orc_text(img_path)
        l = str_dw(text)
        xls_change(r'test1.xls', l)

