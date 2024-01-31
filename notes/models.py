from django.db import models
from django.contrib.auth.models import User


def some_function():
    from .models import Signup, Notes


# Create your models here.
class Signup(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    contact=models.CharField(max_length=10,null=True)
    branch=models.CharField(max_length=30)
    role=models.CharField(max_length=15)
    contact=models.CharField(max_length=10)

    def __str__(self):
        return self.user.username
    
class Notes(models.Model):
     STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('All', 'All'),

        # Add other statuses as needed
    ]
     
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     uploadingdate = models.DateTimeField(max_length=30)
     branch = models.CharField(max_length=30)
     subject = models.CharField(max_length=30)
     notesfile = models.FileField(upload_to='uploads/', null=True, blank=True)
     filetype = models.CharField(max_length=30, null=True)
     description = models.TextField(max_length=200, null=True)
     status = models.CharField(max_length=15, null=True,choices=STATUS_CHOICES)

     def __str__(self):
         return f"{self.user.username} {self.status}"


# class Notes(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     uploadingdate=models.DateTimeField(max_length=30)
#     branch=models.CharField(max_length=30)
#     subject=models.CharField(max_length=30)
#     notesfile=models.FileField(max_length=10, null=True)
#     filetype=models.CharField(max_length=30, null=True)
#     description=models.TextField(max_length=200, null=True)
#     status=models.CharField(max_length=15, null=True)


#     def __str__(self):
#         return self.signup.user.username+" "+self.status