# Generated by Django 2.0.7 on 2018-07-06 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rorender', '0003_auto_20180706_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='port',
            field=models.IntegerField(default=135),
            preserve_default=False,
        ),
    ]