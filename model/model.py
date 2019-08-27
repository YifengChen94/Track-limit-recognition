import tensorflow as tf
import configparser
from builder.model_builder import build_model

class Model(object):

    def __init__(self,config):

        self.model = config["model"]["model"]
        self.num_classes = config["model"]["classes"]
        self.sess =tf.Session()
        self.crop_width = config["model"]["width"]
        self.crop_height =config["model"]["height"]
        self.frontend = config["model"]["frontend"]
        self.checkpoint_path  = config["model"]["checkpoint"]
        self.net_input = tf.placeholder(tf.float32,shape=[None,None,None,3])
        self.net_out = self.__build()

    def __build(self):




        network, _ = build_model(self.model, net_input=self.net_input,
                                                num_classes=self.num_classes,
                                                crop_width=self.crop_width,
                                                crop_height=self.crop_height,
                                                frontend= self.frontend,
                                                is_training=False)

        self.sess.run(tf.global_variables_initializer())

        print('Loading model checkpoint weights')
        saver=tf.train.Saver(max_to_keep=1000)
        saver.restore(self.sess, self.checkpoint_path)
        return network

    def run(self,image):
        feed_dict = {self.net_input: image}
        results = self.sess.run(self.net_out, feed_dict)
        return results

    def close(self):
        self.sess.close()