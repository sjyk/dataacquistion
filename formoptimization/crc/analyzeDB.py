import environ

from crc import models
from erutils import *

a = models.Response.objects.all()
textToEntityRelations(a)
	