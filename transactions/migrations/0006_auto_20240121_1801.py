# Generated by Django 3.2 on 2024-01-21 18:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_debtcategory_debtdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debtdetail',
            name='category',
        ),
        migrations.AddField(
            model_name='debtdetail',
            name='debt_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DebtCategory',
        ),
    ]
