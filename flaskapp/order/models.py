#!/usr/bin/python
# -*- coding:utf8 -*-
import os

from flask import request
from flaskapp.extensions import db
from sqlalchemy import or_
from jieba.analyse.analyzer import ChineseAnalyzer



class Basic_info(db.Model):
    __tablename__ = 'basic_info'

    id = db.Column(db.INTEGER, primary_key=True)
    avator = db.Column(db.TEXT)
    name = db.Column(db.TEXT)
    college = db.Column(db.TEXT)
    institute = db.Column(db.TEXT)
    tel = db.Column(db.TEXT)
    email = db.Column(db.TEXT)
    C = db.Column(db.INT)
    J = db.Column(db.INT)
    Q = db.Column(db.INT)

    def __repr__(self):
        return 'info:{},{}'.format(self.id, self.name)

    @staticmethod
    def get_basic_info(id, path):
        info = Basic_info.query.filter_by(id=id).first()

        college = info.college
        name = info.name
        avator = Avator.get_avator(id, path)
        institute = info.institute
        tel = info.tel
        email = info.email
        c = info.C
        j = info.J
        q = info.Q
        C = '长江学者' if c else ''
        J = '杰出青年' if j else ''
        Q = '千人计划' if q else ''
        return name, college, avator, institute, tel, email, C, J, Q

    def search_box(self, name):
        """
        根据搜索框对专家的模糊搜索
        :param name: 搜索框中输入的不完全专家名称
        :return: 通过模糊搜索之后得到结果的陈列
        """
        info = Basic_info.query.filter(or_(Basic_info.name.like('%' + name + '%')))
        return info

    # 返回对应id专家的详细信息
    # def get_basic_info(id):
    #     info = basic_info.query.filter_by(id=id).first()
    #
    #     college = info.college
    #     name = info.name
    #     institute = info.institute
    #     tel = info.tel
    #     email = info.email
    #     c = info.C
    #     j = info.J
    #     q = info.Q
    #     C = '长江学者' if c else ''
    #     J = '杰出青年' if j else ''
    #     Q = '千人计划' if q else ''
    #
    #     return college, name, institute, tel, email, C, J, Q

    @staticmethod
    # 返回id编号从a到b专家的查询结果，可以直接调用pignate
    def get_many(a, b):
        '''
        获得编号从a到b的专家的基本信息
        :param a:
        :param b:
        :return:
       '''
        # 查询专家基本信息的表
        info = Basic_info.query.filter(Basic_info.id >= a, Basic_info.id <= b)
        return info


class Avator(db.Model):
    __tablename__ = 'avator'

    id = db.Column(db.INTEGER, primary_key=True)
    img = db.Column(db.BLOB)

    def __repr__(self):
        return 'info_img:{}'.format(self.id)

    @staticmethod
    # 根据id获取头像信息
    def get_avator(id, path):
        '''
        根据id来获取对应专家的头像
        当数据据和缓存都没有时候，默认给一个空白头像
        :param id:  专家的id
        :param path: 存放头像缓存的路径,默认路径为'path/interface/avator'
        :return: 返回头像的对应的路径
        '''

        # 为头像缓存添加路径
        if not os.path.exists(path):
            os.mkdir(path)

        # 调用时返回的是调用函数的路径
        # root = os.getcwd()
        # print 'root', root
        # 头像缓存在get_avator中，如果存在就无需从数据库中获取了（以id.jpg的方式缓存）
        img_name = str(id) + '.jpg'
        avator_path = os.path.join(path, img_name)
        # print 'avator_path', avator_path

        if os.path.exists(avator_path):
            print img_name + ' is existed'
            return img_name
        # 缓存中没有，从数据库中获取
        else:
            try:
                img = Avator.query.filter_by(id=id).first().img
                avator = open(avator_path, 'wb')
                avator.write(img)
                avator.close()
                print 'get avator: ', img_name
                return img_name

            except:
                print 'cant find avator, plz give a blank one'
                return 'blank.jpg'

    @staticmethod
    def init_avator():
        info = Basic_info.query.filter(Basic_info.id >= 0).all()
        for data in info:
            Avator.get_avator(data.id, 'flaskapp/static/order/avator/')

class Details(db.Model):
    __tablename__ = 'details'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.TEXT)
    college = db.Column(db.TEXT)
    career = db.Column(db.TEXT)
    contribute = db.Column(db.TEXT)
    job = db.Column(db.TEXT)

    @staticmethod
    def get_details(id):
        try:
            pro = Details.query.filter_by(id=id).first()
            career = pro.career.split('。')
            contribute = pro.contribute.split('。')
            job = pro.job.split('。')
            return career, contribute, job
        except Exception as e:
            print e

class Professor():
    '''
    返回专家的信息
    get_many(a , b, path): 返回 id（a~b）之间的专家基本数据(query对象，可以接pagenate)
    init(id, path): 返回对应id专家的所有信息
    '''

    def __init__(self, id, path):
        self.id = id
        self.career, self.contribute, self.job = Details.get_details(id)
        self.name, self.college, self.avator, self.institute, self.tel, self.email, self.C, self.J, self.Q = Basic_info.get_basic_info(
            id, path)


class Lab_Form(db.Model):
    __tablename__ = 'info_lab'
    __analyzer__ = ChineseAnalyzer()

    id = db.Column(db.INTEGER, primary_key=True)
    lab_name =  db.Column(db.TEXT)
    lab_school = db.Column(db.TEXT)
    lab_introduction = db.Column(db.TEXT)
    lab_location = db.Column(db.TEXT)
    lab_postcode = db.Column(db.TEXT)
    lab_supportunit = db.Column(db.TEXT)
    lab_tel = db.Column(db.TEXT)
    lab_fax = db.Column(db.TEXT)
    lab_mail = db.Column(db.TEXT)
    lab_url = db.Column(db.TEXT)
    lab_director = db.Column(db.TEXT)
    lab_contactor = db.Column(db.TEXT)

    def __repr__(self):
        return '<Lab_Form {}'.format(self.lab_name, self.lab_school, self.lab_introduction,
                                     self.lab_location, self.lab_postcode, self.lab_supportunit,
                                     self.lab_director,self.lab_contactor)

    def get_info(self, name):
        """
        根据名称查询数据库
        :param name: 实验室名称
        :return: 实验室基本信息
        """
        info = Lab_Form.query.filter_by(lab_name=name).first()
        return info

    def select_info(self):
        """
        获取第page页数据
        :param page: 页数
        :return: 分页后的数据
        """
        try:
            info = Lab_Form.query
            return info
        except IOError:
            return None

    def search_box(self, name):
        """
        根据搜索框对实验室模糊搜索
        :param name: 搜索框中输入的不完全实验室名称
        :return: 通过模糊搜索之后得到结果的陈列
        """
        info = Lab_Form.query.filter(or_(Lab_Form.lab_name.like('%' + name + '%')))
        return info



