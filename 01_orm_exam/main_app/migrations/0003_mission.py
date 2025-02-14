# Generated by Django 5.0.4 on 2024-08-03 11:16

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_spacecraft'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(2)])),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Planned', 'Planned'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')], default='Planned', max_length=9)),
                ('launch_date', models.DateField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('astronauts', models.ManyToManyField(to='main_app.astronaut')),
                ('commander', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commanded_missions', to='main_app.astronaut')),
                ('spacecraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.spacecraft')),
            ],
        ),
    ]
