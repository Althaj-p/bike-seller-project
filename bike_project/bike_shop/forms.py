from django.forms import ModelForm
from . models import *

class bikeForm(ModelForm):
    class Meta:
        model = bikes
        fields='__all__'
class companyForm(ModelForm):
    class Meta:
        model=company
        fields='__all__'
class typeForm(ModelForm):
    class Meta:
        model=Type
        fields='__all__'