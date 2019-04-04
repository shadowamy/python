# -*- coding: UTF-8 -*-
import socket, os, struct, socketserver

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '192.168.160.1'
host = 'localhost'
s.connect((host, 12307))

def file_send(filepath):
    if os.path.isfile(filepath):
        fileinfo_size = struct.calcsize('128sl')  # 定义打包规则
        # 定义文件头信息，包含文件名和文件大小
        fhead = struct.pack('128sl', os.path.basename(filepath.encode()), os.stat(filepath.encode()).st_size)
        s.send(fhead)
        print('client filepath: ', filepath)
        # with open(filepath,'rb') as fo: 这样发送文件有问题，发送完成后还会发一些东西过去
        fo = open(filepath, 'rb')
        while True:
            filedata = fo.read(1024)
            if not filedata:
                break
            s.send(filedata)
        fo.close()
        print('send over...')
        '''
        data = s.recv(512)
        data_check = data.decode()
        print(data_check)
        if data_check == 'Yes':
            pass
        elif data_check == 'No':
            pass
        '''

def file_get():
    #connection.settimeout(600)
    fileinfo_size = struct.calcsize('128sl')
    buf = s.recv(fileinfo_size)
    if buf:  # 如果不加这个if，第一个文件传输完成后会自动走到下一句
        filename, filesize = struct.unpack('128sl', buf)
        filename_f = (filename.decode()).strip('\00')
        filenewname = os.path.join('./', filename_f)
        print('file new name is %s, filesize is %s' % (filenewname, filesize))
        recvd_size = 0  # 定义接收了的文件大小
        file = open(filenewname, 'wb')
        print('start receiving...')
        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                rdata = s.recv(1024)
                recvd_size += len(rdata)
            else:
                rdata = s.recv(filesize - recvd_size)
                recvd_size = filesize
            file.write(rdata)
        file.close()
        print('receive done')

def order_check(order):
    listOrder = order.split()
    #print(listOrder)
    if listOrder[0] == 'show':
        s.send(order.encode())
        str_temp = s.recv(1024)
        filestr = str_temp.decode()
        #print(filestr)
        filelist = filestr.split()
        i = 1
        print('file list in order:')
        for li in filelist:
            print(str(i)+'  '+li)
            i+=1

    elif listOrder[0] == 'add':
        if len(listOrder)<2:
            print("Please enter filename")
            return

        if not os.path.exists(listOrder[1]):
            print("Your entering file is not exist, please confirm your file name")

        else:
            s.send(order.encode())
            file_send(listOrder[1])
            print('add '+listOrder[1]+' successfully')

    elif listOrder[0] == 'change':
        #listOrder[2] is new file, listOrder[1] is old file
        if not os.path.exists(listOrder[2]):
            print("Your entering new-file is not exist, please confirm your file name")

        else:
            s.send(order.encode())
            check = (s.recv(1024)).decode()
            print(check)
            if(check == 'unable'):
                print("Your entering old-file is not exist, please confirm your file name")

            elif(check == 'enable'):
                file_send(listOrder[2])
                print('change' + ' ' + listOrder[1] + ' ' + 'into' + ' ' + listOrder[2] + ' ' + 'successfully')

    elif listOrder[0] == 'delete':
        if len(listOrder)<2:
            print("Please enter filename")
            return
        s.send(order.encode())
        message = (s.recv(1024)).decode()
        print(message)

    elif listOrder[0] == 'get':
        if len(listOrder)<2:
            print("Please enter filename")
            return
        s.send(order.encode())
        check = (s.recv(1024)).decode()
        if (check == 'unable'):
            print("Your entering getting file is not exist, please confirm your file name")

        elif (check == 'enable'):
            file_get()
            print('get '+listOrder[1]+' successfully')

while True:

    Order = input('Please Enter orders:\r\n')
    #s.send(Order.encode())
    order_check(Order)
    #s.send(Order.encode())
