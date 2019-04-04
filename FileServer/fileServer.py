# -*- coding: UTF-8 -*-
import socket, time, socketserver, struct
import os, threading

host = 'localhost'
port = 12307
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型
s.bind((host, port))  # 绑定需要监听的Ip和端口号，tuple格式
s.listen(1)
fileHouse = 'fileHouse'

def file_send(connection, filepath):
    #filepath = fileHouse+'\\\\'+ filepath_temp
    #filepath = os.path.join(fileHouse, filepath_temp)
    if os.path.isfile(filepath):
        #fileinfo_size = struct.calcsize('128sl')  # 定义打包规则
        # 定义文件头信息，包含文件名和文件大小
        fhead = struct.pack('128sl', os.path.basename(filepath.encode()), os.stat(filepath.encode()).st_size)
        connection.send(fhead)
        print('client filepath: ', filepath)
        # with open(filepath,'rb') as fo: 这样发送文件有问题，发送完成后还会发一些东西过去
        fo = open(filepath, 'rb')
        while True:
            filedata = fo.read(1024)
            if not filedata:
                break
            connection.send(filedata)
        fo.close()
        print('send over...')

def add_thread(connection, address):

    connection.settimeout(600)
    fileinfo_size = struct.calcsize('128sl')
    buf = connection.recv(fileinfo_size)
    if buf:  # 如果不加这个if，第一个文件传输完成后会自动走到下一句
        filename, filesize = struct.unpack('128sl', buf)
        filename_f = (filename.decode()).strip('\00')
        #filenewname = os.path.join('./', filename_f)
        filenewname = os.path.join(fileHouse, filename_f)
        print ('file new name is %s, filesize is %s' % (filenewname, filesize))
        recvd_size = 0  # 定义接收了的文件大小
        file = open(filenewname, 'wb')
        print ('start receiving...')
        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                rdata = connection.recv(1024)
                recvd_size += len(rdata)
            else:
                rdata = connection.recv(filesize - recvd_size)
                recvd_size = filesize
            file.write(rdata)
        file.close()
        print ('receive done')
        # connection.close()

def show_thread(connection):
    filelist = os.listdir(fileHouse)
    filestr = ' '.join(filelist)
    connection.send(filestr.encode())
    print('show file list successfully')

def delete_thread(connection, filename_temp):
    filename = fileHouse + '\\\\' + filename_temp
    if not os.path.exists(filename):
        message = 'Your entering file is not exist, please confirm your file name'

    else:
        os.remove(filename)
        message = 'delete'+' '+filename+' '+'successfully'
        print(message)

    connection.send(message.encode())

def change_thread(connection, address, listOrder):
    oldfilename_or = listOrder[1]
    oldfilename = fileHouse + '\\\\' + oldfilename_or
    newfilename = listOrder[2]
    if not os.path.exists(oldfilename):
        connection.send('unable'.encode())
    else:
        connection.send('enable'.encode())
        os.remove(oldfilename)
        add_thread(connection, address)
        print('change'+' '+oldfilename_or+' '+'into'+' '+newfilename+' '+'successfully')

def get_thread(connection, address, filename_temp):
    filename = fileHouse+'\\\\'+filename_temp
    #filename = os.path.join(fileHouse, filename_temp)
    if not os.path.exists(filename):
        connection.send('unable'.encode())

    else:
        connection.send('enable'.encode())
        file_send(connection, filename)

def quit_thread(connection):
    connection.close()
    print("The fileHouse system exit...")
    os._exit(0)

def order_thread(connection, address):
    while True:
        try:
            connection.settimeout(600)
            order = connection.recv(512)
            #print (order.decode())
            listOrder = (order.decode()).split()
            if listOrder[0] == 'show':
                show_thread(connection)

            elif listOrder[0] == 'add':
                add_thread(connection, address)

            elif listOrder[0] == 'change':
                change_thread(connection, address, listOrder)

            elif listOrder[0] == 'delete':
                delete_thread(connection, listOrder[1])

            elif listOrder[0] == 'get':
                get_thread(connection, address, listOrder[1])

            elif listOrder[0] == 'quit':
                quit_thread(connection)

        except socket.timeout:
            connection.close()

while True:
    connection, address = s.accept()
    print('Connected by ', address)
    #thread = threading.Thread(target=conn_thread,args=(connection,address)) #使用threading也可以
    thread = threading.Thread(target=order_thread, args=(connection, address))
    thread.start()

s.close()