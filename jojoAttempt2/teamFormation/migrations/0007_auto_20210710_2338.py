# Generated by Django 2.2.10 on 2021-07-10 23:38

from django.db import migrations, models
import teamFormation.validators


class Migration(migrations.Migration):

    dependencies = [
        ('teamFormation', '0006_auto_20210710_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvupload',
            name='csvFile',
            field=models.FileField(upload_to='', validators=[teamFormation.validators.validate_file_extension]),
        ),
    ]
