# Generated by Django 2.0.5 on 2018-05-27 10:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('User', '0002_user_is_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, default='', max_length=512, verbose_name='关于我'),
        ),
        migrations.AddField(
            model_name='user',
            name='birth',
            field=models.DateTimeField(blank=True, null=True, verbose_name='生日'),
        ),
    ]
