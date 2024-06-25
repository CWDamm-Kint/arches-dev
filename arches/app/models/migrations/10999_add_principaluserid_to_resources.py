# Generated by Django 2.2.6 on 2019-12-13 11:56

from django.conf import settings
from django.db import migrations, models, transaction
from django.db.models import deletion

from arches.app.models.models import EditLog
from arches.app.models.resource import Resource


class Migration(migrations.Migration):

    dependencies = [
        ("models", "10798_jsonld_importer"),
    ]

    def forward_func(state, editor):
        pass
        # Resource.objects.update(
        #     principaluser_id=settings.DEFAULT_RESOURCE_IMPORT_USER["userid"]
        # )
        # for editlog_create in EditLog.objects.filter(edittype="create"):
        #     res = Resource.objects.get(
        #         resourceinstanceid=editlog_create.resourceinstanceid
        #     )
        #     res.principaluser_id = editlog_create.userid
        #     res.save()

        # for resource in Resource.objects.all():
        #     resource.principaluser_id = resource.get_instance_creator()
        #     resource.save()

    def reverse_func(state, editor):
        pass

    operations = [
        migrations.AddField(
            model_name="resourceinstance",
            name="principaluser",
            field=models.ForeignKey(
                on_delete=deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                blank=True,
                null=True,
            ),
        ),
    ]
