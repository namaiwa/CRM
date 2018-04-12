from django.shortcuts import render


class BaseAdmin(object):
    def __init__(self):
        if 'delete_selected' not in self.actions:
            self.actions.append('delete_selected')

    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []
    default_action = ['delete_selected']
    actions = []

    def delete_selected(self, request, queryset):
        url = request.get_full_path()
        params = {"objs": queryset, 'url': url, 'appname': url.split('/')[2], 'modelname': url.split('/')[3]}
        return render(request, 'SuperAdmin/obj_delete.html', params)






class AdminSites(object):
    def __init__(self):
        self.display = {}

    def register(self, model, admin_class=BaseAdmin):
        app_name = model._meta.app_label
        model_name = model._meta.model_name
        # if admin_class:
        #     admin_class = admin_class()
        # else:
        #     admin_class = BaseAdmin()
        # admin_class.model = model
        if not self.display.get(app_name):
            self.display[app_name] = {}
        self.display[app_name][model_name] = {'admin_class': admin_class, 'model': model}


site = AdminSites()
