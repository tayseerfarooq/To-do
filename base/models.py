from django.db import models
from django.contrib.auth.models import User #import user table for model
# Create your models here.


#we will use one to many relationship for multiple tickets for one user.
#database table and then do migrations 


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank = True) #if the user is deleted then delete all tasks and null values are accepted
    title= models.CharField(max_length=200)

    description= models.TextField(null=True,blank=True) #add a description to your todo
    complete= models.BooleanField(default=False) #retuerns boolean value to the todo task and sets False as default
    created= models.DateTimeField(auto_now_add=True) #created time 


    def __str__(self):
        return self.title


    class Meta:
        ordering = ['complete']
    