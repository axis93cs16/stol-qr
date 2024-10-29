from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter(name='dictprint')
def dictprint(queryset1):
    return queryset1.__dict__

@register.filter(name='listprint')
def dictprint(queryset1):
    return queryset1.__list__


@register.filter(name='get_value')
def get_value(dictionary, key):
    return dictionary.get(key)

