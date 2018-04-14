from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from SuperAdmin.sites import site
from SuperAdmin import app_setup, form_handle
from UserManager.permission import check_permission
app_setup.app_discover()


@login_required
@check_permission
def app_form_list(request, appname):
    models_name = site.display.get(appname)
    print(models_name)
    for i in models_name:
        print(i)

    return render(request, 'SuperAdmin/app_form.html', {'modelsname': models_name, 'appname': appname})


@login_required
@check_permission
def table_list(request, appname, modelname):
    admin_dict = site.display[appname][modelname]
    model_class = admin_dict['model']
    admin_class = admin_dict['admin_class']

    if request.method == 'POST':
        query_dict = request.POST
        action = query_dict.get('action')
        if action:
            selected_objs_num = dict(query_dict).get('select_obj')      # query_dict.get('select_obj')只能获取到列表中最后一个值
            querysets = model_class.objects.filter(id__in=selected_objs_num)
            action_func = getattr(admin_class(), action)
            page_obj = action_func(request, querysets)
            if page_obj:
                return page_obj
        else:
            objs_num = dict(query_dict).get('obj_num')
            obj_del = model_class.objects.filter(id__in=objs_num)
            obj_del.delete()

    querysets = model_class.objects.all().order_by('-id')

    # 过滤
    # todo filter_conditions
    filter_conditions = {}
    for key, value in request.GET.items():
        if key not in ('_page', '_o', '_q'):
            if value:
                filter_conditions[key] = value

    querysets = querysets.filter(**filter_conditions)

    # 搜索
    search_key = request.GET.get('_q', '')
    if search_key:
        q = Q()
        q.connector = 'OR'
        for search_field in admin_class.search_fields:
            q.children.append(('%s__contains' % search_field, search_key))
        querysets = querysets.filter(q)

    # 排序
    order_column = request.GET.get('_o')
    column_number = 0
    if order_column:
        column_list = admin_class.list_display
        column_number = int(order_column)
        column_name = column_list[abs(column_number)-1]
        order_key = column_name
        if order_column.startswith('-'):
            order_key = '-' + column_name
        querysets = querysets.order_by(order_key)

    # 分页
    paginator = Paginator(querysets, 5)
    page = request.GET.get('_page')
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        querysets = paginator.page(1)
    except EmptyPage:
        querysets = paginator.page(paginator.num_pages)

    params = {
        'appname':appname,
        'search_key': search_key,
        'column_number': column_number,
        'modelname': modelname,
        'querysets': querysets,
        'admin_class': admin_class,
        'model_class': model_class,
        'url': request.get_full_path(),
        'filter_condition': filter_conditions,
     }
    return render(request, 'SuperAdmin/table_list.html', params)


@login_required
@check_permission
def obj_change(request, appname, modelname, obj_id):
    admin_dict = site.display[appname][modelname]
    model_class = admin_dict['model']
    obj = model_class.objects.get(id=obj_id)
    admin_class = admin_dict['admin_class']

    DynamicModelForm = form_handle.create_dynamic_model_form(model_class, admin_class, form_add=False)
    if request.method == 'GET':
        form_obj = DynamicModelForm(instance=obj)
    elif request.method == 'POST':
        form_obj = DynamicModelForm(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('table_list', appname, modelname)

    return render(request, 'SuperAdmin/obj_change.html', locals())


@login_required
@check_permission
def obj_add(request, appname, modelname):
    admin_dict = site.display[appname][modelname]
    model_class = admin_dict['model']
    admin_class = admin_dict['admin_class']

    DynamicModelForm = form_handle.create_dynamic_model_form(model_class, admin_class)
    if request.method == 'GET':
        form_obj = DynamicModelForm()
    elif request.method == 'POST':
        form_obj = DynamicModelForm(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('table_list', appname, modelname)

    return render(request, 'SuperAdmin/obj_add.html', locals())


@login_required
@check_permission
def obj_delete(request, appname, modelname, obj_id):
    admin_dict = site.display[appname][modelname]
    model_class = admin_dict['model']
    admin_class = admin_dict['admin_class']
    obj = model_class.objects.get(id=obj_id)
    url = request.get_full_path().replace('delete', 'change')

    if request.method == 'GET':
        return render(request, 'SuperAdmin/obj_delete.html', locals())
    elif request.method == 'POST':
        obj.delete()
        return redirect('table_list', appname, modelname)


def acc_login(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('superadmin')
        else:
            msg = '用户名或密码错误'

    return render(request, 'SuperAdmin/login.html', context={'error_msg': msg})


def acc_logout(request):
    logout(request)
    return redirect('acc_login')


@login_required
def index(request):
    return render(request, 'SuperAdmin/superadmin_index.html', {'site': site})
