import serial
import time
import sqlOprate

#delta(100, 400)   极度疲劳和昏睡
#theta(30, 100)    意愿受挫或者抑郁以及精神病患者
#Alpha(2, 25)      清醒、安静并闭眼时该节律最为明显，睁开眼睛（受到光刺激）或接受其它刺激时，α波即刻消失
#Beta(1,20)        精神紧张和情绪激动或亢奋时出现此波，当人从噩梦中惊醒时

t = serial.Serial('com12',57600)
#t.open()
while True:
    data = t.read()
    if(data[0] and data[0] == 0x20):
        data2 = t.read(34)
        if(len(data2)>=31 and data2[0] == 0x02 and data2[2] == 0x83 and data2[3] == 0x18):
            #print(data2)
            Delta = data2[4]<<16 | data2[5]<<8 | data2[6]
            Theta = data2[7]<<16 | data2[8]<<8 | data2[9]
            LowAlpha = data2[10]<<16 | data2[11]<<8 | data2[12]
            HighAlpha = data2[13]<<16 | data2[14]<<8 | data2[15]
            LowBeta = data2[16]<<16 | data2[17]<<8 | data2[18]
            HighBeta = data2[19]<<16 | data2[20]<<8 | data2[21]
            LowGamma = data2[22]<<16 | data2[23]<<8 | data2[24]
            MiddleGamma = data2[25]<<16 | data2[26]<<8 | data2[27]
            Attention = data2[29]
            Meditation = data2[31]

            if(MiddleGamma != 0):
                rela_Delta = (int)(Delta / MiddleGamma)
                rela_Theta = (int)(Theta / MiddleGamma)
                rela_LowAlpha = (int)(LowAlpha / MiddleGamma)
                rela_LowBeta = (int)(LowBeta / MiddleGamma)

                if (rela_Delta >400 or rela_Delta<100):
                    sqlOprate.eegOprate('delta', rela_Delta)

                elif (rela_Theta>100 or rela_Theta<30):
                    sqlOprate.eegOprate('theta', rela_Theta)

                elif (rela_LowAlpha > 25 or rela_LowAlpha < 2):
                    sqlOprate.eegOprate('alpha', rela_LowAlpha)

                elif (rela_LowBeta > 20 or rela_LowBeta < 1):
                    sqlOprate.eegOprate('beta', rela_LowBeta)

            #print(Delta, Theta, LowAlpha, HighAlpha, LowBeta, HighBeta, LowGamma, MiddleGamma, Attention, Meditation)
        time.sleep(0.1)
    #print(data)
