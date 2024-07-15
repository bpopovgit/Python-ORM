# Generated by Django 5.0.4 on 2024-07-15 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_car'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('is_finished', models.BooleanField(default=False)),
            ],
        ),
    ]
