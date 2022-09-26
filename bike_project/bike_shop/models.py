from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class reg_tbl(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    user_name=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=100,null=True)
    mobile=models.IntegerField(null=True)
    def __str__(self):
        return self.user_name
class company(models.Model):
    name=models.CharField(max_length=50,null=True)
    slug=models.SlugField(max_length=50,null=True)
    logo=models.FileField(null=True)
    def __str__(self):
        return self.name
class bikes(models.Model):
    company=models.ForeignKey(company,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.FileField()
    slug=models.SlugField(max_length=250)
    added_date=models.DateTimeField(auto_now_add=True)
    desc=models.TextField(max_length=500)
    available=models.BooleanField()
    def __str__(self):
        return self.name



