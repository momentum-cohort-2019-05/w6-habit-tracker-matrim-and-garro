# Generated by Django 2.2.3 on 2019-07-02 16:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyrecord',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
