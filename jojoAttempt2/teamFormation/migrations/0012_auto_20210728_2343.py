# Generated by Django 3.2.5 on 2021-07-28 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamFormation', '0011_rename_downloads_numberofdownloads_download'),
    ]

    operations = [
        migrations.CreateModel(
            name='projectFirstParam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberOfProjects', models.IntegerField(blank=True, null=True)),
                ('numberOfChoices', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='csvupload',
            name='algorithm',
            field=models.IntegerField(choices=[('1', 'Team First'), ('2', 'Project First')], default='1'),
        ),
    ]