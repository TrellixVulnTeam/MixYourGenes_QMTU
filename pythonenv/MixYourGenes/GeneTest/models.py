from django.db import models
from home import models as AccountModel
# Create your models here.
from django.db import models
class trait(models.Model):
    name = models.CharField(max_length=30, primary_key=True, default="")
    url=models.CharField(max_length=2000)
    inheritance=models.CharField(max_length=30)
    type=models.CharField(max_length=100)
    segment=models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name

class gene(models.Model):
    NCIB_ID=models.CharField(max_length=300, primary_key=True, default="")
    name = models.CharField(max_length=30)
    genotype = models.FloatField(max_length=1)
    img=models.ImageField(blank=True)
    description=models.TextField()
    trait_name=models.ForeignKey(trait,on_delete=models.CASCADE)
    IsXLinked=models.BooleanField(default=False)
    def __str__(self):
        return self.name

class have(models.Model):
    user_id = models.ForeignKey(AccountModel.UserProfileInfo, on_delete=models.CASCADE, default="")
    gene_name = models.ForeignKey(gene, on_delete=models.CASCADE)

class tests(models.Model):
    user_id1=models.ForeignKey(AccountModel.UserProfileInfo,on_delete=models.CASCADE,related_name="User1")
    user_id2=models.ForeignKey(AccountModel.UserProfileInfo,on_delete=models.CASCADE,related_name="User2")
    accessor=models.ForeignKey(AccountModel.UserProfileInfo,on_delete=models.CASCADE,related_name="Child", blank=True, null=True)
    date=models.DateField(auto_now=True)
    test_type=models.CharField(max_length=100)
    test_id=models.CharField(max_length=100, primary_key=True, default="")
    def __str__(self):
        return self.test_id


class figure(models.Model):
    test_id=models.ForeignKey(tests,on_delete=models.CASCADE,default="")
    user1_x=models.FloatField(max_length=1, default=0)
    user2_x=models.FloatField(max_length=1, default=0)
    common=models.FloatField(max_length=1, default=0)
    new=models.FloatField(max_length=1, default=0)


class results(models.Model):
    test_id=models.ForeignKey(tests, on_delete=models.CASCADE, default="")
    min_possibility=models.FloatField(max_length=1, default=0)
    max_possibility=models.FloatField(max_length=1, default=1)

class recombination(models.Model):
    test_id=models.ForeignKey(tests, on_delete=models.CASCADE, default="")
    user_id=models.ForeignKey(AccountModel.UserProfileInfo, on_delete=models.CASCADE,default="")
    user_gene=models.ForeignKey(gene, on_delete=models.CASCADE,default="")
    #user_gene=models.CharField(max_length=30,default="")
    possibility=models.FloatField(max_length=1)
    type=models.CharField(max_length=3,default="MAX")
    label=models.CharField(max_length=100,default="")
