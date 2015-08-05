from django.db import models

class Response(models.Model):
	responseId = models.BigIntegerField(default=0)
	collectorId = models.BigIntegerField(default=0)
	startDate = models.DateTimeField()
	endDate = models.DateTimeField()
	confirm = models.BooleanField()
	metroArea = models.CharField(max_length=256)
	zipCode = models.CharField(max_length=10)
	q1 = models.CharField(max_length=5)
	q2 = models.CharField(max_length=5)
	q3 = models.CharField(max_length=5)
	q4 = models.CharField(max_length=5)
	q5 = models.CharField(max_length=5)
	q6 = models.CharField(max_length=5)
	q7 = models.CharField(max_length=5)
	openEnded = models.CharField(max_length=1024)
	gender = models.CharField(max_length=32)
	age = models.CharField(max_length=32)
	income = models.CharField(max_length=32)
	education = models.CharField(max_length=32)

	class Meta:
		app_label = 'crc'


