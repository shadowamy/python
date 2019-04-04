# -*- coding:utf-8 -*-

import cv2
import numpy as np
from PIL import Image, ImageFilter
import pytesseract
import xlwt
import xlrd
import os
from xlutils.copy import copy
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
xls_row = 1

def orc_text(image_path):
    text = ''
    img = cv2.imread(image_path)

    '''
    # 锐化
    # 1
    blur=cv2.GaussianBlur(img,(0,0),3)
    image=cv2.addWeighted(img,1.5,blur,-0.5,0)
    # 2
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    image = cv2.filter2D(img, -1, kernel)
    # 3
    image=cv2.bilateralFilter(img,9,75,75)
    # 4
    sigma = 1; threshold = 5; amount = 1
    blurred=cv2.GaussianBlur(img,(0,0),1,None,1)
    lowContrastMask = abs(img - blurred) < threshold
    sharpened = img*(1+amount) + blurred*(-amount)
    image=cv2.bitwise_or(sharpened.astype(np.uint8),lowContrastMask.astype(np.uint8))
    '''

    # 去除水印，清晰化
    #hight, width, depth = img.shape[0:3]
    # 图片二值化处理，把(50, 50, 50)-(255, 255, 255)以外的颜色变成0
    thresh = cv2.inRange(img, np.array([50, 50, 50]), np.array([255, 255, 255]))

    # 创建形状和尺寸的结构元素
    kernel = np.ones((1, 1), np.uint8)

    # 扩张待修复区域
    hi_mask = cv2.dilate(thresh, kernel, iterations=1)
    specular = cv2.inpaint(img, hi_mask, 5, flags=cv2.INPAINT_TELEA)

    #cv2.imwrite("change.png", specular);

    for i in range(specular.shape[1]):
        for j in range(specular.shape[0]):
            if (specular[j, i, 0] > 13 and specular[j, i, 1] > 13 and specular[j, i, 2] > 13):
                specular[j, i, 0] = 12
                specular[j, i, 1] = 12
                specular[j, i, 2] = 12

            if (specular[j, i, 0] < 10 and specular[j, i, 1] < 10 and specular[j, i, 2] < 10):
                specular[j, i, 0] = 255
                specular[j, i, 1] = 255
                specular[j, i, 2] = 255

    # 文字识别

    dst2 = Image.fromarray(cv2.cvtColor(specular, cv2.COLOR_BGR2RGB))
    #dst2.show()
    dst2.filter(ImageFilter.CONTOUR)
    dst2.load()
    text = pytesseract.image_to_string(dst2, lang='chi_sim').replace(' ', '')

    return text

def xls_create(xls_path):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)
    sheet.write(0, 0, '企业注册号'.encode('utf-8').decode('utf-8'))
    sheet.write(0, 1, '企业名称'.encode('utf-8').decode('utf-8'))
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
    if(list and len(list[0])<14):
        list[0] = list[0] + list[1]
        list[1] = list[2]
    if len(list)>=9:
        while(i<2):
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
    print (str(ans_list).decode("utf-8").encode('gbk'))
    #xls_change(r'test1.xls', ans_list)
    return ans_list

#text = orc_text('D:/python/image/7.png')
#print(text)

if(not os.path.exists(r'test1.xls')): #xls表与py脚本同目录，若不存在进行创建
    xls_create(r'test1.xls')
    print 'create xls success'

	
str_root = input("请输入图片目录\n".decode('UTF-8').encode('GBK'))

while(not os.path.exists(str_root)):
	print('请输入正确的图片目录\n'.decode('UTF-8').encode('GBK'))
	str_root = input("请输入图片目录\n".decode('UTF-8').encode('GBK'))
print('输入成功，请等待图片处理\n'.decode('UTF-8').encode('GBK'))

rootdir = str_root #
file_list = os.listdir(rootdir)
for i in range(0, len(file_list )):
    img_path = os.path.join(rootdir,file_list[i])
    if os.path.isfile(img_path):
        #print(img_path)
        text = orc_text(img_path)
        l = str_dw(text)
        xls_change(r'test1.xls', l)

print('图片处理完成'.decode('UTF-8').encode('GBK'))
