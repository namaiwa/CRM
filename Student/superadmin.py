from SuperAdmin.sites import site, BaseAdmin
from Student import models
# Register your models here.


class TestAdmin(BaseAdmin):
    list_display = ['name']


site.register(models.Test, TestAdmin)

