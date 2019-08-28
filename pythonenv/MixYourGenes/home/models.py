from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=True,primary_key=True)
    # Add any additional attributes you want
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    profile_pic = models.ImageField(upload_to='profile_pictures',blank=True)
    sex=models.BooleanField(default=True)
    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
class Sibling(models.Model):
    user=models.ForeignKey(UserProfileInfo,on_delete=False,related_name="User")
    sibling=models.ForeignKey(UserProfileInfo,on_delete=False,related_name="Sibling")

class Parent(models.Model):
        user=models.ForeignKey(UserProfileInfo, on_delete=False, related_name="child", default=None)
        dad=models.ForeignKey(UserProfileInfo, on_delete=False, related_name="DAD", default=None)
        mom=models.ForeignKey(UserProfileInfo, on_delete=False, related_name="MOM",default=None)
