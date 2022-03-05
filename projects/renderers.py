from rest_framework import renderers

from .serializers import ContributorWriteFormSerializer


class ProjectContributorListRenderer(renderers.BrowsableAPIRenderer):
    def show_form_for_method(self, view, method, request, obj):
        if request.method != "GET":
            return False
        return super().show_form_for_method(view, method, request, obj)

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(
            data, accepted_media_type, renderer_context
        )
        serializer = ContributorWriteFormSerializer()

        if renderer_context["request"].method == "GET":
            post_form = self.render_form_for_serializer(serializer)
        else:
            post_form = None
        context["post_form"] = post_form
        return context
