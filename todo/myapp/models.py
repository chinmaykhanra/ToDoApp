from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model) :
    task_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length = 200, null=True)
    description = models.CharField(max_length = 500, null=True)
    complete = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True)
    due_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.title
     
    
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length = 500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Contact by {self.name}"
   