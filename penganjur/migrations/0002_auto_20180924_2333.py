# Generated by Django 2.1.1 on 2018-09-24 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('penganjur', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aktiviti',
            name='buka',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Tarikh dibuka'),
        ),
        migrations.AlterField(
            model_name='aktiviti',
            name='tutup',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Tarikh ditutup'),
        ),
    ]