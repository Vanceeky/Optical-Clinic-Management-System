from django import forms
from .models import *

class Add_Category(forms.ModelForm):

	class Meta:
		model = Category
		fields = '__all__'

class Add_Product(forms.ModelForm):

    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                
                "class": "form-control"
            }
        ))


