from django.db import models
# Create your models here.
class TokenModel(models.Model): 
    token = models.UUIDField()
    assign = models.CharField(max_length=50)
    assigned_to = models.CharField(max_length=50,null=True)