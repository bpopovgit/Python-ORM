from datetime import date

from django.db import models


# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)


class Department(models.Model):
    class Location(models.TextChoices):
        VARNA = 'Sofia', 'Sofia',
        BURGAS = 'Plovdiv', 'Plovdiv',
        PLOVDIV = 'Varna', 'Varna',
        SOFIA = 'Burgas', 'Burgas'

    # city_choices = [
    #     ('V', 'Varna'),
    #     ('Pl', 'Plovdiv'),
    #     ('Sf', 'Sofia'),
    #     ('Bs', 'Burgas')
    # ]
    code = models.CharField(
        max_length=4,
        primary_key=True,
        unique=True,
    )

    name = models.CharField(
        max_length=50,
        unique=True
    )

    employees_count = models.IntegerField(
        default=0,
        verbose_name="Employees Count",
    )

    location = models.CharField(
        max_length=20, choices=Location.choices
    )

    last_edited_on = models.DateTimeField(
        auto_now=True,
        editable=False,
    )


class Project(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    duration_in_days = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Duration in Days"
    )

    estimated_hours = models.FloatField(
        blank=True, null=True,
        verbose_name="Estimated Hours"
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        default=date.today(),
        verbose_name="Start Date"
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    last_edited_on = models.DateTimeField(
        auto_now=True,
        editable=False
    )
