from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView
from django.contrib.auth.models import User
from .foms import RegistrationForm,LoginForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from social.views import signin_required
from django.views.decorators.cache import never_cache

# Create your views here.
class SignUpView(CreateView):
    model=User
    template_name="register.html"
    form_class=RegistrationForm
    success_url= reverse_lazy("login")

class SignInView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        try:
            form = LoginForm(request.POST)

            if form.is_valid(): 
                uname = form.cleaned_data.get("username")
                pwd = form.cleaned_data.get("password")
                user = authenticate(request, username=uname, password=pwd)
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, self.template_name, {"form": form})   
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")  

@never_cache
@signin_required
def logoutpage(request):
    try:
        logout(request)
        return redirect('login')
    except:
        pass
