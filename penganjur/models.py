from django.db import models

# Create your models here.
class Aktiviti(models.Model):

	TERBUKA = 'TERBUKA'
	TERTUTUP = 'TERTUTUP'
	STATUS_AKTIVITI_CHOICES = (
		(TERBUKA, 'Terbuka'),
		(TERTUTUP, 'Tertutup'),
	)

	mula = models.DateTimeField('Tarikh mula',blank=False)
	akhir = models.DateTimeField('Tarikh akhir',blank=False)
	hadpeserta = models.IntegerField('Had Peserta',blank=True,null=True,default=0) 
	tempat = models.CharField('Tempat',max_length=300,blank=False,null=False)
	tajuk = models.CharField('Tajuk',max_length=300,blank=False,null=False)
	penceramah = models.CharField('Penceramah',max_length=300,blank=True,null=True)
	penganjur = models.CharField('Penganjur',max_length=300,blank=False,null=False)
	status = models.CharField('Status Anjuran',max_length=10,choices=STATUS_AKTIVITI_CHOICES,default=TERTUTUP)
	buka = models.DateTimeField('Tarikh dibuka',blank=True,null=True)
	tutup = models.DateTimeField('Tarikh ditutup',blank=True,null=True)

	def __str__(self):
		return str(self.pk)