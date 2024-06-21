from django.urls import path

from event.views import EventViewSet, AddUserParticipantAPIView

app_name = "event"
urlpatterns = [
    path(
        "<int:pk>",
        EventViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="event_retrieve_update_destroy",
    ),
    path(
        "",
        EventViewSet.as_view({"post": "create"}),
        name="event_create",
    ),
    path(
        "list/<int:user_id>",
        EventViewSet.as_view({"get": "list"}),
        name="event_list",
    ),
    path(
        "<int:pk>/participate",
        AddUserParticipantAPIView.as_view(),
        name="add_user_participant",
    ),
]
