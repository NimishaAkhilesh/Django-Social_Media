from django.contrib import admin
from .models import Posts,Comments,UserProfile
# Register your models here.

admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(UserProfile)
