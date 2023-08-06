from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import Objects, Properties and Relationships from a directory"

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("--disable-autovacuum", action="store_true")
        parser.add_argument("--disable-indexes", action="store_true")
        parser.add_argument("--filetype", action="append")

    def handle(self, *args, **options):
        cmd_options = {
            "disable_autovacuum": options["disable_autovacuum"],
            "disable_indexes": options["disable_indexes"],
        }
        cmd_options_relations = {
            "disable_autovacuum": options["disable_autovacuum"],
        }
        path = Path(options["path"])
        file_types = options["filetype"]
        if not file_types:
            file_types = all
        else:
            file_types = [file_type.lower() for file_type in file_types]
            for file_type in file_types:
                if file_type not in ("property", "object", "relationship"):
                    raise ValueError(f"Unknown value '{file_type}'")

        # First, import properties (before objects - so when objects are
        # imported we'll fill search_data with property data)
        if file_types is all or "property" in file_types:
            filenames = path.glob("*property*.csv*")
            filenames = [str(filename.absolute()) for filename in filenames]
            ok = call_command("import_properties", *filenames, **cmd_options) == "True"
            if not ok:
                return ok

        # Second, import objects
        if file_types is all or "object" in file_types:
            filenames = path.glob("*object*.csv*")
            filenames = [str(filename.absolute()) for filename in filenames]
            ok = call_command("import_objects", *filenames, **cmd_options) == "True"
            if not ok:
                return ok

        # Finally, import relations
        if file_types is all or "relationship" in file_types:
            relations_filenames = []
            for filename in path.glob("*relationship*.csv*"):
                relationship = filename.absolute().name.split("relationship")[1].split(".csv")[0]
                filename = str(filename.absolute())
                if relationship.startswith("-"):
                    relationship = relationship[1:]
                if relationship.endswith("-"):
                    relationship = relationship[:-1]
                relations_filenames.append(f"{relationship}--{filename}")

            ok = call_command("import_relations", *relations_filenames, **cmd_options_relations) == "True"
            if not ok:
                return ok
