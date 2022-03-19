from django import template
from collab_app.models import Category

register = template.Library()

@register.inclusion_tag('collab_app/link_box.html')
def links():
    # pubs = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]
    # pubs[0].num_books
    return {'links': Category.objects.all()[:5]}