# Generated by Django 3.2.4 on 2021-07-06 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamFormation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size',
            name='teamSize',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='upload',
            name='csvFile',
            field=models.FileField(upload_to=''),
        ),
    ]
