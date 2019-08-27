
import sys
import os
from utils.uuid import UUID
import pymssql

import configparser
from datetime import datetime



class SQLImage(object):
    # 传入一个ConfigParser类
    # 或者传入一个.conf配置文件

    def __init__(self,config):
        if type(config)==configparser.ConfigParser:
            self.config = config
        else:
            if not os.path.exists(config):
                raise FileExistsError("Can not find %s"%config)
            self.config=configparser.ConfigParser()
            self.config.read(config)


    def SelectOutput(self):


        conn = pymssql.connect(server=self.config["sqlserver"]["ip"],
                               user=self.config["sqlserver"]["user"],
                               password=self.config["sqlserver"]["password"],
                               database=self.config["sqlserver"]["db"])
        cursor = conn.cursor()
        try:

            insert_string = (" Select * from outputimage")
            cursor.execute(insert_string)
            values = cursor.fetchall()

            return values
            # 如果数据库没有设置自动提交，这里要提交一下


        except EOFError as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def SelectInput(self):


        conn = pymssql.connect(server=self.config["sqlserver"]["ip"],
                               user=self.config["sqlserver"]["user"],
                               password=self.config["sqlserver"]["password"],
                               database=self.config["sqlserver"]["db"])
        cursor = conn.cursor()
        try:

            insert_string = (" Select * from inputimage")
            cursor.execute(insert_string)
            values = cursor.fetchall()

            return values
            # 如果数据库没有设置自动提交，这里要提交一下


        except EOFError as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    def InsertInput(self,path):




        if not os.path.exists(path):
            raise FileExistsError(path)
        with open(path,"rb") as f:
            image = f.read()

        conn=pymssql.connect(server=self.config["sqlserver"]["ip"],
                                      user=self.config["sqlserver"]["user"],
                                       password=self.config["sqlserver"]["password"],
                                       database=self.config["sqlserver"]["db"])
        cursor = conn.cursor()


        try:

            insert_string =(" INSERT INTO inputimage (image_id,image,datetime) " \
                        "values (%s,%s,%s)")
            string_info = (UUID.get(), image, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))




            cursor.execute(insert_string,string_info)
            # 如果数据库没有设置自动提交，这里要提交一下
            conn.commit()
        except EOFError as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def UpdateOutput(self,image,id):


        conn = pymssql.connect(server=self.config["sqlserver"]["ip"],
                               user=self.config["sqlserver"]["user"],
                               password=self.config["sqlserver"]["password"],
                               database=self.config["sqlserver"]["db"])
        cursor = conn.cursor()

        try:

            insert_string = (" UPDATE outputimage SET image_id=%s, image=%s, datetime=%s " \
                             "WHERE image_id=%s")
            string_info = (id, image, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),id)

            cursor.execute(insert_string, string_info)
            # 如果数据库没有设置自动提交，这里要提交一下
            conn.commit()
        except EOFError as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def InsertOutput(self,image,id):


        conn = pymssql.connect(server=self.config["sqlserver"]["ip"],
                               user=self.config["sqlserver"]["user"],
                               password=self.config["sqlserver"]["password"],
                               database=self.config["sqlserver"]["db"])
        cursor = conn.cursor()

        try:

            insert_string = (" INSERT INTO outputimage (image_id,image,datetime) " \
                             "values (%s,%s,%s)")
            string_info = (id, image, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            cursor.execute(insert_string, string_info)
            # 如果数据库没有设置自动提交，这里要提交一下
            conn.commit()
        except EOFError as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


            # 关闭数据库连接



#SQLImage.Select()
#SQLImage("../properties.conf").InsertInput("../picture/42520.png")


