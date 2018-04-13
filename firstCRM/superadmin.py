from SuperAdmin.sites import site, BaseAdmin
from firstCRM import models
# Register your models here.


class TestAdmin(BaseAdmin):
    list_display = ['id', 'name', 'date', 'contact', 'source', 'consultant', 'referral_from', 'status']
    list_filter = ['name', 'date', 'contact', 'consultant', 'referral_from']
    search_fields = ['name']
    readonly_fields = ['referral_from', 'status']
    actions = ['test']

    def test(self, request, querysets):
        print('.....', self, request, querysets)
        querysets.update(referral_from=None)


class CourseAdmin(BaseAdmin):
    list_display = ['name', 'price', 'period']
    search_fields = ['name']


site.register(models.ClassList)
site.register(models.Course, CourseAdmin)
site.register(models.CourseRecord)
site.register(models.Customer, TestAdmin)
site.register(models.Menus)
site.register(models.Role)
site.register(models.Student)
site.register(models.StudyRecord)
site.register(models.UserProfile)
site.register(models.StudentEnrollment)
site.register(models.ContractTemplate)
site.register(models.PaymentRecord)
site.register(models.Branch)
