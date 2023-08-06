import csv
import random

from django.core.management.base import BaseCommand
from model_bakery.baker import random_gen


class Command(BaseCommand):
    help = "Create fake relations"

    def add_arguments(self, parser):
        parser.add_argument("output_filename")
        parser.add_argument("number_rows", type=int)

    def gen_row(self):
        return {
            "from_node_uuid": random_gen.gen_uuid(),
            "to_node_uuid": random_gen.gen_uuid(),
            "inicio": random_gen.gen_date(),
            "fim": random_gen.gen_date() if random.random() < 0.9 else "",
            "descricao": random_gen.gen_text() if random.random() < 0.9 else "",
            "quantidade": random_gen.gen_integer() if random.random() < 0.9 else "",
            "valor": random_gen.gen_integer() if random.random() < 0.9 else "",
        }

    def handle(self, *args, **options):
        with open(options["output_filename"], mode="w", newline="") as csvfile:
            fieldnames = [
                "from_node_uuid",
                "to_node_uuid",
                "inicio",
                "fim",
                "descricao",
                "quantidade",
                "valor",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for _ in range(options["number_rows"]):
                writer.writerow(self.gen_row())
