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

class Institution_Form(db.Model):
    __tablename__ = 'info_institution'
    #__searchable__ = ['company', 'address']
    __analyzer__ = ChineseAnalyzer()

    id = db.Column(db.INTEGER, primary_key=True)
    institution_name = db.Column(db.TEXT)
    institution_introduction = db.Column(db.TEXT)
    institution_history = db.Column(db.TEXT)
    institution_research_area = db.Column(db.TEXT)

    def __repr__(self):
        return '<Institution_Form {}'.format(self.institution_introduction, self.institution_history, self.institution_research_area)


# flask_whooshalchemyplus.whoosh_index(app, Sheet_Form)

def select_id(id):
    """
    按id查询数据库表info_jizhuan
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


def select_box():
    """
    根据用户自定义搜索内容进行查找
    :return: 按照搜索内容的关键词进行搜索的相关专家或者学校（机构）陈列页面
    """
    info_text = request.values.get("condition")
    print info_text
    info = Sheet_Form.query.filter(Sheet_Form.company.like('%' +info_text +'%')).paginate(per_page=6, error_out=False)
    return info

def select_address_checkbox(page):
    """
    地区复选框搜索功能
    :param page: 页数
    :return: 分页后的查询结果
    """

    info_address = request.values.getlist("address")
    info = Sheet_Form.query.filter(Sheet_Form.address.like('%' + info_address[0] + '%')).paginate(page, per_page=6, error_out=False)
    return info, info_address[0]

def select_institution():
    """
    对机构信息的展示
    :return: 当前查看机构的简介，历史，主研方向
    """

    # current_institution = request.values.get('institution')
    info_insti = Institution_Form.query.filter().first()   #paginate(per_page=6, error_out=False)
    return info_insti

if __name__ == '__main__':
    abc = select_id(1)
    print abc.company
    print select_id(2).company
