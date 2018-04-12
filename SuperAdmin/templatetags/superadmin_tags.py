from django.template import Library
from django.utils.safestring import mark_safe
import datetime
import re

register = Library()


@register.simple_tag
def build_table_row(model_obj, admin_class):
    elem = ''
    if admin_class.list_display:
        for index, column_name in enumerate(getattr(admin_class, 'list_display')):
            try:
                field_text = getattr(model_obj, 'get_%s_display' % column_name)()
            except:
                field_text = getattr(model_obj, column_name)
            finally:
                td_eme = "<td> %s </td>" % field_text
                if index == 0:
                    td_eme = "<td><a href='%s/change/'> %s </a></td>" % (model_obj.id, field_text)
                elem += td_eme
    else:
        td_eme = "<td><a href='%s/change/'> %s </a></td>" % (model_obj.id, model_obj)
        elem += td_eme
    return mark_safe(elem)

# 过滤
@register.simple_tag
def build_filter_column(filter_column, model_class, filter_condition):
    column_obj = model_class._meta.get_field(filter_column)
    try:
        filter_ele = "<select name='%s'>" % filter_column
        for choice_value, choice_display in column_obj.get_choices():
            selected = ''
            # if filter_column in filter_condition:
            if filter_condition.get(filter_column) == str(choice_value):
                selected = 'selected'

            option = "<option value='%s' %s>%s</option>" % (choice_value, selected, choice_display)
            filter_ele += option
    except AttributeError:
        filter_ele = "<select name='%s__gte'>" % filter_column
        if column_obj.get_internal_type() in ('DateField', 'DateTomeField'):
            datetime_obj = datetime.datetime.now()
            time_list = [
                ('', '----'),
                (datetime_obj, '今日'),
                (datetime_obj-datetime.timedelta(7), '七天内'),
                (datetime_obj.replace(day=1), '本月'),
                (datetime_obj-datetime.timedelta(90), '三个月内'),
                (datetime_obj.replace(month=1, day=1), '本年'),
            ]
            for time_v, time_k in time_list:
                time_str = '' if not time_v else '%s-%s-%s' % (time_v.year, time_v.month, time_v.day,)
                selected = ''
                if filter_condition.get('%s__gte' % filter_column) == time_str:
                    selected = 'selected'
                option = "<option value='%s' %s>%s</option>" % (time_str, selected, time_k)
                filter_ele += option

    filter_ele += "</select>"
    return mark_safe(filter_ele)


# 分页
@register.simple_tag
def make_pagelist(querysets, url):
    ele = ''
    for i in range(-2, 3):
        active = ''
        page_num = querysets.number + i
        if page_num in querysets.paginator.page_range:
            if page_num == querysets.number:
                active = 'active'
            new_url = make_page_url(url, page_num)
            option = '''<li class="%s"><a href="%s">%s</a></li>''' % (active, new_url, page_num)
            ele += option

    return mark_safe(ele)


# 排序标志
@register.simple_tag
def order_symbol(column, forloop_count):
    if column == forloop_count:
        directions = 'top'
    elif column == -forloop_count:
        directions = 'bottom'
    else:
        directions = ''
    ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>''' % directions
    return mark_safe(ele)


# ?date__gte=2018-4-2&contact=&consultant=&referral_from=&_o=2
@register.simple_tag
def make_order_url(url, column_number, forloop_counter):
    if column_number == forloop_counter:
        forloop_counter *= -1
    order_str = '_o='+str(forloop_counter)
    if '_page=' in url:
        url = re.sub(r'[&?]_page=(\d+)', '', url)
    if '/?' in url:
        if '_o=' in url:
            new_url = re.sub(r'_o=(-?\d+)', order_str, url)
        else:
            new_url = url + '&' + order_str
    else:
        new_url = url + '?' + order_str
    return new_url\



@register.simple_tag
def make_page_url(url, page_number):
    page = '_page=' + str(page_number)
    if '/?' in url:
        if '_page=' in url:
            new_url = re.sub(r'_page=(\d+)', page, url)
        else:
            new_url = url + '&' + page
    else:
        new_url = url + '?' + page
    return new_url


@register.simple_tag
def get_value(obj, row_name):
    return getattr(obj, row_name)
