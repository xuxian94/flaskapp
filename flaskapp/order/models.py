#!/usr/bin/python
# -*- coding:utf8 -*-
from flask import request
from flaskapp.extensions import db
from sqlalchemy import or_
from flask_bootstrap import Bootstrap
import flask_whooshalchemyplus
from jieba.analyse.analyzer import ChineseAnalyzer


class Sheet_Form(db.Model):
    __tablename__ = 'info_jizhuan'
    __searchable__ = ['company', 'address']
    __analyzer__ = ChineseAnalyzer()

    id = db.Column(db.INTEGER, primary_key=True)
    company = db.Column(db.TEXT)
    url = db.Column(db.TEXT)
    tel = db.Column(db.TEXT)
    fax = db.Column(db.TEXT)
    mail = db.Column(db.TEXT)
    contacts = db.Column(db.TEXT)
    address = db.Column(db.TEXT)
    remarks = db.Column(db.TEXT)

    def __repr__(self):
        return '<Sheet_Form {}'.format(self.company)


# flask_whooshalchemyplus.whoosh_index(app, Sheet_Form)

def select_id(id):
    """
    按id查询数据库
    :param id: id
    :return: 对应id的数据
    """

    if id is not None:
        try:
            info = Sheet_Form.query.filter_by(id=id).first()
            return info
        except IOError:
            return None
        return None


def select_all():
    """
        方法：获取所有数据
    """
    try:
        info_all = Sheet_Form.query.all()
        return info_all
    except IOError:
        return None
    return None


def select_paginate(page):
    """
    获取第page页数据
    :param page: 页数
    :return: 分页后的数据
    """
    try:
        pagination = Sheet_Form.query.paginate(page, per_page=6, error_out=False)
        return pagination
    except IOError:
        return None
    return None


def select_paginate_by_add(con, page):
    """
    按照address或company字段的查询并分页显示功能
        可修改查询字段
        暂时替代搜索框的搜索
        在add页面中显示
    :param con: 搜索关键字
    :param page: 页数
    :return: 分页后的查询结果
    """

    try:
        pagination = Sheet_Form.query.filter(
            or_(Sheet_Form.address.like('%' + con + '%'), Sheet_Form.company.like('%' + con + '%'))).paginate(page,
                                                                                                              per_page=6,
                                                                                                              error_out=False)
        return pagination
    except IOError:
        return None
    return None


def search_engine(content, page):
    """
    综合搜索引擎
        尚未完成
    :param content: 搜索关键字
    :param page: 页数
    :return: 分页后的查询结果
    """
    pagination = Sheet_Form.query.whoosh_search(content).paginate(page, per_page=6, error_out=False)
    return pagination


def select_address_checkbox(page):
    """
    地区复选框搜索功能
    :param page: 页数
    :return: 分页后的查询结果
    """


    info_address = request.values.getlist("address")
    naginations = []

    # for info_address in info_address_all:
    #     info=Sheet_Form.query.filter(Sheet_Form.address.like('%'+info_address+'%'))
    #     naginations.append(info)
    info = Sheet_Form.query.filter(Sheet_Form.address.like('%' + info_address[0] + '%')).paginate(page, per_page=6,
                                                                                                  error_out=False)
    # return naginations
    return info, info_address[0]


if __name__ == '__main__':
    abc = select_id(1)
    print abc.company
    print select_id(2).company
