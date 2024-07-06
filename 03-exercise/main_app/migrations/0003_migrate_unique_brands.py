# Generated by Django 5.0.4 on 2024-07-06 03:23

from django.db import migrations


def create_unique_brands(apps, schema_editor):
    shoe_model = apps.get_model('main_app', 'Shoe')
    unique_brands = apps.get_model('main_app', 'UniqueBrands')

    unique_brand_names = shoe_model.objects.values_list('brand', flat=True).distinct()

    unique_brands.objects.bulk_create([unique_brands(brand_name=brand_name) for brand_name in unique_brand_names])

    # for brand_name in unique_brand_names:
    #     unique_brands.create(brand=brand_name)


def reverse_unique_brands(apps, schema_editor):
    unique_brands = apps.get_model('main_app', 'UniqueBrands')
    unique_brands.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0002_uniquebrands'),
    ]

    operations = [
        migrations.RunPython(create_unique_brands, reverse_unique_brands)
    ]
