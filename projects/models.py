from django.db import models
from django.conf import settings


class Project(models.Model):
    FRONT_END, BACK_END, IOS, ANDROID = "FE", "BE", "IO", "AN"
    PROJECT_TYPES = (
        (FRONT_END, "front-end"),
        (BACK_END, "back-end"),
        (IOS, "iOS"),
        (ANDROID, "Android"),
    )

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=PROJECT_TYPES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )


class Contributor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Issue(models.Model):
    BUG, ENHANCEMENT, TASK = "B", "E", "T"
    ISSUE_TAGS = (
        (BUG, "bug"),
        (ENHANCEMENT, "enhancement"),
        (TASK, "task"),
    )

    LOW, MEDIUM, HIGH = "L", "M", "H"
    PRIORITY_LEVELS = ((LOW, "low"), (MEDIUM, "medium"), (HIGH, "high"))

    TODO, IN_PROGRESS, DONE = "T", "I", "D"
    STATUS_KINDS = (
        (TODO, "todo"),
        (IN_PROGRESS, "in progress"),
        (DONE, "done"),
    )

    title = models.CharField(max_length=50)
    description = models.TextField()
    tag = models.CharField(max_length=1, choices=ISSUE_TAGS)
    priority = models.CharField(max_length=1, choices=PRIORITY_LEVELS)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_KINDS)
    author = models.ForeignKey(
        Contributor,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_issues",
    )
    assignee = models.ForeignKey(
        Contributor,
        null=True,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    description = models.TextField()
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
