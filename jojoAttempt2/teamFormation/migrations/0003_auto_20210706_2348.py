# Generated by Django 3.2.4 on 2021-07-06 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamFormation', '0002_auto_20210706_2148'),
    ]

    operations = [
        migrations.DeleteModel(
            name='characteristics',
        ),
        migrations.DeleteModel(
            name='size',
        ),
        migrations.DeleteModel(
            name='upload',
        ),
    ]
