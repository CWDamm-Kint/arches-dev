# Generated by Django 4.2.13 on 2024-05-14 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("models", "10555_rename_controlled_list_values"),
    ]

    operations = [
        migrations.AlterField(
            model_name="controlledlistitemvalue",
            name="language",
            field=models.ForeignKey(
                blank=True,
                db_column="languageid",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="models.language",
                to_field="code",
            ),
        ),
    ]
