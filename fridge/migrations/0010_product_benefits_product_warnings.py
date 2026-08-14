from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fridge", "0009_product_nutrition_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="benefits",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="product",
            name="warnings",
            field=models.TextField(blank=True, default=""),
        ),
    ]
