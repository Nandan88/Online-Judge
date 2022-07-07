from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# from ojapp import admin

# Create your models here.
# admin.py me models ko register karna padega
# Also app.py se name copy karke settings me Installed apps me daala

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_score(sender, instance, created, **kwargs):
    if created:
        Score.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_score(sender, instance, **kwargs):
    instance.score.save()


class Problem(models.Model):
    name=models.CharField(max_length=200)
    # problem_statement=models.CharField(max_length=255)
    problem_statement=models.TextField(max_length=25000)
    constraints=models.CharField(max_length=255)
    code=models.CharField(max_length=255)
    input = models.TextField(max_length=25000,default=1)
    output = models.TextField(max_length=25000,default=1)
    difficult=models.IntegerField(default=1)

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
    