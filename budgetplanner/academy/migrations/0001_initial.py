# Generated by Django 3.2 on 2024-01-20 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleAcademy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField(max_length=528)),
                ('url', models.URLField(blank=True, max_length=1024, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'ArticleAcademy',
                'ordering': ['title'],
            },
        ),
    ]
