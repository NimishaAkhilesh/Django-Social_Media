from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    bio = models.CharField(max_length=256)
    profile_pic = models.ImageField(upload_to="profile", null=True, blank=True)
    cover_pic = models.ImageField(upload_to="covers", null=True, blank=True)
    dob = models.DateTimeField(null=True)
    gender_choice=(
        ("male","male"),
        ("female","female"),
        ("others","Others")
    )
    gender=models.CharField(max_length=50,choices=gender_choice,null=True,blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    place=models.CharField(max_length=100,null=True,blank=True)
    followings=models.ManyToManyField(User,related_name='followings',blank=True)
    user_followers=models.ManyToManyField(User,related_name='user_followers',blank=True)

    def __str__(self):
        return self.user.username
    

    @property
    def friend_request(self):
        all_users=User.objects.all().exclude(username=self.user)
        my_friends=self.followings.all()
        suggestions=set(all_users)-set(my_friends)
        return suggestions
    

    @property
    def my_friends(self):
        friends=self.followings.all()
        return friends
    
    @property
    def followers(self):
        return self.user_followers.all()
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to="posts", null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    liked_by=models.ManyToManyField(User,related_name="post")
    
    @property 
    def get_comments(self):
        return Comments.objects.filter(post=self)
    @property
    def comment_count(self):
        return Comments.objects.filter(post=self).count

    def __str__(self):
        return self.title


class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)


    
