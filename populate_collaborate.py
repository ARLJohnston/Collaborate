import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'collab_app.settings')

import django
django.setup()
from collab_app import Category, Page


def populate():
    university_pages = [
        {'title': 'University Page',
         'comment':'Welcome to university pages'}        
        ]

    categories_pages = [
        {'title':'University',
         'comment':'catergories'},
         ]

    forms_pages = [
        {'title':'Forms', 'comment':'forms'}
        ]

    
    def add_page(cat, title, url, views=0):
        p = Page.objects.get_or_create(category=cat, title=title)[0]
        p.url=url
        p.views=views +1
        p.save()
        return p


    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


if __name__ == '__main__':
    print('Starting population script...')
    populate()
