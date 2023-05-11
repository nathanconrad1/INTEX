from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Target_Diet
from .models import Food, Person
 
class Target_Diet_Form(forms.ModelForm):
    class Meta:
        model = Target_Diet
        fields = '__all__'

# class Food_Form(forms.ModelForm):
#     class Meta:
#         model = Food
#         fields = ['food_name', 'food_K', 'food_na', 'food_phos', 'food_protein', 'food_water']
# Create your forms here.






