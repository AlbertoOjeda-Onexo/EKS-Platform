# Generated by Django 5.1.5 on 2025-07-23 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HumanResources', '0011_alter_customfieldvacantposition_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfieldvaluecandidate',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='candidates/'),
        ),
        migrations.AlterField(
            model_name='customfieldvaluevacantposition',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='vacant_position/'),
        ),
    ]
