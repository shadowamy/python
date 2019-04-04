# -*- coding: UTF-8 -*-

from imageai.Detection import ObjectDetection
import os
import socket
import keras

#翻译列表 列表中的'':''表示无法识别
Translate={'person':'人',  'bicycle':'自行车',  'car':'汽车',  'motorcycle':'摩托车',  'airplane':'飞机',  'bus':'公共汽车', 'train':'火车',
           'truck':'卡车',  'boat':'船', 'traffic light':'红绿灯',  'fire hydrant':'消防栓',  'stop sign':'停车标志',  'parking meter':'停车计时器',
           'bench':'长凳',  'bird':'鸟',  'cat':'猫',  'dog':'狗',  'horse':'马',  'sheep':'羊',  'cow':'牛',  'elephant':'大象',
           'bear':'熊', 'zebra':'斑马', 'giraffe':'长颈鹿',  'backpack':'背包',  'umbrella':'雨伞', 'handbag':'手提包', 'tie':'领带',
           'suitcase':'手提箱',  'frisbee':'飞盘',  'skis':'滑雪板', 'snowboard':'滑雪板',  'sports ball':'运动球',  'kite':'风筝',
           'baseball bat':'棒球棒',  'baseball glove':'棒球手套',  'skateboard':'滑板', 'surfboard':'冲浪板',  'tennis racket':'网球拍',
           'bottle':'瓶子', 'wine glass':'酒杯',  'cup':'杯子', 'fork':'叉', 'knife':'刀', 'spoon':'勺子',  'bowl':'碗',
           'banana':'香蕉',  'apple':'苹果', 'sandwich':'三明治', 'orange':'橙色', 'broccoli':'西兰花', 'carrot':'胡萝卜', 'hot dog':'热狗',
           'pizza':'披萨',  'donut':'甜甜圈', 'cake':'蛋糕', 'chair':'椅子','couch':'沙发', 'potted plant':'盆栽植物', 'bed':'床',
           'dining table':'餐桌',  'toilet':'厕所', 'tv':'电视', 'laptop':'笔记本电脑', 'mouse':'鼠标', 'remote':'遥控器', 'keyboard':'键盘',
           'cell phone':'手机', 'microwave':'微波炉', 'oven':'烤箱', 'toaster':'烤面包机', 'sink':'水池', 'refrigerator':'冰箱',
           'book':'书', 'clock':'时钟', 'vase':'花瓶',  'scissors':'剪刀', 'teddy bear':'泰迪熊',  'hair drier':'吹风机',
           'toothbrush':'牙刷','':'data_lack'}

keras.backend.clear_session()

#导入图像模型
execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
#detector.loadModel(detection_speed="fastest")
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))

print("model loading...")
detector.loadModel()
print("loading successful!!!")

#创建socket server

tcpServerSocket=socket.socket()#创建socket对象
host = 'localhost'#获取本地主机名
print(host)
port=12345#设置端口
tcpServerSocket.bind((host,port))#将地址与套接字绑定，且套接字要求是从未被绑定过的
tcpServerSocket.listen(5)#代办事件中排队等待connect的最大数目

while True:

    print("server listening...")
    c, addr = tcpServerSocket.accept()
    print('连接地址：', addr)

    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "img/rasp.jpg"),
                                                 output_image_path=os.path.join(execution_path, "img/image2new.jpg"))
    result = "";
    maxNum = 0;
    for eachObject in detections:
        if (eachObject["percentage_probability"] > maxNum):
            maxNum = eachObject["percentage_probability"]
            source = eachObject["name"]
            result = Translate[source]
    print(result)

    c.send(result.encode("GBK"))
    c.close()
