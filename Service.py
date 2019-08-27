import json
import time
import winerror
import servicemanager
import win32serviceutil
import win32service
import win32event
import os
import sys
import time
import configparser
from ImageDB.sql import SQLImage
import os
import cv2
from io import BytesIO
from utils import helpers
from utils.processing import Processing
from model.model import Model
import matplotlib.pylab as plt
from datetime import datetime
from  PIL import Image

from datetime import datetime

import numpy as np


class ServiceSeg(win32serviceutil.ServiceFramework):  # 继承win32serviceutil.ServiceFramework类
    # 服务名

    config = configparser.ConfigParser()
    config.read("D:/codepython/Segmentation/properties.conf")
    _svc_name_ = config["service"]["name"]
    # 服务在windows系统中显示的名称
    _svc_display_name_ = config["service"]["DisplayName"]
    # 服务的描述
    _svc_description_ = config["service"]["Description"]


    def __init__(self, args):

        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        config = configparser.ConfigParser()
        config.read("D:/codepython/Segmentation/properties.conf")

        self.config = config
        self.model = Model(self.config)
        self.run = True

        # Delete_record(database=self.database).delet_info()

    def SvcDoRun(self):

        sql = SQLImage(self.config)
        while (self.run):

            results = sql.SelectInput()

            if results!=[]:
                res= results[-1]
                image_id = res[0]
                bytesImage = res[1]

                image = plt.imread(BytesIO(bytesImage), "jpg")

                image = cv2.resize(image, (int(self.config["image"]["width"]),
                                           int(self.config["image"]["height"])))

                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                input_image = np.expand_dims(image, axis=0) / 255.0

                output_image = self.model.run(input_image)

                # 得到返回图片结果，并转为array类型，取后三维度结果，shape (conf.with,cong.height,2)
                output_image = np.array(output_image[0, :, :, :])
                mask = Processing.process(output_image, self.config)
                _, buf = cv2.imencode(".jpg", mask)
                img_bin = Image.fromarray(np.uint8(buf)).tobytes()
                if sql.SelectOutput()!=[]:
                    sql.UpdateOutput(image=img_bin, id=image_id)
                else:
                    sql.InsertOutput(image=img_bin,id=image_id)

            else:
                time.sleep(0.5)

    def SvcStop(self):
        # 先告诉SCM停止这个过程
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 设置事件
        self.model.close()
        win32event.SetEvent(self.hWaitStop)
        self.run = False


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(ServiceSeg)
