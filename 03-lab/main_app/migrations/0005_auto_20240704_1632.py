# Generated by Django 5.0.4 on 2024-07-04 13:32
import random

from django.db import migrations


class Migration(migrations.Migration):

    def generate_barcodes(apps, schema_editor):
        product_model = apps.get_model('main_app', 'Product')
        all_products = product_model.objects.all()
        barcodes = random.sample(range(100000000, 1000000000), len(all_products))
        for product, barcode in zip(all_products, barcodes):
            product.barcode = barcode
            product.save()

    def reverse_barcodes(apps, schema_editor):
        product_model = apps.get_model('main_app', 'Product')
        for product in product_model.objects.all():
            product.barcode = 0
            product.save()



    dependencies = [
        ('main_app', '0004_product_barcode'),
    ]

    operations = [
        migrations.RunPython(generate_barcodes, reverse_barcodes)
    ]
