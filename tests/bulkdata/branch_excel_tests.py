"""
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import json
import shutil
import os
from arches.app.models.models import EditLog
from arches.app.models.graph import Graph
from arches.app.utils.betterJSONSerializer import JSONDeserializer
from arches.app.utils.data_management.resource_graphs.importer import (
    import_graph as resource_graph_importer,
)
from arches.app.utils.i18n import LanguageSynchronizer
from arches.app.etl_modules.branch_excel_importer import BranchExcelImporter
from arches.app.etl_modules.branch_excel_exporter import BranchExcelExporter
from arches.app.models.system_settings import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import connection
from django.http import HttpRequest
from django.test import TransactionTestCase

# these tests can be run from the command line via
# python manage.py test tests.bulkdata.excel_export_tests --settings="tests.test_settings"


class BranchExcelTests(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        LanguageSynchronizer.synchronize_settings_with_db()
        with open(
            os.path.join("tests/fixtures/resource_graphs/branch_excel_test.json"), "r"
        ) as f:
            archesfile = JSONDeserializer().deserialize(f)
        resource_graph_importer(archesfile["graph"])
        graph = Graph.objects.get(graphid="a5c3946a-a9c0-4472-9191-ffc0f35a5901")
        admin = User.objects.get(username="admin")
        graph.publish(user=admin)

        request = HttpRequest()
        request.method = "POST"
        request.user = User.objects.get(username="admin")
        load_id = "d481d116-7c1e-4b36-b7ef-85963d482db0"
        xls_file = "branch_excel_test.xlsx"
        details = {
            "result": {
                "summary": {
                    "name": "branch_excel_test.xlsx",
                    "size": "6.61 kb",
                    "cumulative_files_size": 6773,
                    "files": {"branch_excel_test.xlsx": {"size": "6.61 kb"}},
                }
            }
        }

        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO load_event (loadid, complete, etl_module_id, user_id) values (%s, FALSE, '0a0cea7e-b59a-431a-93d8-e9f8c41bdd6b', 1)""",
                [
                    load_id,
                ],
            )

        request.POST.__setitem__("load_id", load_id)
        request.POST.__setitem__("load_details", json.dumps(details))

        tmp_path = default_storage.path(
            os.path.join(settings.UPLOADED_FILES_DIR, "tmp", load_id)
        )
        xls_file = default_storage.path(
            os.path.join(settings.UPLOADED_FILES_DIR, xls_file)
        )

        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        shutil.copy(xls_file, tmp_path)
        importer = BranchExcelImporter(request=request, loadid=load_id)
        importer.write(request)

    def tearDown(self):
        file_name = "branch_exporter_test"
        exported_file_path = os.path.join(
            "tests/fixtures/data/archestemp", file_name + "." + "zip"
        )
        if os.path.exists(exported_file_path):
            os.remove(exported_file_path)

    def test_write(self):
        load_id = "d481d116-7c1e-4b36-b7ef-85963d482db0"
        edits = EditLog.objects.filter(transactionid=load_id)
        self.assertTrue(len(edits) == 9)

    def test_export(self):
        load_id = "2d288e76-ebd3-11ee-85b8-0242ac120005"
        graph_id = "a5c3946a-a9c0-4472-9191-ffc0f35a5901"
        graph_name = "branch_excel_test"
        resource_ids = None
        file_name = "branch_exporter_test"
        kwargs = {"filename": file_name}

        exporter = BranchExcelExporter(loadid=load_id)
        exporter.run_export_task(
            load_id=load_id,
            graph_id=graph_id,
            graph_name=graph_name,
            resource_ids=resource_ids,
            **kwargs,
        )
        exported_file_path = os.path.join(
            "tests/fixtures/data/archestemp", file_name + "." + "zip"
        )
        exported = os.path.exists(exported_file_path)

        self.assertTrue(exported)
