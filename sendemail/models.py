from django.db import models

class account(models.Model):
    firstname=models.CharField(max_length=255, default='')
    lastname=models.CharField(max_length=255, default='')
    email=models.EmailField(max_length=255, default='')
    password=models.CharField(max_length=255, default='')
    ContactNo=models.CharField(max_length=255, default='')
    oTP=models.IntegerField( default='0')
    oTPStatus=models.CharField(max_length=255, default='False')


    def __str__(self):
        return self.firstname
 