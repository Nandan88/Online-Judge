from django.db import models
from django.contrib.auth.models import User

# from ojapp import admin

# Create your models here.
# admin.py me models ko register karna padega
# Also app.py se name copy karke settings me Installed apps me daala
class Problem(models.Model):
    name=models.CharField(max_length=200)
    # problem_statement=models.CharField(max_length=255)
    problem_statement=models.TextField(max_length=25000)
    constraints=models.CharField(max_length=255)
    code=models.CharField(max_length=255)
    input = models.CharField(max_length=255,default=1)
    output = models.CharField(max_length=255,default=1)

    def __str__(self):
        return self.name

class Solution(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    verdict=models.CharField(max_length=50)
    submitted_at=models.DateTimeField()
    # submitted_code=models.CharField(max_length=255)
    submitted_code=models.TextField(max_length=25000)

    def __str__(self):
        return self.verdict
    

class Testcases(models.Model):
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)

    def __str__(self):
        return self.input
    