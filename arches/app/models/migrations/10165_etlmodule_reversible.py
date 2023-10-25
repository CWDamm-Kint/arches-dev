# Generated by Django 4.2.4 on 2023-10-25 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '10121_workflowhistory'),
    ]

    set_reversibility = """
        UPDATE etl_modules
        SET reversible = false
        WHERE etlmoduleid IN (
            '357d11c8-ca38-40ec-926f-1946ccfceb92',
            '63ae4bd2-404a-402f-9917-b18b21215cf2',
            'db0e9807-b254-458d-bd62-cfb1da21fe95'
        )
    """

    operations = [
        migrations.AddField(
            model_name='etlmodule',
            name='reversible',
            field=models.BooleanField(default=True),
        ),
        migrations.RunSQL(
            set_reversibility,
            migrations.RunSQL.noop,
        ),
    ]
