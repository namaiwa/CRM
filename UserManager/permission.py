from django.shortcuts import render,redirect,HttpResponse
from django.conf import settings
from django.urls import resolve
from UserManager.permission_list import perm_dic


def perm_check(*args, **kvargs):
    request = args[0]
    url_obj = resolve(request.path)
    url_name = url_obj.url_name

    perm_hook_func = None
    for permission_key, permission_value in perm_dic.items():
        perm_url_name = permission_value[0]
        perm_url_method = permission_value[1]
        perm_url_args = permission_value[2]
        perm_url_kwargs = permission_value[3]
        if len(permission_value) > 4:
            perm_hook_func = permission_value[4]
        else:
            perm_hook_func = None
        print(permission_key, permission_value)
        kwargs_flag = False     # 关键字参数判断标志
        args_flag = False       # url参数判断标志
        hook_flag = True       # 钩子函数判断标志

        if perm_url_name == url_name:           # 判断url
            if perm_url_method == request.method:       # 判断请求方法

                if not perm_url_args:
                    args_flag = True
                else:
                    for k, v in url_obj.kwargs:
                        if v in perm_url_args:
                            args_flag = True
                        else:
                            args_flag = False
                            break

                if args_flag:       # 判断url参数

                    if not perm_url_kwargs:
                        kwargs_flag = True
                    else:
                        for k, v in perm_url_kwargs:
                            request_method_params = getattr(request, perm_url_method)
                            if request_method_params.get(k):
                                if not v:
                                    kwargs_flag = True
                                else:
                                    if str(v) == request_method_params.get(k):
                                        kwargs_flag = True
                                    elif request_method_params.get(k) in v:
                                        kwargs_flag = True
                                    else:
                                        kwargs_flag = False
                                        break
                            else:
                                kwargs_flag = False
                                break

                    if kwargs_flag:     # 判断关键字参数

                        if perm_hook_func:
                            hook_flag = perm_hook_func(request)

                        if hook_flag:       # 判断钩子函数

                            perm_obj = 'UserManager.%s' % permission_key
                            print(perm_obj)
                            if request.user.has_perm(perm_obj):         # 判断是否有权限
                                return True
    return False   # 循环结束，没有匹配到


def check_permission(func):
    def inner(*args, **kwargs):
        if perm_check(*args, **kwargs):
            return func(*args, **kwargs)
        else:
            request = args[0]
            return render(request, 'usermanager/403_no_permission.html')
    return inner
