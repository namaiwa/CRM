from django.contrib import admin
from firstCRM import models
# Register your models here.


class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date', 'contact', 'source', 'consultant', 'referral_from']
    list_filter = ['name', 'date', 'contact', 'consultant', 'referral_from', 'consult_courses']
    search_fields = ['name', 'date', 'status_choices']
    readonly_fields = ['referral_from']
    actions = ['test']

    def test(self, request, queryset):
        print('.....', self, request, queryset)


admin.site.register(models.Branch)
admin.site.register(models.ClassList)
admin.site.register(models.Course)
admin.site.register(models.CourseRecord)
admin.site.register(models.Customer, TestAdmin)
admin.site.register(models.CustomerFollowUp)
# admin.site.register(models.Menus)
# admin.site.register(models.Role)
admin.site.register(models.Student)
admin.site.register(models.StudyRecord)
admin.site.register(models.StudentEnrollment)
admin.site.register(models.ContractTemplate)
admin.site.register(models.PaymentRecord)

