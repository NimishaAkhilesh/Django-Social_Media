from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, View
from .forms import UserProfileForm, PostForm
from django.urls import reverse_lazy
from .models import UserProfile, Posts, Comments
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User

# ========decoraters=========


def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request, *args, **kwargs)
    return wrapper


decs = [signin_required, never_cache]

# ========end=============


# ========indexview========

@method_decorator(decs, name="dispatch")
class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):

        if request.user:
            usresprofile = UserProfile.objects.all()
            lst = []
            followers = 0
            for p in usresprofile:
                for u in p.followings.all():
                    lst.append(u)

            followers = lst.count(self.request.user)

            posts = Posts.objects.all().order_by("-created_date")
            form = PostForm
            context = {"form": form, "posts": posts, "followers": followers}
            return render(request, "index.html", context)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):

        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid:
            form.instance.user = request.user
            form.save()
            return redirect('home')
        else:
            return render(request, 'index.html', {"form": form})

    # model=Posts
    # form_class=PostForm
    # template_name="index.html"
    # success_url=reverse_lazy("home")

# =========end===========


# ==========profile create view========


@method_decorator(decs, name="dispatch")
class ProfileCreateView(CreateView):
    form_class = UserProfileForm
    template_name = "profile-add.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # def post(self,request,*args, **kwargs):
    #     form=UserProfileForm(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         return redirect('home')
    #     else:
    #         return render(request,self.template_name,{"form":form})

# =====end=======


@method_decorator(decs, name="dispatch")
class MyProfileView(TemplateView):
    def get(self,request,*args, **kwargs):
        post=Posts.objects.filter(user=request.user)
        return render(request,'profile.html',{"mypost":post})



@method_decorator(decs, name="dispatch")
class ProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profile-edit.html"
    success_url = reverse_lazy("myprofile")


@method_decorator(decs, name="dispatch")
class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        usr = request.user
        pst = Posts.objects.get(id=id)
        cmt = request.POST.get("comment")
        Comments.objects.create(user=usr, post=pst, comment=cmt)
        return redirect('home')


@method_decorator(decs, name="dispatch")
class AddLikeView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        pst = Posts.objects.get(id=id)
        pst.liked_by.add(request.user)
        pst.save()
        return redirect("home")


def following_view(request, *args, **kwargs):
    id = kwargs.get("pk")
    usr = User.objects.get(id=id)
    follow_usr=UserProfile.objects.get(user=usr)
    follow_usr.user_followers.add(request.user)
    request.user.profile.followings.add(usr)
    return redirect("myprofile")

def following_remove(request,*args, **kwargs):
    id=kwargs.get("pk")
    usr=User.objects.get(id=id)
    request.user.profile.followings.remove(usr)
    return redirect("myprofile")



