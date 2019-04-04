from socket import *
 
'''
    客户端
'''
# 创建socket
tcpClientSocket = socket(AF_INET,SOCK_STREAM)
 
# 连接服务器
serAddr = ("169.254.139.147",8080)
tcpClientSocket.connect(serAddr)
 
while True:
    # 提示用户输入输入
    sendData = input("请输入内容:")
    if len(sendData) > 0:
        tcpClientSocket.send(sendData.encode('utf8'))
    else:
        break
 
    # 接收对方发送的消息
    recv = tcpClientSocket.recv(1024)
    print("127.0.0.1:\n" + recv.decode('utf8'))
 
# 关闭套接字

