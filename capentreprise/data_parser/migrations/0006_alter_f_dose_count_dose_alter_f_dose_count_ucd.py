# Generated by Django 5.0.2 on 2024-02-22 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_parser', '0005_alter_f_dose_count_dose_alter_f_dose_count_ucd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='f_dose',
            name='count_dose',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='f_dose',
            name='count_ucd',
            field=models.FloatField(default=None, null=True),
        ),
    ]
