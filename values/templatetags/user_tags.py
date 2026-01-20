from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def is_value_reviewer(user):
    """Check if user is in the Value Reviewers group"""
    if not user or not user.is_authenticated:
        return False
    try:
        reviewers_group = Group.objects.get(name="Value Reviewers")
        return reviewers_group in user.groups.all()
    except Group.DoesNotExist:
        return False
