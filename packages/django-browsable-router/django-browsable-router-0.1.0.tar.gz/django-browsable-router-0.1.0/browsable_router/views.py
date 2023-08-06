from typing import Any, Dict

from django.urls import NoReverseMatch
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


__all__ = ["APIRootView"]


class APIRootView(APIView):
    """Welcome! This is the API root."""

    api_root_dict: Dict[str, str] = {}

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        routes = {}
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items() or {}:
            if namespace:
                url_name = namespace + ":" + url_name
            try:
                routes[key] = reverse(
                    viewname=url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get("format", None),
                )
            except NoReverseMatch:
                continue

        return Response(routes)
