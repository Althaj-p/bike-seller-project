from operator import length_hint
from symbol import power
from turtle import width
from unittest.util import _MAX_LENGTH
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
class Type(models.Model):
    name=models.CharField(max_length=50,null=False)
    slug=models.CharField(max_length=50,null=False)
    def __str__(self):
        return self.name

class bikes(models.Model):
    company=models.ForeignKey(company,on_delete=models.CASCADE)
    type=models.ForeignKey(Type,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.FileField()
    slug=models.SlugField(max_length=250)
    added_date=models.DateTimeField(auto_now_add=True)
    desc=models.TextField(max_length=500)
    available=models.BooleanField()
    fuel=models.CharField(max_length=20,null=True)
    mileage=models.FloatField(max_length=10,null=True)
    engine=models.FloatField(max_length=10,null=True)
    torque=models.FloatField(max_length=10,null=True)
    power=models.FloatField(max_length=10,null=True)
    weight=models.FloatField(max_length=10,null=True)
    fuel_tank=models.FloatField(max_length=10,null=True)
    brakes=models.CharField(max_length=50,null=True)
    fuel_delivery=models.CharField(max_length=50,null=True)
    length=models.FloatField(max_length=10,null=True)
    width=models.FloatField(max_length=10,null=True)
    height=models.FloatField(max_length=10,null=True)
    gears=models.IntegerField(null=True)
    image2=models.FileField(null=True)
    image3=models.FileField(null=True)
    image4=models.FileField(null=True)
    image5=models.FileField(null=True)


    def __str__(self):
        return self.name





