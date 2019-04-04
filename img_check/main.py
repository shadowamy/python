from imageai.Prediction import ImagePrediction
import os
import datetime

starttime = datetime.datetime.now()
execution_path = os.getcwd()

prediction = ImagePrediction()

prediction.setModelTypeAsResNet()

prediction.setModelPath( execution_path + "\\resnet50_weights_tf_dim_ordering_tf_kernels.h5")

prediction.loadModel()

predictions, percentage_probabilities = prediction.predictImage("D:\iot\competation\电子信息\py - 副本\photo.jpg", result_count=5)

for index in range(len(predictions)):

  print (str(predictions[index]) + " : " + str(percentage_probabilities[index]))

endtime = datetime.datetime.now()
print ((endtime - starttime).seconds)
