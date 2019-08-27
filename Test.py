
import cv2
import numpy as np
from ImageDB.sql import SQLImage
import os

from io import BytesIO
from utils import helpers
from utils.processing import Processing
from model.model import Model
import matplotlib.pylab as plt
import time
from  PIL import Image
import configparser
class Test(object):
    def __init__(self):

      self.config = configparser.ConfigParser()
      self.config.read("properties.conf")

    def build(self):


      '''
      主函数用于场景分割
        输入：
          图片路径
        输出
          分割结果
      :param path:
      :return:
   '''

      model = Model(self.config)

      results= SQLImage(self.config).SelectInput()

      for res in results:
        image_id = res[0]
        bytesImage = res[1]
        image = plt.imread(BytesIO(bytesImage), "jpg")


        image  = cv2.resize(image,(int(self.config["image"]["width"]),
                                   int(self.config["image"]["height"])))



        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


        input_image = np.expand_dims(image, axis=0) / 255.0

        output_image = model.run(input_image)

        # 得到返回图片结果，并转为array类型，取后三维度结果，shape (conf.with,cong.height,2)
        output_image = np.array(output_image[0,:,:,:])
        mask =  Processing.process(output_image,self.config)
        result = cv2.addWeighted(image, 0.7, mask, 0.3, 0)
        result = cv2.cvtColor(np.uint8(result), cv2.COLOR_RGB2BGR)
        _, buf = cv2.imencode(".jpg",result)
        img_bin = Image.fromarray(np.uint8(buf)).tobytes()

        SQLImage(self.config).InsertOutput(image=img_bin,id=image_id)
        # plt 显示
        cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        cv2.imshow("result", result)
        if cv2.waitKey(1) & 0xFF == ord("q"):
          break

      model.close()
if __name__ == "__main__":
  Test().build()