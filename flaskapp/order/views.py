#!/usr/bin/python
# -*- coding:utf8 -*-
from flask import render_template, Blueprint
from flask_login import login_required
from models import *

blueprint = Blueprint('order', __name__, static_folder='../static/order')


@blueprint.route('/searchbox1/<int:page>')
@login_required
def searchbox1(page):
    """
    用户自定义搜索，根据专家名称进行模糊搜索
    :return: 专家搜索结果的陈列页面
    """
    basic_info = Basic_info()

    # 初次运行网站时执行，获得专家图片缓存（路径：'flaskapp/static/order/avator/'）
    # Avator.init_avator()

    expert_name = request.values.get('condition1')
    if not expert_name:
        expert_name = ""
    pagination = basic_info.search_box(expert_name).paginate(page=page, per_page=6, error_out=False)
    return render_template('order/index.html', title='三螺旋', expert_name=expert_name, pagination=pagination)

# @blueprint.route('/order_confirm')
# @login_required
# def about():
#     """
#         路由：order_confirm.html
#         跳转订单确认页面
#     """
#     return render_template('order/order_confirm.html')


# @blueprint.route('/order_list')
# @login_required
# def order():
#     """
#         路由：order_list.html
#         跳转订单列表页面
#     """
#     return render_template('order/order_list.html')


# @blueprint.route('/<string:con>/<int:page>')
# @login_required
# def add(con, page):
#     """
#         路由：add.html
#         按地址或公司名查询
#         返回结果在add.html中显示
#     """
#     # pagination = search_engine(area, page)
#     pagination = select_paginate_by_add(con, page)
#     return render_template('order/add.html', title="三螺旋", pagination=pagination, name=con)


# @blueprint.route('/demand')
# @login_required
# def demand():
#     """
#         路由：
#         触发搜索
#         返回add方法
#     """
#     content = request.args.get('requirement')
#     return add(content, 1)

@blueprint.route('/profile/<int:id>')
@login_required
def profile(id):
    info = Professor(id, 'avator/')
    return render_template('order/profile.html', title="三螺旋", info=info)


@blueprint.route('/searchbox2/<int:page>')
@login_required
def searchbox2(page):
    """
    用户自定义搜索，根据重点实验室名称进行模糊搜索
    :return: 实验室陈列页面
    """
    lab_info = Lab_Form()
    lab_name = request.values.get('condition2')
    if not lab_name:
        lab_name = ""
    pagination = lab_info.search_box(lab_name).paginate(page=page, per_page=6, error_out=False)
    return render_template('laboratory/lab_search.html', title='三螺旋', lab_name = lab_name, pagination=pagination)

@blueprint.route('/lab_infoshow/<string:name>')
def lab_infoshow(name):
    labform = Lab_Form()
    info = labform.get_info(name=name)
    return render_template('laboratory/lab_infoshow.html', title="三螺旋", info=info)



