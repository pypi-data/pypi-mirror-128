from collections import OrderedDict

import rows

from urlid_graph.commands import ImportCommand
from urlid_graph.models import Property


class Command(ImportCommand):
    schema = OrderedDict(
        [
            ("id", rows.fields.IntegerField),
            ("object_uuid", rows.fields.UUIDField),
            ("value_type", rows.fields.IntegerField),
            ("name", rows.fields.TextField),
            ("value", rows.fields.TextField),
            ("source", rows.fields.TextField),
            ("value_datetime", rows.fields.DatetimeField),
            ("updated_at", rows.fields.DatetimeField),
        ]
    )
    table_name = Property._meta.db_table
