import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'collaborate.settings')

import django

django.setup()
from collab_app.models import Category, Page, Comment, Like, University, Forum, UserProfile
from django.contrib.auth.models import User


def populate():
    university_comments = [
        {'body': 'I don\'t know'},
        {'body': 'Tea is better than coffee'}
    ]

    university_pages = [
        {'title': 'Where are the best coffee shops?',
         'text': 'I\'m a first year looking for the best coffee shops around campus. Any suggestions?',
         'comments': university_comments
         }
    ]

    university_categories = [
        {'name': 'Student life',
         'pages': university_pages},
        {'name': 'Uni work',
         'pages': university_pages}
    ]

    universities = [
        {
            "name": "University of glasgow",
            "categories": university_categories
        },
        {
            "name": "University of Strathclyde",
            "categories": university_categories
        }
    ]

    general_comments = [
        {'body': 'First'},
        {'body': 'Glasgow is the best uni!'}
    ]

    general_pages = [
        {'title': 'I have no friends. Help!',
         'text': 'I moved to the city two months ago and I still do not know anyone. How do you make new friends at '
                 'uni?',
         'comments': university_comments
         },
        {'title': 'Any tips to do better at uni?',
         'text': 'I\'m finding first year really difficult. Not only the work, but also I\'m only sleeping an average '
                 'of 4h a day. Is anyone having a similar experience?',
         'comments': university_comments
         }
    ]

    general_categories = [
        {'name': 'Managing work, uni and social life',
         'pages': general_pages}
    ]

    # Print out the categories we have added.
    forums = {'General': {'Category': general_categories},
              'Universities': {'University': universities}
              }

    test_users = [{'id': 123456, 'user_name': 'AlistairJ', 'superuser': True, 'first_name': 'Alistair',
                   'last_name': 'Johnston', 'email': 'alistair1234@test.com'},
                  {'id': 284982, 'user_name': 'HollyEdees123', 'superuser': True, 'first_name': 'Holly',
                   'last_name': 'Edees', 'email': 'holly_edees@test.com'},
                  {'id': 391774, 'user_name': 'MaxWW', 'superuser': True, 'first_name': 'Max',
                   'last_name': 'Wraith-Whiting', 'email': 'MaxWW02@test.com'},
                  {'id': 442983, 'user_name': 'Gulati_Naman', 'superuser': True, 'first_name': 'Naman',
                   'last_name': 'Gulati', 'email': '00naman@test.com'},
                  {'id': 594999, 'user_name': 'MarinaSJP', 'superuser': True, 'first_name': 'Marina',
                   'last_name': 'San Jose Pena', 'email': 'marinasj@test.com'}]

    for user in test_users:
        add_user(user['id'], user['user_name'], user['superuser'], user['email'], user['first_name'], user['last_name'])

    users = User.objects.all()
    user_list = []
    for user in users:
        user_id = user.id
        user_profile = add_user_profile(user, user_id)
        user_list.append(user_profile)

    for forum, forum_data in forums.items():
        f = add_forum(forum)
        if forum == 'General':
            for category in forum_data['Category']:  # general_categories
                print("inside category")
                cat = add_cat(category['name'], f)
                for page in category['pages']:  # page inside each category
                    print("inside page")
                    p = add_page(cat, page['title'], page['text'], random.choice(user_list))
                    for com in page['comments']:  # every comment inside every page
                        print("inside comment")
                        add_comment(p, com['body'], random.choice(user_list))

        elif forum == 'Universities':
            for university in forum_data['University']:
                print("inside unis")
                uni = add_university(university)
                for category in university['categories']:  # general_categories
                    print("inside category")
                    cat = add_cat(category['name'], f)
                    for page in category['pages']:  # page inside each category
                        print("inside page")
                        p = add_page(cat, page['title'], page['text'], random.choice(user_list))
                        for com in page['comments']:  # every comment inside every page
                            print("inside comments")
                            add_comment(p, com['body'], random.choice(user_list))


def add_user_profile(user, user_id):
    u = UserProfile.objects.get_or_create(user=user, user_id=user_id)[0]
    u.save()
    return u


def add_user(user_id, user_name, superuser, email, first_name, last_name):
    u = User.objects.get_or_create(id=user_id, username=user_name, is_superuser=superuser, email=email,
                                   first_name=first_name, last_name=last_name)
    return u


def add_page(cat, title, text, user):
    p = Page.objects.get_or_create(category=cat, title=title, text=text, user=user)[0]
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


def add_comment(post, body, user):
    l = Comment.objects.get_or_create(post=post, body=body, user=user)[0]
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
