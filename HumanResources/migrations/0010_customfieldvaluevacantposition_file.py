# Generated by Django 5.1.5 on 2025-07-18 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HumanResources', '0009_customfieldvaluecandidate_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customfieldvaluevacantposition',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/vacant_position/'),
        ),
    ]
