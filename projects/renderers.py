"""
This module overrides some of the browsable API forms to make it smoother,
it is not exhaustive yet.
"""

from rest_framework import renderers

from .serializers import (
    ContributorCreateFormSerializer,
    ProjectCreateFormSerializer,
)


class ProjectCreateRenderer(renderers.BrowsableAPIRenderer):
    def show_form_for_method(self, view, method, request, obj):
        if request.method != "POST":
            return False
        return super().show_form_for_method(view, method, request, obj)

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(
            data, accepted_media_type, renderer_context
        )

        try:
            many = getattr(data.serializer, "many", False)

            if many is False:
                serializer = ProjectCreateFormSerializer(data)
            else:
                serializer = ProjectCreateFormSerializer()

            if renderer_context["request"].method == "GET":
                post_form = self.render_form_for_serializer(serializer)
            else:
                post_form = None
            context["post_form"] = post_form

        except AttributeError:
            # If something goes wrong data has no serializer attribute.
            pass

        finally:
            return context


class ProjectContributorListRenderer(renderers.BrowsableAPIRenderer):
    def show_form_for_method(self, view, method, request, obj):
        if request.method != "GET":
            return False
        return super().show_form_for_method(view, method, request, obj)

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(
            data, accepted_media_type, renderer_context
        )
        serializer = ContributorCreateFormSerializer()

        if renderer_context["request"].method == "GET":
            post_form = self.render_form_for_serializer(serializer)
        else:
            post_form = None
        context["post_form"] = post_form
        return context
