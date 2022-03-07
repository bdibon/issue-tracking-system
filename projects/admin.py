from django.contrib import admin

from .models import Contributor, Project, Issue, Comment


class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "project",
    )


admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
