from .models import UserProfile,Posts
from django.forms import ModelForm
from django import forms



class UserProfileForm(ModelForm):

    class Meta:
        model=UserProfile
        exclude=("user","followings","user_followers",
        )
        widgets = {
           
            "dob": forms.DateInput(attrs={'class': 'form-control',"type":"date"}),
         
        }
        
class PostForm(ModelForm):
    

    class Meta:

        model=Posts
        fields=["title","image"]     
        widgets = {
    "title": forms.TextInput(attrs={'class': 'form-control',"type":"text"}),
    

    } 
