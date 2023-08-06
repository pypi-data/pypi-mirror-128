from collections import defaultdict
from functools import lru_cache
from urllib.parse import urljoin

from cached_property import cached_property
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVectorField
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections, models
from django.db.utils import NotSupportedError
from django.template import Context, Template

from urlid_graph import settings as urlid_graph_settings

from . import formatting


def get_urlid_database_uri():
    db = settings.DATABASES[urlid_graph_settings.DJANGO_DATABASE]
    return f"postgres://{db['USER']}:{db['PASSWORD']}@{db['HOST']}:{db['PORT']}/{db['NAME']}"


@lru_cache(maxsize=64)
def get_template(template_code):
    return Template(template_code)


class EntityQuerySet(models.QuerySet):
    def by_name(self, names):
        return self.filter(name__in=[name.lower().strip() for name in names])


class BrasilIOEntityQuerySet(EntityQuerySet):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                base_url="https://id.brasil.io/",
                version=1,
            )
        )


class Entity(models.Model):
    brasilio = BrasilIOEntityQuerySet.as_manager()
    objects = EntityQuerySet.as_manager()

    uuid = models.UUIDField(primary_key=True)
    base_url = models.TextField(blank=False, null=False)
    name = models.TextField(blank=False, null=False)
    version = models.TextField(blank=False, null=False)

    @property
    def url(self):
        return urljoin(self.base_url, f"/{self.name}/v{self.version}/")

    @property
    def label_properties(self):
        return getattr(self.config, "label_properties", None) or []

    @property
    def label_template(self):
        return getattr(self.config, "label_template", None) or None

    @property
    def graph_node_conf(self):
        return getattr(self.config, "graph_node_conf", None) or {}

    @property
    def config(self):
        try:
            return EntityConfig.objects.for_entity(self.name)
        except ObjectDoesNotExist:
            return None

    @property
    def label(self):
        return getattr(self.config, "label", None) or self.name

    def __str__(self):
        return f"Entity {self.url}"


class ObjectMixin:
    """Mixin used by Object and ObjectRepository classes"""

    @property
    def url(self):
        return urljoin(self.entity.url, f"{self.internal_id}/")

    @property
    def label(self):
        label_template = self.entity.label_template
        if label_template is not None:
            return get_template(label_template).render(Context(self.properties))
        else:
            for prop_name in self.entity.label_properties:
                label = self.properties.get(prop_name)
                if label:
                    return label

        return f"{self.entity.name}: {self.internal_id}"

    @cached_property
    def properties(self):
        props = Property.objects.for_object(self).order_by("value_datetime")
        return {p.name: p.converted_value for p in props}

    def inject_properties(self, property_set):
        prop_key = "properties"
        if prop_key in self.__dict__:
            del self.__dict__[prop_key]
        self.__dict__[prop_key] = {p.name: p.converted_value for p in property_set}

    @cached_property
    def full_properties(self):
        db_props = Property.objects.for_object(self).order_by("-value_datetime")
        props = defaultdict(list)
        for prop in db_props:
            props[prop.name].append(
                {
                    "value": prop.value,
                    "value_type": prop.value_type,
                    "source": prop.source,
                    "value_datetime": prop.value_datetime.isoformat() if prop.value_datetime else None,
                }
            )
        return props

    def get_label_for_property(self, prop_name):
        try:
            config = EntityPropertyConfig.objects.for_object(self.entity.name, prop_name)
            return config.label
        except ObjectDoesNotExist:
            return prop_name

    def __str__(self):
        return f"Object {self.url}"


class Object(ObjectMixin, models.Model):
    # XXX: DO NOT USE! Use ObjectRepository instead

    uuid = models.UUIDField(primary_key=False, blank=False, null=False, db_index=True)
    entity = models.ForeignKey(
        Entity, on_delete=models.DO_NOTHING, db_column="entity_uuid", db_constraint=False, db_index=True
    )
    internal_id = models.TextField(blank=False, null=False)


class PropertyQuerySet(models.QuerySet):
    def for_object(self, obj):
        return self.filter(object_id=obj.uuid)

    def for_objects(self, objs):
        return self.filter(object_id__in=[obj.uuid for obj in objs])


class Property(models.Model):
    STR, DATE, DATETIME, FLOAT, INT, BOOL = range(1, 7)
    TYPE_CHOICES = [
        (STR, "str"),
        (DATE, "date"),
        (DATETIME, "datetime"),
        (FLOAT, "float"),
        (INT, "int"),
        (BOOL, "bool"),
    ]
    objects = PropertyQuerySet.as_manager()

    object = models.ForeignKey(
        "ObjectRepository",
        on_delete=models.DO_NOTHING,
        db_column="object_uuid",
        db_constraint=False,
        db_index=False,
    )
    name = models.TextField(blank=False, null=False)
    value = models.TextField(blank=True, null=True)
    value_type = models.SmallIntegerField(blank=False, null=False, choices=TYPE_CHOICES)
    source = models.TextField(blank=False, null=False)
    value_datetime = models.DateTimeField(blank=False, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["object", "value_type"]),
        ]

    def __str__(self):
        return f"Property {self.name} of {self.object.uuid}"

    @property
    def converted_value(self):
        value = (self.value or "").strip()
        if not value:
            return None

        property_convert_function = {
            Property.STR: str,
            Property.DATE: formatting.convert_date,
            Property.DATETIME: formatting.convert_datetime,
            Property.FLOAT: float,
            Property.INT: int,
            Property.BOOL: formatting.convert_bool,
        }
        return property_convert_function[self.value_type](value)


class EntityConfigManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(config_type=ElementConfig.ENTITY_CONFIG)

    @lru_cache()
    def for_entity(self, entity_name):
        return self.get_queryset().get(name=entity_name)


class RelationshipConfigManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(config_type=ElementConfig.REL_CONFIG)

    @lru_cache()
    def get_by_name(self, relationship_name):
        return self.get_queryset().get(name=relationship_name)


class EntityPropertyConfigManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(config_type=ElementConfig.PROPERTY_CONFIG, parent_type=ElementConfig.ENTITY_CONFIG)

    @lru_cache()
    def for_object(self, parent_name, prop_name):
        return self.get_queryset().get(parent_name=parent_name, name=prop_name)


class RelPropertyConfigManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(config_type=ElementConfig.PROPERTY_CONFIG, parent_type=ElementConfig.REL_CONFIG)


class StatsConfigManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(config_type=ElementConfig.STATS_CONFIG)

    def get_stats(self):
        return self.get(name="stats")


class ElementConfig(models.Model):
    ENTITY_CONFIG, REL_CONFIG, PROPERTY_CONFIG, STATS_CONFIG = 1, 2, 3, 4
    TYPE_CHOICES = [
        (ENTITY_CONFIG, "entity"),
        (REL_CONFIG, "relationship"),
        (PROPERTY_CONFIG, "property"),
        (STATS_CONFIG, "stats"),
    ]
    PARENT_TYPE_CHOICES = [
        (ENTITY_CONFIG, "entity"),
        (REL_CONFIG, "relationship"),
    ]

    config_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    name = models.TextField()
    parent_type = models.PositiveSmallIntegerField(choices=PARENT_TYPE_CHOICES, null=True)
    parent_name = models.TextField(null=True)
    label = models.TextField()
    data = models.JSONField()

    class Meta:
        unique_together = ["config_type", "name", "parent_type", "parent_name"]


class EntityConfig(ElementConfig):
    objects = EntityConfigManager()

    class Meta:
        proxy = True

    @property
    def label_properties(self):
        return self.data.get("label_properties", [])

    @property
    def label_template(self):
        return self.data.get("label_template", None)

    @property
    def graph_node_conf(self):
        return self.data.get("graph_node_conf", {})


class RelationshipConfig(ElementConfig):
    objects = RelationshipConfigManager()

    class Meta:
        proxy = True

    @property
    def from_graph_node_conf(self):
        return self.data.get("from_graph_node_conf", {})

    @property
    def to_graph_node_conf(self):
        return self.data.get("to_graph_node_conf", {})


class EntityPropertyConfig(ElementConfig):
    objects = EntityPropertyConfigManager()

    class Meta:
        proxy = True


class RelPropertyConfig(ElementConfig):
    objects = RelPropertyConfigManager()

    class Meta:
        proxy = True


class StatsConfig(ElementConfig):
    objects = StatsConfigManager()

    class Meta:
        proxy = True


class ObjectRepositoryQuerySet(models.QuerySet):
    def from_uuids(self, uuids):
        return self.filter(uuid__in=uuids).select_related("entity")

    def with_properties(self):
        props = Property.objects.for_objects(self.all()).order_by("value_datetime")

        qs = []
        for obj in self.all():
            objs_props = [p for p in props if p.object_id == obj.uuid]
            obj.inject_properties(objs_props)
            qs.append(obj)
        return qs

    def refresh(self, concurrently=False):
        """Refresh the materialized view in which this model is based on"""

        view_name = "urlid_graph_object_fts"
        regular_query = f"REFRESH MATERIALIZED VIEW {view_name}"
        concurrently_query = f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view_name}"

        with connections[urlid_graph_settings.DJANGO_DATABASE].cursor() as cursor:
            if not concurrently:
                cursor.execute(regular_query)
            else:
                try:
                    cursor.execute(concurrently_query)
                except NotSupportedError:
                    # Materialized view not populated, so CONCURRENTLY cannot
                    # be used
                    cursor.execute(regular_query)

    def search(self, search_query, config=urlid_graph_settings.SEARCH_LANGUAGE):
        """Full-Text Search in object's search_data"""

        qs = self.filter(internal_id__isnull=False, entity__isnull=False)
        search_query = search_query or ""
        if not search_query:
            return qs
        words = search_query.split()
        query = None
        done = []  # to preserve order
        for word in words:
            if not word or word in done:
                continue
            if query is None:
                query = SearchQuery(word, config=config)
            else:
                query = query & SearchQuery(word, config=config)
            done.append(word)
        qs = qs.annotate(search_rank=SearchRank(models.F("search_data"), query)).filter(search_data=query)
        # Using `qs.query.add_ordering` will APPEND ordering fields instead
        # of OVERWRITTING (`qs.order_by` will overwrite).
        qs.query.add_ordering("-search_rank")
        return qs

    def search_many_entities(self, query, entities=all, limit_per_entity=10):
        """Search BrasilIO objects in more than one entity, by name

        Prefer to use this method since it also filter objects by entity (more performance)"""

        if entities is all:
            entities = Entity.brasilio.all()
        else:
            entities = Entity.brasilio.by_name(entities)

        results = []
        for entity in entities:
            qs = self.filter(entity=entity).search(query).select_related("entity")
            results.extend(qs[:limit_per_entity])
        results.sort(key=lambda row: row.search_rank, reverse=True)
        return results


class ObjectRepository(ObjectMixin, models.Model):
    objects = ObjectRepositoryQuerySet.as_manager()

    uuid = models.UUIDField(primary_key=True)
    entity = models.ForeignKey(
        Entity, on_delete=models.DO_NOTHING, db_column="entity_uuid", db_constraint=False, db_index=False
    )
    internal_id = models.TextField(blank=False, null=False)
    search_data = SearchVectorField(null=True)

    class Meta:
        db_table = "urlid_graph_object_repository"
        managed = False
        indexes = [GinIndex(fields=["search_data"])]
        unique_together = ["entity", "uuid", "internal_id"]


class SavedGraph(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    edges = ArrayField(models.CharField(max_length=255))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    class Meta:
        unique_together = (("user", "name"),)
