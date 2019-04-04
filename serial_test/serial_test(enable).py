import binascii
import serial  
import time
def hexShow(argv):        #十六进制显示 方法1
    try:
        result = ''  
        hLen = len(argv)  
        for i in range(hLen):  
         hvol = argv[i]
         hhex = '%02x'%hvol  
         result += hhex+' '  
        print('hexShow:',result)
    except:
        pass
while True:  #循环重新启动串口
    t = serial.Serial('com12',57600)  
    print(t.portstr)
    '''
    strInput = input('enter some words:') 
    try:    #如果输入不是十六进制数据-- 
        n =t.write(bytes.fromhex(strInput))
    except: #--则将其作为字符串输出
        n =t.write(bytes(strInput,encoding='utf-8'))
    
    print(n)
    '''
    time.sleep(1)     #sleep() 与 inWaiting() 最好配对使用
    num=t.inWaiting()
    a = t.read(num)
    print(len(a))
    

    if num: 
        try:   #如果读取的不是十六进制数据--
            data= str(binascii.b2a_hex(t.read(num)))[2:-1] #十六进制显示方法2
            print(data)
        except: #--则将其作为字符串读取
            str = t.read(num)  
#print(str)  
            hexShow(str)

    serial.Serial.close(t)
    time.sleep(3)
