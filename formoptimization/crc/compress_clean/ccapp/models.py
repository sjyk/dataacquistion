from django.db import models

# Create your models here.

class InputParam(models.Model):
	param_text=models.CharField(max_length=200)
	def __str__(self):
		return self.param_text
	
class ParamVal(models.Model):
	param_name=models.ForeignKey(InputParam)
	val=models.CharField(max_length=256)
	def __str__(self):
		return self.val
