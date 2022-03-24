from django import template
from collab_app.models import Category

register = template.Library()

@register.inclusion_tag('collab_app/link_box.html')
def get_links():
    """WARNING: THIS IS A TEMPORARY METHOD"""
    return {'links': Category.objects.all()[:1]}