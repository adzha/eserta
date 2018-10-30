from django.db import models
from django.contrib.auth.models import User
import penganjur 
# Create your models here.

class Profail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nokp = models.CharField(max_length=12, blank=True)
    notentera = models.CharField(max_length=8, blank=True)
    nama = models.CharField(max_length=300, blank=True)
    # birth_date = models.DateField(null=True, blank=True)
    def __str__(self):
    	return self.nama


class Pendaftaran(models.Model):
	aktiviti = models.ForeignKey('penganjur.Aktiviti',on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tarikhmasadaftar = models.DateTimeField('Tarikh/Masa Daftar',blank=False,null=False)

	def __str__(self):
		return str(self.pk)

class Kehadiran(models.Model):
	aktiviti = models.ForeignKey('penganjur.Aktiviti',on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tarikhmasahadir = models.DateTimeField('Tarikh/Masa Hadir',blank=False,null=False)

	def __str__(self):
		return str(self.pk)