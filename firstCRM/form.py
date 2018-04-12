from firstCRM import models
from django.forms import ModelForm


class Form(ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
