import os

from django import conf
from django.shortcuts import render, redirect
from . import models


def dashboard(request):
    return render(request, 'firstCRM/dashboard.html')


def stu_enrollment(request):
    customers = models.Customer.objects.all()
    classes = models.ClassList.objects.all()
    if request.method == 'GET':
        return render(request, 'firstCRM/stu_enrollment.html', locals())
    if request.method == 'POST':
        customer_id = request.POST.get('name')
        class_grade_id = request.POST.get('class_id')
        if customer_id and class_grade_id:
            enrollment_obj = models.StudentEnrollment.objects.get_or_create(
                customer_id=customer_id,
                class_grade_id=class_grade_id,
                consultant_id=request.user.id)[0]
            name = enrollment_obj.customer
            class_ = enrollment_obj.class_grade
            msg = '请将此链接发给学员：127.0.0.1:8000/crm/stu_enrollment/%s' % enrollment_obj.id
            return render(request, 'firstCRM/enrollment_url_display.html', locals())
        elif request.POST.get('e_id'):
            enrollment_obj = models.StudentEnrollment.objects.get(id=request.POST.get('e_id'))
            customer_id = enrollment_obj.customer_id
            name = enrollment_obj.customer
            class_ = enrollment_obj.class_grade
            if request.POST.get('flag') == 'check':
                enrollment_obj.contract_approved = True
                enrollment_obj.save()

                name.status = 1
                name.save()

                student_obj = models.Student.objects.get_or_create(customer_id=customer_id)[0]
                student_obj.class_grades.add(enrollment_obj.class_grade_id)
                student_obj.save()
                return render(request, 'firstCRM/wait.html', {'msg': '报名成功'})

            if enrollment_obj.contract_agreed:
                msg = '客户已同意，请做最后确认'
                flag = "check"
                return render(request, 'firstCRM/enrollment_url_display.html', locals())
            else:
                warning = '客户未同意条款，请等待客户同意条款并完成表单'
                msg = '请将此链接发给学员：127.0.0.1:8000/crm/stu_enrollment/%s' % enrollment_obj.id
                return render(request, 'firstCRM/enrollment_url_display.html', locals())



def enrollment_agree(request, enrollment_id):
    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)
    customer_obj = enrollment_obj.customer
    class_obj = enrollment_obj.class_grade
    contract_obj = class_obj.contract
    if request.method == "POST":
        if request.POST.get('agree'):
            file_obj = request.FILES.get('files')
            print(file_obj.size)
            if 10000 < file_obj.size < 10000000:
                file_name = '%s.png' % customer_obj.id
                file_path = os.path.join(conf.settings.STATICFILES_DIRS[0], 'img', file_name)
                with open(file_path, 'wb') as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)
                enrollment_obj.contract_agreed = True
                enrollment_obj.save()
                return render(request, 'firstCRM/wait.html', {'msg': '已提交，等待审核'})
            msg = '请核对文件重新上传'
        else:
            msg = '请同意合同内容'
    return render(request, 'firstCRM/enrollment_agree.html', locals())
