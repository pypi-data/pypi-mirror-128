import traceback

import rows
from django.core.management.base import BaseCommand
from django.db import connections

from .models import get_urlid_database_uri
from .utils import DatabaseConnection, read_total_size, working
import urlid_graph.settings as urlid_graph_settings


class ImportCommand(BaseCommand):
    help = "Import rows into table"
    schema = None

    def add_arguments(self, parser):
        parser.add_argument("-b", "--batch-size", type=int, default=8388608)
        parser.add_argument("--disable-autovacuum", action="store_true")
        parser.add_argument("--disable-indexes", action="store_true")
        parser.add_argument("input_filename", nargs="+")

    def import_data(self, input_filename, batch_size):
        rows_progress = rows.utils.ProgressBar(
            prefix="Importing data",
            pre_prefix="Detecting file size",
            unit="bytes",
            total=read_total_size(input_filename),
        )
        try:
            rows_output = rows.utils.pgimport(
                input_filename,
                encoding="utf-8",
                dialect="excel",
                table_name=self.table_name,
                database_uri=get_urlid_database_uri(),
                schema=self.schema,
                create_table=False,
                chunk_size=batch_size,
                callback=rows_progress.update,
            )
        except RuntimeError:
            rows_progress.close()
            # TODO: process the exception and show a good error message
            raise
        else:
            rows_progress.description = f"Imported {rows_output['rows_imported']} rows to '{self.table_name}'"
            rows_progress.close()

    def handle(self, *args, **options):
        input_filenames = options["input_filename"]
        batch_size = options["batch_size"]
        disable_autovacuum = options["disable_autovacuum"]
        disable_indexes = options["disable_indexes"]

        connection = connections[urlid_graph_settings.DJANGO_DATABASE]
        db = DatabaseConnection(connection=connection)
        ok = True

        try:
            with working("Disabling sync commit"):
                db.disable_sync_commit()
            if disable_autovacuum:
                with working(f"Disabling autovacuum for {self.table_name}"):
                    db.disable_autovacuum(self.table_name)
            if disable_indexes:
                with working(f"Disabling indexes on {self.table_name}"):
                    db.execute_query(
                        f"UPDATE pg_index SET indisready = FALSE WHERE indrelid = '{self.table_name}'::regclass"
                    )
            with working("Disabling triggers"):
                db.execute_query(f"ALTER TABLE {self.table_name} DISABLE TRIGGER ALL")

            for filename in input_filenames:
                self.import_data(filename, batch_size)

        except:  # noqa
            traceback.print_exc()
            ok = False

        finally:
            if disable_indexes:
                with working(f"Reindexing table {self.table_name}"):
                    db.execute_query(f"REINDEX TABLE {self.table_name}")
            with working(f"Reenabling triggers on {self.table_name}"):
                db.execute_query(f"ALTER TABLE {self.table_name} ENABLE TRIGGER ALL")
            with working(f"Running VACUUM ANALYZE on {self.table_name}"):
                db.vacuum_analyze(self.table_name)
            if disable_autovacuum:
                with working(f"Enabling autovacuum for {self.table_name}"):
                    db.enable_autovacuum(self.table_name)
            with working("Enabling sync commit"):
                db.enable_sync_commit()

        return str(ok)  # Used by import_data when calling this command programatically
