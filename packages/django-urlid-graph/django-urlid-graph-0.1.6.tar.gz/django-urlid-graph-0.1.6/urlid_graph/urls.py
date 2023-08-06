from django.urls import path, re_path

from . import views

list_actions = {"get": "list", "post": "create"}
single_actions = {
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
}


app_name = "graph_api"

urlpatterns = [
    path("search", views.SearchOnGraphEndpoint.as_view(), name="search"),
    path("config", views.GraphDataVisConfig.as_view(), name="config"),
    path(
        "export-properties-csv",
        views.ExportVerticesCSVView.as_view(),
        name="export-properties-csv",
    ),
    path(
        "save-graph",
        views.SavedGraphViewSet.as_view(list_actions),
        name="save-graph",
    ),
    re_path(
        "^save-graph/(?P<pk>\d*)$",
        views.SavedGraphViewSet.as_view(single_actions),
        name="save-graph",
    ),  # noqa
    re_path(
        "^saved-graph-detail/(?P<pk>\d*)$",
        views.SavedGraphDetails.as_view(),
        name="saved-graph-detail",
    ),  # noqa
    path(
        "node/<uuid:uuid>",
        views.GraphNodeDetailEndpoint.as_view(),
        name="node_detail",
    ),
    path(
        "node/<uuid:uuid>/relationships",
        views.NodeRelationshipsEndpoint.as_view(),
        name="node_rels",
    ),
    path(
        "node/relationships",
        views.AllNodesRelationshipsEndpoint.as_view(),
        name="all_nodes_rels",
    ),
    path(
        "edge/<str:edge_id>",
        views.GraphEdgeDetailEndpoint.as_view(),
        name="edge_detail",
    ),
    path(
        "shortest-path/<uuid:from_uuid>/<uuid:to_uuid>",
        views.ShortestPathEndpoint.as_view(),
        name="shortest_path",
    ),
]
