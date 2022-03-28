import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'collaborate.settings')

import django

django.setup()
from collab_app.models import Category, Page, Comment, Like, University, Forum, UserProfile, ForumCategoryAssociation
from django.contrib.auth.models import User



def populate():
    glasgow_coffee_comments = [
        {'body': 'I don\'t know'},
        {'body': 'Tea is better than coffee.'},
        {'body': 'You should try Morning Glory in Great Western Road!!'}
    ]

    glasgow_party_comments = [
        {'body': 'I don\'t like clubbing, so idk'},
        {'body': 'Definitely Hive!!'},
        {'body': 'It HAS to be the garage'},
        {'body': 'Neither, Mango beats both'}
    ]

    glasgow_student_life_pages = [
        {'title': 'Where are the best coffee shops?',
         'text': 'I\'m a first year looking for the best coffee shops around campus. Any suggestions?',
         'comments': glasgow_coffee_comments
         },
        {'title': 'What is better, Hive or The Garage?',
         'text': 'I\'m looking to finally settling the debate!',
         'comments': glasgow_party_comments
         }
    ]

    glasgow_studying_comments = [
        {'body': 'I just cram the day before the exam tbh lmao'},
        {'body': 'Personally, the pomodoro technique seems to work the best! I urge you to try it too!!'}
    ]

    glasgow_uni_work_pages = [
        {'title': 'Do you follow any study techniques?',
         'text': 'I\'ve been trying several different studying techniques and nothing seems to work. What do you guys '
                 'do?',
         'comments': glasgow_studying_comments
         }
    ]

    glasgow_categories = [
        {'name': 'Student life',
         'pages': glasgow_student_life_pages},
        {'name': 'Uni work',
         'pages': glasgow_uni_work_pages}
    ]

    cambridge_sun_comments = [
        {'body': 'So pretty!'},
    ]

    cambridge_student_life_pages = [
        {'title': 'Sunny day in Cambridge <3',
         'text': 'I\'m a first year looking for the best coffee shops around campus. Any suggestions?',
         'comments': cambridge_sun_comments
         },
    ]

    cambridge_badminton_comments = [
        {'body': 'I\'d love to!'},
    ]

    cambridge_sport_pages = [
        {'title': 'Anyone want to be my badminton buddy?',
         'text': 'I want to play badminton but have no one to do it with :(',
         'comments': cambridge_badminton_comments
         }
    ]

    cambridge_categories = [
        {'name': 'Sports',
         'pages': cambridge_sport_pages},
        {'name': 'Student life',
         'pages': cambridge_student_life_pages}
    ]

    universities = {
        'University of Glasgow': glasgow_categories,
        'University of Cambridge': cambridge_categories
    }

    general_do_better_comments = [
        {'body': 'Be sure to eat healthy and always sleep over 7h every day. Uni is not worth your mental and '
                 'physical health.'},
        {'body': 'Get in contact with other classmates. Form a study group where you can help each other.'}
    ]

    general_friends_comments = [
        {'body': 'Join societies! That\'s the quickest way of finding people with similar interests.'},
    ]

    general_pages = [
        {'title': 'I have no friends. Help!',
         'text': 'I moved to the city two months ago and I still do not know anyone. How do you make new friends at '
                 'uni?',
         'comments': general_friends_comments
         },
        {'title': 'Any tips to do better at uni?',
         'text': 'I\'m finding first year really difficult. Not only the work, but also I\'m only sleeping an average '
                 'of 4h a day.',
         'comments': general_do_better_comments
         }
    ]

    general_categories = [
        {'name': 'Managing work, uni and social life',
         'pages': general_pages}
    ]

    # Print out the categories we have added.
    forums = {'General': {'Category': general_categories},
              'University of Glasgow': {'University': universities['University of Glasgow']},
              'University of Cambridge': {'University': universities['University of Cambridge']}
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
                forum_category = add_forum_category_association(f, cat)
                add_pages_comments(category, forum_category.category, user_list)

        else:
            university_categories = forum_data['University']
            print("inside unis")
            add_university(forum, random.choice(user_list), f)
            for category in university_categories:  # university_categories
                print("inside category")
                cat = add_cat(category['name'], f)
                forum_category = add_forum_category_association(f, cat)
                add_pages_comments(category, forum_category.category, user_list)


def add_forum_category_association(forum, category):
    fc = ForumCategoryAssociation.objects.get_or_create(forum=forum, category=category)[0]
    fc.save()
    return fc


def add_pages_comments(category, cat, user_list):
    for page in category['pages']:  # page inside each category
        print("inside page")
        p = add_page(cat, page['title'], page['text'], random.choice(user_list))
        for com in page['comments']:  # every comment inside every page
            print("inside comments")
            add_comment(p, com['body'], random.choice(user_list))


def add_user_profile(user, user_id):
    u = UserProfile.objects.get_or_create(user=user, user_id=user_id,)[0]
    u.save()
    return u


def add_user(user_id, user_name, superuser, email, first_name, last_name):
    u = User.objects.get_or_create(id=user_id, username=user_name, is_superuser=superuser, email=email,
                                   first_name=first_name, last_name=last_name, password=user_name + '27')
    return u


def add_page(cat, title, text, user):
    p = Page.objects.get_or_create(category=cat, title=title, text=text, user=user)[0]
    p.save()
    return p


def add_cat(name, forum):
    c = Category.objects.get_or_create(name=name, forum=forum)[0]
    c.save()
    return c


def add_comment(post, body, user):
    com = Comment.objects.get_or_create(post=post, body=body, user=user)[0]
    com.save()
    return com


def add_university(name, user, forum):
    uni = University.objects.get_or_create(name=name, forum=forum)[0]
    uni.user.set([user])
    uni.save()
    return uni


def add_forum(name):
    forum = Forum.objects.get_or_create(name=name)[0]
    forum.save()
    return forum


if __name__ == '__main__':
    print('Starting population script...')
    populate()
