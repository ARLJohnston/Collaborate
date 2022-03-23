import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'collab_app.settings')

import django
django.setup()
from collab_app.models import Category, Page, Like


def populate():
    university_pages = [
        {'title': 'University Page',
         'comment':'Welcome to university pages'}        
        ]

    categories_pages = [
        {'title':'Categories',
         'comment':'catergories'},
         ]

    comment_pages = [
        {'topic': 'How to do better in Computer Science',
         'comment':'Just looking for more stackoverflow'}        
        ]
    user_pages = [
        {'topic': 'How to do better in Computer Science',
         'comment':'Just looking for more stackoverflow'}        
        ]
    forum_pages = [
        {'topic': 'How to do better in Computer Science',
         'comment':'Just looking for more stackoverflow'}        
        ]

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')
 
def add_page(cat, title):
    p = Page.objects.get_or_create(category=cat, title=title)[0]   
    p.save()
    return p
  
def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]    
    c.save()
    return c

def add_like(comment)
    l = Like.objects.get_or_create(comment=comment)[0] 
    l.save()
    return l

if __name__ == '__main__':
    print('Starting population script...')
    populate()
