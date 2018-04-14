from . import permission_hook


perm_dic = {
    'firstCRM_table_list': ['table_list', 'GET', [], {}, permission_hook.view_my_own_customers],  # 可以查看每张表里所有的数据
    'firstCRM_table_list_view': ['obj_change', 'GET', [], {}],  # 可以访问表里每条数据的修改页
    'firstCRM_table_list_change': ['obj_change', 'POST', [], {}],  # 可以对表里的每条数据进行修改
    'firstCRM_table_obj_add': ['obj_add', 'POST', [], {}],  # 可以创建表里的数据
}
