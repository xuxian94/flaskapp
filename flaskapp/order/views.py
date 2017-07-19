#!/usr/bin/python
# -*- coding:utf8 -*-
from flask import render_template, request, Blueprint
from models import *

blueprint = Blueprint('order', __name__, static_folder='../static/order')


@blueprint.route('/index')
def blank():
    """
        路由：index.html
        初始主页，即分页第一页
        分页显示了所有数据
    """
    pagination = select_paginate(1)
    return render_template('order/index.html', title='三螺旋', pagination=pagination)


@blueprint.route('/search/<int:page>')
def search(page):
    """
        路由：all.html
        地区复选框功能
    """
    if not page :
        page =1
    info_address_list,info_address = select_address_checkbox(page)
    return render_template('order/search.html', title='三螺旋', pagination=info_address_list,con = info_address)


@blueprint.route('/<int:page>')
def company(page):
    """
        路由：index.html
        按page定位到第几页进行显示
    """
    pagination = select_paginate(page)
    return render_template('order/index.html', title='三螺旋', pagination=pagination)


@blueprint.route('/order_confirm')
def about():
    """
        路由：order_confirm.html
        跳转订单确认页面
    """
    return render_template('order/order_confirm.html')


@blueprint.route('/order_list')
def order():
    """
        路由：order_list.html
        跳转订单列表页面
    """
    return render_template('order/order_list.html')


@blueprint.route('/<string:con>/<int:page>')
def add(con, page):
    """
        路由：add.html
        按地址或公司名查询
        返回结果在add.html中显示
    """
    # pagination = search_engine(area, page)
    pagination = select_paginate_by_add(con, page)
    return render_template('order/add.html', title="三螺旋", pagination=pagination, name=con)


@blueprint.route('/demand')
def demand():
    """
        路由：
        触发搜索
        返回add方法
    """
    content = request.args.get('requirement')
    return add(content, 1)
