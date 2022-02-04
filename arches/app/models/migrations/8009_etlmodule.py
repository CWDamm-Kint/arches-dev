# Generated by Django 2.2.24 on 2021-12-03 13:27

import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import re
import uuid

add_etl_manager = """
    insert into plugins (
        pluginid,
        name,
        icon,
        component,
        componentname,
        config,
        slug,
        sortorder)
    values (
        '7720e9fa-876c-4127-a77a-b099cd2a5d45',
        'ETL Manager',
        'fa fa-database',
        'views/components/plugins/etl-manager',
        'etl-manager',
        '{"show": true}',
        'etl-manager',
        2);
    """
remove_etl_manager = """
    delete from plugins where pluginid = '7720e9fa-876c-4127-a77a-b099cd2a5d45';
    """

add_csv_importer = """
    insert into etl_modules (
        etlmoduleid,
        name,
        description,
        component,
        componentname,
        modulename,
        classname,
        config,
        icon,
        slug)
    values (
        '0a0cea7e-b59a-431a-93d8-e9f8c41bdd6b',
        'Import Single CSV',
        'Import a Single CSV file to Arches',
        'views/components/etlmodules/import-single-csv',
        'import-single-csv',
        'import_single_csv.py',
        'ImportSingleCsv',
        '{"bgColor": "#9591ef", "circleColor": "#b0adf3"}',
        'fa fa-upload',
        'import-single-csv');
    """
remove_csv_importer = """
    delete from etl_modules where etlmoduleid = '0a0cea7e-b59a-431a-93d8-e9f8c41bdd6b';
    """


class Migration(migrations.Migration):

    dependencies = [
        ("models", "8085_relational_data_model_handle_dates"),
    ]

    operations = [
        migrations.CreateModel(
            name="ETLModule",
            fields=[
                ("etlmoduleid", models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ("name", models.TextField()),
                ("description", models.TextField(blank=True, null=True)),
                ("component", models.TextField()),
                ("componentname", models.TextField()),
                ("modulename", models.TextField(blank=True, null=True)),
                ("classname", models.TextField(blank=True, null=True)),
                ("config", django.contrib.postgres.fields.jsonb.JSONField(blank=True, db_column="config", null=True)),
                ("icon", models.TextField()),
                (
                    "slug",
                    models.TextField(
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                    ),
                ),
            ],
            options={
                "db_table": "etl_modules",
                "managed": True,
            },
        ),
        migrations.RunSQL(
            add_etl_manager,
            remove_etl_manager,
        ),
        migrations.RunSQL(
            add_csv_importer,
            remove_csv_importer,
        ),
    ]
