
import cv2
import numpy as np
import time
import requests
from utils import helpers
import matplotlib.pylab as plt


class config(object):
  def __init__(self):
    self.width = 352 # 图片宽
    self.height = 288 #图片高
    self.color = (255,240,0) # 掩模颜色
    self.url  = "http://127.0.0.1:8500" #请求url 端口8500
    self.label_values = [[255,255,255],[0,0,0]]  # label标签，没啥用


def SetJson(image):
  '''
  用于拼接成json格式
  :param image: 输入resize后的图片
  :return: 返回json数据
  '''
  input_image = np.expand_dims(np.float32(image), axis=0) / 255.0
  input_image = input_image.tolist()
  json_data = {"model_name": "default"}
  image_data = {"images": input_image}
  json_data["data"] = image_data
  return json_data


def nms(input_image):
  '''
  非极大值抑制用于找寻mask连通区域最大的一块
  输入：
    原始图像
  输出：
    连通区域最大的一块轮廓
  '''
  if len(input_image.shape) == 3:
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
  # 二值化处理
  res, input_image = cv2.threshold(input_image, 127, 255, 0)
  kernel = np.ones((5, 5), np.uint8)
  # 形态学处理腐蚀
  input_image = cv2.morphologyEx(input_image, cv2.MORPH_OPEN, kernel)
  input_image = cv2.morphologyEx(input_image, cv2.MORPH_CLOSE, kernel)

  # 找轮廓
  contours, hierachy = cv2.findContours(input_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

  # 遍历返回最大连通区域
  max_area = 0
  temp = 0
  for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > max_area:
      max_area = area
      temp = cnt
  return temp

def main(path):

  '''
  主函数用于场景分割
    输入：
      图片路径
    输出
      分割结果
  :param path:
  :return:
  '''
  conf = config()
  vid = cv2.VideoCapture(path)
  if not vid.isOpened():
    raise IOError("Can not open webcam or video")

  while True:
    return_value, frame = vid.read()
    image  = cv2.resize(frame,(conf.width,conf.height))
    json_data = SetJson(image)
    start_time = time.time()
    result = requests.post(conf.url, json=json_data)

    print("cost time:%s"%(str(time.time()-start_time)))
    # 得到返回图片结果，并转为array类型，取后三维度结果，shape (conf.with,cong.height,2)
    output_image = np.array(result.json()["prediction"])[0,:,:,:]

    # 对于最后维度的双通道，返回其最大值所在下标，这里就完成了分割，对于每个位置上的点，0表示轨道，1表示背景
    output_image = helpers.reverse_one_hot(output_image)

    # 上色
    out_vis_image = helpers.colour_code_segmentation(output_image, conf.label_values)

    #
    out_vis_image = cv2.cvtColor(np.uint8(out_vis_image), cv2.COLOR_RGB2BGR)

    mask = np.zeros(out_vis_image.shape).astype(np.uint8)  #得到一张全黑的背景

    # 非极大值抑制得到连通区域最大的轮廓
    postion = nms(out_vis_image)

    # 填充颜色
    _ = cv2.fillPoly(mask, [postion], conf.color, cv2.LINE_AA)
    result = cv2.addWeighted(image, 0.7, mask, 0.3, 0)
    result = cv2.cvtColor(np.uint8(result), cv2.COLOR_RGB2BGR)

    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.imshow("result", result)
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break
    # # plt 显示
    # plt.imshow(result,cmap="gray")
    # plt.show()

if __name__ == "__main__":
  main(path="./video/4Videolog.avi")