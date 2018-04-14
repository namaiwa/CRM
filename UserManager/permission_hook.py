

# 定制钩子函数
def view_my_own_customers(request):
    if str(request.user.id) == request.GET.get('consultant'):
        return True
    else:
        return False
