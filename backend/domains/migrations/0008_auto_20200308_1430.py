# Generated by Django 3.0.2 on 2020-03-08 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0007_auto_20200307_2355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bocenodegroup',
            name='nodes',
        ),
        migrations.AddField(
            model_name='bocenodegroup',
            name='nodes',
            field=models.ManyToManyField(blank=True, to='domains.BoceNode', verbose_name='节点列表'),
        ),
    ]
