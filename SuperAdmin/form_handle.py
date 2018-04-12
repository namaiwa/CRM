from django.forms import ModelForm


def create_dynamic_model_form(model_obj, admin_class, form_add=True):
    class Meta:
        model = model_obj
        fields = '__all__'
        if not form_add:
            exclude = admin_class.readonly_fields

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})

        return ModelForm.__new__(cls)

    DynamicModelForm = type('DynamicModelForm', (ModelForm,), {'Meta': Meta, '__new__': __new__})
    return DynamicModelForm
