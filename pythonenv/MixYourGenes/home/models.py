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

#    @staticmethod
#    def get_child(self):
#        if self.sex:
#            ch=type(self).objects.filter(dad=type(self))
#        else:
#            ch=type(self).objects.filter(mom=type(self))
#
#        if len(ch)>0:
#            return ch
#        else:
#            return None
#
#    @staticmethod
#    def get_other_parent():
#        if self.get_child() is not None:
#            if self.sex:
#                return self.get_child().mom
#            else:
#                return self.get_child().dad
#        else:
#            return None


class Sibling(models.Model):
    sibling1=models.ForeignKey(UserProfileInfo,on_delete=False,related_name="User")
    sibling2=models.ForeignKey(UserProfileInfo,on_delete=False,related_name="Sibling")

#class Parent(models.Model):
#        user=models.ForeignKey(UserProfileInfo, on_delete=False, related_name="child", default=None)
#        dad=models.ForeignKey(UserProfileInfo, on_delete=False, related_name="DAD", default=None)
#        mom=models.ForeignKey(UserProfileInfo, on_delete=False, related_name="MOM",default=None)
