import  cv2

from utils import helpers
import numpy as np


class Processing(object):

    # 输入一个config,image返回一个mask
    @staticmethod
    def process(image,config):


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

            # 对于最后维度的双通道，返回其最大值所在下标，这里就完成了分割，对于每个位置上的点，0表示轨道，1表示背景
        output_image = helpers.reverse_one_hot(image)

        # 上色
        out_vis_image = helpers.colour_code_segmentation(output_image, eval(config["image"]["label_values"]))

        #
        out_vis_image = cv2.cvtColor(np.uint8(out_vis_image), cv2.COLOR_RGB2BGR)

        mask = np.zeros(out_vis_image.shape).astype(np.uint8)  # 得到一张全黑的背景

        # 非极大值抑制得到连通区域最大的轮廓
        postion = nms(out_vis_image)

        # 填充颜色
        _ = cv2.fillPoly(mask, [postion], eval(config["image"]["color"]), cv2.LINE_AA)
        return mask


