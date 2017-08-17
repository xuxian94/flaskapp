#!/usr/bin/python
# -*- coding:utf8 -*-
import os

from flask import request
from flaskapp.extensions import db
from sqlalchemy import or_
from jieba.analyse.analyzer import ChineseAnalyzer


class basic_info(db.Model):
    __tablename__ = 'basic_info'

    id = db.Column(db.INTEGER, primary_key=True)
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
    # 返回对应id专家的详细信息
    def get_basic_info(id):
        info = basic_info.query.filter_by(id=id).first()

        college = info.college
        name = info.name
        institute = info.institute
        tel = info.tel
        email = info.email
        c = info.C
        j = info.J
        q = info.Q
        C = '长江学者' if c else ''
        J = '杰出青年' if j else ''
        Q = '千人计划' if q else ''

        return college, name, institute, tel, email, C, J, Q

    @staticmethod
    # 返回id编号从a到b专家的查询结果，可以直接调用pignate
    def get_many(a, b):
        '''
        获得编号从a到b的专家的基本信息
        :param a:
        :param b:
        :return:
       '''
        # 单表查询，添加其他表好像没有用
        info = basic_info.query.filter(basic_info.id >= a, basic_info.id <= b)
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


class details(db.Model):
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
            pro = details.query.filter_by(id=id).first()
            career = pro.career.split('。')
            contribute = pro.contribute.split('。')
            job = pro.job.split('。')
            return career, contribute, job
        except Exception as e:
            print e

class Professor():
    """
    返回专家的信息
    get_many(a , b, path): 返回 id（a~b）之间的专家基本数据(query对象，可以接pagenate)
    init(id, path): 返回对应id专家的所有信息
    """

    def __init__(self, id, path='flaskapp/static/order/avator'):
        self.id = id

        self.career, self.contribute, self.job = details.get_details(id)

        self.college, self.name,  self.institute, self.tel, self.email, self.C, self.J, self.Q = basic_info.get_basic_info(
                    id)

        self.avator = Avator.get_avator(id, path)

        # 静态方法，
    @staticmethod
    def get_many(a, b, path):
        """

        :param a: 起始id
        :param b: 结束id
        :param path: 头像存放地址
        :return: basic_info表中的信息
        """
        # 获取id(a~b)的所有图片
        for i in range(a, b + 1):
            Avator.get_avator(i, path)

        return basic_info.get_many(a, b)

# class Sheet_Form(db.Model):
#     __tablename__ = 'info_jizhuan'
#     __searchable__ = ['company', 'address']
#     __analyzer__ = ChineseAnalyzer()
#
#     id = db.Column(db.INTEGER, primary_key=True)
#     company = db.Column(db.TEXT)
#     url = db.Column(db.TEXT)
#     tel = db.Column(db.TEXT)
#     fax = db.Column(db.TEXT)
#     mail = db.Column(db.TEXT)
#     contacts = db.Column(db.TEXT)
#     address = db.Column(db.TEXT)
#     remarks = db.Column(db.TEXT)
#
#     def __repr__(self):
#         return '<Sheet_Form {}'.format(self.company)
#
#     def select_institution(self):
#         """
#         获取关于机构第page页数据
#         :param page: 页数
#         :return: 分页后的数据
#         """
#         try:
#             info = Sheet_Form.query
#             return info
#         except IOError:
#             return None
#         return None
#
#     def get_info(self, id):
#         """
#         根据id搜索数据库
#         :param id: id
#         :return: 专家基本信息
#         """
#         info = Sheet_Form.query.filter_by(id=id).first()
#         return info
#
# class Lab_Form(db.Model):
#     __tablename__ = 'info_lab'
#     __analyzer__ = ChineseAnalyzer()
#
#     id = db.Column(db.INTEGER, primary_key=True)
#     lab_name =  db.Column(db.TEXT)
#     lab_school = db.Column(db.TEXT)
#     lab_introduction = db.Column(db.TEXT)
#     lab_location = db.Column(db.TEXT)
#     lab_postcode = db.Column(db.TEXT)
#     lab_supportunit = db.Column(db.TEXT)
#     lab_tel = db.Column(db.TEXT)
#     lab_fax = db.Column(db.TEXT)
#     lab_mail = db.Column(db.TEXT)
#     lab_url = db.Column(db.TEXT)
#     lab_director = db.Column(db.TEXT)
#     lab_contactor = db.Column(db.TEXT)
#
#     def __repr__(self):
#         return '<Lab_Form {}'.format(self.lab_name, self.lab_school, self.lab_introduction,
#                                      self.lab_location, self.lab_postcode, self.lab_supportunit,
#                                      self.lab_director,self.lab_contactor)
#
#     def get_info(self, name):
#         """
#         根据id搜索数据库
#         :param id: id
#         :return: 专家基本信息
#         """
#         info = Lab_Form.query.filter_by(lab_name=name).first()
#         return info
#
#     def select_info(self):
#         """
#         获取第page页数据
#         :param page: 页数
#         :return: 分页后的数据
#         """
#         try:
#             info = Lab_Form.query
#             return info
#         except IOError:
#             return None
#         return None
#
#
# # flask_whooshalchemyplus.whoosh_index(app, Sheet_Form)
#
# def select_id(id):
#     """
#     按id查询数据库表info_jizhuan
#     :param id: id
#     :return: 对应id的数据
#     """
#
#     if id is not None:
#         try:
#             info = Sheet_Form.query.filter_by(id=id).first()
#             return info
#         except IOError:
#             return None
#         return None
#
#
# def select_all():
#     """
#         方法：获取所有数据
#     """
#     try:
#         info_all = Sheet_Form.query.all()
#         return info_all
#     except IOError:
#         return None
#     return None
#
#
# def select_paginate(page):
#     """
#     获取第page页数据
#     :param page: 页数
#     :return: 分页后的数据
#     """
#     try:
#         pagination = Sheet_Form.query.paginate(page, per_page=6, error_out=False)
#         return pagination
#     except IOError:
#         return None
#     return None
#
#
# def select_paginate_by_add(con, page):
#     """
#     按照address或company字段的查询并分页显示功能
#         可修改查询字段
#         暂时替代搜索框的搜索
#         在add页面中显示
#     :param con: 搜索关键字
#     :param page: 页数
#     :return: 分页后的查询结果
#     """
#
#     try:
#         pagination = Sheet_Form.query.filter(
#             or_(Sheet_Form.address.like('%' + con + '%'), Sheet_Form.company.like('%' + con + '%'))).paginate(page,
#                                                                                                               per_page=6,
#                                                                                                               error_out=False)
#         return pagination
#     except IOError:
#         return None
#     return None
#
#
# def search_engine(content, page):
#     """
#     综合搜索引擎
#         尚未完成
#     :param content: 搜索关键字
#     :param page: 页数
#     :return: 分页后的查询结果
#     """
#     pagination = Sheet_Form.query.whoosh_search(content).paginate(page, per_page=6, error_out=False)
#     return pagination
#
#
# def select_box():
#     """
#     根据用户自定义搜索内容进行查找
#     :return: 按照搜索内容的关键词进行搜索的相关专家或者学校（机构）陈列页面
#     """
#     info_text = request.values.get("condition")
#     # print info_text
#     info = Sheet_Form.query.filter(Sheet_Form.company.like('%' +info_text +'%')).paginate(per_page=6, error_out=False)
#     return info
#
# def select_address_checkbox(page):
#     """
#     地区复选框搜索功能
#     :param page: 页数
#     :return: 分页后的查询结果
#     """
#
#     info_address = request.values.getlist("address")
#     info = Sheet_Form.query.filter(Sheet_Form.address.like('%' + info_address[0] + '%')).paginate(page, per_page=6, error_out=False)
#     return info, info_address[0]
#
#
# class Basic_Info_Form(db.Model):
#     """
#     人物基本信息表
#     """
#     __tablename__ = 'basic_info'
#
#     ID = db.Column(db.INTEGER, primary_key=True)
#     Name = db.Column(db.TEXT)
#     Sex = db.Column(db.TEXT)
#     Company = db.Column(db.TEXT)
#     Duty = db.Column(db.TEXT)
#     Tel = db.Column(db.TEXT)
#     Email = db.Column(db.TEXT)
#     web = db.Column(db.TEXT)
#
#     def __repr__(self):
#         return '<Basic_Info_Form {}'.format(self.Name)
#
#     def select_info(self):
#         """
#         获取第page页数据
#         :param page: 页数
#         :return: 分页后的数据
#         """
#         try:
#             info = Basic_Info_Form.query
#             return info
#         except IOError:
#             return None
#         return None
#
#     def select_address_radio(self, page):
#         """
#         地区复选框搜索功能
#         :param page: 页数
#         :return: 分页后的查询结果
#         """
#
#         info_address = request.values.getlist("address")
#         info = Basic_Info_Form.query.filter(Basic_Info_Form.Company.like('%' + info_address[0] + '%')).paginate(page,
#                                                                                                                 per_page=6,
#                                                                                                                 error_out=False)
#         # return naginations
#         return info, info_address[0]
#
#     def get_info(self, id):
#         """
#         根据id搜索数据库
#         :param id: id
#         :return: 专家基本信息
#         """
#         info = Basic_Info_Form.query.filter_by(ID=id).first()
#         return info
#
#
# class Avator(db.Model):
#     __tablename__ = 'avator'
#
#     ID = db.Column(db.INTEGER, primary_key=True)
#     img = db.Column(db.BLOB)
#
#     def __repr__(self):
#         return '<Avator {}'.format(self.id)
#
#     # 根据id获取头像信息
#     def get_avator(self, id, path='/Users/xuxian/doing/flaskapp/flaskapp/static/order/avator/'):
#         """
#         根据id来获取对应专家的头像
#         当数据据和缓存都没有时候，默认给一个空白头像
#         :param id:  专家的id
#         :param path: 存放头像缓存的路径,默认路径为'path/interface/avator'
#         :return: 返回头像的路径
#         """
#
#         # 为头像缓存添加路径
#         if not os.path.exists(path):
#             os.mkdir(path)
#
#         # 调用时返回的是调用函数的路径
#         # root = os.getcwd()
#         # print 'root', root
#         # 头像缓存在get_avator中，如果存在就无需从数据库中获取了（以id.jpg的方式缓存）
#         img_name = str(id) + '.jpg'
#         avator_path = os.path.join(path, img_name)
#         # print 'avator_path', avator_path
#
#         if os.path.exists(avator_path):
#             print avator_path
#             print img_name + ' is existed'
#             return img_name
#         # 缓存中没有，从数据库中获取
#         else:
#
#             try:
#                 img = Avator.query.filter_by(ID=id).first().img
#                 avator = open(avator_path, 'wb')
#                 avator.write(img)
#                 avator.close()
#                 print 'get avator: ', img_name
#                 return img_name
#
#             except:
#                 print 'cant find avator, plz give a blank one'
#                 return 'blank.jpg'


if __name__ == '__main__':

    info = Professor.get_many(0 ,1590, 'avator/').all()
