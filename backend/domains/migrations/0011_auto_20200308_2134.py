# Generated by Django 3.0.2 on 2020-03-08 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0010_auto_20200308_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xxljob',
            name='dbrand',
        ),
        migrations.AddField(
            model_name='xxljob',
            name='dbrand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='domains.Brand', verbose_name='域名品牌'),
        ),
    ]
