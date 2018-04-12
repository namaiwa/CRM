from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# 用户信息表
class UserProfile(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING)
    name = models.CharField(max_length=64, verbose_name='姓名')
    role = models.ManyToManyField('Role', blank=True)

    def __str__(self):
        return self.name


# 角色信息表
class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    menus = models.ManyToManyField('Menus', blank=True)

    def __str__(self):
        return self.name


# 客户信息表
class Customer(models.Model):
    name = models.CharField(max_length=64)
    contact_type_choices = ((0, 'qq'), (1, '微信'), (2, '手机'))
    contact = models.SmallIntegerField(choices=contact_type_choices, default=0)
    source_choices = ((0, 'QQ群'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (4, '转介绍'), (5, '其它'),)
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True, verbose_name="转介绍")
    consult_courses = models.ManyToManyField("Course", verbose_name="咨询课程")
    consult_content = models.TextField(verbose_name="咨询内容")
    status_choices = ((0, '未报名'), (1, '已报名'), (2, '已退学'))
    status = models.SmallIntegerField(choices=status_choices)
    consultant = models.ForeignKey("UserProfile", models.DO_NOTHING, verbose_name="课程顾问")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# 学员信息表
class Student(models.Model):
    customer = models.ForeignKey("Customer", models.DO_NOTHING)
    class_grades = models.ManyToManyField("ClassList")

    def __str__(self):
        return '%s' % self.customer


# 客户跟踪记录信息表
class CustomerFollowUp(models.Model):
    customer = models.ForeignKey("Customer", models.DO_NOTHING)
    content = models.TextField(verbose_name="跟踪内容")
    user = models.ForeignKey("UserProfile", models.DO_NOTHING, verbose_name="跟进人")
    status_choices = ((0, '近期无报名计划'),
                      (1, '一个月内报名'),
                      (2, '2周内内报名'),
                      (3, '已报名'),
                      )
    status = models.SmallIntegerField(choices=status_choices)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content


# 课程信息表
class Course(models.Model):
    name = models.CharField(verbose_name='课程名称', max_length=64, unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name="课程周期(月)", default=5)
    outline = models.TextField(verbose_name="大纲")

    def __str__(self):
        return self.name


# 班级信息表
class ClassList(models.Model):
    branch = models.ForeignKey("Branch", models.DO_NOTHING)
    course = models.ForeignKey("Course", models.DO_NOTHING)
    class_type_choices = ((0, '脱产'), (1, '周末'), (2, '网络班'))
    class_type = models.SmallIntegerField(choices=class_type_choices, default=0)
    semester = models.SmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile", verbose_name="讲师")
    start_date = models.DateField("开班日期")
    graduate_date = models.DateField("毕业日期", blank=True, null=True)

    def __str__(self):
        return "%s(%s)期" % (self.course.name, self.semester)

    class Meta:
        unique_together = ('branch', 'class_type', 'course', 'semester')


# 上课记录信息表
class CourseRecord(models.Model):
    class_grade = models.ForeignKey("ClassList", models.DO_NOTHING, verbose_name="上课班级")
    day_num = models.PositiveSmallIntegerField(verbose_name="课程节次")
    teacher = models.ForeignKey("UserProfile", models.DO_NOTHING)
    title = models.CharField("本节主题", max_length=64)
    content = models.TextField("本节内容")
    has_homework = models.BooleanField("本节有作业", default=True)
    homework = models.TextField("作业需求", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s第(%s)节" % (self.class_grade, self.day_num)

    class Meta:
        unique_together = ('class_grade', 'day_num')


# 学习信息表
class StudyRecord(models.Model):
    course_record = models.ForeignKey("CourseRecord", models.DO_NOTHING)
    student = models.ForeignKey("Student", models.DO_NOTHING)

    score_choices = ((100, "A+"),
                     (90, "A"),
                     (85, "B+"),
                     (80, "B"),
                     (75, "B-"),
                     (70, "C+"),
                     (60, "C"),
                     (40, "C-"),
                     (-50, "D"),
                     (0, "N/A"),
                     (-100, "COPY"),
                     )
    score = models.SmallIntegerField(choices=score_choices, default=0)
    show_choices = ((0, '缺勤'),
                    (1, '已签到'),
                    (2, '迟到'),
                    (3, '早退'),
                    )
    show_status = models.SmallIntegerField(choices=show_choices, default=1)
    note = models.TextField("成绩备注", blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" % (self.course_record, self.student, self.score)


# 菜单信息
class Menus(models.Model):
    name = models.CharField(max_length=64)
    url_type_choices = ((0, 'absolute'), (1, 'dynamic'))
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'url_name')


# 校区
class Branch(models.Model):
    name = models.CharField(max_length=64, unique=True)
    addr = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name
