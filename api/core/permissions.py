from django.views.generic import View
from rest_framework import permissions
from rest_framework.request import Request


class IsAuthenticatedOrRetrieveListOnlyViewSet(permissions.BasePermission):
    """
    Allow not authenticated users to only retrieve. Every other action is for authenticated users
    This permission is only suitable for ViewSets
    """

    def has_permission(self, request: Request, view: View) -> bool:
        if not hasattr(view, "action"):
            raise AttributeError(
                "This view does not have actions. You should use this permission only in ViewSets."
            )

        if not request.user.is_authenticated:
            if hasattr(view, "action") and view.action in ("retrieve", "list"):  # type: ignore
                return True
            else:
                return False
        else:
            return True
