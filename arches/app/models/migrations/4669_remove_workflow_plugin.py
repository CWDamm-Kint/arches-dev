# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('models', '4665_remove_disco_widgets'),
    ]

    operations = [
        migrations.RunSQL(
            """
            delete from plugins where pluginid = 'e366a702-441e-11e9-9d27-c4b301baab9f';
            """,
            """
            insert into plugins (
                    pluginid,
                    name,
                    icon,
                    component,
                    componentname,
                    config)
                values (
                    'e366a702-441e-11e9-9d27-c4b301baab9f',
                    'Workflow',
                    'fa fa-step-forward',
                    'views/components/plugins/workflow',
                    'workflow-plugin',
                    '{}'
                );
            """
        )
    ]
