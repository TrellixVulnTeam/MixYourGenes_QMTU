from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=True,primary_key=True)
    mom = models.ForeignKey('self',on_delete=models.CASCADE, related_name="MOM", blank=True, null=True)
    dad = models.ForeignKey('self',on_delete=models.CASCADE, related_name="DAD", blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pictures',blank=True)
    sex=models.BooleanField(default=True)
    def __str__(self):
        return self.user.username

class Sibling(models.Model):
    sibling1=models.ForeignKey(UserProfileInfo,on_delete=False,related_name="User")
    sibling2=models.ForeignKey(UserProfileInfo,on_delete=False,related_name="Sibling")

#class Parent(models.Model):
#        user=models.ForeignKey(UserProfileInfo, on_delete=False, related_name="child", default=None)
#        dad=models.ForeignKey(UserProfileInfo, on_delete=False, related_name="DAD", default=None)
#        mom=models.ForeignKey(UserProfileInfo, on_delete=False, related_name="MOM",default=None)
