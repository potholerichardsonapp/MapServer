# Generated by Django 2.0.4 on 2018-04-14 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datareport',
            name='generator',
            field=models.CharField(default='a', max_length=200),
            preserve_default=False,
        ),
    ]
