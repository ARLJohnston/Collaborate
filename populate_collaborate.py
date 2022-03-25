import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'collaborate.settings')

import django

django.setup()
from collab_app.models import Category, Page, Comment, Like, University, Forum


def populate():
    universities = [
        {'title': 'University Page',
         'description': 'Welcome to university pages'}
    ]

    university_categories = [
        {'title': 'Categories',
         'description': 'categories'}
    ]

    general_categories = [
        {'title': 'Categories',
         'description': 'categories'}
    ]

    general_pages = [
        {'title': 'How to do better in Computer Science',
         'description': 'Just looking for more stackoverflow',
         }]

    university_pages = [
        {'title': 'How to do better in Computer Science',
         'description': 'Just looking for more stackoverflow'}
    ]
    general_comments = [
        {'post': 'How to do better in Computer Science',
         'body': 'Just looking for more stackoverflow'}
    ]

    university_comments = [
        {'title': 'How to do better in Computer Science',
         'description': 'Just looking for more stackoverflow'}
    ]

    # Print out the categories we have added.
    forums = {'General': {'Category': general_categories, 'Page': general_pages, 'Comment': general_comments},
             'Universities': {'University': universities, 'Category': university_categories, 'Page': university_pages,
                              'Comment': university_comments}
             }

    for forum, forum_data in forums.items():
        f = add_forum(forum)
        if forum == 'General':
            for c in forum_data['Category']:
                print(forum_data)
                cat = add_cat(forum_data, f)
                for p in forum_data['Page']:
                    post = add_page(cat, p['title'])
                    for com in forum_data['Comment']:
                        add_comment(post, com['body'])

        elif forum == 'Universities':
            for u in forum_data['University']:
                uni = add_university(u)
                for c in forum_data['Category']:
                    cat = add_cat(c, f)
                    for p in forum_data['Page']:
                        post = add_page(cat, p['title'])
                        for com in forum_data['Comment']:
                            add_comment(post, com['body'])

    '''
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')'''


def add_page(cat, title):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.save()
    return p


def add_cat(name, forum):
    c = Category.objects.get_or_create(name=name, forum=forum)[0]
    c.save()
    return c


def add_like(comment):
    l = Like.objects.get_or_create(comment=comment)[0]
    l.save()
    return l


def add_comment(post, body):
    l = Comment.objects.get_or_create(post=post, body=body)[0]
    l.save()
    return l


def add_university(name):
    l = University.objects.get_or_create(name=name)[0]
    l.save()
    return l


def add_forum(name):
    l = Forum.objects.get_or_create(name=name)[0]
    l.save()
    return l


if __name__ == '__main__':
    print('Starting population script...')
    populate()
