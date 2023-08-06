from collections import OrderedDict

import rows

from urlid_graph.commands import ImportCommand
from urlid_graph.models import Object


class Command(ImportCommand):
    schema = OrderedDict(
        [
            ("entity_uuid", rows.fields.UUIDField),
            ("internal_id", rows.fields.TextField),
            ("uuid", rows.fields.UUIDField),
        ]
    )
    table_name = Object._meta.db_table
