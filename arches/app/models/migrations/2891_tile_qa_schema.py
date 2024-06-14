# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-25 15:53


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("models", "2337_fuzzy_dates"),
    ]

    def add_permissions(apps, schema_editor, with_create_permissions=True):
        db_alias = schema_editor.connection.alias
        Group = apps.get_model("auth", "Group")
        Permission = apps.get_model("auth", "Permission")
        User = apps.get_model("auth", "User")

        resource_reviewer_group = Group.objects.using(db_alias).create(
            name="Resource Reviewer"
        )
        read_nodegroup = Permission.objects.get(
            codename="read_nodegroup",
            content_type__app_label="models",
            content_type__model="nodegroup",
        )
        resource_reviewer_group.permissions.add(read_nodegroup)

        try:
            admin_user = User.objects.using(db_alias).get(username="admin")
            admin_user.groups.add(resource_reviewer_group)
            print("added admin group")
        except Exception as e:
            print(e)

    def remove_permissions(apps, schema_editor, with_create_permissions=True):
        db_alias = schema_editor.connection.alias
        Group = apps.get_model("auth", "Group")
        resource_reviewer_group = Group.objects.using(db_alias).get(
            name="Resource Reviewer"
        )
        User = apps.get_model("auth", "User")

        try:
            admin_user = User.objects.using(db_alias).get(username="admin")
            admin_user.groups.remove(resource_reviewer_group)
            print("removed admin group")
        except:
            pass

        resource_reviewer_group.delete()

    operations = [
        migrations.RunPython(add_permissions, reverse_code=remove_permissions),
    ]
