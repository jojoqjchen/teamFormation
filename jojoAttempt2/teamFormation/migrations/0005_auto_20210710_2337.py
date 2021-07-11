# Generated by Django 2.2.10 on 2021-07-10 23:37

from django.db import migrations, models
import teamFormation.validators


class Migration(migrations.Migration):

    dependencies = [
        ('teamFormation', '0004_csvupload_pickcols_teamsize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvupload',
            name='csvFile',
            field=models.FileField(upload_to='', validators=[teamFormation.validators.validate_file_extension]),
        ),
    ]
