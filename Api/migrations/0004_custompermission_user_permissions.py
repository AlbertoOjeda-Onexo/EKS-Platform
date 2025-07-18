# Generated by Django 5.2.4 on 2025-07-09 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0003_alter_user_userrol'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='Api.custompermission'),
        ),
    ]
