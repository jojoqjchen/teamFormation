# Generated by Django 3.2.5 on 2021-07-20 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamFormation', '0010_numberofdownloads'),
    ]

    operations = [
        migrations.RenameField(
            model_name='numberofdownloads',
            old_name='downloads',
            new_name='download',
        ),
    ]
