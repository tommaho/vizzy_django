# Generated by Django 5.0.2 on 2024-03-02 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vizzy', '0002_remove_dataset_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='columns',
            field=models.TextField(),
        ),
    ]